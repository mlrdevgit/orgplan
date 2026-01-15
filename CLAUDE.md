# CLAUDE.md - AI Assistant Guide for orgplan

This document provides comprehensive guidance for AI assistants working with the orgplan codebase. It covers architecture, conventions, workflows, and best practices.

## Project Overview

**orgplan** is a plaintext productivity management system written in Python that:
- Manages tasks and notes in markdown files (`YYYY/MM-notes.md`)
- Provides a stable Python API for querying tasks
- Supports explicit, opt-in command plugins
- Maintains separation between core tooling (public) and data (private)
- Is Windows-friendly (no symlinks required)
- Built with testing from day one using `unittest`

**Key Stats:**
- Language: Python 3.9+
- Core codebase: ~445 lines (excluding tests)
- Test coverage: 6 comprehensive test files
- CI/CD: GitHub Actions (Ubuntu + Windows, Python 3.11-3.12)
- Dependencies: Pure stdlib (no external packages)

## Project Structure

```
orgplan/
├── orgplan/                    # Main Python package
│   ├── __init__.py            # Public API exports
│   ├── __main__.py            # Entry point (python -m orgplan)
│   ├── api.py                 # OrgplanAPI (public surface)
│   ├── cli.py                 # CLI dispatcher and registry builder
│   ├── config.py              # JSON config loader
│   ├── dates.py               # DateService utilities
│   ├── markup.py              # Markdown parser (TODO list + notes)
│   ├── plugins.py             # Plugin discovery and loader
│   ├── registry.py            # Command registry
│   └── tasks.py               # Task model and stores
├── tests/                      # Test suite (unittest)
│   ├── test_config.py
│   ├── test_file_task_store.py
│   ├── test_markup.py
│   ├── test_plugins.py
│   ├── test_reference_plugin.py
│   └── test_tasks.py
├── examples/
│   └── reference_plugin/      # Working plugin example
│       └── orgplan_plugin.py
├── docs/                       # Documentation
│   ├── architecture.md        # System architecture overview
│   ├── config.md              # Configuration format
│   ├── format.md              # File format specification
│   └── plugins.md             # Plugin development guide
├── .github/workflows/
│   └── ci.yml                 # CI pipeline
├── pyproject.toml             # Build configuration
├── README.md                  # User documentation
└── PLAN.md                    # Implementation roadmap
```

## Core Architecture

### Data Flow

```
1. Load Config (JSON) → data_root, plugins, plugin_opts
2. Build FileTaskStore → reads from data_root/YYYY/MM-notes.md
3. Create OrgplanAPI → wraps task_store + date_service
4. Create Registry → holds API + config
5. Load Plugins → imports orgplan_plugin.py, calls register(registry)
6. Dispatch Command → CLI looks up by name, executes with args
```

### Key Components

| Component | File | Purpose |
|-----------|------|---------|
| `OrgplanAPI` | api.py | Public API surface for plugins (versioned) |
| `FileTaskStore` | tasks.py | Reads tasks from `YYYY/MM-notes.md` |
| `InMemoryTaskStore` | tasks.py | In-memory store for testing |
| `Task` | tasks.py | Task data model |
| `parse_todo_list()` | markup.py | Parses TODO section |
| `parse_month_notes()` | markup.py | Parses TODO + attaches notes |
| `Registry` | registry.py | Command registry + API access |
| `load_plugins()` | plugins.py | Plugin discovery and loading |
| `main()` | cli.py | CLI entrypoint and dispatcher |
| `DateService` | dates.py | Date utilities |
| `load_config()` | config.py | Config loading and validation |

### Task Model

```python
class Task:
    title: str           # Task text (after removing status/tags)
    state: str           # "open" | "done" | "canceled" | "delegated" | "pending"
    due_date: date       # Optional datetime.date
    tags: list[str]      # Tags: p0, p1, p2, 1h, 2h, 4h, 1d, blocked, weekly, monthly
    notes: str           # Optional: from matching header section
    line_number: int     # Optional: for reference/debugging
```

### File Format

**Location:** `data_root/YYYY/MM-notes.md`

**TODO List Section:**
```markdown
# TODO List
- [DONE] #p1 #4h Task title here
- #p2 #blocked Another task
- Task without status or tags
```

**Notes Section:**
```markdown
# Task title here
Additional notes for the task.
Can span multiple lines.
```

**Status Codes:**
- `[DONE]` → state="done"
- `[CANCELED]` → state="canceled"
- `[DELEGATED]` → state="delegated"
- `[PENDING]` → state="pending"
- (no status) → state="open"

**Recognized Tags:**
- Priority: `#p0`, `#p1`, `#p2`
- Estimates: `#1h`, `#2h`, `#4h`, `#1d`
- State: `#blocked`
- Recurrence: `#weekly`, `#monthly`

## Code Conventions & Patterns

### Design Patterns

1. **Dependency Injection**
   - `FileTaskStore` accepts `DateService` and parser for testability
   - Services are passed as constructor arguments

2. **Strategy Pattern**
   - Multiple task store implementations (`InMemoryTaskStore`, `FileTaskStore`)
   - Swappable parsers in `FileTaskStore`

3. **Facade Pattern**
   - `OrgplanAPI` wraps multiple services (tasks, dates)
   - Plugins interact with API, not internals

4. **Registry Pattern**
   - `Registry` manages command lookup
   - Prevents duplicate registration

5. **Module-Based Plugins**
   - Explicit paths (no auto-discovery)
   - Standard module name (`orgplan_plugin.py`)
   - Standard entry point (`register(registry)`)

### Naming Conventions

- **Private functions/methods:** `_prefixed` (e.g., `_parse_task_line`, `_normalize_path`)
- **Test classes:** `*Tests` suffix (e.g., `ConfigTests`)
- **Test methods:** `test_*` prefix (e.g., `test_parse_todo_list`)
- **Module imports:** Prefer explicit imports over `from module import *`

### Code Style

- **Line length:** No strict limit, but be reasonable
- **Docstrings:** Triple-quoted strings for module/function docs
- **Type hints:** Not currently used (Python 3.9+ compatible)
- **Error handling:** Raise specific exceptions with clear messages
- **Path handling:** Use `os.path.join()` for cross-platform compatibility
- **File encoding:** Always use `encoding="utf-8"` for file operations

### Key Principles

1. **Explicit over implicit** - Plugin paths in config, no auto-discovery
2. **Read-only by design** - Currently only reads tasks (no write/update)
3. **Windows-friendly** - No symlinks, uses `os.path` properly
4. **Pure stdlib** - No external dependencies
5. **Testable** - Dependency injection, fixtures, output capture
6. **Stateless core** - Registry and API are immutable once built

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository (already done in your case)
cd /home/user/orgplan

# No installation needed for development
# Run directly: python3 -m orgplan

# Or install in editable mode
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
# Run all tests
python3 -m unittest discover -s tests -p "test_*.py"

# Run specific test file
python3 -m unittest tests.test_tasks

# Run specific test case
python3 -m unittest tests.test_tasks.TaskTests.test_task_filtering
```

**IMPORTANT:** Always run tests before committing changes!

### Running the CLI

```bash
# Using module invocation (no install needed)
python3 -m orgplan --config /path/to/orgplan.config.json help

# If installed
orgplan --config /path/to/orgplan.config.json help

# With ORGPLAN_CONFIG env var
export ORGPLAN_CONFIG=/path/to/orgplan.config.json
python3 -m orgplan help
```

### Configuration for Development

Create a test config file:

```json
{
  "data_root": "/home/user/orgplan-test-data",
  "plugins": [
    "/home/user/orgplan/examples/reference_plugin"
  ],
  "plugin_opts": {}
}
```

Create test data structure:
```bash
mkdir -p /home/user/orgplan-test-data/2025
echo "# TODO List
- #p1 Test task one
- [DONE] #p2 Test task two" > /home/user/orgplan-test-data/2025/01-notes.md
```

## Plugin Development

### Plugin Contract

**File:** `orgplan_plugin.py` (exact name required)

**Entry Point:** `register(registry)` function

### Basic Plugin Template

```python
"""My custom orgplan plugin."""

import argparse

def register(registry):
    """Register commands with the orgplan registry."""
    api = registry.api
    config = registry.config

    def my_command(args):
        """
        Command function.

        Args:
            args: list[str] - Command-line arguments

        Returns:
            int - Exit code (0 = success)
        """
        parser = argparse.ArgumentParser(prog="my-command")
        parser.add_argument("--option", help="Example option")
        opts = parser.parse_args(args)

        # Access API
        year, month = api.dates.current_year_month()
        tasks = api.tasks.list(year=year, month=month, state="open")

        # Process and output
        print(f"Found {len(tasks)} open tasks for {year:04d}-{month:02d}")
        for task in tasks:
            print(f"  - {task.title}")

        return 0

    # Register command
    registry.add_command("my-command", my_command)
```

### Accessing Core APIs

**Available through `registry.api`:**

- `api.tasks.list(year=None, month=None, state=None)` - Query tasks
- `api.dates.current_year_month(today=None)` - Get current (year, month)
- `api.dates.parse_year_month(value)` - Parse "YYYY-MM" string
- `api.api_version` - API version string (currently "1.0")

**Available through `registry.config`:**

- `config.data_root` - Path to data directory
- `config.plugins` - List of plugin paths
- `config.plugin_opts` - Plugin-specific configuration dict

### Plugin Best Practices

1. **Use argparse** for command-line argument parsing
2. **Return exit codes** (0 = success, non-zero = error)
3. **Print to stdout** for normal output, stderr for errors
4. **Handle missing data** gracefully (empty task lists, missing files)
5. **Add docstrings** to command functions
6. **Test your plugin** with various edge cases

### Example: Accessing Plugin-Specific Config

```python
def register(registry):
    config = registry.config
    plugin_config = config.plugin_opts.get("my-plugin", {})
    api_key = plugin_config.get("api_key")

    def sync_command(args):
        if not api_key:
            print("Error: api_key not configured", file=sys.stderr)
            return 1
        # Use api_key...
        return 0

    registry.add_command("sync", sync_command)
```

## Testing Requirements

### Test Structure

All tests use Python's `unittest` framework. Key patterns:

1. **Temporary directories** for file I/O tests
2. **Fixture services** (e.g., `FixedDateService`) for deterministic tests
3. **StringIO capture** for command output verification
4. **Import reloading** for plugin testing

### Writing Tests

**Example test case:**

```python
import unittest
import tempfile
import os
from orgplan.tasks import FileTaskStore, Task
from orgplan.dates import DateService

class MyTests(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_something(self):
        """Test description."""
        # Arrange
        store = FileTaskStore(self.temp_dir, DateService())

        # Act
        result = store.list(year=2025, month=1)

        # Assert
        self.assertEqual(len(result), 0)
```

### Test Coverage Expectations

When modifying code:
- **Add tests** for new functionality
- **Update tests** for changed behavior
- **Ensure tests pass** before committing
- **Test edge cases** (empty inputs, missing files, invalid data)

### Common Test Utilities

```python
# Fixed date service for deterministic tests
class FixedDateService:
    def __init__(self, year, month):
        self._year = year
        self._month = month

    def current_year_month(self, today=None):
        return self._year, self._month

# Capture stdout/stderr
from io import StringIO
import sys

output = StringIO()
sys.stdout = output
# ... run code ...
sys.stdout = sys.__stdout__
result = output.getvalue()
```

## Git Workflow

### Branch Strategy

- Work on feature branches with prefix `claude/` and session ID suffix
- Current branch: `claude/add-claude-documentation-LyQyS`
- Never push to main/master without explicit permission

### Making Commits

**Before committing:**
1. Run all tests: `python3 -m unittest discover -s tests -p "test_*.py"`
2. Check git status: `git status`
3. Review changes: `git diff`

**Commit message format:**
- First line: Short summary (50 chars) in imperative mood
- Body: Explain "why" not "what" (optional)
- Example: "Add support for line numbers in tasks"

**Commit workflow:**
```bash
# Stage changes
git add file1.py file2.py

# Commit with message
git commit -m "Your commit message here"

# Push to remote
git push -u origin claude/add-claude-documentation-LyQyS
```

### Important Git Rules

1. **Never** update git config
2. **Never** run destructive git commands without explicit user request
3. **Never** skip hooks (--no-verify, --no-gpg-sign)
4. **Never** force push to main/master
5. **Always** push to the designated feature branch

## Important Rules for AI Assistants

### DO

✅ **Read files before modifying** - Never propose changes to code you haven't read
✅ **Run tests after changes** - Always verify tests pass
✅ **Follow existing patterns** - Match the codebase style
✅ **Use descriptive commit messages** - Explain the "why"
✅ **Handle errors gracefully** - Provide clear error messages
✅ **Preserve cross-platform compatibility** - Use `os.path.join()`
✅ **Test edge cases** - Empty inputs, missing files, invalid data
✅ **Update tests when changing behavior** - Keep tests in sync
✅ **Use dependency injection** - Allow services to be passed in
✅ **Document new functions** - Add docstrings

### DON'T

❌ **Don't add external dependencies** - Keep it pure stdlib
❌ **Don't add write/update functionality** - System is read-only by design
❌ **Don't auto-discover plugins** - Must be explicit in config
❌ **Don't break Windows compatibility** - No symlinks, test paths carefully
❌ **Don't skip tests** - Always run before committing
❌ **Don't commit without testing** - Tests must pass
❌ **Don't use hardcoded paths** - Paths come from config
❌ **Don't expose storage details** - Plugins use API, not internals
❌ **Don't modify core API without version bump** - API stability is critical
❌ **Don't commit secrets** - No API keys, tokens, or credentials

## Common Tasks

### Adding a New Command to Reference Plugin

1. Read `examples/reference_plugin/orgplan_plugin.py`
2. Add command function to `register()`:
   ```python
   def new_command(args):
       parser = argparse.ArgumentParser(prog="new-command")
       # Add arguments
       opts = parser.parse_args(args)
       # Implement command
       return 0

   registry.add_command("new-command", new_command)
   ```
3. Test manually: `python3 -m orgplan new-command`
4. Add test in `tests/test_reference_plugin.py`
5. Run tests: `python3 -m unittest tests.test_reference_plugin`

### Modifying the Parser

1. Read `orgplan/markup.py`
2. Understand parsing logic in `parse_todo_list()` or `parse_month_notes()`
3. Make changes
4. Update tests in `tests/test_markup.py`
5. Run tests: `python3 -m unittest tests.test_markup`
6. Test with real data files

### Adding New Task Fields

1. Read `orgplan/tasks.py` to understand `Task` class
2. Add field to `Task.__init__()`
3. Update `Task.__repr__()`
4. Modify parser in `markup.py` to populate field
5. Update tests in `tests/test_tasks.py` and `tests/test_markup.py`
6. Run all tests
7. Document in `docs/format.md`

### Adding New Tag Types

1. Read `orgplan/markup.py`
2. Add tag to `_TAG_SET` (line 18)
3. Document in `docs/format.md`
4. Add test case in `tests/test_markup.py`
5. Run tests

### Debugging Plugin Issues

1. Check `ORGPLAN_CONFIG` environment variable
2. Verify plugin path in config JSON
3. Ensure `orgplan_plugin.py` exists at plugin path
4. Check `register()` function is defined
5. Add print statements to debug command execution
6. Check command registration: `python3 -m orgplan help`

## Key Files Reference

### Core Modules (orgplan/)

| File | Lines | Key Functions/Classes |
|------|-------|----------------------|
| `api.py` | 12 | `OrgplanAPI` |
| `cli.py` | 52 | `main()`, `_build_registry()` |
| `config.py` | 46 | `load_config()`, `Config` |
| `dates.py` | 21 | `DateService` |
| `markup.py` | 145 | `parse_todo_list()`, `parse_month_notes()` |
| `plugins.py` | 25 | `load_plugins()` |
| `registry.py` | 22 | `Registry` |
| `tasks.py` | 90 | `Task`, `FileTaskStore`, `InMemoryTaskStore` |

### Critical Code Sections

**Task parsing** (markup.py:32-57):
- Finds TODO header
- Extracts list items
- Parses status, tags, title

**Task notes attachment** (markup.py:60-102):
- Matches headers to task titles
- Captures notes content
- Trims blank lines

**File path construction** (tasks.py:65-66):
```python
def get_month_path(self, year, month):
    return os.path.join(self._data_root, f"{year:04d}", f"{month:02d}-notes.md")
```

**Command registration** (registry.py:15-19):
```python
def add_command(self, name, func):
    if name in self._commands:
        raise ValueError(f"Command {name!r} already registered")
    self._commands[name] = func
```

## Troubleshooting

### Common Issues

**"Config file not found"**
- Set `ORGPLAN_CONFIG` environment variable
- Or use `--config` flag: `python3 -m orgplan --config /path/to/config.json`

**"data_root does not exist"**
- Create directory: `mkdir -p /path/to/data_root`
- Or update config JSON with correct path

**"Unknown command"**
- Check command is registered: `python3 -m orgplan help`
- Verify plugin path in config
- Check `orgplan_plugin.py` exists and has `register()` function

**"Import error" when loading plugin**
- Verify Python path
- Check for syntax errors in `orgplan_plugin.py`
- Ensure all imports are available

**Tests failing**
- Check Python version (3.9+ required)
- Verify test data setup in `setUp()` methods
- Check for OS-specific path issues

**"No module named orgplan"**
- Run from repository root
- Or install: `pip install -e .`

### Debugging Tips

1. **Add print statements** to trace execution
2. **Use Python debugger** (`import pdb; pdb.set_trace()`)
3. **Check file paths** with `os.path.exists()`
4. **Inspect task objects** with `print(repr(task))`
5. **Test parser directly** in Python REPL:
   ```python
   from orgplan.markup import parse_month_notes
   with open("/path/to/01-notes.md") as f:
       tasks = parse_month_notes(f.read())
   print(tasks)
   ```

## API Version Compatibility

Current API version: **1.0**

Plugins can check compatibility:
```python
def register(registry):
    if registry.api.api_version != "1.0":
        raise RuntimeError(f"Unsupported API version: {registry.api.api_version}")
```

**API Stability Promise:**
- Breaking changes will require version bump
- Plugins depend on stable API, not internals
- Current API is read-only (tasks, dates)

## Future Considerations (from PLAN.md)

### Near-term (Phase 1)
- Define stable data model for tasks
- Add import/export helpers
- Improve error messages for plugin loading
- Enhanced plugin documentation

### Later (Phase 2)
- Plugin hooks (not just commands)
- Integrations with external services (separate repos)
- Schema versioning and migrations
- Write/update support (TBD)

**Important:** These are future plans, not current requirements. Focus on current read-only design.

## Resources

- **README.md** - User documentation and setup
- **docs/architecture.md** - System architecture overview
- **docs/config.md** - Configuration format details
- **docs/format.md** - File format specification
- **docs/plugins.md** - Plugin development guide
- **PLAN.md** - Implementation roadmap and future plans
- **examples/reference_plugin/** - Working plugin example

## Summary Checklist for AI Assistants

When working with orgplan:

- [ ] Read relevant files before making changes
- [ ] Maintain Python 3.9+ compatibility
- [ ] Preserve Windows compatibility (use `os.path`)
- [ ] Keep pure stdlib (no external dependencies)
- [ ] Follow existing code patterns and style
- [ ] Add/update tests for changes
- [ ] Run tests before committing
- [ ] Write clear commit messages
- [ ] Use dependency injection for testability
- [ ] Preserve API stability
- [ ] Document new features
- [ ] Handle edge cases gracefully
- [ ] Check both success and error paths

---

**Version:** 1.0 (January 2025)
**Last Updated:** 2026-01-15
**Maintained By:** orgplan project
