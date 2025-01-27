import logging
import os
import sys

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
    data_file = '../data/members/member_data.json'
    output_file_path = '../data/result/member_data_with_ids.json'

    """
    데이터에 ID를 부여하고 JSON 파일로 저장하는 메인 함수.

    Parameters:
    - data_file (str): JSON 데이터를 읽어올 파일 경로
    - output_directory (str): 저장할 파일 디렉토리 경로
    """
    # 멤버 기준 데이터 로드
    members = plugin_loader.members_utils.get_all_members()

    # JSON 파일로부터 데이터를 로드
    data = plugin_loader.file_utils.load_single_json(data_file)
    if not data:  # 데이터가 없으면 실행 중단
        return

    # 데이터에 id를 할당후 정렬
    data_with_ids = plugin_loader.members_utils.assign_ids(data, members)
    sorted_data = sorted(data_with_ids, key=lambda x: x.get('rank', float('inf')))

    # 결과를 JSON 파일로 저장
    plugin_loader.file_utils.save_single_json(output_file_path, sorted_data)


# 사용 예시
if __name__ == "__main__":
    # 메인 함수 실행 (파일 경로 및 출력 디렉토리 지정)
    main()
