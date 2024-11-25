import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # 날짜 포맷팅을 위해 추가
import koreanize_matplotlib
import polars as pl
import os
import sys
import glob
from datetime import datetime
from scripts.plugin_loader import PluginLoader

# 현재 스크립트의 상위 두 경로를 추가하여 plugin_loader.py 파일을 불러옴
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# PluginLoader 인스턴스 생성
plugin_loader = PluginLoader()


def load_json_files(data_dir, file_pattern):
    """주어진 디렉토리에서 JSON 파일을 로드하고 날짜순으로 정렬하여 반환합니다."""
    pattern = os.path.join(data_dir, file_pattern)
    file_list = sorted(glob.glob(pattern))
    return file_list


def extract_rank(data, target_member_id):
    """데이터에서 특정 member_id의 랭크를 추출하거나 존재하지 않으면 None을 반환합니다."""
    df = pl.DataFrame(data)
    member_data = df.filter(pl.col('member_id') == target_member_id)
    if member_data.is_empty():
        return None
    else:
        return member_data.select('rank').to_numpy()[0, 0]


def get_member_id():
    """사용자로부터 유효한 member_id를 입력받습니다."""
    while True:
        try:
            member_id_input = input("추적할 member_id를 입력하세요: ").strip()
            if not member_id_input:
                print("member_id는 비어 있을 수 없습니다. 다시 입력해주세요.")
                continue
            target_member_id = int(member_id_input)
            if target_member_id < 0:
                print("member_id는 양의 정수여야 합니다. 다시 입력해주세요.")
                continue
            return target_member_id
        except ValueError:
            print("유효한 정수를 입력해주세요.")


def main():
    # 스타일 적용
    plt.style.use('ggplot')

    # 사용자로부터 특정 member_id 입력 받기
    TARGET_MEMBER_ID = get_member_id()

    # JSON 파일이 저장된 디렉토리 경로
    DATA_DIR = '../../data/battles/'

    # battle_*.json 파일 패턴
    FILE_PATTERN = 'battle_*.json'

    # 모든 JSON 파일 경로 리스트 (날짜순으로 정렬)
    file_list = load_json_files(DATA_DIR, FILE_PATTERN)

    if not file_list:
        print(f"디렉토리 '{DATA_DIR}'에 '{FILE_PATTERN}' 패턴에 맞는 파일이 존재하지 않습니다.")
        return

    # 날짜와 랭크를 저장할 리스트 초기화
    dates = []
    ranks = []
    missing_dates = []

    # 각 파일을 순회하며 데이터 추출
    for file_path in file_list:
        # 파일명에서 날짜 추출 (예: battle_20240714.json -> 2024-07-14)
        file_name = os.path.basename(file_path)
        date_str = file_name.replace('battle_', '').replace('.json', '')
        try:
            date = datetime.strptime(date_str, '%Y%m%d').date()
        except ValueError:
            print(f"날짜 형식이 올바르지 않은 파일: {file_name}")
            continue

        # JSON 파일 읽기
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"파일을 읽는 중 오류 발생: {file_name}, 오류: {e}")
            continue

        # 특정 member_id의 랭크 추출
        rank = extract_rank(data, TARGET_MEMBER_ID)
        if rank is None:
            # member_id가 존재하지 않는 경우, 해당 날짜를 제외하고 기록
            missing_dates.append(date)
            print(f"member_id {TARGET_MEMBER_ID}가 파일 {file_name}에 존재하지 않습니다. 해당 날짜를 제외합니다.")
            continue

        # 리스트에 추가
        dates.append(date)
        ranks.append(rank)

    # 데이터가 충분히 있는지 확인
    if not dates:
        print("지정된 member_id에 대한 데이터가 존재하지 않습니다.")
        return

    # Polars DataFrame 생성 (옵션)
    rank_df = pl.DataFrame({
        'date': dates,
        'rank': ranks
    })

    # 멤버 기준 데이터 로드
    member_name = plugin_loader.members_utils.get_member_name(TARGET_MEMBER_ID)

    # 시각화
    plt.figure(figsize=(12, 6))
    plt.plot(rank_df['date'], rank_df['rank'], marker='o', linestyle='-', color='red',label=f'랭크')

    # y축을 반전하여 랭크 1이 위에 오도록 설정 (옵션)
    plt.gca().invert_yaxis()

    # x축 날짜 형식을 월-일로 설정
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xlabel('날짜', fontsize=12, labelpad=10)
    plt.ylabel('랭크', fontsize=12, labelpad=10)
    plt.title(f'[{member_name}]님의 랭크 변화', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=10, color='#624E88', fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold', color='darkblue')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()

    plt.tight_layout()
    plt.show()

    # 제외된 날짜 출력 (옵션)
    if missing_dates:
        print("\n해당 member_id가 존재하지 않아 제외된 날짜들:")
        for date in missing_dates:
            print(date)


if __name__ == "__main__":
    main()
