import unittest

from orgplan.markup import parse_month_notes, parse_todo_list


class MarkupTests(unittest.TestCase):
    def test_parses_todo_list_canonical_header(self):
        text = """# TODO List\n- [DONE] #p1 #4h Learn LLMs\n# Next\n"""
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Learn LLMs")
        self.assertEqual(tasks[0].state, "done")
        self.assertEqual(tasks[0].tags, ["p1", "4h"])

    def test_parses_todo_list_no_space_header(self):
        text = """#TODO List\n- #blocked #monthly Fix backlog\n"""
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Fix backlog")
        self.assertEqual(tasks[0].tags, ["blocked", "monthly"])

    def test_ignores_unknown_status(self):
        text = """# TODO List\n- [SOMEDAY] #p2 Someday task\n"""
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "[SOMEDAY] Someday task")
        self.assertEqual(tasks[0].state, "open")

    def test_parses_task_notes(self):
        text = """# TODO List\n- Ship it\n\n# Ship it\nNotes line 1\nNotes line 2\n\n# Other\nExtra notes\n"""
        tasks = parse_month_notes(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].notes, "Notes line 1\nNotes line 2")

    def test_notes_header_ignores_tags_and_status(self):
        text = """# TODO List\n- [DONE] #p1 Ship it\n\n# [DONE] #p1 Ship it\nNotes line 1\n"""
        tasks = parse_month_notes(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Ship it")
        self.assertEqual(tasks[0].notes, "Notes line 1")

    def test_notes_header_trims_whitespace(self):
        text = """# TODO List\n- Ship it\n\n#   Ship it   \nNotes line 1\n"""
        tasks = parse_month_notes(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].notes, "Notes line 1")

    def test_notes_trim_blank_lines(self):
        text = """# TODO List\n- Ship it\n\n# Ship it\n\nNotes line 1\n\n\n"""
        tasks = parse_month_notes(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].notes, "Notes line 1")


if __name__ == "__main__":
    unittest.main()
