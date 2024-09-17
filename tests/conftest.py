# tests/conftest.py

from unittest.mock import patch

import pytest

from decorators.plugin_decorator import PLUGIN_METHODS
from helpers.members_utils import MembersUtils


@pytest.fixture(scope="function", autouse=True)
def reset_plugin_methods():
    """
    각 테스트가 실행되기 전에 PLUGIN_METHODS를 초기화합니다.
    """
    PLUGIN_METHODS.clear()
    yield
    PLUGIN_METHODS.clear()


@pytest.fixture(scope="function", autouse=True)
def reset_members_cache():
    """
    각 테스트가 실행되기 전에 MembersUtils의 캐시를 초기화합니다.
    """
    MembersUtils._members_cache = None
    yield
    MembersUtils._members_cache = None


@pytest.fixture
def sample_members_data():
    """
    테스트에 사용할 샘플 멤버 데이터를 제공합니다.
    """
    return {
        1: {'name': 'Alice', 'status': 1},
        2: {'name': 'Bob', 'status': 0},
        3: {'name': 'Charlie', 'status': 1},
    }


@pytest.fixture
def sample_play_data():
    """
    테스트에 사용할 샘플 플레이 데이터를 제공합니다.
    """
    return [
        {'name': 'Alice', 'score': 100},
        {'name': 'Charlie', 'score': 150},
        {'name': 'Eve', 'score': 200},  # 존재하지 않는 멤버
    ]


@pytest.fixture
def mock_file_utils():
    """
    file_utils 플러그인의 메서드를 모킹합니다.
    """
    with patch('helpers.file_utils.FileUtils.save_to_json') as mock_save, \
            patch('helpers.file_utils.FileUtils.load_json_files_from_folder') as mock_load:
        mock_save.return_value = None
        mock_load.return_value = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
        yield mock_save, mock_load
