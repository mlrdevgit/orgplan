import os
import tempfile
import unittest

from orgplan.api import OrgplanAPI
from orgplan.config import Config
from orgplan.dates import DateService
from orgplan.plugins import load_plugins
from orgplan.registry import Registry
from orgplan.tasks import InMemoryTaskStore


class PluginTests(unittest.TestCase):
    def test_loads_register_function(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_path = os.path.join(tmpdir, "orgplan_plugin.py")
            with open(plugin_path, "w", encoding="utf-8") as handle:
                handle.write(
                    "def register(registry):\n"
                    "    registry.add_command('hello', lambda args: 0)\n"
                )

            config = Config(plugins=[tmpdir])
            api = OrgplanAPI(task_store=InMemoryTaskStore(), date_service=DateService())
            registry = Registry(api, config=config)
            load_plugins(config, registry)

            self.assertIn("hello", registry.list_commands())


if __name__ == "__main__":
    unittest.main()
