# Plugins

Plugins are loaded explicitly from paths listed in your config. Each plugin must
provide an `orgplan_plugin.py` module with a `register(registry)` function.

## Plugin contract

- Module name: `orgplan_plugin`
- Entry point: `register(registry)`
- Register commands with `registry.add_command(name, func)`
- Command functions receive `args` (list of strings) and return an exit code

## Accessing core APIs

Plugins receive a registry with `registry.api`:

- `registry.api.tasks` for task queries
- `registry.api.dates` for date helpers
- `registry.config` for config data (including `data_root`)

Example skeleton:

```python
# orgplan_plugin.py

def register(registry):
    api = registry.api

    def hello(args):
        year, month = api.dates.current_year_month()
        tasks = api.tasks.list(year=year, month=month, state="open")
        print(f"{len(tasks)} open tasks for {year:04d}-{month:02d}")
        return 0

    registry.add_command("hello", hello)
```

## Reference plugin

A working reference plugin lives at `examples/reference_plugin/orgplan_plugin.py`.
It provides the following commands:

### General Commands
- `healthcheck` - Verifies `data_root` if set
- `tasks-month` - Lists tasks for current year+month (optional `--state`)
- `tasks-count` - Counts tasks by state (optional `--year`/`--month`)

### State Filter Commands
- `tasks-open` - Lists open tasks (optional `--year`/`--month`)
- `tasks-done` - Lists done tasks (optional `--year`/`--month`)
- `tasks-canceled` - Lists canceled tasks (optional `--year`/`--month`)
- `tasks-non-open` - Lists all non-open tasks (done, canceled, delegated, pending) with state labels (optional `--year`/`--month`)

### Priority Filter Commands
- `tasks-p0` - Lists P0 priority tasks (optional `--year`/`--month`/`--state`)
- `tasks-p1` - Lists P1 priority tasks (optional `--year`/`--month`/`--state`)
- `tasks-priority` - Lists all P0/P1 priority tasks with priority labels (optional `--year`/`--month`/`--state`)

All filter commands display task titles, due dates, and relevant tags. When year/month are not specified, defaults to the current year and month.
