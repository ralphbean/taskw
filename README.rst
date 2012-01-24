taskw - Python API for the taskwarrior DB
=========================================

.. split here

This is a python API for the `taskwarrior <http://taskwarrior.org>`_ command
line tool.

Getting taskw
-------------

Installing
++++++++++

Using ``taskw`` requires that you first install `taskwarrior
<http://taskwarrior.org>`_.

Installing it from http://pypi.python.org/pypi/taskw is easy with ``pip``::

    $ pip install taskw

The Source
++++++++++

You can find the source on github at http://github.com/ralphbean/taskw


Examples
--------

Looking at tasks
++++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> tasks = w.load_tasks()
    >>> tasks.keys()
    ['completed', 'pending']
    >>> type(tasks['pending'])
    <type 'list'>
    >>> type(tasks['pending'][0])
    <type 'dict'>

Adding tasks
++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> w.task_add("Eat food")
    >>> w.task_add("Take a nap", priority="H", project="life")

Completing tasks
++++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> w.task_done(46)

Looking at the config
+++++++++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> config = w.load_config()
    >>> config['data']['location']
    '/home/threebean/.task'
    >>> config['_forcecolor']
    'yes'
