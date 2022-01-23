import datetime
import random

import dateutil.tz
import pytz

from taskw.utils import (
    convert_dict_to_override_args,
    decode_task,
    encode_task,
    encode_task_experimental,
    DATE_FORMAT,
    clean_ctrl_chars,
)

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
        assert orig == TASK

    def test_with_escaped_quotes(self):
        expected = {'this': r'has a "quote" in it.'}
        line = r'[this:"has a \"quote\" in it."]'
        r = decode_task(line)
        assert r == expected

    def test_with_escaped_quotes_roundtrip(self):
        expected = {'this': r'has a "quote" in it.'}
        line = r'[this:"has a \"quote\" in it."]'
        r = decode_task(encode_task(decode_task(line)))
        assert r == expected

    def test_with_escaped_quotes_full(self):
        line = r'[this:"has a \"quote\" in it."]'
        r = encode_task(decode_task(line))
        assert r == r

    def test_with_backticks(self):
        expected = {'this': r'has a fucking `backtick` in it'}
        line = r'[this:"has a fucking `backtick` in it"]'
        r = decode_task(line)
        assert r == expected
        r = decode_task(encode_task(decode_task(line)))
        assert r == expected

    def test_with_backslashes(self):
        expected = {'andthis': r'has a fucking \backslash in it'}
        line = r'[andthis:"has a fucking \\backslash in it"]'
        r = decode_task(line)
        assert r == expected
        r = decode_task(encode_task(decode_task(line)))
        assert r == expected

    def test_with_unicode(self):
        expected = {
            'andthis': 'has a fucking \\backslash in it'
        }
        line = r'[andthis:"has a fucking \\backslash in it"]'
        r = decode_task(line)
        assert r == expected
        r = decode_task(encode_task(decode_task(line)))
        assert r == expected

    def test_decode(self):
        r = decode_task(encode_task(TASK))
        assert r == TASK

    def test_decode_leading_whitespace_in_value(self):
        r = decode_task(encode_task(TASK_LEADING_WS))
        assert r == TASK_LEADING_WS

    def test_composition(self):
        assert TASK == decode_task(encode_task(TASK))

    def test_double_composition(self):
        assert TASK == decode_task(encode_task(decode_task(encode_task(TASK))))

    def test_ordering(self):
        task1 = dict(shuffled(TASK.items()))
        task2 = dict(shuffled(TASK.items()))
        assert encode_task(task1) == encode_task(task2)

    def test_taskwarrior_null_encoding_bug_workaround(self):
        task = {
            'priority': ''
        }
        actual_encoded = encode_task_experimental(task)[0]
        expected_encoded = "priority:"

        assert actual_encoded == expected_encoded

    def test_encodes_dates(self):
        arbitrary_date = datetime.date(2014, 3, 2)
        task = {
            'arbitrary_field': arbitrary_date
        }

        actual_encoded_task = encode_task_experimental(task)
        expected_encoded_task = encode_task_experimental(
            {
                'arbitrary_field': arbitrary_date.strftime(DATE_FORMAT)
            }
        )

        assert actual_encoded_task == expected_encoded_task

    def test_encodes_naive_datetimes(self):
        arbitrary_naive_datetime = datetime.datetime.now()
        task = {
            'arbitrary_field': arbitrary_naive_datetime
        }

        actual_encoded_task = encode_task_experimental(task)
        expected_encoded_task = encode_task_experimental(
            {
                'arbitrary_field': (
                    arbitrary_naive_datetime
                    .replace(tzinfo=dateutil.tz.tzlocal())
                    .astimezone(pytz.utc).strftime(DATE_FORMAT)
                )
            }
        )

        assert actual_encoded_task == expected_encoded_task

    def test_encodes_zoned_datetimes(self):
        arbitrary_timezone = pytz.timezone('America/Los_Angeles')
        arbitrary_zoned_datetime = datetime.datetime.now().replace(
            tzinfo=arbitrary_timezone
        )
        task = {
            'arbitrary_field': arbitrary_zoned_datetime
        }

        actual_encoded_task = encode_task_experimental(task)
        expected_encoded_task = encode_task_experimental(
            {
                'arbitrary_field': (
                    arbitrary_zoned_datetime
                    .astimezone(pytz.utc).strftime(DATE_FORMAT)
                )
            }
        )

        assert actual_encoded_task == expected_encoded_task

    def test_convert_dict_to_override_args(self):
        overrides = {
            'one': {
                'two': 1,
                'three': {
                    'alpha': 'a'
                },
                'four': 'lorem ipsum',
            },
            'two': {
            }
        }

        expected_overrides = [
            'rc.one.two=1',
            'rc.one.three.alpha=a',
            'rc.one.four="lorem ipsum"',
        ]
        actual_overrides = convert_dict_to_override_args(overrides)

        assert set(actual_overrides) == set(expected_overrides)


class TestCleanExecArg(object):
    def test_clean_null(self):
        assert b"" == clean_ctrl_chars(b"\x00")

    def test_all_ctrl_chars(self):
        """ Test that most (but not all) control characters are removed """
        # input = bytes(range(0x20))
        input = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'  # For python 2 compatibility
        assert b"\t\n\v\f\r" == clean_ctrl_chars(input)
