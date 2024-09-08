import json
import os
from datetime import datetime


def assign_ids(data, members):
    """
    주어진 데이터에 멤버 이름을 기준으로 ID를 부여하는 함수.

    Parameters:
    - data (list of dict): 플레이 정보가 담긴 데이터 리스트
    - members (dict): 멤버 이름과 ID가 포함된 기준 데이터

    Returns:
    - list of dict: ID가 부여된 데이터
    """
    # name을 기준으로 id 맵핑
    id_map = {value['name']: key for key, value in members.items()}

    # 데이터를 id를 기준으로 변환
    for member in data:
        if member['name'] in id_map:
            member['member_id'] = id_map[member['name']]  # name에 맞는 id를 부여
        else:
            print(f"Warning: '{member['name']}' is not in the members dictionary, skipping...")

    return data


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


def main(data_file, members, output_directory):
    """
    데이터에 ID를 부여하고 JSON 파일로 저장하는 메인 함수.

    Parameters:
    - data_file (str): JSON 데이터를 읽어올 파일 경로
    - members (dict): 멤버 이름과 ID가 포함된 기준 데이터
    - output_directory (str): 저장할 파일 디렉토리 경로
    """
    # JSON 파일로부터 데이터를 로드
    data = load_json(data_file)
    if not data:  # 데이터가 없으면 실행 중단
        return

    # 데이터에 id를 할당하고 id 기준으로 정렬
    data_with_ids = assign_ids(data, members)
    sorted_data = sorted(data_with_ids, key=lambda x: x.get('id', float('inf')))

    # 타임스탬프 기반의 파일명 생성
    timestamp_filename = generate_timestamp_filename(prefix="completed")
    output_file = os.path.join(output_directory, timestamp_filename)

    # 정렬된 데이터를 타임스탬프 기반 파일명으로 JSON 파일로 저장
    save_json(sorted_data, output_file)


# 사용 예시
if __name__ == "__main__":
    # members 기준 데이터
    members = {
        1: {'name': "기무니", 'status': 1},
        2: {'name': "주키니콩", 'status': 1},
        3: {'name': "유디", 'status': 1},
        4: {'name': "우리집왕떡이", 'status': 1},
        5: {'name': "졔타몽", 'status': 1},
        6: {'name': "비셩이", 'status': 1},
        7: {'name': "시간부자무직백수", 'status': 1},
        8: {'name': "미동", 'status': 1},
        9: {'name': "도라지공주", 'status': 1},
        10: {'name': "보석리아", 'status': 1},
        11: {'name': "희크리", 'status': 1},
        12: {'name': "무명", 'status': 1},
        13: {'name': "충주", 'status': 1},
        14: {'name': "고구마깡", 'status': 1},
        15: {'name': "감자깡", 'status': 1},
        16: {'name': "행복한곰이", 'status': 1},
        17: {'name': "먼지야", 'status': 1},
        18: {'name': "비둘기님", 'status': 1},
        19: {'name': "비누칠", 'status': 1},
        20: {'name': "우당탕탕", 'status': 1},
        21: {'name': "예슬쿵야", 'status': 1},
        22: {'name': "디제이", 'status': 1},
        23: {'name': "고양이랑", 'status': 1},
        24: {'name': "룰루", 'status': 0},
        25: {'name': "백현", 'status': 1},
        26: {'name': "밤양갱", 'status': 1},
        27: {'name': "큐밍", 'status': 1},
        28: {'name': "클라우드", 'status': 1},
        29: {'name': "치즈", 'status': 1},
        30: {'name': "유진공주", 'status': 1},
        31: {'name': "전애옹이다옹", 'status': 1},
        32: {'name': "리틀띰", 'status': 1},
        33: {'name': "경자", 'status': 1},
        34: {'name': "252", 'status': 1},
        35: {'name': "오농농", 'status': 1},
        36: {'name': "고짱이", 'status': 1},
        37: {'name': "보라너굴", 'status': 1},
        38: {'name': "하눌", 'status': 1},
        39: {'name': "타기", 'status': 1},
        40: {'name': "초코칩쿠키", 'status': 1},
        41: {'name': "티티나나", 'status': 1},
        42: {'name': "슈퍼샤이", 'status': 1},
        43: {'name': "이주연", 'status': 0},
        44: {'name': "나무", 'status': 1},
        45: {'name': "빌런즈", 'status': 1},
        46: {'name': "아르미아", 'status': 1},
        47: {'name': "저거저거", 'status': 0},
        48: {'name': "문짱이", 'status': 1},
        49: {'name': "펭도리", 'status': 1},
        50: {'name': "SNFZO", 'status': 0},
        51: {'name': "조니", 'status': 1},
        52: {'name': "할매", 'status': 0},
        53: {'name': "riguleto", 'status': 1},
    }

    # 메인 함수 실행 (파일 경로 및 출력 디렉토리 지정)
    main("../../input/member/member_data.json", members, "../../output/member")
