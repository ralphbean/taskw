taskw - Python API for the taskwarrior DB
=========================================

This is a python API for the `taskwarrior <http://taskwarrior.org>`_ command
line tool.

Example
-------

::
    >>> from taskw import load_tasks
    >>> tasks = load_tasks()
    >>> tasks.keys()
    ['completed', 'pending']
    >>> type(tasks['pending'])
    <type 'list'>
    >>> type(tasks['pending'][0])
    <type 'dict'>

    >>> from taskw import load_config
    >>> config = load_config()
    >>> config['data']['location']
    '/home/threebean/.task'
    >>> config['_forcecolor']
    'yes'

