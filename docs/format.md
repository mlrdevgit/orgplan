# File format

## Layout
Monthly notes live at `YYYY/MM-notes.md`. Monthly metadata lives at `YYYY/MM-meta.md`.

## TODO list section
The TODO list section begins with the canonical header:

```
# TODO List
```

The parser also accepts the historical variant without the space:

```
#TODO List
```

Tasks are list items under this header. Parsing stops at the next header line
that begins with `#`.

## Task list item format
A task list item is a single markdown list entry. Example:

```
- [DONE] #p1 #4h Learn how to refine an LLM
```

Supported status blocks (prefix, optional). These are present in the file but
are not part of the `Task.title` value in the object model:
- `[DONE]`
- `[CANCELED]`
- `[DELEGATED]`
- `[PENDING]`

Supported tags (order independent, optional). These are present in the file but
are not part of the `Task.title` value in the object model:
- Priority: `#p0`, `#p1`, `#p2`
- Estimates: `#1h`, `#2h`, `#4h`, `#1d`
- State: `#blocked`
- Recurrence: `#weekly`, `#monthly`

Any remaining text after removing the status block and tags is the task title.
Leading and trailing whitespace is trimmed for `Task.title`.

## Task notes
After the TODO list section, each task may include a top-level header that
matches the task title. Matching trims leading/trailing whitespace and ignores
status blocks and tags in the header text. The body under that header is
captured as `Task.notes` verbatim (excluding the header line).

## Timestamps

Tasks support three types of timestamps, which can appear in either the task
line or the notes section.

### Timestamp formats

Basic formats (day name is optional):
- `<YYYY-MM-DD>` - Date only, e.g., `<2025-06-15>`
- `<YYYY-MM-DD Day>` - Date with day name, e.g., `<2025-06-15 Mon>`
- `<YYYY-MM-DD Day HH:MM>` - Date and time, e.g., `<2025-06-15 Mon 14:30>`

The day name can be abbreviated (Mon, Tue) or full (Monday, Tuesday).

### Timestamp types

1. **DEADLINE:** - Task deadline, stored in `Task.deadline` list
2. **SCHEDULED:** - Scheduled start/work time, stored in `Task.scheduled` list
3. Plain timestamps - Stored in `Task.timestamp` list

### Examples

```
# TODO List
- Ship feature DEADLINE: <2025-06-30>
- Meeting <2025-06-15 Mon 14:30>
- Project DEADLINE: <2025-07-01> SCHEDULED: <2025-06-15>
```

Timestamps can also appear in notes:

```
# Ship feature
DEADLINE: <2025-06-30>
Some notes here.
SCHEDULED: <2025-06-20>
```

### Parsing rules

- Multiple timestamps of each type are allowed per task
- Timestamps in the task line take precedence over timestamps in notes
- If any timestamp appears in the task line, notes timestamps are ignored
- `Task.due_date` returns the first deadline, or first scheduled if no deadline

### Object model

Timestamps are stored as `datetime.date` or `datetime.datetime` objects:

- `Task.deadline` - List of deadlines (date or datetime)
- `Task.scheduled` - List of scheduled times (date or datetime)
- `Task.timestamp` - List of plain timestamps (date or datetime)
- `Task.due_date` - Property returning first deadline or first scheduled
