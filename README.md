# orgplan
Plaintext productivity with a small, explicit core API and command-oriented plugins.

## High-level goals
- Keep the core tooling public while allowing private data to live elsewhere.
- Provide a stable Python API for querying tasks/notes without exposing storage details.
- Support explicit, opt-in plugins that register commands.
- Be Windows-friendly (no symlinks required).
- Build in automated tests from day one with `unittest`.

## Non-goals (initial)
- No automated syncing with external services in the core repo.
- No requirement to colocate data with scripts or plugins.
- No write/update support for task files (read-only for now).

## Scope (initial)
- Python-only core library and CLI.
- Plugin loader that enables explicit plugin paths from config.
- Task querying primitives (year + month + state) exposed via core API.

## Plugins
Plugins live in separate repos or folders and expose an `orgplan_plugin.py` module
with a `register(registry)` function. See `docs/plugins.md` and the reference
plugin at `examples/reference_plugin/orgplan_plugin.py`.

## Setup
1) Create a private data directory (example: `C:\Users\you\orgplan-data`).
2) Create `orgplan.config.json` that points to your data directory and plugins.
3) Set `ORGPLAN_CONFIG` to the path of that config file.
4) Ensure your monthly files live under `YYYY/MM-notes.md`.

Example config:

```json
{
  "data_root": "C:\\Users\\you\\orgplan-data",
  "plugins": [
    "C:\\Users\\you\\repos\\orgplan\\examples\\reference_plugin"
  ],
  "plugin_opts": {}
}
```

Run the CLI:

```bash
python3 -m orgplan --config C:\Users\you\orgplan.config.json help
```

## Quickstart
1) Create `YYYY/MM-notes.md` under your `data_root`:

```
# TODO List
- [DONE] #p1 Ship the first cut
- #blocked #weekly Follow up on dependencies
```

2) Run a reference command:

```bash
python3 -m orgplan --config C:\Users\you\orgplan.config.json tasks-month
```

## Available Commands (Reference Plugin)

The reference plugin provides several commands for querying and filtering tasks. All commands support `--year` and `--month` parameters (defaults to current month if not specified).

### General Commands

**List tasks for current month:**
```bash
python3 -m orgplan tasks-month
python3 -m orgplan tasks-month --state done  # Filter by state
```

**Count tasks by state:**
```bash
python3 -m orgplan tasks-count
python3 -m orgplan tasks-count --year 2025 --month 1
```

**Check plugin health:**
```bash
python3 -m orgplan healthcheck
```

### Filter by Task State

**List open tasks:**
```bash
python3 -m orgplan tasks-open
python3 -m orgplan tasks-open --year 2025 --month 1
```

**List done tasks:**
```bash
python3 -m orgplan tasks-done
```

**List canceled tasks:**
```bash
python3 -m orgplan tasks-canceled
```

**List all non-open tasks (done, canceled, delegated, pending):**
```bash
python3 -m orgplan tasks-non-open
```
Shows state labels like `[DONE]`, `[CANCELED]`, etc.

### Filter by Priority

**List P0 priority tasks:**
```bash
python3 -m orgplan tasks-p0
python3 -m orgplan tasks-p0 --state open  # Only open P0 tasks
```

**List P1 priority tasks:**
```bash
python3 -m orgplan tasks-p1
```

**List all P0/P1 priority tasks:**
```bash
python3 -m orgplan tasks-priority
python3 -m orgplan tasks-priority --state open  # Only open priority tasks
```
Shows priority labels like `[P0]`, `[P1]`.

All filter commands display task titles, due dates, and relevant tags.

## File format
Monthly notes live at `YYYY/MM-notes.md` and begin with `# TODO List`.
The parser also accepts the historical `#TODO List` variant. See `docs/format.md`
for the full combined tag set and parsing rules.

## Documentation
- `docs/architecture.md`
- `docs/config.md`
- `docs/format.md`
- `docs/plugins.md`

## Development
Run tests with:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

For local development, use `python3 -m orgplan` (no install needed). If you
prefer an editable install, `pip install -e .` also works.
To uninstall, run `pip uninstall orgplan`.

## Troubleshooting
- `ORGPLAN_CONFIG` missing: set `ORGPLAN_CONFIG` or pass `--config` to the CLI.
- `data_root does not exist`: create the directory or update the config path.
- Avoid machine-wide installs: use `python3 -m venv .venv` and
  `.venv/bin/pip install -e .` (Windows: `.venv\\Scripts\\pip install -e .`).
