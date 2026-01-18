"""Task storage primitives."""

import datetime
import os


class Task:
    def __init__(self, title, state="open", due_date=None, tags=None, notes=None,
                 line_number=None, deadline=None, scheduled=None, timestamp=None):
        self.title = title
        self.state = state
        self._legacy_due_date = due_date
        self.tags = list(tags or [])
        self.notes = notes
        self.line_number = line_number
        self.deadline = list(deadline or [])
        self.scheduled = list(scheduled or [])
        self.timestamp = list(timestamp or [])

    @property
    def due_date(self):
        """Return first deadline, or first scheduled, or legacy due_date."""
        if self.deadline:
            return self.deadline[0]
        if self.scheduled:
            return self.scheduled[0]
        return self._legacy_due_date

    def __repr__(self):
        return (
            "Task("
            f"title={self.title!r}, "
            f"state={self.state!r}, "
            f"due_date={self.due_date!r}, "
            f"tags={self.tags!r}, "
            f"notes={self.notes!r}, "
            f"line_number={self.line_number!r}, "
            f"deadline={self.deadline!r}, "
            f"scheduled={self.scheduled!r}, "
            f"timestamp={self.timestamp!r}"
            ")"
        )


class InMemoryTaskStore:
    def __init__(self, tasks=None):
        self._tasks = list(tasks or [])

    def list(self, year=None, month=None, state=None):
        tasks = self._tasks
        if state is not None:
            tasks = [task for task in tasks if task.state == state]

        if year is not None or month is not None:
            filtered = []
            for task in tasks:
                due_date = task.due_date
                if not isinstance(due_date, datetime.date):
                    continue
                if year is not None and due_date.year != year:
                    continue
                if month is not None and due_date.month != month:
                    continue
                filtered.append(task)
            tasks = filtered

        return list(tasks)


class FileTaskStore:
    def __init__(self, data_root, date_service=None, parser=None):
        self._data_root = data_root
        self._date_service = date_service
        if parser is None:
            from orgplan.markup import parse_month_notes

            parser = parse_month_notes
        self._parser = parser

    def get_month_path(self, year, month):
        return os.path.join(self._data_root, f"{year:04d}", f"{month:02d}-notes.md")

    def month_exists(self, year, month):
        return os.path.exists(self.get_month_path(year, month))

    def list(self, year=None, month=None, state=None):
        if year is None or month is None:
            if self._date_service is None:
                raise ValueError("date_service is required to default year/month")
            year, month = self._date_service.current_year_month()

        path = self.get_month_path(year, month)
        if not os.path.exists(path):
            return []

        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()

        tasks = self._parser(text)

        if state is not None:
            tasks = [task for task in tasks if task.state == state]

        return list(tasks)
