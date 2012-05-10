""" Various utilties """

import re
from operator import itemgetter
import six

encode_replacements = {
    '"': '&dquot;',
    '[': '&open;',
    ']': '&close;',
    '/': '\\/',
}
decode_replacements = dict([[v, k] for k, v in encode_replacements.items()])


def clean_task(task):
    """ Clean a task by replacing any dangerous characters """
    return task


def encode_task(task):
    """ Convert a dict-like task to its string representation """
    # First, clean the task:
    task = task.copy()
    for k in task:
        for unsafe, safe in six.iteritems(encode_replacements):
            task[k] = task[k].replace(unsafe, safe)

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
    for key, value in re.findall(r'(\w+):"(.*?)"', line):
        task[key] = value
        for unsafe, safe in six.iteritems(decode_replacements):
            task[key] = task[key].replace(unsafe, safe)

    return task
