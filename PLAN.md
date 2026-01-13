# Implementation Plan

## Immediate tasks (phase 0)
1) Define the public configuration contract.
   - Decide on a JSON config format (`orgplan.config.json`).
   - Include `data_root`, `plugins`, and `plugin_opts`.
   - Add a loader module that accepts `ORGPLAN_CONFIG`.

2) Establish the core API surface.
   - Create `OrgplanAPI` with `tasks`, `notes`, and `dates` services.
   - Add `api_version` and a minimal compatibility check.

3) Create the plugin system (commands only).
   - Implement plugin discovery via explicit paths from config.
   - Require a `register(registry)` entrypoint in each plugin.
   - Define `Registry.add_command(name, func)`.

4) Build a small CLI entrypoint.
   - Command dispatcher wired to the registry.
   - `orgplan help` lists available commands.

5) Implement task querying primitives.
   - Basic `TaskStore.list(year=..., month=..., state=...)`.
   - `DateService.current_month()` and parsing helpers.

6) Testing from day one.
   - Create `tests/` with `unittest`.
   - Add tests for config loading, plugin registration, and task querying.
   - Ensure tests run headless and non-interactive.

7) Add a reference plugin.
   - Small example plugin in `examples/` or `plugins/`.
   - Shows how to register a command and call core APIs.

8) CI setup (optional but recommended).
   - Add GitHub Actions for Windows + Linux running `unittest`.

## Near-term (phase 1)
- Define a stable data model for tasks (fields, states, metadata).
- Add import/export helpers for task files.
- Improve error messages around plugin loading.
- Document plugin contract in `docs/plugins.md`.

## Later (phase 2)
- Plugin hooks (if needed), not just commands.
- Integrations (e.g., Microsoft To Do, Google Tasks) as separate repos.
- Add migrations / schema versioning if the data model changes.
