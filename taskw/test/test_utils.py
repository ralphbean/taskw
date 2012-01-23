from nose.tools import eq_

from taskw.utils import decode_task, encode_task

TASK = {'description': "task 2 http://www.google.com/",
        'entry': "1325011643",
        'project': "work",
        'start': "1326079920", 'status': "pending",
        'uuid': "c1c431ea-f0dc-4683-9a20-e64fcfa65fd1"}


TASK_LEADING_WS = TASK.copy()
TASK_LEADING_WS.update({'description': "      task 3"})


class TestUtils(object):

    def test_no_side_effects(self):
        orig = TASK.copy()
        decode_task(encode_task(TASK))
        eq_(orig, TASK)

    def test_decode(self):
        r = decode_task(encode_task(TASK))
        eq_(r, TASK)

    def test_decode_leading_whitespace_in_value(self):
        r = decode_task(encode_task(TASK_LEADING_WS))
        eq_(r, TASK_LEADING_WS)

    def test_composition(self):
        eq_(TASK, decode_task(encode_task(TASK)))

    def test_double_composition(self):
        eq_(TASK, decode_task(encode_task(decode_task(encode_task(TASK)))))
