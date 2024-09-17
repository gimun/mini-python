# helpers/test_plugin.py

import logging
from decorators.plugin_decorator import register_plugin_method

logger = logging.getLogger(__name__)


class TestPlugin:
    @staticmethod
    def initialize():
        logger.info("TestPlugin initialized.")

    @staticmethod
    @register_plugin_method('test_plugin')
    def greet(name):
        message = f"Hello, {name}! This is TestPlugin."
        logger.info(message)
        return message

    @staticmethod
    @register_plugin_method('test_plugin')
    def add(a, b):
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            logger.error("Both a and b must be numeric.")
            raise TypeError("Both a and b must be numeric.")
        result = a + b
        logger.info(f"Adding {a} + {b} = {result}")
        return result
