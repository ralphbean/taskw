""" Various utilties """
from __future__ import print_function

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

from distutils.version import LooseVersion


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
])

decode_replacements = OrderedDict([
    [v, k] for k, v in encode_replacements.items()
    if k not in ('\n')  # We skip these.
])

logical_replacements = OrderedDict([
    ('?', '\\?'),
    ('+', '\\+'),
    ('(', '\\('),
    (')', '\\)'),
    ('[', '\\['),
    (']', '\\]'),
    ('{', '\\{'),
    ('}', '\\}'),
])


def encode_task_value(key, value, query=False):
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
                # don't replace '?' if this is an exact match
                if left == '?' and '.' not in key:
                    continue
                value = value.replace(left, right)
        else:
            for unsafe, safe in six.iteritems(
                encode_replacements_experimental
            ):
                value = value.replace(unsafe, safe)
    else:
        value = str(value)
    return value


def encode_query(value, version, query=True):
    args = []

    if isinstance(value, dict):
        value = six.iteritems(value)

    for k, v in value:
        if isinstance(v, list):
            args.append(
                "( %s )" % (" %s " % k).join([
                    encode_query([item], version, query=False)[0] for item in v
                ])
            )
        else:
            if k.endswith(".is") and version >= LooseVersion('2.4'):
                args.append(
                    '%s == "%s"' % (
                        k[:-3],
                        encode_task_value(k, v, query=query)
                    )
                )
            else:
                args.append(
                    '%s:%s' % (
                        k,
                        encode_task_value(k, v, query=query)
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
        task[k] = encode_task_value(k, task[k])

    # Then, format it as a string
    return [
        "%s:\"%s\"" % (k, v) if v else "%s:" % (k, )
        for k, v in sorted(task.items(), key=itemgetter(0))
    ]


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


def make_annotation_comparable(annotation):
    """ Make an annotation comparable.

    Some transformations occur internally when storing a message in
    Taskwarrior.  Let's flatten those out.

    """
    return re.sub(
        r'[\W_]',
        '',
        annotation
    )


def get_annotation_value(annotation):
    """ Can either be a dictionary, or a string. """
    if isinstance(annotation, dict):
        return annotation['description']
    return annotation


def annotation_exists_in_list(authoritative, new):
    comparable_annotations = []
    for item in authoritative:
        if not item:
            continue
        annotation = get_annotation_value(item)
        comparable_annotations.append(
            make_annotation_comparable(annotation)
        )
    return make_annotation_comparable(new) in comparable_annotations


def merge_annotations(left, right):
    for annotation in right:
        if not annotation_exists_in_list(left, annotation):
            left.append(right)

    return left


def annotation_list_to_comparison_map(annotations):
    mapping = {}
    for annotation in annotations:
        comparable = make_annotation_comparable(annotation)
        mapping[comparable] = annotation
    return mapping


def convert_dict_to_override_args(config, prefix=''):
    """ Converts a dictionary of override arguments into CLI arguments.

    * Converts leaf nodes into dot paths of key names leading to the leaf
      node.
    * Does not include paths to leaf nodes not being non-dictionary type.

    See `taskw.test.test_utils.TestUtils.test_convert_dict_to_override_args`
    for details.

    """
    args = []
    for k, v in six.iteritems(config):
        if isinstance(v, dict):
            args.extend(
                convert_dict_to_override_args(
                    v,
                    prefix='.'.join([
                        prefix,
                        k,
                    ]) if prefix else k
                )
            )
        else:
            v = six.text_type(v)
            left = 'rc' + (('.' + prefix) if prefix else '') + '.' + k
            right = v if ' ' not in v else '"%s"' % v
            args.append('='.join([left, right]))
    return args
