import importlib.util
import json
import os
from datetime import datetime

# members_utils 모듈 경로 설정
module_path = os.path.abspath('../../scripts/members_utils.py')
spec = importlib.util.spec_from_file_location("members_utils", module_path)
members_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(members_utils)

# members_utils 모듈에서 함수 가져오기
get_all_members = members_utils.get_all_members
assign_ids = members_utils.assign_ids


def save_json(data, file_name):
    """
    주어진 데이터를 JSON 파일로 저장하는 함수.

    Parameters:
    - data (list of dict): 저장할 데이터 리스트
    - file_name (str): 저장할 파일 이름
    """
    try:
        # 파일의 절대 경로 확인
        absolute_path = os.path.abspath(file_name)
        print(f"파일이 출력되는 절대 경로: {absolute_path}")

        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"JSON 파일이 '{file_name}'으로 생성되었습니다.")
    except Exception as e:
        print(f"Error: 파일을 저장하는 중 문제가 발생했습니다: {e}")


def load_json(file_name):
    """
    JSON 파일을 불러오는 함수.

    Parameters:
    - file_name (str): 읽어올 파일 이름

    Returns:
    - list of dict: JSON에서 불러온 데이터
    """
    try:
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"Error: '{file_name}' 파일이 존재하지 않습니다.")

        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error: 파일을 불러오는 중 문제가 발생했습니다: {e}")
        return []


def generate_timestamp_filename(prefix="completed", extension="json"):
    """
    타임스탬프를 기반으로 한 파일 이름을 생성하는 함수.

    Parameters:
    - prefix (str): 파일 이름의 접두사 (기본값: 'completed')
    - extension (str): 파일 확장자 (기본값: json)

    Returns:
    - str: 타임스탬프를 포함한 파일 이름
    """
    # 현재 시간 타임스탬프 생성 (YYYYMMDD_HHMMSS 형식)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def main(data_file, output_directory):
    """
    데이터에 ID를 부여하고 JSON 파일로 저장하는 메인 함수.

    Parameters:
    - data_file (str): JSON 데이터를 읽어올 파일 경로
    - output_directory (str): 저장할 파일 디렉토리 경로
    """
    # 멤버 기준 데이터 로드
    members = get_all_members()

    # JSON 파일로부터 데이터를 로드
    data = load_json(data_file)
    if not data:  # 데이터가 없으면 실행 중단
        return

    # 데이터에 id를 할당하고 id 기준으로 정렬
    data_with_ids = assign_ids(data, members)
    sorted_data = sorted(data_with_ids, key=lambda x: x.get('member_id', float('inf')))

    # 타임스탬프 기반의 파일명 생성
    timestamp_filename = generate_timestamp_filename(prefix="completed")
    output_file = os.path.join(output_directory, timestamp_filename)

    # 정렬된 데이터를 타임스탬프 기반 파일명으로 JSON 파일로 저장
    save_json(sorted_data, output_file)


# 사용 예시
if __name__ == "__main__":
    # 메인 함수 실행 (파일 경로 및 출력 디렉토리 지정)
    main("../../input/member/member_data.json", "../../output/member")
