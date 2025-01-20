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

def validate_members(data):
    """
    주어진 데이터에서 멤버 이름이 활성 멤버에 모두 존재하는지 확인하고,
    활성 멤버 이름이 데이터에 모두 존재하는지 확인하며,
    중복된 이름이 있는지도 검사하는 유틸리티.

    Parameters:
    - data (list of dict): 검사할 멤버 이름이 담긴 데이터 리스트.

    Returns:
    - bool: 모든 멤버가 존재하면 True, 아니면 False.
    - list: 존재하지 않는 멤버 이름 목록.
    """
    # 활성 멤버 목록 가져오기
    active_members = plugin_loader.members_utils.get_active_members()
    active_member_names = {info['name'] for info in active_members.values()}

    # 데이터에서 존재하지 않는 멤버 이름 찾기
    missing_in_data = [name for name in active_member_names if name not in {member['name'] for member in data}]
    missing_members = [member['name'] for member in data if member['name'] not in active_member_names]

    # 중복된 이름 확인
    name_counts = {}
    for member in data:
        name_counts[member['name']] = name_counts.get(member['name'], 0) + 1
    duplicate_names = [name for name, count in name_counts.items() if count > 1]

    # 결과 반환
    if missing_members:
        logger.error(f"검사 실패: 잘못된 이름들: {missing_members}")

    if duplicate_names:
        logger.error(f"검사 실패: 중복된 이름들: {duplicate_names}")

    if missing_in_data:
        logger.error(f"검사 실패: 데이터가 없는 멤버들: {missing_in_data}")

    if not missing_members and not missing_in_data and not duplicate_names:
        logger.info("모든 멤버가 활성 목록과 데이터에 모두 존재하며, 중복이 없습니다.")
        return True, []

    return False, missing_members + duplicate_names

def main():
    # 입력 폴더 경로 설정
    data_file = '../data/members/member_data.json'

    # JSON 파일로부터 데이터를 로드
    data = plugin_loader.file_utils.load_single_json(data_file)
    if not data:  # 데이터가 없으면 실행 중단
        return

    # 멤버 검사
    valid, missing = validate_members(data)
    if valid:
        logger.info("검사 통과: 모든 멤버가 활성 목록에 존재합니다.")
    else:
        logger.error(f"검사 실패: 잘못된 이름 또는 중복된 이름 - {missing}")


# 사용 예시
if __name__ == "__main__":
    # 메인 함수 실행 (파일 경로 및 출력 디렉토리 지정)
    main()
