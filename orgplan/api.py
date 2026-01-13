"""Public API surface for plugins and CLI."""

API_VERSION = "1.0"


class OrgplanAPI:
    def __init__(self, task_store, note_store=None, date_service=None):
        self.tasks = task_store
        self.notes = note_store
        self.dates = date_service
        self.api_version = API_VERSION
