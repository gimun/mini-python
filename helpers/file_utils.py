import os
import json
import logging
from decorators.plugin_decorator import register_plugin_method

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FileUtils:
    @staticmethod
    def initialize():
        """플러그인 초기화"""
        logger.info("file_utils 플러그인이 초기화되었습니다.")

    @staticmethod
    @register_plugin_method('file_utils')
    def load_single_json(file_path):
        """단일 JSON 파일을 읽어 데이터를 반환하는 함수"""
        try:
            file_path = FileUtils.get_absolute_path(file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

            data = FileUtils._load_json_file(file_path)
            if not data:
                logger.warning(f"{file_path}에서 유효한 데이터가 없습니다.")
            return data
        except Exception as e:
            logger.error(f"JSON 파일을 불러오는 중 오류 발생: {e}", exc_info=True)
            raise

    @staticmethod
    @register_plugin_method('file_utils')
    def save_single_json(output_file_path, data):
        """단일 JSON 파일을 저장하는 함수"""
        try:
            output_file_path = FileUtils._prepare_output_path(output_file_path)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"JSON 데이터가 {output_file_path}에 저장되었습니다.")
        except Exception as e:
            logger.error(f"JSON 파일 저장 중 오류 발생: {e}", exc_info=True)
            raise

    @staticmethod
    @register_plugin_method('file_utils')
    def save_to_json(output_file_path, data_frame):
        """DataFrame을 JSON 파일로 저장하는 함수"""
        try:
            output_file_path = FileUtils._prepare_output_path(output_file_path)
            data_frame.write_json(output_file_path)  # 데이터프레임을 JSON으로 저장
            logger.info(f"JSON 결과가 {output_file_path}에 저장되었습니다.")
        except Exception as e:
            logger.error(f"JSON 파일 저장 중 오류 발생: {e}", exc_info=True)
            raise

    @staticmethod
    @register_plugin_method('file_utils')
    def load_json_files_from_folder(folder_path):
        """지정된 폴더 내의 모든 JSON 파일을 읽어 데이터로 반환"""
        try:
            folder_path = FileUtils.get_absolute_path(folder_path)
            if not os.path.exists(folder_path):
                raise FileNotFoundError(f"폴더를 찾을 수 없습니다: {folder_path}")

            json_files = FileUtils._get_json_files(folder_path)
            if not json_files:
                logger.warning(f"{folder_path}에 JSON 파일이 없습니다.")

            all_data = FileUtils._load_all_json_files(json_files)
            if not all_data:
                logger.warning(f"{folder_path}에서 유효한 데이터가 없습니다.")
            return all_data
        except Exception as e:
            logger.error(f"JSON 파일을 불러오는 중 오류 발생: {e}", exc_info=True)
            raise

    @staticmethod
    def get_absolute_path(relative_path):
        """주어진 상대 경로를 절대 경로로 변환"""
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))
        logger.debug(f"상대 경로 '{relative_path}' -> 절대 경로 '{abs_path}'로 변환")
        return abs_path

    @staticmethod
    def _prepare_output_path(output_file_path):
        """출력 파일 경로를 절대 경로로 변환하고 폴더가 없으면 생성"""
        output_file_path = FileUtils.get_absolute_path(output_file_path)
        output_folder = os.path.dirname(output_file_path)
        os.makedirs(output_folder, exist_ok=True)  # 존재하지 않는 폴더는 생성
        logger.debug(f"출력 폴더가 생성되었거나 이미 존재합니다: {output_folder}")
        return output_file_path

    @staticmethod
    def _get_json_files(folder_path):
        """지정된 폴더에서 JSON 파일 목록을 반환"""
        json_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]
        logger.debug(f"폴더 {folder_path}에서 {len(json_files)}개의 JSON 파일을 발견했습니다.")
        return json_files

    @staticmethod
    def _load_all_json_files(json_files):
        """모든 JSON 파일을 읽어 데이터를 반환"""
        all_data = []
        for json_file in json_files:
            data = FileUtils._load_json_file(json_file)
            if data:
                all_data.extend(data)
        return all_data

    @staticmethod
    def _load_json_file(file_path):
        """JSON 파일을 읽어 데이터를 반환"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.debug(f"JSON 데이터 {file_path}에서 로드됨")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파일 디코딩 오류 {file_path}: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"JSON 파일 읽기 오류 {file_path}: {e}", exc_info=True)
        return []
