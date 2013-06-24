taskw - Python API for the taskwarrior DB
=========================================

.. split here

This is a python API for the `taskwarrior <http://taskwarrior.org>`_ command
line tool.

It contains two implementations: ``taskw.TaskWarrior`` and
``taskw.TaskWarriorExperimental``.  The first implementation is relatively
stable.  It manipulates the ``~/.task/`` dbs directly.  The second
implementation is in alpha and will be made default some day.  It interacts
with taskwarrior by shelling out to taskwarrior import and export commands
as per the upstream guidelines.

Build Status
------------

.. |master| image:: https://secure.travis-ci.org/ralphbean/taskw.png?branch=master
   :alt: Build Status - master branch
   :target: http://travis-ci.org/#!/ralphbean/taskw

.. |develop| image:: https://secure.travis-ci.org/ralphbean/taskw.png?branch=develop
   :alt: Build Status - develop branch
   :target: http://travis-ci.org/#!/ralphbean/taskw

+----------+-----------+
| Branch   | Status    |
+==========+===========+
| master   | |master|  |
+----------+-----------+
| develop  | |develop| |
+----------+-----------+

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

    Experimental mode

    >>> from taskw import TaskWarriorExperimental
    >>> w = TaskWarriorExperimental()
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
    >>> w.task_add("Take a nap", priority="H", project="life", due="1359090000")

Completing tasks
++++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> w.task_done(46)

Being Flexible
++++++++++++++

You can point ``taskw`` at different taskwarrior databases.

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior(config_filename="~/some_project/.taskrc")
    >>> w.task_add("Use 'taskw'.")

Looking at the config
+++++++++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> config = w.load_config()
    >>> config['data']['location']
    '/home/threebean/.task'
    >>> config['_forcecolor']
    'yes'
