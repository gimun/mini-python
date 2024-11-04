# scripts/battle/monthly_rank_calculator.py

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


def calculate_rank_and_play_count(df):
    """rank_score 계산 및 play_count 갱신"""
    return (
        df.with_columns(
            pl.when(pl.col('rank') <= 50).then(51 - pl.col('rank')).otherwise(0).alias('rank_score')
        )
        .with_columns(
            pl.when(pl.col('rank_score') > 0).then(pl.col('play_count') + 1)
            .otherwise(pl.col('play_count')).alias('play_count')
        )
    )


def group_by_member_id(df):
    """member_id 별로 그룹화하여 rank_score와 play_count 합계를 계산."""
    return df.group_by('member_id').agg([
        pl.sum('play_count').alias('play_count'),
        pl.sum('rank_score').alias('rank_score')
    ])


def main():
    # TODO: 중복 코드 제거 및 rank_calculator.py 통합
    # 입력 폴더 및 출력 파일 경로 설정
    folder_path = '../data/battles_2411'
    output_file_path = '../data/result/monthly_rank_score.json'

    # JSON 파일 불러오기
    try:
        all_data = plugin_loader.file_utils.load_json_files_from_folder(folder_path)
        logger.info(f"Loaded JSON data from '{folder_path}'.")
    except Exception as e:
        logger.error(f"Failed to load JSON data from '{folder_path}': {e}", exc_info=True)
        return

    if not all_data:
        logger.error("No data loaded from the JSON files. Exiting.")
        return

    # 데이터를 Polars DataFrame으로 변환
    combined_df = pl.DataFrame(all_data)
    logger.info("Converted JSON data to Polars DataFrame.")

    # play_count 열이 존재하지 않으면 기본 값 0으로 설정
    combined_df = ensure_column_exists(combined_df, 'play_count', 0)
    logger.info("Ensured 'play_count' column exists in DataFrame.")

    # status가 1인 member_id 목록 필터링
    try:
        active_member_ids = plugin_loader.members_utils.get_active_member_ids()
        active_members_df = plugin_loader.members_utils.load_active_members_as_df()
        logger.info("Loaded active member IDs and DataFrame.")
    except Exception as e:
        logger.error(f"Failed to load active member information: {e}", exc_info=True)
        return

    combined_df = combined_df.filter(pl.col('member_id').is_in(active_member_ids))
    logger.info("Filtered DataFrame to include only active members.")

    # rank_score 계산 및 play_count 갱신
    combined_df = calculate_rank_and_play_count(combined_df)
    logger.info("Calculated 'rank_score' and updated 'play_count'.")

    # member_id 별로 그룹화하여 rank_score와 play_count의 합계 계산
    grouped_df = group_by_member_id(combined_df)
    logger.info("Grouped DataFrame by 'member_id' and aggregated 'rank_score' and 'play_count'.")

    # 랭킹 데이터와 활성 멤버 정보 join
    final_df = active_members_df.join(grouped_df, on='member_id', how='left')
    logger.info("Joined aggregated data with active members DataFrame.")

    # rank_score가 없거나 NaN인 경우 0으로 설정
    final_df = final_df.with_columns(
        pl.col('play_count').fill_null(0),
        pl.col('rank_score').fill_null(0)
    )
    logger.info("Filled null values in 'play_count' and 'rank_score' with 0.")

    # rank_score 기준으로 내림차순 정렬 및 rank 부여
    final_df = final_df.sort(by='rank_score', descending=True).with_columns(
        pl.arange(1, final_df.height + 1).alias('rank')
    )
    logger.info("Sorted DataFrame by 'rank_score' and assigned ranks.")

    # 결과를 JSON 파일로 저장
    try:
        plugin_loader.file_utils.save_to_json(output_file_path, final_df)
        logger.info(f"Saved final DataFrame to '{output_file_path}'.")
    except Exception as e:
        logger.error(f"Failed to save final DataFrame to '{output_file_path}': {e}", exc_info=True)


if __name__ == "__main__":
    main()
