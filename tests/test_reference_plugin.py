import datetime
import importlib
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

from orgplan.api import OrgplanAPI
from orgplan.config import Config
from orgplan.registry import Registry
from orgplan.tasks import InMemoryTaskStore, Task


class FixedDateService:
    def __init__(self, year, month):
        self._year = year
        self._month = month

    def current_year_month(self, today=None):
        return self._year, self._month


class ReferencePluginTests(unittest.TestCase):
    def _load_plugin(self):
        plugin_dir = os.path.join(os.path.dirname(__file__), "..", "examples", "reference_plugin")
        plugin_dir = os.path.abspath(plugin_dir)
        sys.path.insert(0, plugin_dir)
        sys.modules.pop("orgplan_plugin", None)
        return importlib.import_module("orgplan_plugin"), plugin_dir

    def _build_registry(self, tasks, data_root=None):
        api = OrgplanAPI(
            task_store=InMemoryTaskStore(tasks),
            date_service=FixedDateService(2024, 1),
        )
        config = Config(data_root=data_root)
        return Registry(api, config=config)

    def test_registers_commands(self):
        plugin, _ = self._load_plugin()
        registry = self._build_registry([])
        plugin.register(registry)
        commands = registry.list_commands()
        self.assertEqual(commands, ["healthcheck", "tasks-count", "tasks-month"])

    def test_tasks_month_command(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2)),
            Task("beta", state="open", due_date=datetime.date(2024, 1, 3)),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-month")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command([])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("alpha", output)
        self.assertIn("beta", output)

    def test_tasks_count_command(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2)),
            Task("beta", state="done", due_date=datetime.date(2024, 1, 3)),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-count")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("done: 1", output)
        self.assertIn("open: 1", output)

    def test_healthcheck_command(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin, _ = self._load_plugin()
            registry = self._build_registry([], data_root=tmpdir)
            plugin.register(registry)

            command = registry.get_command("healthcheck")
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = command([])

            output = buffer.getvalue()
            self.assertEqual(exit_code, 0)
            self.assertIn("reference plugin OK", output)


if __name__ == "__main__":
    unittest.main()
