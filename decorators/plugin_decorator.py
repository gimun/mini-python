# decorators/plugin_decorator.py

import logging
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)

PLUGIN_METHODS: Dict[str, List[str]] = {}


def register_plugin_method(plugin_name: str) -> Callable:
    """
    Decorator to register a plugin's method.

    Args:
        plugin_name (str): The name of the plugin.

    Returns:
        Callable: The decorator function.
    """

    def decorator(func: Callable) -> Callable:
        if plugin_name not in PLUGIN_METHODS:
            PLUGIN_METHODS[plugin_name] = []
            logger.debug(f"Plugin '{plugin_name}' registered in PLUGIN_METHODS.")

        if func.__name__ not in PLUGIN_METHODS[plugin_name]:
            PLUGIN_METHODS[plugin_name].append(func.__name__)
            logger.debug(f"Method '{func.__name__}' registered for plugin '{plugin_name}'.")
        # else:
        #     logger.warning(f"Method '{func.__name__}' is already registered for plugin '{plugin_name}'.")

        return func

    return decorator
