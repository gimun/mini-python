import os
import json
import logging
import polars as pl
from decorators.plugin_decorator import register_plugin_method

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# JSON 파일 경로 설정
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'members.json')


class MembersUtils:
    """멤버 정보를 관리하는 유틸리티 클래스."""

    _members_cache = None  # 캐시 변수: 멤버 데이터를 저장

    @staticmethod
    def initialize():
        """플러그인 초기화 메서드"""
        logger.debug("members_utils 플러그인이 초기화되었습니다.")

    @classmethod
    def load_members(cls):
        """
        JSON 파일에서 멤버 데이터를 읽어와 캐싱 후 반환.
        """
        if cls._members_cache is None:
            logger.debug("members.json 데이터를 로드 중입니다...")
            cls._members_cache = cls._load_members_from_file()

        return cls._members_cache

    @staticmethod
    def _load_members_from_file():
        """
        JSON 파일을 읽어 멤버 데이터를 반환하는 헬퍼 함수.
        """
        try:
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                members = json.load(file)
            logger.debug("members.json 데이터가 성공적으로 로드되었습니다.")
            return {int(key): value for key, value in members.items()}  # key를 정수로 변환
        except FileNotFoundError:
            logger.error(f"JSON 파일을 찾을 수 없습니다: {JSON_FILE_PATH}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파일 파싱 오류: {e}")
            return {}

    @staticmethod
    @register_plugin_method('members_utils')
    def get_active_member_ids():
        """
        상태가 1인 멤버의 ID 목록을 반환.
        """
        active_members = MembersUtils.get_active_members()
        active_ids = list(active_members.keys())
        logger.debug(f"활성 멤버 ID 목록: {active_ids}")
        return active_ids

    @staticmethod
    def get_active_members():
        """
        상태가 1인 활성 멤버 정보를 반환.
        """
        members = MembersUtils.load_members()
        active_members = {member_id: info for member_id, info in members.items() if info.get('status') == 1}
        logger.debug(f"활성 멤버 정보: {active_members}")
        return active_members

    @staticmethod
    @register_plugin_method('members_utils')
    def load_active_members_as_df():
        """
        상태가 1인 활성 멤버 정보를 Polars DataFrame으로 반환.
        """
        active_members = MembersUtils.get_active_members()
        if not active_members:
            logger.warning("활성 멤버가 없습니다.")
        else:
            logger.debug(f"활성 멤버 데이터프레임 생성 중...")

        active_members_df = pl.DataFrame({
            'member_id': list(active_members.keys()),
            'name': [info.get('name') for info in active_members.values()]
        })
        logger.debug(f"활성 멤버 DataFrame 생성 완료: {active_members_df}")
        return active_members_df

    @staticmethod
    @register_plugin_method('members_utils')
    def get_member(member_id):
        """
        특정 ID의 멤버 정보를 반환.
        """
        member = MembersUtils.load_members().get(member_id)
        if member:
            logger.debug(f"멤버 {member_id} 정보: {member}")
        else:
            logger.warning(f"멤버 {member_id}을(를) 찾을 수 없습니다.")
        return member

    @staticmethod
    @register_plugin_method('members_utils')
    def get_member_name(member_id):
        """
        특정 ID의 멤버 이름 정보를 반환.
        """
        member = MembersUtils.get_member(member_id)
        if member:
            logger.debug(f"멤버 {member_id} 정보: {member}")
        else:
            logger.warning(f"멤버 {member_id}을(를) 찾을 수 없습니다.")
        return member['name']

    @staticmethod
    @register_plugin_method('members_utils')
    def get_all_members():
        """
        모든 멤버 정보를 반환.
        """
        members = MembersUtils.load_members()
        logger.debug(f"전체 멤버 수: {len(members)}")
        return members

    @staticmethod
    @register_plugin_method('members_utils')
    def assign_ids(data, members):
        """
        주어진 데이터에 멤버 이름을 기준으로 ID를 부여.

        Parameters:
        - data (list of dict): 플레이 정보가 담긴 데이터 리스트
        - members (dict): 멤버 이름과 ID가 포함된 기준 데이터

        Returns:
        - list of dict: ID가 부여된 데이터 리스트
        """
        id_map = {value['name']: key for key, value in members.items()}
        missing_members = []

        for member in data:
            member_id = id_map.get(member['name'])
            if member_id:
                member['member_id'] = member_id  # name에 맞는 id를 부여
            else:
                missing_members.append(member['name'])
                logger.warning(f"'{member['name']}'은 멤버 데이터에 존재하지 않습니다.")

        if missing_members:
            logger.warning(f"ID가 부여되지 않은 멤버들: {missing_members}")

        return data
