# tests/test_plugin_decorator.py
from decorators.plugin_decorator import register_plugin_method, PLUGIN_METHODS


def reset_plugin_methods():
    """테스트 전에 PLUGIN_METHODS를 초기화합니다."""
    PLUGIN_METHODS.clear()


def test_register_plugin_method():
    reset_plugin_methods()

    @register_plugin_method('test_plugin')
    def sample_method():
        pass

    assert 'test_plugin' in PLUGIN_METHODS
    assert 'sample_method' in PLUGIN_METHODS['test_plugin']
