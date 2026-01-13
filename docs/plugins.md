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
It provides:

- `tasks-month` (current year+month, optional `--state`)
- `tasks-count` (counts by state, optional `--year`/`--month`)
- `healthcheck` (verifies `data_root` if set)
