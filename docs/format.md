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
