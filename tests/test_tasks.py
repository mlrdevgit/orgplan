import datetime
import unittest

from orgplan.tasks import InMemoryTaskStore, Task


class TaskStoreTests(unittest.TestCase):
    def test_filters_by_year_and_month(self):
        tasks = [
            Task("jan", due_date=datetime.date(2024, 1, 5)),
            Task("feb", due_date=datetime.date(2024, 2, 10)),
            Task("next", due_date=datetime.date(2025, 1, 1)),
        ]
        store = InMemoryTaskStore(tasks)
        results = store.list(year=2024, month=1)
        self.assertEqual([task.title for task in results], ["jan"])

    def test_filters_by_state(self):
        tasks = [
            Task("open", state="open", due_date=datetime.date(2024, 1, 5)),
            Task("done", state="done", due_date=datetime.date(2024, 1, 6)),
        ]
        store = InMemoryTaskStore(tasks)
        results = store.list(state="done")
        self.assertEqual([task.title for task in results], ["done"])


if __name__ == "__main__":
    unittest.main()
