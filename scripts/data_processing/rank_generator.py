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


def main():
    # 입력 폴더 및 출력 파일 경로 설정
    data_file = '../data/rankings/member_data_without_rank.json'
    output_file_path = '../data/result/member_data_with_rank.json'

    """
    데이터에 rank 부여하고 JSON 파일로 저장하는 메인 함수.

    Parameters:
    - data_file (str): JSON 데이터를 읽어올 파일 경로
    - output_directory (str): 저장할 파일 디렉토리 경로
    """

    # JSON 파일로부터 데이터를 로드
    data = plugin_loader.file_utils.load_single_json(data_file)
    if not data:  # 데이터가 없으면 실행 중단
        return

    # 데이터를 Polars DataFrame으로 변환
    combined_df = pl.DataFrame(data)

    # total_score 기준으로 내림차순 정렬 및 rank 부여 (내림차순으로 rank 부여)
    combined_df = combined_df.sort(by='total_score', descending=True).with_columns(
        pl.arange(1, combined_df.height + 1).alias('rank')
    )

    # 결과를 JSON 파일로 저장
    plugin_loader.file_utils.save_to_json(output_file_path, combined_df)


if __name__ == "__main__":
    main()
