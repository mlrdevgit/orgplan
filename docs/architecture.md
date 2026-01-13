# Architecture

## Overview
The core library is deliberately small. It wires configuration, storage, and
plugins so commands can operate on tasks and notes without knowing file layouts.

## Data flow
1) `orgplan.config.load_config` loads config JSON.
2) `orgplan.cli` builds a `FileTaskStore` from `data_root`.
3) `OrgplanAPI` exposes `tasks` and `dates` services.
4) `Registry` holds commands and the API instance.
5) `orgplan.plugins.load_plugins` imports each `orgplan_plugin` and calls
   `register(registry)`.
6) The CLI dispatches a command by name.

## Core components
- `orgplan.api.OrgplanAPI`: Public API surface for plugins.
- `orgplan.tasks.FileTaskStore`: Reads tasks from `YYYY/MM-notes.md` files.
- `orgplan.markup.parse_todo_list`: Parses the TODO list section.
- `orgplan.registry.Registry`: Command registry and API access.
- `orgplan.plugins.load_plugins`: Explicit plugin loader.
- `orgplan.cli`: CLI entrypoint and command dispatcher.
