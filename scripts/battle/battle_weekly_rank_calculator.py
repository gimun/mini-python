# scripts/battle/rank_calculator.py

import glob
import json
import logging
import os
import sys

import polars as pl

from scripts.plugin_loader import PluginLoader

# 현재 스크립트의 상위 두 경로를 추가하여 plugin_loader.py 파일을 불러옴
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# PluginLoader 인스턴스 생성
plugin_loader = PluginLoader()


def ensure_column_exists(df, column_name, default_value):
    """DataFrame에 지정된 열이 없을 경우, 기본값으로 추가."""
    if column_name not in df.columns:
        return df.with_columns(pl.Series(column_name, [default_value] * df.height))
    return df


def calculate_rank_score(df):
    """
    rank_score 계산:
    - 게임 미참여자는 고정적으로 rank=51, rank_score=0을 부여.
    - 동일한 score는 동일한 rank를 부여.
    - 동점자가 있으면 다음 순위를 건너뛰도록 처리.
    - 1등: 50점, 2등: 49점, ... 50등: 1점, 이후 0점.
    """
    # score가 null인 경우 0으로 설정 (순위 계산을 위해 필요)
    df = df.with_columns(pl.col("score").fill_null(0))

    # score > 0인 경우에만 rank 부여, 그렇지 않으면 51위 고정
    df = df.with_columns(
        pl.when(pl.col("score") > 0)
        .then(pl.col("score").rank(method="min", descending=True).cast(pl.Int64))
        .otherwise(51)  # 미참여자는 51위 고정
        .alias("rank")
    )

    # 순위별 점수 부여 (1등: 50점, 2등: 49점, ..., 50등: 1점, 이후 0점)
    rank_to_score = {rank: max(51 - rank, 0) for rank in df["rank"].unique().to_list()}

    # rank_score 계산 (게임 미참여자는 0점으로 설정)
    df = df.with_columns(
        pl.when(pl.col("rank") <= 50)
        .then(pl.col("rank").map_elements(lambda r: rank_to_score.get(r, 0), return_dtype=pl.Int64))
        .otherwise(0)  # 51위는 0점
        .alias("rank_score")
    )

    return df


def update_play_count(df):
    """
    play_count 갱신:
    - rank_score가 0보다 크면 play_count + 1
    - 그렇지 않으면 play_count 그대로 유지
    """
    return df.with_columns(
        pl.when(pl.col("rank_score") > 0)
        .then(pl.col("play_count") + 1)
        .otherwise(pl.col("play_count"))
        .alias("play_count")
    )


def group_by_member_id(df):
    """member_id 별로 그룹화하여 rank_score와 play_count 합계를 계산."""
    return df.group_by('member_id').agg([
        pl.sum('play_count').alias('play_count'),
        pl.sum('rank_score').alias('rank_score')
    ])


def load_recent_json_files(folder_path, pattern, recent_n=3):
    """
    지정된 폴더에서 JSON 파일을 로드하고, 숫자 부분을 기준으로 정렬 후 최근 n개의 파일을 반환.
    """
    pattern = os.path.join(folder_path, pattern)
    file_list = glob.glob(pattern)

    # 파일 이름에서 숫자를 추출하여 정렬
    file_list = sorted(
        file_list,
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[-1])
    )

    if len(file_list) < recent_n:
        logger.warning(f"전체 {len(file_list)}개의 파일이 로드되었습니다. 최근 {recent_n}개의 파일만 처리합니다.")
    return file_list[-recent_n:]


def main():
    # 입력 폴더 및 출력 파일 경로 설정
    folder_path = '../../data/battles_rank'
    output_final_file_path = '../data/result_battles/weekly_rank_score.json'
    output_individual_folder = '../data/result_battles/individual_games'

    # 개별 게임 결과를 저장할 폴더가 없으면 생성
    os.makedirs(output_individual_folder, exist_ok=True)

    # TDDO: recent_n 수정 작업
    try:
        recent_files = load_recent_json_files(folder_path, 'battle_*.json', recent_n=3)
        logger.info(f"Loaded {len(recent_files)} recent JSON files from '{folder_path}'.")
    except Exception as e:
        logger.error(f"Failed to load JSON files from '{folder_path}': {e}", exc_info=True)
        return

    if not recent_files:
        logger.error("No data loaded from the JSON files. Exiting.")
        return

    # 멤버 정보 로드
    try:
        active_member_ids = plugin_loader.members_utils.get_active_member_ids()
        active_members_df = plugin_loader.members_utils.load_active_members_as_df()
    except Exception as e:
        logger.error(f"Failed to load active member information: {e}", exc_info=True)
        return

    # 개별 게임 결과를 저장할 리스트
    individual_game_dfs = []
    individual_game_rank_scores = []

    # 각 게임별로 데이터 처리
    for idx, file_path in enumerate(recent_files, start=1):
        # JSON 파일 읽기
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded data from '{file_path}'.")
        except Exception as e:
            logger.error(f"Failed to load data from '{file_path}': {e}", exc_info=True)
            continue

        if not data:
            logger.warning(f"No data found in '{file_path}'. Skipping.")
            continue

        # 데이터를 Polars DataFrame으로 변환
        game_df = pl.DataFrame(data)
        if game_df.is_empty():
            logger.warning(f"Empty DataFrame for '{file_path}'. Skipping.")
            continue

        # play_count 열이 존재하지 않으면 기본 값 0으로 설정
        game_df = ensure_column_exists(game_df, 'play_count', 0)

        # active_member_ids 필터링
        game_df = game_df.filter(pl.col('member_id').is_in(active_member_ids))

        if game_df.is_empty():
            logger.warning(f"All members filtered out for '{file_path}'. Skipping.")
            continue

        game_df = calculate_rank_score(game_df)

        # play_count 갱신
        game_df = update_play_count(game_df)

        # member_id 별로 그룹화하여 rank_score와 play_count의 합계 계산
        grouped_game_df = group_by_member_id(game_df)

        # 개별 게임 결과를 저장할 DataFrame 준비 (한 번에 join 수행)
        final_game_df = active_members_df.join(
            grouped_game_df.join(game_df.select(['member_id', 'rank', 'score']), on='member_id', how='left'),
            on='member_id',
            how='left'
        ).with_columns(
            pl.col('rank').fill_null(51),
            pl.col('score').fill_null(0),
            pl.col('play_count').fill_null(0),
            pl.col('rank_score').fill_null(0)
        ).sort('rank')

        try:
            # 게임별 파일명 생성 (예: game_1_rank_score.json)
            individual_game_file = os.path.join(output_individual_folder, f'game_{idx}_rank_score.json')

            # rank와 score도 포함하여 저장
            plugin_loader.file_utils.save_to_json(individual_game_file, final_game_df)
            logger.info(f"Saved individual game DataFrame with rank and score to '{individual_game_file}'.")
        except Exception as e:
            logger.error(f"Failed to save individual game DataFrame to '{individual_game_file}': {e}", exc_info=True)

        individual_game_dfs.append(final_game_df)

        game_rank_score_df = final_game_df.select(['member_id', 'rank', 'score', 'rank_score']).rename({
            'rank_score': f'game_{idx}_rank_score',
            'rank': f'game_{idx}_rank',
            'score': f'game_{idx}_score'
        })
        individual_game_rank_scores.append(game_rank_score_df)

    if not individual_game_dfs:
        logger.error("No individual game data processed. Exiting.")
        return

    # 모든 개별 게임 DataFrame을 합산
    try:
        # 모든 게임의 rank_score와 play_count를 합산
        aggregated_df = pl.concat(individual_game_dfs).group_by('member_id').agg([
            pl.sum('play_count').alias('play_count'),
            pl.sum('rank_score').alias('rank_score')
        ])
        logger.info("Aggregated 'play_count' and 'rank_score' across all games.")
    except Exception as e:
        logger.error(f"Failed to aggregate individual game data: {e}", exc_info=True)
        return

    # 최종 결과 DataFrame 생성
    try:
        final_df = active_members_df.join(aggregated_df, on='member_id', how='left')
        logger.info("Joined aggregated data with active members DataFrame for final results.")
    except Exception as e:
        logger.error(f"Failed to join aggregated data with active members DataFrame: {e}", exc_info=True)
        return

    # rank_score와 play_count가 없거나 NaN인 경우 0으로 설정
    final_df = final_df.with_columns(
        pl.col('play_count').fill_null(0),
        pl.col('rank_score').fill_null(0)
    )

    # rank_score 기준으로 내림차순 정렬 및 rank 부여
    final_df = final_df.sort(by='rank_score', descending=True).with_columns(
        pl.col('rank_score')
        .rank(method='min', descending=True)
        .cast(pl.Int64)  # 순위를 정수형으로 변환
        .alias('rank')
    )

    # 개별 게임별 rank_score를 최종 결과에 병합
    for game_rank_score_df in individual_game_rank_scores:
        final_df = final_df.join(game_rank_score_df, on='member_id', how='left')

    # 개별 게임 rank_score가 없거나 NaN인 경우 0으로 설정
    for idx in range(1, len(individual_game_rank_scores) + 1):
        column_name = f'game_{idx}_rank_score'
        final_df = final_df.with_columns(
            pl.col(column_name).fill_null(0)
        )

    # 최종 결과를 JSON 파일로 저장
    try:
        plugin_loader.file_utils.save_to_json(output_final_file_path, final_df)
        logger.info(f"Saved final aggregated DataFrame to '{output_final_file_path}'.")
    except Exception as e:
        logger.error(f"Failed to save final aggregated DataFrame to '{output_final_file_path}': {e}", exc_info=True)


if __name__ == "__main__":
    main()
