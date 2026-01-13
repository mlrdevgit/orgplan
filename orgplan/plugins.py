"""Plugin loader for explicit plugin paths."""

import importlib
import sys


class PluginError(RuntimeError):
    pass


def load_plugins(config, registry):
    for path in config.plugins:
        if path not in sys.path:
            sys.path.insert(0, path)
        try:
            module = importlib.import_module("orgplan_plugin")
        except Exception as exc:
            raise PluginError(f"Failed to import plugin at {path}") from exc

        register = getattr(module, "register", None)
        if not callable(register):
            raise PluginError(f"Plugin at {path} has no register(registry) function")

        register(registry)
