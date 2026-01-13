"""CLI entrypoint for orgplan."""

import argparse
import sys

from orgplan.api import OrgplanAPI
from orgplan.config import load_config
from orgplan.dates import DateService
from orgplan.plugins import load_plugins
from orgplan.registry import Registry
from orgplan.tasks import FileTaskStore


def _build_registry(config):
    task_store = FileTaskStore(data_root=config.data_root, date_service=DateService())
    api = OrgplanAPI(task_store=task_store, date_service=DateService())
    registry = Registry(api, config=config)
    load_plugins(config, registry)
    return registry


def main(argv=None):
    parser = argparse.ArgumentParser(prog="orgplan")
    parser.add_argument("--config", help="Path to orgplan config JSON")
    parser.add_argument("command", nargs="?", default="help")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    config = load_config(args.config)
    registry = _build_registry(config)

    if args.command == "help":
        commands = registry.list_commands()
        if commands:
            print("Available commands:")
            for name in commands:
                print(f"  {name}")
        else:
            print("No commands registered.")
        return 0

    command = registry.get_command(args.command)
    if command is None:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 2

    return command(args.args)


if __name__ == "__main__":
    raise SystemExit(main())
