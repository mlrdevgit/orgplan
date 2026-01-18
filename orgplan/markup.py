"""Parsing helpers for orgplan markdown files."""

import datetime
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

# Timestamp pattern: <YYYY-MM-DD> or <YYYY-MM-DD Day> or <YYYY-MM-DD Day HH:MM>
_TIMESTAMP_PATTERN = re.compile(
    r"<(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    r"(?:\s+\w+)?"  # Optional day name (Mon, Tue, Wednesday, etc)
    r"(?:\s+(?P<hour>\d{2}):(?P<minute>\d{2}))?"  # Optional time HH:MM
    r">"
)


def _extract_datetime(match):
    """Extract datetime.date or datetime.datetime from a regex match."""
    try:
        year = int(match.group("year"))
        month = int(match.group("month"))
        day = int(match.group("day"))
        hour = match.group("hour")
        minute = match.group("minute")

        if hour and minute:
            return datetime.datetime(year, month, day, int(hour), int(minute))
        else:
            return datetime.date(year, month, day)
    except (ValueError, AttributeError):
        return None


def _parse_timestamps(text):
    """Parse timestamps from text, returning (deadlines, scheduled, timestamps).

    Returns:
        tuple: (list[datetime], list[datetime], list[datetime])
    """
    deadlines = []
    scheduled_list = []
    plain_timestamps = []

    # Track which character positions contain prefixed timestamps
    prefixed_timestamp_starts = set()

    # Parse DEADLINE: timestamps - track where the <timestamp> portion starts
    for match in re.finditer(r"DEADLINE:\s*(<\d{4}-\d{2}-\d{2}[^>]*>)", text):
        # Find the actual timestamp within this match
        ts_match = _TIMESTAMP_PATTERN.search(match.group(0))
        if ts_match:
            dt = _extract_datetime(ts_match)
            if dt:
                deadlines.append(dt)
                # Record the absolute position of the timestamp
                prefixed_timestamp_starts.add(match.start() + ts_match.start())

    # Parse SCHEDULED: timestamps
    for match in re.finditer(r"SCHEDULED:\s*(<\d{4}-\d{2}-\d{2}[^>]*>)", text):
        ts_match = _TIMESTAMP_PATTERN.search(match.group(0))
        if ts_match:
            dt = _extract_datetime(ts_match)
            if dt:
                scheduled_list.append(dt)
                prefixed_timestamp_starts.add(match.start() + ts_match.start())

    # Parse plain timestamps (exclude those already found as prefixed)
    for match in _TIMESTAMP_PATTERN.finditer(text):
        if match.start() in prefixed_timestamp_starts:
            continue

        dt = _extract_datetime(match)
        if dt:
            plain_timestamps.append(dt)

    return deadlines, scheduled_list, plain_timestamps


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
            notes_lines = notes.splitlines()
            while notes_lines and not notes_lines[0].strip():
                notes_lines.pop(0)
            while notes_lines and not notes_lines[-1].strip():
                notes_lines.pop()
            task.notes = "\n".join(notes_lines)

            # Extract timestamps from notes (only if not already set from task line)
            if task.notes and not (task.deadline or task.scheduled or task.timestamp):
                deadlines, scheduled_list, timestamps = _parse_timestamps(task.notes)
                task.deadline = deadlines
                task.scheduled = scheduled_list
                task.timestamp = timestamps

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

    # Extract timestamps from the task line
    deadlines, scheduled_list, timestamps = _parse_timestamps(content)

    return Task(
        title=title,
        state=state,
        tags=tags,
        line_number=line_number,
        deadline=deadlines,
        scheduled=scheduled_list,
        timestamp=timestamps,
    )


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
