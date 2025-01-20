# scripts/plugin_loader.py

import importlib
import os
import sys
import logging
from types import SimpleNamespace
from scripts.plugin_manager import PluginManager
from decorators.plugin_decorator import PLUGIN_METHODS
from typing import Any

# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PluginLoader:
    # Type hints for IDE support
    test_plugin: Any = None
    file_utils: Any = None
    members_utils: Any = None

    def __init__(self):
        self.plugin_manager = PluginManager()
        self.register_and_load_plugins()
        # self.print_plugin_status()

    def register_and_load_plugins(self):
        """디렉토리 내의 모든 플러그인 모듈을 자동으로 발견하여 등록하고 로드"""
        try:
            plugins_dir = self._get_absolute_path("../helpers")
            logger.info(f"플러그인 디렉토리: {plugins_dir}")

            # 플러그인 디렉토리 내의 모든 .py 파일을 찾아 임포트
            for filename in os.listdir(plugins_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = filename[:-3]
                    module_path = os.path.join(plugins_dir, filename)
                    full_module_name = f"helpers.{module_name}"
                    logger.debug(f"플러그인 모듈 발견: {module_name} ({module_path})")

                    if full_module_name not in sys.modules:
                        importlib.import_module(full_module_name)
                        logger.info(f"플러그인 모듈 '{full_module_name}' 임포트 완료.")
                    else:
                        logger.info(f"플러그인 모듈 '{full_module_name}' 이미 임포트됨.")

            logger.info(f"등록된 플러그인 메서드: {PLUGIN_METHODS}")  # 등록된 메서드 확인

            for plugin_name, methods in PLUGIN_METHODS.items():
                plugin_path = f"../helpers/{plugin_name}.py"
                absolute_path = self._get_absolute_path(plugin_path)

                if os.path.exists(absolute_path):
                    logger.debug(f"'{plugin_name}' 플러그인의 경로: {absolute_path}")
                    self.plugin_manager.add_plugin_info(plugin_name, absolute_path, methods)
                    logger.info(f"'{plugin_name}' 플러그인이 등록되었습니다.")
                else:
                    logger.error(f"'{plugin_name}' 플러그인 경로를 찾을 수 없습니다: {absolute_path}")

            # 모든 플러그인 로드
            self.plugin_manager.load_all_plugins()
            logger.info("모든 플러그인들이 성공적으로 로드되었습니다.")

            # 플러그인 메서드를 네임스페이스에 추가
            self._assign_plugin_methods()

        except Exception as e:
            logger.error(f"플러그인 로드 중 오류 발생: {e}", exc_info=True)

    def _assign_plugin_methods(self):
        """플러그인의 메서드를 네임스페이스 객체에 할당"""
        for plugin_name, methods in PLUGIN_METHODS.items():
            plugin_namespace = SimpleNamespace()
            for method_name in methods:
                try:
                    method = self.plugin_manager.get_plugin_method(plugin_name, method_name)
                    setattr(plugin_namespace, method_name, method)
                except AttributeError as e:
                    logger.error(f"Failed to load method '{method_name}' from plugin '{plugin_name}': {e}")

            setattr(self, plugin_name, plugin_namespace)

            # Debug: Check if methods are assigned correctly
            for method_name in methods:
                method = getattr(self, plugin_name, None)
                if method:
                    func = getattr(method, method_name, None)
                    if callable(func):
                        logger.debug(f"Method '{method_name}' correctly assigned to '{plugin_name}'.")
                    else:
                        logger.error(f"Method '{method_name}' not correctly assigned to '{plugin_name}'.")
                else:
                    logger.error(f"Plugin namespace for '{plugin_name}' is missing.")

    def get_plugin_method(self, plugin_name: str, method_name: str) -> Any:
        """Retrieve a specific plugin method. This might be redundant if already handled in PluginManager."""
        return self.plugin_manager.get_plugin_method(plugin_name, method_name)

    @staticmethod
    def _get_absolute_path(relative_path: str) -> str:
        """Convert a relative path to an absolute path."""
        absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))
        logger.debug(f"'{relative_path}' -> 절대 경로: {absolute_path}")
        return absolute_path

    def print_plugin_status(self):
        """Print the status of loaded plugins and their methods."""
        logger.info(f"로드된 플러그인: {self.plugin_manager.list_plugins()}")

        for plugin_name in self.plugin_manager.list_plugins():
            methods = self.plugin_manager.list_plugin_methods(plugin_name)
            logger.info(f"'{plugin_name}' 모듈이 로드되었습니다. 메서드: {methods}")
