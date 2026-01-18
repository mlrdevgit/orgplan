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


class TaskTests(unittest.TestCase):
    def test_due_date_property_returns_first_deadline(self):
        task = Task(
            "test",
            deadline=[datetime.date(2025, 6, 20), datetime.date(2025, 6, 25)],
        )
        self.assertEqual(task.due_date, datetime.date(2025, 6, 20))

    def test_due_date_property_returns_scheduled_if_no_deadline(self):
        task = Task(
            "test",
            scheduled=[datetime.date(2025, 6, 10)],
        )
        self.assertEqual(task.due_date, datetime.date(2025, 6, 10))

    def test_due_date_property_prefers_deadline_over_scheduled(self):
        task = Task(
            "test",
            deadline=[datetime.date(2025, 6, 20)],
            scheduled=[datetime.date(2025, 6, 10)],
        )
        self.assertEqual(task.due_date, datetime.date(2025, 6, 20))

    def test_due_date_property_returns_legacy_if_no_timestamps(self):
        task = Task("test", due_date=datetime.date(2025, 6, 30))
        self.assertEqual(task.due_date, datetime.date(2025, 6, 30))

    def test_due_date_property_returns_none_if_nothing(self):
        task = Task("test")
        self.assertIsNone(task.due_date)

    def test_task_with_all_timestamp_fields(self):
        task = Task(
            "test",
            deadline=[datetime.date(2025, 6, 20)],
            scheduled=[datetime.date(2025, 6, 15)],
            timestamp=[datetime.datetime(2025, 6, 10, 14, 30)],
        )
        self.assertEqual(len(task.deadline), 1)
        self.assertEqual(len(task.scheduled), 1)
        self.assertEqual(len(task.timestamp), 1)
        self.assertEqual(task.due_date, datetime.date(2025, 6, 20))


if __name__ == "__main__":
    unittest.main()
