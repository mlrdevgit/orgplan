import datetime
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


class TimestampParsingTests(unittest.TestCase):
    def test_parses_deadline_from_task_line(self):
        text = "# TODO List\n- Ship it DEADLINE: <2025-06-15>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0].deadline), 1)
        self.assertEqual(tasks[0].deadline[0], datetime.date(2025, 6, 15))
        self.assertEqual(tasks[0].due_date, datetime.date(2025, 6, 15))

    def test_parses_scheduled_from_task_line(self):
        text = "# TODO List\n- Ship it SCHEDULED: <2025-06-15>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0].scheduled), 1)
        self.assertEqual(tasks[0].scheduled[0], datetime.date(2025, 6, 15))
        self.assertEqual(tasks[0].due_date, datetime.date(2025, 6, 15))

    def test_parses_plain_timestamp_from_task_line(self):
        text = "# TODO List\n- Ship it <2025-06-15>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0].timestamp), 1)
        self.assertEqual(tasks[0].timestamp[0], datetime.date(2025, 6, 15))

    def test_parses_timestamp_with_day_name(self):
        text = "# TODO List\n- Ship it <2025-06-15 Mon>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].timestamp[0], datetime.date(2025, 6, 15))

    def test_parses_timestamp_with_full_day_name(self):
        text = "# TODO List\n- Ship it <2025-06-15 Monday>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].timestamp[0], datetime.date(2025, 6, 15))

    def test_parses_timestamp_with_time(self):
        text = "# TODO List\n- Meeting <2025-06-15 Mon 14:30>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(
            tasks[0].timestamp[0], datetime.datetime(2025, 6, 15, 14, 30)
        )

    def test_parses_timestamp_date_and_time_without_day(self):
        text = "# TODO List\n- Meeting <2025-06-15 14:30>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(
            tasks[0].timestamp[0], datetime.datetime(2025, 6, 15, 14, 30)
        )

    def test_parses_multiple_deadlines(self):
        text = "# TODO List\n- Task DEADLINE: <2025-06-15> DEADLINE: <2025-06-20>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0].deadline), 2)
        self.assertEqual(tasks[0].deadline[0], datetime.date(2025, 6, 15))
        self.assertEqual(tasks[0].deadline[1], datetime.date(2025, 6, 20))

    def test_parses_deadline_and_scheduled_together(self):
        text = "# TODO List\n- Task DEADLINE: <2025-06-20> SCHEDULED: <2025-06-10>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0].deadline), 1)
        self.assertEqual(len(tasks[0].scheduled), 1)
        self.assertEqual(tasks[0].deadline[0], datetime.date(2025, 6, 20))
        self.assertEqual(tasks[0].scheduled[0], datetime.date(2025, 6, 10))

    def test_due_date_prefers_deadline_over_scheduled(self):
        text = "# TODO List\n- Task DEADLINE: <2025-06-20> SCHEDULED: <2025-06-10>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(tasks[0].due_date, datetime.date(2025, 6, 20))

    def test_parses_timestamps_from_notes(self):
        text = "# TODO List\n- Ship it\n\n# Ship it\nDEADLINE: <2025-06-15>\n"
        tasks = parse_month_notes(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0].deadline), 1)
        self.assertEqual(tasks[0].deadline[0], datetime.date(2025, 6, 15))

    def test_task_line_timestamps_override_notes(self):
        text = "# TODO List\n- Ship it DEADLINE: <2025-06-15>\n\n# Ship it\nDEADLINE: <2025-07-01>\n"
        tasks = parse_month_notes(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].deadline[0], datetime.date(2025, 6, 15))

    def test_timestamps_with_tags_and_status(self):
        text = "# TODO List\n- [DONE] #p1 Ship it DEADLINE: <2025-06-15>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Ship it DEADLINE: <2025-06-15>")
        self.assertEqual(tasks[0].state, "done")
        self.assertEqual(tasks[0].tags, ["p1"])
        self.assertEqual(tasks[0].deadline[0], datetime.date(2025, 6, 15))

    def test_plain_timestamp_not_confused_with_deadline(self):
        text = "# TODO List\n- Task DEADLINE: <2025-06-15> and <2025-06-20>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0].deadline), 1)
        self.assertEqual(len(tasks[0].timestamp), 1)
        self.assertEqual(tasks[0].deadline[0], datetime.date(2025, 6, 15))
        self.assertEqual(tasks[0].timestamp[0], datetime.date(2025, 6, 20))

    def test_no_timestamps_yields_empty_lists(self):
        text = "# TODO List\n- Ship it\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].deadline, [])
        self.assertEqual(tasks[0].scheduled, [])
        self.assertEqual(tasks[0].timestamp, [])
        self.assertIsNone(tasks[0].due_date)

    def test_plain_timestamp_not_confused_by_nearby_deadline_text(self):
        # Plain timestamp should be recognized even if "DEADLINE:" appears
        # elsewhere in the text (not immediately before the timestamp)
        text = "# TODO List\n- Task about DEADLINE: concept then <2025-06-20>\n"
        tasks = parse_todo_list(text)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0].deadline), 0)
        self.assertEqual(len(tasks[0].timestamp), 1)
        self.assertEqual(tasks[0].timestamp[0], datetime.date(2025, 6, 20))


if __name__ == "__main__":
    unittest.main()
