# tests/test_plugin_loader.py
import pytest
from scripts.plugin_loader import PluginLoader


@pytest.fixture
def plugin_loader():
    return PluginLoader()


def test_get_plugin_method(plugin_loader):
    method = plugin_loader.test_plugin.greet

    # Assertions
    assert callable(method)
    assert method('Alice') == "Hello, Alice! This is TestPlugin."
    plugin_loader.test_plugin.greet('Alice')
