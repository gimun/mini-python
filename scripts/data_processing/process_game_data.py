import json
import os
from datetime import datetime


def assign_ids(data, games):
    """
    주어진 데이터에 게임 이름을 기준으로 ID를 부여하는 함수.

    Parameters:
    - data (list of dict): 플레이 정보가 담긴 데이터 리스트
    - games (dict): 게임 이름과 ID가 포함된 기준 데이터

    Returns:
    - list of dict: ID가 부여된 데이터
    """
    # name을 기준으로 id 맵핑
    id_map = {value['name']: key for key, value in games.items()}

    # 데이터를 id를 기준으로 변환
    for game in data:
        if game['name'] in id_map:
            game['id'] = id_map[game['name']]  # name에 맞는 id를 부여
        else:
            print(f"Warning: '{game['name']}' is not in the games dictionary, skipping...")

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


def main(data_file, games, output_directory):
    """
    데이터에 ID를 부여하고 JSON 파일로 저장하는 메인 함수.

    Parameters:
    - data_file (str): JSON 데이터를 읽어올 파일 경로
    - games (dict): 게임 이름과 ID가 포함된 기준 데이터
    - output_directory (str): 저장할 파일 디렉토리 경로
    """
    # JSON 파일로부터 데이터를 로드
    data = load_json(data_file)
    if not data:  # 데이터가 없으면 실행 중단
        return

    # 데이터에 id를 할당하고 id 기준으로 정렬
    data_with_ids = assign_ids(data, games)
    sorted_data = sorted(data_with_ids, key=lambda x: x.get('id', float('inf')))

    # 타임스탬프 기반의 파일명 생성
    timestamp_filename = generate_timestamp_filename(prefix="completed")
    output_file = os.path.join(output_directory, timestamp_filename)

    # 정렬된 데이터를 타임스탬프 기반 파일명으로 JSON 파일로 저장
    save_json(sorted_data, output_file)


# 사용 예시
if __name__ == "__main__":
    # games 기준 데이터
    games = {
        1: {'name': '뚫어뚫어'},
        2: {'name': '뿌려뿌려'},
        3: {'name': '무찔무찔'},
        4: {'name': '뛰어말어'},
        5: {'name': '높이높이'},
        6: {'name': '넘어넘어'},
        7: {'name': '놓아놓아'},
        8: {'name': '빙글빙글'},
        9: {'name': '뿌셔뿌셔'},
        10: {'name': '미끌미끌'},
        11: {'name': '돌아돌아'},
        12: {'name': '달려달려'},
        13: {'name': '올라올라'},
        14: {'name': '어푸어푸'},
        15: {'name': '붙어붙어'},
        16: {'name': '날아날아'},
        17: {'name': '날려날려'},
        18: {'name': '건너건너'},
        19: {'name': '폴짝폴짝'},
        20: {'name': '쏘아쏘아'},
        21: {'name': '오락가락'},
        22: {'name': '삼단정리'},
        23: {'name': '니편내편'},
        24: {'name': '가둬가둬'}
    }

    # 메인 함수 실행 (파일 경로 및 출력 디렉토리 지정)
    main("../../input/data.json", games, "../../output")
