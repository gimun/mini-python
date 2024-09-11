# members_utils.py
import polars as pl
import json
import os

# JSON 파일 경로 설정
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'members.json')


def load_members():
    """
    JSON 파일에서 멤버 데이터를 읽어와서 반환하는 함수입니다.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'members.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        members = json.load(file)

    # JSON에서 읽어온 데이터의 key를 정수형으로 변환
    members = {int(key): value for key, value in members.items()}
    return members


def load_members_as_df():
    """
    멤버 정보를 Polars DataFrame으로 반환하는 함수입니다.
    """
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        members = json.load(file)
    # JSON에서 읽어온 데이터의 key를 정수형으로 변환
    members_df = pl.DataFrame({
        'member_id': [int(key) for key in members.keys()],
        'name': [value['name'] for value in members.values()]
    })
    return members_df


def load_active_members_as_df():
    """
    상태가 1인 활성 멤버 정보를 Polars DataFrame으로 반환하는 함수입니다.
    """
    active_members = get_active_members()
    active_members_df = pl.DataFrame({
        'member_id': list(active_members.keys()),
        'name': [info['name'] for info in active_members.values()]
    })
    return active_members_df


def get_member(member_id):
    """
    특정 ID의 멤버 정보를 반환하는 함수입니다.

    :param member_id: 멤버의 ID
    :return: 해당 ID의 멤버 정보 딕셔너리
    """
    members = load_members()
    return members.get(member_id, None)


def get_all_members():
    """
    모든 멤버 정보를 반환하는 함수입니다.

    :return: 모든 멤버 정보 딕셔너리
    """
    return load_members()


def get_active_members():
    """
    상태가 1인 활성 멤버의 정보를 반환하는 함수입니다.

    :return: 활성 멤버 정보 딕셔너리
    """
    members = load_members()
    return {member_id: info for member_id, info in members.items() if info['status'] == 1}


def get_active_member_ids():
    """
    status가 1인 member_id 목록을 반환하는 함수.
    """
    members = load_members()
    return [int(member_id) for member_id, info in members.items() if info['status'] == 1]


def get_inactive_members():
    """
    상태가 0인 비활성 멤버의 정보를 반환하는 함수입니다.

    :return: 비활성 멤버 정보 딕셔너리
    """
    members = load_members()
    return {member_id: info for member_id, info in members.items() if info['status'] == 0}


def get_member_name(member_id):
    """member_id로 멤버의 이름을 반환하는 함수입니다."""
    members = load_members()
    member = members.get(member_id)
    return member['name'] if member else None


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
