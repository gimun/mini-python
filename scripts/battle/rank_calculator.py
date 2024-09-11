import importlib.util
import json
import os
import polars as pl

# 모듈 경로 설정
module_path = os.path.abspath('../../scripts/members_utils.py')

# 모듈을 동적으로 로드
spec = importlib.util.spec_from_file_location("members_utils", module_path)
members_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(members_utils)

# members_utils 모듈에서 함수 가져오기
get_active_member_ids = members_utils.get_active_member_ids
load_active_members_as_df = members_utils.load_active_members_as_df


def load_json_files_from_folder(folder_path):
    """지정된 폴더 내의 모든 JSON 파일을 읽어 데이터로 반환."""
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    all_data = []

    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)  # 데이터를 모두 합침
        except Exception as e:
            print(f"Error reading {json_file}: {e}")

    return all_data


def save_to_json(output_file_path, df):
    """DataFrame을 JSON 파일로 저장."""
    output_folder = os.path.dirname(output_file_path)

    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    df.write_json(output_file_path)
    print(f"결과가 {output_file_path}에 저장되었습니다.")


def main():
    # 입력 폴더 및 출력 파일 경로 설정
    folder_path = os.path.abspath('../../input/battle')
    output_file_path = os.path.abspath('../../output/battle/grouped_rank_score.json')

    # 폴더가 존재하는지 확인
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"지정된 폴더 경로가 존재하지 않습니다: {folder_path}")

    # JSON 파일 불러오기
    all_data = load_json_files_from_folder(folder_path)

    if not all_data:
        print("No data loaded from the JSON files.")
        return

    # 데이터를 Polars DataFrame으로 변환
    combined_df = pl.DataFrame(all_data)

    # status가 1인 member_id 목록 필터링
    active_member_ids = get_active_member_ids()

    # member_id가 active_member_ids에 속하는 데이터만 필터링
    combined_df = combined_df.filter(pl.col('member_id').is_in(active_member_ids))

    # rank_score 계산 (rank가 50 이하인 경우 점수 부여)
    combined_df = combined_df.with_columns(
        pl.when(pl.col('rank') <= 50).then(51 - pl.col('rank'))
        .otherwise(0).alias('rank_score')
    )

    # member_id 별로 그룹화하여 rank_score의 합계 계산
    grouped_df = combined_df.group_by('member_id').agg(pl.sum('rank_score').alias('rank_score'))

    # 활성 멤버 정보 DataFrame 로드
    active_members_df = load_active_members_as_df()

    # 랭킹 데이터와 활성 멤버 정보 join
    final_df = active_members_df.join(grouped_df, on='member_id', how='left')

    # rank_score가 없거나 NaN인 경우 0으로 설정
    final_df = final_df.with_columns(
        pl.col('rank_score').fill_null(0)
    )

    # rank_score 기준으로 내림차순 정렬 및 rank 부여
    final_df = final_df.sort(by='rank_score', descending=True).with_columns(
        pl.arange(1, final_df.height + 1).alias('rank')
    )

    # 결과를 JSON 파일로 저장
    save_to_json(output_file_path, final_df)


if __name__ == "__main__":
    main()
