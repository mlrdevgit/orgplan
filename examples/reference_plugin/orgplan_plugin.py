"""Reference plugin demonstrating command registration and core API usage."""

import argparse
import os


def _parse_args(parser, args):
    return parser.parse_args(args)


def register(registry):
    api = registry.api

    def tasks_month(args):
        parser = argparse.ArgumentParser(prog="tasks-month")
        parser.add_argument("--state", default="open", help="Filter by task state")
        opts = _parse_args(parser, args)

        year, month = api.dates.current_year_month()
        tasks = api.tasks.list(year=year, month=month, state=opts.state)

        label = f"{year:04d}-{month:02d}"
        if not tasks:
            print(f"No {opts.state} tasks for {label}.")
            return 0

        print(f"{opts.state} tasks for {label}:")
        for task in tasks:
            due = task.due_date.isoformat() if task.due_date else "no-date"
            print(f"- {task.title} ({due})")
        return 0

    def tasks_count(args):
        parser = argparse.ArgumentParser(prog="tasks-count")
        parser.add_argument("--year", type=int, help="Year to filter tasks")
        parser.add_argument("--month", type=int, help="Month to filter tasks")
        opts = _parse_args(parser, args)

        tasks = api.tasks.list(year=opts.year, month=opts.month)
        counts = {}
        for task in tasks:
            counts[task.state] = counts.get(task.state, 0) + 1

        if not counts:
            print("No tasks found.")
            return 0

        for state in sorted(counts.keys()):
            print(f"{state}: {counts[state]}")
        return 0

    def healthcheck(args):
        parser = argparse.ArgumentParser(prog="healthcheck")
        _parse_args(parser, args)

        data_root = None
        if registry.config is not None:
            data_root = registry.config.data_root

        if data_root and not os.path.exists(data_root):
            print(f"Data root does not exist: {data_root}")
            return 1

        print("orgplan reference plugin OK")
        return 0

    registry.add_command("tasks-month", tasks_month)
    registry.add_command("tasks-count", tasks_count)
    registry.add_command("healthcheck", healthcheck)
