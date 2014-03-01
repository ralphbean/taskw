""" Various utilties """

import datetime
import re
from operator import itemgetter

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import dateutil.tz
import pytz
import six

DATE_FORMAT = '%Y%m%dT%H%M%SZ'


encode_replacements = OrderedDict([
    ('\\', '\\\\'),
    ('\"', '&dquot;'),
    ('"', '&dquot;'),
    ('[', '&open;'),
    (']', '&close;'),
    ('\n', ' '),
    ('/', '\\/'),
])

encode_replacements_experimental = OrderedDict([
    ('\"', '&dquot;'),
    ('"', '&dquot;'),
    ('[', '&open;'),
    (']', '&close;'),
    ('\n', ' '),
])

decode_replacements = OrderedDict([
    [v, k] for k, v in encode_replacements.items()
    if k not in ('\n')  # We skip these.
])

logical_replacements = OrderedDict([
    ('(', '\\('),
    (')', '\\)'),
    ('[', '\\['),
    (']', '\\]'),
])


def encode_task_value(value, query=False):
    if value is None:
        value = ''
    elif isinstance(value, datetime.datetime):
        if not value.tzinfo:
            #  Dates not having timezone information should be
            #  assumed to be in local time
            value = value.replace(tzinfo=dateutil.tz.tzlocal())
        #  All times should be converted to UTC before serializing
        value = value.astimezone(pytz.utc).strftime(DATE_FORMAT)
    elif isinstance(value, datetime.date):
        value = value.strftime(DATE_FORMAT)
    elif isinstance(value, six.string_types):
        if query:
            # In some contexts, parentheses are interpreted for use in
            # logical expressions.  They must *sometimes* be escaped.
            for left, right in six.iteritems(logical_replacements):
                value = value.replace(left, right)
        else:
            for unsafe, safe in six.iteritems(
                encode_replacements_experimental
            ):
                value = value.replace(unsafe, safe)
    else:
        value = str(value)
    return value


def encode_query(value):
    args = []
    for k, v in six.iteritems(value):
        args.append(
            '%s:\"%s\"' % (
                k,
                encode_task_value(v, query=True)
            )
        )
    return args


def clean_task(task):
    """ Clean a task by replacing any dangerous characters """
    return task


def encode_task_experimental(task):
    """ Convert a dict-like task to its string representation
        Used for adding a task via `task add`
    """
    # First, clean the task:
    task = task.copy()
    if 'tags' in task:
        task['tags'] = ','.join(task['tags'])
    for k in task:
        task[k] = encode_task_value(task[k])

    # Then, format it as a string
    return "%s\n" % " ".join([
        "%s:\"%s\"" % (k, v)
        for k, v in sorted(task.items(), key=itemgetter(0))
    ])


def encode_task(task):
    """ Convert a dict-like task to its string representation """
    # First, clean the task:
    task = task.copy()
    if 'tags' in task:
        task['tags'] = ','.join(task['tags'])
    for k in task:
        for unsafe, safe in six.iteritems(encode_replacements):
            if isinstance(task[k], six.string_types):
                task[k] = task[k].replace(unsafe, safe)

        if isinstance(task[k], datetime.datetime):
            task[k] = task[k].strftime("%Y%m%dT%M%H%SZ")

    # Then, format it as a string
    return "[%s]\n" % " ".join([
        "%s:\"%s\"" % (k, v)
        for k, v in sorted(task.items(), key=itemgetter(0))
    ])


def decode_task(line):
    """ Parse a single record (task) from a task database file.

    I don't understand why they don't just use JSON or YAML.  But
    that's okay.

    >>> decode_task('[description:"Make a python API for taskwarrior"]')
    {'description': 'Make a python API for taskwarrior'}

    """

    task = {}
    for key, value in re.findall(r'(\w+):"(.*?)(?<!\\)"', line):
        value = value.replace('\\"', '"')  # unescape quotes
        task[key] = value
        for unsafe, safe in six.iteritems(decode_replacements):
            task[key] = task[key].replace(unsafe, safe)
    if 'tags' in task:
        task['tags'] = task['tags'].split(',')
    return task
