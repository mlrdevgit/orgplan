"""Command registry for plugins and CLI."""


class Registry:
    def __init__(self, api, config=None):
        self.api = api
        self.config = config
        self._commands = {}

    def add_command(self, name, func):
        if not callable(func):
            raise ValueError("Command must be callable")
        if name in self._commands:
            raise ValueError(f"Command already registered: {name}")
        self._commands[name] = func

    def get_command(self, name):
        return self._commands.get(name)

    def list_commands(self):
        return sorted(self._commands.keys())
