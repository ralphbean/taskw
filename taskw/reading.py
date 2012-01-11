import codecs
import os
import re

open = lambda fname : codecs.open(fname, "r", "utf-8")


def load_tasks():
    """ Load all tasks.

    >>> tasks = load_tasks()
    >>> tasks.keys()
    ['completed', 'pending']
    >>> type(tasks['pending'])
    <type 'list'>
    >>> type(tasks['pending'][0])
    <type 'dict'>

    """

    def _load_tasks(filename):
        config = load_config()
        with open(os.path.join(config['data']['location'], filename)) as f:
            lines = f.readlines()

        return map(parse_line, lines)

    return dict(
        (db, _load_tasks('%s.data' % db)) for db in ['completed', 'pending']
    )

def load_config():
    """ Load ~/.taskrc into a python dict

    >>> config = load_config()
    >>> config['data']['location']
    '/home/threebean/.task'
    >>> config['_forcecolor']
    'yes'

    """

    with open(os.path.expanduser('~/.taskrc')) as f:
        lines = f.readlines()

    _usable = lambda l : not(l.startswith('#') or l.strip() == '')
    lines = filter(_usable, lines)

    def _build_config(key, value, d):
        """ Called recursively to split up keys """
        pieces = key.split('.', 1)
        if len(pieces) == 1:
            d[pieces[0]] = value.strip()
        else:
            d[pieces[0]] = _build_config(pieces[1], value, {})

        return d

    d = {}
    for line in lines:
        if '=' not in line:
            continue

        key, value = line.split('=')
        d = _build_config(key, value, d)

    return d

def parse_line(line):
    """ Parse a single record (task) from a task database file.

    I don't understand why they don't just use JSON or YAML.  But that's okay.

    >>> parse_line('[description:"Make a python API for taskwarrior"]')
    {'description': 'Make a python API for taskwarrior'}

    """

    d = {}
    for key, value in re.findall(r'(\w+):"(.*?)"', line):
        d[key] = value

    return d
