""" Tests for taskw.reading
"""
import unittest2

import taskw.reading as reading
from taskw.utils import task2str


class TestReading(unittest2.TestCase):
    def test_parse_line(self):
        r = reading.parse_line(task2str(PARSED_TASK))
        self.assertEqual(r, PARSED_TASK)

    def test_parse_line_leading_whitespace_in_value(self):
        r = reading.parse_line(task2str(PARSED_TASK_LEADING_WS))
        self.assertEqual(r, PARSED_TASK_LEADING_WS)

    def test_quote_escaped_tasks(self):
        r = reading.parse_line(task2str(PARSED_TASK_QUOTE))
        self.assertEqual(r, PARSED_TASK_QUOTE)


PARSED_TASK = {'description': "task 2", 'entry': "1325011643",
               'project': "work",
              'start': "1326079920", 'status': "pending",
              'uuid': "c1c431ea-f0dc-4683-9a20-e64fcfa65fd1"}


PARSED_TASK_LEADING_WS = PARSED_TASK.copy()
PARSED_TASK_LEADING_WS.update({'description': "      task 3"})

PARSED_TASK_QUOTE = PARSED_TASK.copy()
PARSED_TASK_QUOTE.update({'description': 'foo \\&dquot;bar\\&dquot;'})
