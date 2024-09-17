# tests/test_plugin_manager.py
import pytest
import os
from scripts.plugin_manager import PluginManager


@pytest.fixture
def plugin_manager():
    return PluginManager()


def test_add_plugin_info(plugin_manager):
    plugin_name = 'test_plugin'
    plugin_path = os.path.abspath('helpers/test_plugin.py')
    methods = ['greet', 'add']

    plugin_manager.add_plugin_info(plugin_name, plugin_path, methods)

    assert plugin_name in plugin_manager.plugin_info
    assert plugin_manager.plugin_info[plugin_name]['path'] == plugin_path
    assert plugin_manager.plugin_info[plugin_name]['methods'] == methods
