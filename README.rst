taskw - Python API for the taskwarrior DB
=========================================

.. split here

This is a python API for the `taskwarrior <http://taskwarrior.org>`_ command
line tool.

It contains two implementations: ``taskw.TaskWarriorShellout`` and
``taskw.TaskWarriorDirect``.  The first implementation is the supported one
recommended by the upstream taskwarrior core project.  It uses the ``task
export`` and ``task import`` commands to manipulate the task database.  The
second implementation opens the task db file itself and directly manipulates
it.  It exists for backwards compatibility, but should only be used when
necessary.

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

Adding tasks
++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> w.task_add("Eat food")
    >>> w.task_add("Take a nap", priority="H", project="life", due="1359090000")

Retrieving tasks
++++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> w.get_task(id=5)

Updating tasks
++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> id, task = w.get_task(id=14)
    >>> task['project'] = 'Updated project name'
    >>> w.task_update(task)

Deleting tasks
++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> w.task_delete(id=3)

Completing tasks
++++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior()
    >>> w.task_done(id=46)

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


Using Python-appropriate Types (Dates, UUIDs, etc)
++++++++++++++++++++++++++++++++++++++++++++++++++

    >>> from taskw import TaskWarrior
    >>> w = TaskWarrior(marshal=True)
    >>> w.get_task(id=10)
    (10,
     {
      'description': 'Hello there!',
      'entry': datetime.datetime(2014, 3, 14, 14, 18, 40, tzinfo=tzutc())
      'id': 10,
      'project': 'Saying Hello',
      'status': 'pending',
      'uuid': UUID('4882751a-3966-4439-9675-948b1152895c')
     }
    )
