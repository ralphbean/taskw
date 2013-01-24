import random

from nose.tools import eq_

from taskw.utils import decode_task, encode_task

TASK = {'description': "task 2 http://www.google.com/",
        'entry': "1325011643",
        'project': "work",
        'due': "1359090000",
        'start': "1326079920", 'status': "pending",
        'uuid': "c1c431ea-f0dc-4683-9a20-e64fcfa65fd1"}


TASK_LEADING_WS = TASK.copy()
TASK_LEADING_WS.update({'description': "      task 3"})


def shuffled(l):
    new = list(l)
    random.shuffle(new)
    return new


class TestUtils(object):

    def test_no_side_effects(self):
        orig = TASK.copy()
        decode_task(encode_task(TASK))
        eq_(orig, TASK)

    def test_with_escaped_quotes(self):
        expected = {'this': r'has a "quote" in it.'}
        line = r'[this:"has a \"quote\" in it."]'
        r = decode_task(line)
        eq_(r, expected)

    def test_with_escaped_quotes_roundtrip(self):
        expected = {'this': r'has a "quote" in it.'}
        line = r'[this:"has a \"quote\" in it."]'
        r = decode_task(encode_task(decode_task(line)))
        eq_(r, expected)

    def test_with_escaped_quotes_full(self):
        line = r'[this:"has a \"quote\" in it."]'
        r = encode_task(decode_task(line))
        eq_(r, r)

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

    def test_ordering(self):
        task1 = dict(shuffled(TASK.items()))
        task2 = dict(shuffled(TASK.items()))
        eq_(encode_task(task1), encode_task(task2))
