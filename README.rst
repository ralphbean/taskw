taskw - Python API for the taskwarrior DB
=========================================

.. split here

This is a python API for the `taskwarrior <http://taskwarrior.org>`_ command
line tool.

Installing
----------

Using ``taskw`` requires that you first install `taskwarrior
<http://taskwarrior.org>`_.

Installing is easy with ``pip``::

    $ pip install taskw

Examples
--------

Looking at tasks
++++++++++++++++

    >>> from taskw import load_tasks
    >>> tasks = load_tasks()
    >>> tasks.keys()
    ['completed', 'pending']
    >>> type(tasks['pending'])
    <type 'list'>
    >>> type(tasks['pending'][0])
    <type 'dict'>

Adding tasks
++++++++++++

    >>> from taskw import task_add
    >>> task_add("Eat food")
    >>> task_add("Take a nap", priority="H", project="life")

Completing tasks
++++++++++++++++

    >>> from taskw import task_done
    >>> task_done(46)

Looking at the config
+++++++++++++++++++++

    >>> from taskw import load_config
    >>> config = load_config()
    >>> config['data']['location']
    '/home/threebean/.task'
    >>> config['_forcecolor']
    'yes'
