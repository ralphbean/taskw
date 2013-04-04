import codecs
import os
import re
import time
import uuid
import subprocess
import json
import pprint

import taskw.utils
from six.moves import filter
from six.moves import map
from six.moves import zip


open = lambda fname, mode: codecs.open(fname, mode, "utf-8")


class TaskWarrior(object):
    """ The task warrior

    Really though, a python object with methods allowing you to interact
    with a taskwarrior database.
    """

    def __init__(self, config_filename="~/.taskrc"):
        self.config_filename = config_filename
        self.config = self.load_config()
        global experimental
        experimental = False
        if 'taskw' in self.config and 'experimental' in self.config[u'taskw']:
            experimental = True

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
            filename = os.path.expanduser(filename)
            with open(filename, 'r') as f:
                lines = f.readlines()

            return list(map(taskw.utils.decode_task, lines))

        def _load_exported_tasks():
            # Load tasks using `task export`
            pending_tasks = list()
            completed_tasks = list()
            tasks = dict()
            pending_tasks = json.loads(subprocess.Popen(['task', 'rc.json.array=TRUE', 'rc.verbose=nothing', 'status:pending', 'export'], stdout=subprocess.PIPE).communicate()[0])
            completed_tasks = json.loads(subprocess.Popen(['task', 'rc.json.array=TRUE', 'rc.verbose=nothing', 'status:completed', 'export'], stdout=subprocess.PIPE).communicate()[0])
            tasks['pending'] = pending_tasks
            tasks['completed'] = completed_tasks
            return tasks

        if experimental is not True:
            return dict(
                (db, _load_tasks('%s.data' % db))
                for db in ['completed', 'pending']
            )
        else:
            return _load_exported_tasks()


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

    def task_add(self, description, tags=None, **kw):
        """ Add a new task.

        Takes any of the keywords allowed by taskwarrior like proj or prior.
        """
        task = {"description": description}
        if tags != None:
            task['tags'] = tags

        task.update(kw)

        # Only UNIX timestamps are currently supported.
        if 'due' in kw:
            task['due'] = str(task['due'])

        if experimental is True:
            subprocess.call(['task', 'add', taskw.utils.encode_task_experimental(task)])
            tasks = self.load_tasks()
            return tasks['pending'][-1]
        else:
            task['status'] = 'pending'

            # TODO -- check only valid keywords

            if not 'entry' in task:
                task['entry'] = str(int(time.time()))

            if not 'uuid' in task:
                task['uuid'] = str(uuid.uuid4())

            id = self._task_add(task, 'pending')
            task['id'] = id
            return task

    def get_task(self, **kw):
        valid_keys = set(['id', 'uuid', 'description'])
        id_keys = valid_keys.intersection(kw.keys())

        if len(id_keys) != 1:
            raise KeyError("get_task must receive one ID keyword argument")

        key = list(id_keys)[0]
        if key not in valid_keys:
            raise KeyError("Argument must be one of %r" % valid_keys)

        tasks = self.load_tasks()

        if key == 'id':
            id = kw[key]

            if len(tasks['pending']) < id:
                raise ValueError("No such pending task with id %i." % id)

            task = tasks['pending'][id - 1]
        else:
            matching = list(filter(
                lambda t: t[key] == kw[key],
                tasks['pending']
            ))

            if not matching:
                raise ValueError("No such pending task with %s %r." % (
                    key, kw[key]))

            task = matching[0]
            id = tasks['pending'].index(task) + 1

        return id, task

    def filter_by(self, func):
        tasks = self.load_tasks()
        filtered = filter(func, tasks)
        return filtered

    def task_done(self, **kw):
        id, task = self.get_task(**kw)

        if experimental is True:
            subprocess.Popen(['task', str(id), 'do'], stdout=subprocess.PIPE).communicate()[0]
            tasks = self.load_tasks()
            return tasks['completed'][-1]

        task['status'] = 'completed'
        task['end'] = kw.get('end') or str(int(time.time()))

        self._task_add(task, 'completed')
        self._task_remove(id, 'pending')
        return task

    def task_update(self, task):
        id, _task = self.get_task(uuid=task['uuid'])

        if 'id' in task:
            del task['id']

        _task.update(task)
        if experimental is True:
            # Unset task attributes that should not be updated
            task_to_modify = _task
            del task_to_modify['uuid']
            del task_to_modify['id']
            modification = taskw.utils.encode_task_experimental(task_to_modify)
            subprocess.call(['task', task[u'uuid'], 'modify', modification])
        else:
            self._task_replace(id, 'pending', _task)
        return id, _task

    def _task_replace(self, id, category, task):
        def modification(lines):
            lines[id - 1] = taskw.utils.encode_task(task)
            return lines

        # FIXME write to undo.data
        self._apply_modification(id, category, modification)

    def _task_remove(self, id, category):
        def modification(lines):
            del lines[id - 1]
            return lines

        # FIXME write to undo.data
        self._apply_modification(id, category, modification)

    def _apply_modification(self, id, category, modification):
        location = self.config['data']['location']
        filename = category + '.data'
        filename = os.path.join(self.config['data']['location'], filename)
        filename = os.path.expanduser(filename)

        with open(filename, "r") as f:
            lines = f.readlines()

        lines = modification(lines)

        with open(filename, "w") as f:
            f.writelines(lines)

    def _task_add(self, task, category):
        location = self.config['data']['location']
        location = os.path.expanduser(location)
        filename = category + '.data'

        # Append the task
        with open(os.path.join(location, filename), "a") as f:
            f.writelines([taskw.utils.encode_task(task)])

        # FIXME - this gets written when a task is completed.  incorrect.
        # Add to undo.data
        with open(os.path.join(location, 'undo.data'), "a") as f:
            f.write("time %s\n" % str(int(time.time())))
            f.write("new %s" % taskw.utils.encode_task(task))
            f.write("---\n")

        with open(os.path.join(location, filename), "r") as f:
            # The 'id' of this latest added task.
            return len(f.readlines())
