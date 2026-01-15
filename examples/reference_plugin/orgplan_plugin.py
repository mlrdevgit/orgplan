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

    def tasks_open(args):
        parser = argparse.ArgumentParser(prog="tasks-open")
        parser.add_argument("--year", type=int, help="Year to filter tasks")
        parser.add_argument("--month", type=int, help="Month to filter tasks")
        opts = _parse_args(parser, args)

        tasks = api.tasks.list(year=opts.year, month=opts.month, state="open")

        if not tasks:
            print("No open tasks found.")
            return 0

        print(f"Open tasks ({len(tasks)}):")
        for task in tasks:
            due = task.due_date.isoformat() if task.due_date else "no-date"
            tags_str = " ".join(f"#{tag}" for tag in task.tags) if task.tags else ""
            print(f"- {task.title} ({due}) {tags_str}")
        return 0

    def tasks_done(args):
        parser = argparse.ArgumentParser(prog="tasks-done")
        parser.add_argument("--year", type=int, help="Year to filter tasks")
        parser.add_argument("--month", type=int, help="Month to filter tasks")
        opts = _parse_args(parser, args)

        tasks = api.tasks.list(year=opts.year, month=opts.month, state="done")

        if not tasks:
            print("No done tasks found.")
            return 0

        print(f"Done tasks ({len(tasks)}):")
        for task in tasks:
            due = task.due_date.isoformat() if task.due_date else "no-date"
            tags_str = " ".join(f"#{tag}" for tag in task.tags) if task.tags else ""
            print(f"- {task.title} ({due}) {tags_str}")
        return 0

    def tasks_canceled(args):
        parser = argparse.ArgumentParser(prog="tasks-canceled")
        parser.add_argument("--year", type=int, help="Year to filter tasks")
        parser.add_argument("--month", type=int, help="Month to filter tasks")
        opts = _parse_args(parser, args)

        tasks = api.tasks.list(year=opts.year, month=opts.month, state="canceled")

        if not tasks:
            print("No canceled tasks found.")
            return 0

        print(f"Canceled tasks ({len(tasks)}):")
        for task in tasks:
            due = task.due_date.isoformat() if task.due_date else "no-date"
            tags_str = " ".join(f"#{tag}" for tag in task.tags) if task.tags else ""
            print(f"- {task.title} ({due}) {tags_str}")
        return 0

    def tasks_non_open(args):
        parser = argparse.ArgumentParser(prog="tasks-non-open")
        parser.add_argument("--year", type=int, help="Year to filter tasks")
        parser.add_argument("--month", type=int, help="Month to filter tasks")
        opts = _parse_args(parser, args)

        all_tasks = api.tasks.list(year=opts.year, month=opts.month)
        tasks = [task for task in all_tasks if task.state != "open"]

        if not tasks:
            print("No non-open tasks found.")
            return 0

        print(f"Non-open tasks ({len(tasks)}):")
        for task in tasks:
            due = task.due_date.isoformat() if task.due_date else "no-date"
            tags_str = " ".join(f"#{tag}" for tag in task.tags) if task.tags else ""
            print(f"- [{task.state.upper()}] {task.title} ({due}) {tags_str}")
        return 0

    def tasks_p0(args):
        parser = argparse.ArgumentParser(prog="tasks-p0")
        parser.add_argument("--year", type=int, help="Year to filter tasks")
        parser.add_argument("--month", type=int, help="Month to filter tasks")
        parser.add_argument("--state", help="Filter by task state (e.g., open, done)")
        opts = _parse_args(parser, args)

        all_tasks = api.tasks.list(year=opts.year, month=opts.month, state=opts.state)
        tasks = [task for task in all_tasks if "p0" in task.tags]

        if not tasks:
            print("No P0 tasks found.")
            return 0

        print(f"P0 tasks ({len(tasks)}):")
        for task in tasks:
            due = task.due_date.isoformat() if task.due_date else "no-date"
            state_str = f"[{task.state.upper()}]" if task.state != "open" else ""
            print(f"- {state_str} {task.title} ({due})".strip())
        return 0

    def tasks_p1(args):
        parser = argparse.ArgumentParser(prog="tasks-p1")
        parser.add_argument("--year", type=int, help="Year to filter tasks")
        parser.add_argument("--month", type=int, help="Month to filter tasks")
        parser.add_argument("--state", help="Filter by task state (e.g., open, done)")
        opts = _parse_args(parser, args)

        all_tasks = api.tasks.list(year=opts.year, month=opts.month, state=opts.state)
        tasks = [task for task in all_tasks if "p1" in task.tags]

        if not tasks:
            print("No P1 tasks found.")
            return 0

        print(f"P1 tasks ({len(tasks)}):")
        for task in tasks:
            due = task.due_date.isoformat() if task.due_date else "no-date"
            state_str = f"[{task.state.upper()}]" if task.state != "open" else ""
            print(f"- {state_str} {task.title} ({due})".strip())
        return 0

    def tasks_priority(args):
        parser = argparse.ArgumentParser(prog="tasks-priority")
        parser.add_argument("--year", type=int, help="Year to filter tasks")
        parser.add_argument("--month", type=int, help="Month to filter tasks")
        parser.add_argument("--state", help="Filter by task state (e.g., open, done)")
        opts = _parse_args(parser, args)

        all_tasks = api.tasks.list(year=opts.year, month=opts.month, state=opts.state)
        tasks = [task for task in all_tasks if "p0" in task.tags or "p1" in task.tags]

        if not tasks:
            print("No P0/P1 tasks found.")
            return 0

        print(f"P0/P1 priority tasks ({len(tasks)}):")
        for task in tasks:
            due = task.due_date.isoformat() if task.due_date else "no-date"
            priority = "P0" if "p0" in task.tags else "P1"
            state_str = f"[{task.state.upper()}]" if task.state != "open" else ""
            print(f"- [{priority}] {state_str} {task.title} ({due})".strip())
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
    registry.add_command("tasks-open", tasks_open)
    registry.add_command("tasks-done", tasks_done)
    registry.add_command("tasks-canceled", tasks_canceled)
    registry.add_command("tasks-non-open", tasks_non_open)
    registry.add_command("tasks-p0", tasks_p0)
    registry.add_command("tasks-p1", tasks_p1)
    registry.add_command("tasks-priority", tasks_priority)
    registry.add_command("healthcheck", healthcheck)
