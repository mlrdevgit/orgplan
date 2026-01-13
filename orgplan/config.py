"""Configuration loading for orgplan."""

import json
import os


class Config:
    def __init__(self, data_root=None, plugins=None, plugin_opts=None):
        self.data_root = data_root
        self.plugins = plugins or []
        self.plugin_opts = plugin_opts or {}


def _normalize_path(value):
    if value is None:
        return None
    return os.path.abspath(os.path.expanduser(value))


def load_config(path=None):
    if path is None:
        path = os.environ.get("ORGPLAN_CONFIG")
    if not path:
        raise ValueError("ORGPLAN_CONFIG is not set and no path was provided")

    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    data_root = _normalize_path(data.get("data_root"))
    plugins = data.get("plugins", [])
    plugin_opts = data.get("plugin_opts", {})

    if not isinstance(plugins, list):
        raise ValueError("plugins must be a list")
    if not isinstance(plugin_opts, dict):
        raise ValueError("plugin_opts must be a dict")

    plugins = [_normalize_path(path) for path in plugins]

    if not data_root:
        raise ValueError("data_root is required in the config JSON")
    if not os.path.isdir(data_root):
        raise ValueError(f"data_root does not exist or is not a directory: {data_root}")

    return Config(data_root=data_root, plugins=plugins, plugin_opts=plugin_opts)
