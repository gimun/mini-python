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


def assign_ids(data):
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


def main():
    # 입력 폴더 및 출력 파일 경로 설정
    data_file = '../data/games/games_data.json'
    output_file_path = '../data/result/games_data_with_ids.json'

    """
    데이터에 ID를 부여하고 JSON 파일로 저장하는 메인 함수.

    Parameters:
    - data_file (str): JSON 데이터를 읽어올 파일 경로
    - games (dict): 게임 이름과 ID가 포함된 기준 데이터
    - output_directory (str): 저장할 파일 디렉토리 경로
    """
    # JSON 파일로부터 데이터를 로드
    data = plugin_loader.file_utils.load_single_json(data_file)
    if not data:  # 데이터가 없으면 실행 중단
        return

    # 데이터에 id를 할당하고 id 기준으로 정렬
    data_with_ids = assign_ids(data)
    sorted_data = sorted(data_with_ids, key=lambda x: x.get('id', float('inf')))

    # 결과를 JSON 파일로 저장
    plugin_loader.file_utils.save_single_json(output_file_path, sorted_data)


# 사용 예시
if __name__ == "__main__":
    main()
