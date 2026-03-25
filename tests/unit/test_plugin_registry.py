"""Unit tests for the plugin registry."""

import pytest

from ocr_webapp.plugins.base import BasePlugin, PluginRegistry


class EchoPlugin(BasePlugin):
    name = "echo"

    def process(self, text: str, **kwargs: object) -> str:
        return text


def test_register_and_get():
    PluginRegistry.register(EchoPlugin())
    plugin = PluginRegistry.get("echo")
    assert plugin.process("hello") == "hello"


def test_unknown_plugin_raises():
    with pytest.raises(KeyError):
        PluginRegistry.get("does_not_exist")
