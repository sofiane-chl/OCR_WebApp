"""Base class for all plugins/extensions.

To add a new plugin:
1. Subclass BasePlugin
2. Implement process()
3. Register it via PluginRegistry.register()

Example
-------
from ocr_webapp.plugins.base import BasePlugin, PluginRegistry

class UpperCasePlugin(BasePlugin):
    name = "uppercase"

    def process(self, text: str, **kwargs: object) -> str:
        return text.upper()

PluginRegistry.register(UpperCasePlugin())
"""

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    name: str = "unnamed"

    @abstractmethod
    def process(self, text: str, **kwargs: object) -> str:
        """Transform or enrich *text* and return the result."""


class PluginRegistry:
    _plugins: dict[str, BasePlugin] = {}

    @classmethod
    def register(cls, plugin: BasePlugin) -> None:
        cls._plugins[plugin.name] = plugin

    @classmethod
    def get(cls, name: str) -> BasePlugin:
        if name not in cls._plugins:
            raise KeyError(f"Plugin '{name}' is not registered.")
        return cls._plugins[name]

    @classmethod
    def all(cls) -> list[BasePlugin]:
        return list(cls._plugins.values())
