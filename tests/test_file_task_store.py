import os
import tempfile
import unittest

from orgplan.dates import DateService
from orgplan.tasks import FileTaskStore


class FixedDateService(DateService):
    def __init__(self, year, month):
        self._year = year
        self._month = month

    def current_year_month(self, today=None):
        return self._year, self._month


class FileTaskStoreTests(unittest.TestCase):
    def test_missing_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = FileTaskStore(tmpdir, date_service=FixedDateService(2024, 1))
            tasks = store.list()
            self.assertEqual(tasks, [])

    def test_get_month_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = FileTaskStore(tmpdir, date_service=FixedDateService(2024, 1))
            path = store.get_month_path(2024, 1)
            self.assertTrue(path.endswith(os.path.join("2024", "01-notes.md")))

    def test_month_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = FileTaskStore(tmpdir, date_service=FixedDateService(2024, 1))
            self.assertFalse(store.month_exists(2024, 1))

            path = store.get_month_path(2024, 1)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("# TODO List\n- Task one\n")

            self.assertTrue(store.month_exists(2024, 1))

    def test_parses_tasks_from_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = FileTaskStore(tmpdir, date_service=FixedDateService(2024, 1))
            path = store.get_month_path(2024, 1)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("# TODO List\n- [DONE] #p1 Ship it\n")

            tasks = store.list(2024, 1)
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0].title, "Ship it")
            self.assertEqual(tasks[0].state, "done")
            self.assertEqual(tasks[0].tags, ["p1"])

    def test_filters_by_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = FileTaskStore(tmpdir, date_service=FixedDateService(2024, 1))
            path = store.get_month_path(2024, 1)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("# TODO List\n- [DONE] Done task\n- Open task\n")

            tasks = store.list(2024, 1, state="done")
            self.assertEqual([task.title for task in tasks], ["Done task"])


if __name__ == "__main__":
    unittest.main()
