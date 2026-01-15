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
        expected = [
            "healthcheck",
            "tasks-canceled",
            "tasks-count",
            "tasks-done",
            "tasks-month",
            "tasks-non-open",
            "tasks-open",
            "tasks-p0",
            "tasks-p1",
            "tasks-priority",
        ]
        self.assertEqual(commands, expected)

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

    def test_tasks_open_command(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2), tags=["p1"]),
            Task("beta", state="done", due_date=datetime.date(2024, 1, 3)),
            Task("gamma", state="open", due_date=datetime.date(2024, 1, 4)),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-open")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("alpha", output)
        self.assertIn("gamma", output)
        self.assertNotIn("beta", output)
        self.assertIn("Open tasks (2)", output)

    def test_tasks_done_command(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2)),
            Task("beta", state="done", due_date=datetime.date(2024, 1, 3), tags=["p0"]),
            Task("gamma", state="done", due_date=datetime.date(2024, 1, 4)),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-done")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertNotIn("alpha", output)
        self.assertIn("beta", output)
        self.assertIn("gamma", output)
        self.assertIn("Done tasks (2)", output)

    def test_tasks_canceled_command(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2)),
            Task("beta", state="canceled", due_date=datetime.date(2024, 1, 3)),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-canceled")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertNotIn("alpha", output)
        self.assertIn("beta", output)
        self.assertIn("Canceled tasks (1)", output)

    def test_tasks_canceled_command_empty(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2)),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-canceled")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("No canceled tasks found", output)

    def test_tasks_non_open_command(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2)),
            Task("beta", state="done", due_date=datetime.date(2024, 1, 3)),
            Task("gamma", state="canceled", due_date=datetime.date(2024, 1, 4)),
            Task("delta", state="delegated", due_date=datetime.date(2024, 1, 5)),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-non-open")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertNotIn("alpha", output)
        self.assertIn("beta", output)
        self.assertIn("gamma", output)
        self.assertIn("delta", output)
        self.assertIn("Non-open tasks (3)", output)
        self.assertIn("[DONE]", output)
        self.assertIn("[CANCELED]", output)
        self.assertIn("[DELEGATED]", output)

    def test_tasks_p0_command(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2), tags=["p0"]),
            Task("beta", state="open", due_date=datetime.date(2024, 1, 3), tags=["p1"]),
            Task("gamma", state="done", due_date=datetime.date(2024, 1, 4), tags=["p0"]),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-p0")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("alpha", output)
        self.assertNotIn("beta", output)
        self.assertIn("gamma", output)
        self.assertIn("P0 tasks (2)", output)

    def test_tasks_p0_command_with_state_filter(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2), tags=["p0"]),
            Task("beta", state="done", due_date=datetime.date(2024, 1, 3), tags=["p0"]),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-p0")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1", "--state", "open"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("alpha", output)
        self.assertNotIn("beta", output)
        self.assertIn("P0 tasks (1)", output)

    def test_tasks_p1_command(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2), tags=["p1"]),
            Task("beta", state="open", due_date=datetime.date(2024, 1, 3), tags=["p0"]),
            Task("gamma", state="done", due_date=datetime.date(2024, 1, 4), tags=["p1"]),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-p1")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("alpha", output)
        self.assertNotIn("beta", output)
        self.assertIn("gamma", output)
        self.assertIn("P1 tasks (2)", output)

    def test_tasks_priority_command(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2), tags=["p0"]),
            Task("beta", state="open", due_date=datetime.date(2024, 1, 3), tags=["p1"]),
            Task("gamma", state="open", due_date=datetime.date(2024, 1, 4), tags=["p2"]),
            Task("delta", state="done", due_date=datetime.date(2024, 1, 5), tags=["p0"]),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-priority")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("alpha", output)
        self.assertIn("beta", output)
        self.assertNotIn("gamma", output)
        self.assertIn("delta", output)
        self.assertIn("P0/P1 priority tasks (3)", output)
        self.assertIn("[P0]", output)
        self.assertIn("[P1]", output)

    def test_tasks_priority_command_empty(self):
        tasks = [
            Task("alpha", state="open", due_date=datetime.date(2024, 1, 2), tags=["p2"]),
        ]
        plugin, _ = self._load_plugin()
        registry = self._build_registry(tasks)
        plugin.register(registry)

        command = registry.get_command("tasks-priority")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = command(["--year", "2024", "--month", "1"])

        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("No P0/P1 tasks found", output)

    def test_all_commands_registered(self):
        plugin, _ = self._load_plugin()
        registry = self._build_registry([])
        plugin.register(registry)
        commands = registry.list_commands()
        expected = [
            "healthcheck",
            "tasks-canceled",
            "tasks-count",
            "tasks-done",
            "tasks-month",
            "tasks-non-open",
            "tasks-open",
            "tasks-p0",
            "tasks-p1",
            "tasks-priority",
        ]
        self.assertEqual(commands, expected)


if __name__ == "__main__":
    unittest.main()
