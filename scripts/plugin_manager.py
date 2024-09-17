# scripts/plugin_manager.py

import importlib.util
import inspect
import logging
import os
from typing import Any, Callable, Dict, List

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PluginManager:
    """
    Manages loading and accessing plugin modules and their methods.
    """

    PLUGIN_PATH_KEY = "path"
    PLUGIN_METHODS_KEY = "methods"

    def __init__(self):
        self.plugins: Dict[str, Any] = {}
        self.plugin_info: Dict[str, Dict[str, Any]] = {}  # 플러그인 정보 관리

    def add_plugin_info(self, plugin_name: str, plugin_path: str, methods: List[str]) -> None:
        """
        Adds information about a plugin.

        Args:
            plugin_name (str): The name of the plugin.
            plugin_path (str): The file path to the plugin module.
            methods (List[str]): List of method names to register from the plugin.
        """
        if plugin_name in self.plugin_info:
            logger.warning(f"Plugin info for '{plugin_name}' already exists.")
        else:
            self.plugin_info[plugin_name] = {
                self.PLUGIN_PATH_KEY: plugin_path,
                self.PLUGIN_METHODS_KEY: methods
            }
            logger.info(f"Plugin info for '{plugin_name}' added.")

    def load_all_plugins(self) -> None:
        """
        Loads all plugins based on the stored plugin_info.
        """
        for plugin_name, info in self.plugin_info.items():
            plugin_path = info.get(self.PLUGIN_PATH_KEY)
            if not os.path.exists(plugin_path):
                logger.error(f"Plugin '{plugin_name}' path does not exist: {plugin_path}")
                continue

            try:
                plugin = self._load_plugin(plugin_name, plugin_path)
                self.plugins[plugin_name] = plugin
                logger.info(f"Plugin '{plugin_name}' successfully loaded.")

                self._initialize_plugin(plugin_name, plugin)
            except Exception as e:
                logger.error(f"Failed to load plugin '{plugin_name}': {e}")
                # Continue loading other plugins instead of raising the exception
                continue

    def _load_plugin(self, plugin_name: str, plugin_path: str) -> Any:
        """
        Loads a plugin module from a given path.

        Args:
            plugin_name (str): The name of the plugin.
            plugin_path (str): The file path to the plugin module.

        Returns:
            Any: The loaded plugin module or instance.
        """
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot find spec for plugin '{plugin_name}' at '{plugin_path}'")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        logger.debug(f"Plugin '{plugin_name}' module loaded from '{plugin_path}'.")

        # Check if plugin has a class to instantiate
        classes = [
            obj for name, obj in inspect.getmembers(module, inspect.isclass)
            if obj.__module__ == module.__name__
        ]
        if classes:
            # Assume the first class is the plugin class
            plugin_class = classes[0]
            plugin_instance = plugin_class()
            logger.debug(f"Plugin '{plugin_name}' class '{plugin_class.__name__}' instantiated.")
            return plugin_instance
        else:
            # Assume the module itself has callable functions
            return module

    def _initialize_plugin(self, plugin_name: str, plugin: Any) -> None:
        """
        Initializes a plugin by calling its 'initialize' method if available.

        Args:
            plugin_name (str): The name of the plugin.
            plugin (Any): The loaded plugin module or instance.
        """
        logger.info(f"Initializing plugin '{plugin_name}'.")

        if hasattr(plugin, 'initialize') and callable(getattr(plugin, 'initialize')):
            try:
                plugin.initialize()
                logger.info(f"Plugin '{plugin_name}' initialized successfully.")
            except Exception as e:
                logger.error(f"Error during initialization of plugin '{plugin_name}': {e}")
                # Depending on requirements, you might want to remove the plugin or keep it loaded
        else:
            logger.info(f"Plugin '{plugin_name}' does not have an 'initialize' method.")

    def get_plugin_method(self, plugin_name: str, method_name: str) -> Callable:
        """
        Retrieves a specific method from a plugin.

        Args:
            plugin_name (str): The name of the plugin.
            method_name (str): The name of the method to retrieve.

        Returns:
            Callable: The requested method.

        Raises:
            ValueError: If the plugin is not loaded.
            AttributeError: If the method is not found or not callable.
        """
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' is not loaded.")

        plugin = self.plugins[plugin_name]
        methods = self.plugin_info.get(plugin_name, {}).get(self.PLUGIN_METHODS_KEY, [])

        if method_name not in methods:
            raise AttributeError(f"Method '{method_name}' is not registered for plugin '{plugin_name}'.")

        # If plugin is an instance, retrieve method from instance
        if hasattr(plugin, method_name):
            method = getattr(plugin, method_name)
            if callable(method):
                return method
            else:
                raise AttributeError(f"Method '{method_name}' in plugin '{plugin_name}' is not callable.")
        else:
            raise AttributeError(f"Method '{method_name}' not found in plugin '{plugin_name}'.")

    def list_plugins(self) -> List[str]:
        """
        Returns a list of loaded plugins.

        Returns:
            List[str]: List of plugin names.
        """
        return list(self.plugins.keys())

    def list_plugin_methods(self, plugin_name: str) -> List[str]:
        """
        Returns a list of methods registered for a specific plugin.

        Args:
            plugin_name (str): The name of the plugin.

        Returns:
            List[str]: List of method names.

        Raises:
            ValueError: If the plugin is not loaded.
        """
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' is not loaded.")
        return self.plugin_info.get(plugin_name, {}).get(self.PLUGIN_METHODS_KEY, [])
