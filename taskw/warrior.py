import codecs
import os
import re
import time
import uuid

import taskw.utils


open = lambda fname, mode: codecs.open(fname, mode, "utf-8")


class TaskWarrior(object):
    """ The task warrior

    Really though, a python object with methods allowing you to interact
    with a taskwarrior database.
    """

    def __init__(self, config_filename="~/.taskrc"):
        self.config_filename = config_filename
        self.config = self.load_config()

    def load_tasks(self):
        """ Load all tasks.

        >>> w = Warrior()
        >>> tasks = w.load_tasks()
        >>> tasks.keys()
        ['completed', 'pending']
        >>> type(tasks['pending'])
        <type 'list'>
        >>> type(tasks['pending'][0])
        <type 'dict'>

        """

        def _load_tasks(filename):
            filename = os.path.join(self.config['data']['location'], filename)
            with open(filename, 'r') as f:
                lines = f.readlines()

            return map(taskw.utils.decode_task, lines)

        return dict(
            (db, _load_tasks('%s.data' % db))
            for db in ['completed', 'pending']
        )

    def load_config(self):
        """ Load ~/.taskrc into a python dict

        >>> w = Warrior()
        >>> config = w.load_config()
        >>> config['data']['location']
        '/home/threebean/.task'
        >>> config['_forcecolor']
        'yes'

        """

        with open(os.path.expanduser(self.config_filename), 'r') as f:
            lines = f.readlines()

        _usable = lambda l: not(l.startswith('#') or l.strip() == '')
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

    def task_add(self, description, **kw):
        """ Add a new task.

        Takes any of the keywords allowed by taskwarrior like proj or prior.
        """
        task = {"description": description}
        task.update(kw)

        task['status'] = 'pending'

        # TODO -- check only valid keywords

        if not 'entry' in task:
            task['entry'] = str(int(time.time()))

        if not 'uuid' in task:
            task['uuid'] = str(uuid.uuid4())

        self._task_add(task, 'pending')

    def task_done(self, id=None, uuid=None):
        if not id and not uuid:
            raise KeyError("task_done must receive either id or uuid")

        tasks = self.load_tasks()

        if id:
            if len(tasks['pending']) < id:
                raise ValueError("No such pending task with id %i." % id)

            task = tasks['pending'][id - 1]
        else:
            matching = filter(lambda t: t['uuid'] == uuid, tasks['pending'])
            if not matching:
                raise ValueError("No such pending task with uuid %i." % uuid)

            task = matching[0]
            id = tasks['pending'].index(task) + 1

        task['status'] = 'completed'
        task['end'] = str(int(time.time()))

        self._task_add(task, 'completed')
        self._task_remove(id, 'pending')

    def _task_remove(self, id, category):
        location = self.config['data']['location']
        filename = category + '.data'
        filename = os.path.join(self.config['data']['location'], filename)

        with open(filename, "r") as f:
            lines = f.readlines()

        del lines[id - 1]

        with open(filename, "w") as f:
            f.writelines(lines)

    def _task_add(self, task, category):
        location = self.config['data']['location']
        filename = category + '.data'

        # Append the task
        with open(os.path.join(location, filename), "a") as f:
            f.writelines([taskw.utils.encode_task(task)])

        # Add to undo.data
        with open(os.path.join(location, 'undo.data'), "a") as f:
            f.write("time %s\n" % str(int(time.time())))
            f.write("new %s" % taskw.utils.encode_task(task))
            f.write("---\n")
