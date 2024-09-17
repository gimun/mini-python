# decorators/__init__.py
from .plugin_decorator import register_plugin_method, PLUGIN_METHODS

# 해당 모듈에서 사용할 수 있는 모든 요소를 정의
__all__ = ['register_plugin_method', 'PLUGIN_METHODS']
