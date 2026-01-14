"""Parsing helpers for orgplan markdown files."""

import re

from orgplan.tasks import Task


_TODO_HEADER_PATTERN = re.compile(r"^#\s*TODO List\s*$")
_HEADER_PATTERN = re.compile(r"^#\s+(.+)$")

_STATUS_MAP = {
    "DONE": "done",
    "CANCELED": "canceled",
    "DELEGATED": "delegated",
    "PENDING": "pending",
}

_TAG_SET = {
    "p0",
    "p1",
    "p2",
    "1h",
    "2h",
    "4h",
    "1d",
    "blocked",
    "weekly",
    "monthly",
}


def parse_todo_list(text):
    """Parse tasks from the TODO list section of a monthly notes file."""
    lines = text.splitlines()
    in_todo = False
    tasks = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if _TODO_HEADER_PATTERN.match(stripped):
            in_todo = True
            continue

        if in_todo and stripped.startswith("#"):
            break

        if not in_todo:
            continue

        if not stripped.startswith("-"):
            continue

        task = _parse_task_line(stripped, line_number=i)
        if task is not None:
            tasks.append(task)

    return tasks


def parse_month_notes(text):
    """Parse tasks from the TODO list and attach matching notes sections."""
    tasks = parse_todo_list(text)
    task_map = {task.title: task for task in tasks}
    if not task_map:
        return tasks

    lines = text.splitlines()
    current_title = None
    current_lines = []

    def flush():
        if current_title is None:
            return
        task = task_map.get(current_title)
        if task is not None:
            notes = "\n".join(current_lines)
            lines = notes.splitlines()
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
            task.notes = "\n".join(lines)

    for line in lines:
        stripped = line.strip()
        header_match = _HEADER_PATTERN.match(stripped)
        if header_match:
            flush()
            title = _normalize_header_title(header_match.group(1))
            if _TODO_HEADER_PATTERN.match(stripped):
                current_title = None
                current_lines = []
            else:
                current_title = title
                current_lines = []
            continue

        if current_title is not None:
            current_lines.append(line)

    flush()
    return tasks


def _parse_task_line(line, line_number=None):
    content = line.lstrip("- ").strip()
    if not content:
        return None

    state, tags, title = parse_title_parts(content)
    if not title:
        return None

    return Task(title=title, state=state, tags=tags, line_number=line_number)


def parse_title_parts(content):
    state = "open"
    match = re.match(r"^\[(?P<status>[A-Z]+)\]\s+(?P<body>.+)$", content)
    if match and match.group("status") in _STATUS_MAP:
        state = _STATUS_MAP[match.group("status")]
        content = match.group("body")

    words = content.split()
    tags = []
    title_words = []
    for word in words:
        if word.startswith("#"):
            tag = word[1:]
            if tag in _TAG_SET:
                tags.append(tag)
                continue
        title_words.append(word)

    title = " ".join(title_words).strip()
    return state, tags, title


def _normalize_header_title(raw_title):
    content = raw_title.strip()
    if not content:
        return ""
    _, _, title = parse_title_parts(content)
    return title
