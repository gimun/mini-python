import logging
import os
import sys
import json

from scripts.plugin_loader import PluginLoader

# 현재 스크립트의 상위 두 경로를 추가하여 plugin_loader.py 파일을 불러옴
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# PluginLoader 인스턴스 생성
plugin_loader = PluginLoader()


def main():
    # JSON 파일로부터 데이터를 로드
    members = plugin_loader.members_utils.get_active_members()

    # status가 1인 name만 리스트로 추출
    active_names = [item["name"] for item in members.values()]

    logger.info(json.dumps(active_names, ensure_ascii=False))

# 사용 예시
if __name__ == "__main__":
    # 메인 함수 실행 (파일 경로 및 출력 디렉토리 지정)
    main()
