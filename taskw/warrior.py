""" Code to interact with taskwarrior

This module contains an abstract base class and two different implementations
for interacting with taskwarrior:  TaskWarriorDirect and TaskWarriorShellout.

If it is determined that there is a binary 'task' on the system and that it is
of a sufficiently advanced version, then TaskWarriorShellout will be made the
default TaskWarrior class.  If not, then the default TaskWarrior class will
fall back to the older TaskWarriorDirect implementation.

"""
import abc
import codecs
import copy
from distutils.version import LooseVersion
import logging
import os
import time
import uuid
import subprocess
import json

import six
from six import with_metaclass
from six.moves import filter
from six.moves import map

import taskw.utils
from taskw.exceptions import TaskwarriorError
from taskw.task import Task
from taskw.taskrc import TaskRc


logger = logging.getLogger(__name__)


open = lambda fname, mode: codecs.open(fname, mode, "utf-8")


class TaskWarriorBase(with_metaclass(abc.ABCMeta, object)):
    """ The task warrior

    Really though, a python object with methods allowing you to interact
    with a taskwarrior database.
    """

    def __init__(
        self,
        config_filename="~/.taskrc",
        config_overrides=None,
        marshal=False
    ):
        self.config_filename = config_filename
        self.config = TaskWarriorBase.load_config(config_filename)
        if marshal:
            raise NotImplementedError(
                "You must use TaskWarriorShellout to use 'marshal'"
            )
        if config_overrides:
            raise NotImplementedError(
                "You must use TaskWarriorShellout to use 'config_overrides'"
            )

    def _stub_task(self, description, tags=None, **kw):
        """ Given a description, stub out a task dict. """

        # If whitespace is not removed here, TW will do it when we pass the
        # task to it.
        task = {"description": description.strip()}

        # Allow passing "tags" in as part of kw.
        if 'tags' in kw and tags is None:
            task['tags'] = tags
            del(kw['tags'])

        if tags is not None:
            task['tags'] = tags

        task.update(kw)

        # Only UNIX timestamps are currently supported.
        if 'due' in kw:
            task['due'] = str(task['due'])

        return task

    def _extract_annotations_from_task(self, task):
        """ Removes annotations from a task and returns a list of annotations
        """
        annotations = list()

        if 'annotations' in task:
            existing_annotations = task.pop('annotations')
            for v in existing_annotations:
                if isinstance(v, dict):
                    annotations.append(v['description'])
                else:
                    annotations.append(v)

        for key in list(task.keys()):
            if key.startswith('annotation_'):
                annotations.append(task[key])
                del(task[key])
        return annotations

    @abc.abstractmethod
    def load_tasks(self, command='all'):
        """ Load all tasks.

        Similar to TaskWarrior, a specific command may be specified:

            all       - a list of all issues
            pending   - a list of all pending issues
            completed - a list of all completed issues

        By default, the 'all' command is run.

        >>> w = TaskWarrior()
        >>> tasks = w.load_tasks()
        >>> tasks.keys()
        ['completed', 'pending']
        >>> type(tasks['pending'])
        <type 'list'>
        >>> type(tasks['pending'][0])
        <type 'dict'>
        """

    @abc.abstractmethod
    def task_add(self, description, tags=None, **kw):
        """ Add a new task.

        Takes any of the keywords allowed by taskwarrior like proj or prior.
        """
        pass

    @abc.abstractmethod
    def task_done(self, **kw):
        pass

    @abc.abstractmethod
    def task_delete(self, **kw):
        pass

    @abc.abstractmethod
    def _load_task(self, **kw):
        pass

    @abc.abstractmethod
    def task_update(self, task):
        pass

    @abc.abstractmethod
    def get_task(self, **kw):
        pass

    def filter_by(self, func):
        tasks = self.load_tasks()
        filtered = filter(func, tasks)
        return filtered

    @classmethod
    def load_config(self, config_filename="~/.taskrc"):
        """ Load ~/.taskrc into a python dict

        >>> config = TaskWarrior.load_config()
        >>> config['data']['location']
        '/home/threebean/.task'
        >>> config['_forcecolor']
        'yes'

        """

        with open(os.path.expanduser(config_filename), 'r') as f:
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

            key, value = line.split('=', 1)
            d = _build_config(key, value, d)

        # Set a default data location if one is not specified.
        if d.get('data') is None:
            d['data'] = {}

        if d['data'].get('location') is None:
            d['data']['location'] = os.path.expanduser("~/.task/")

        return d

    @abc.abstractmethod
    def task_start(self, **kw):
        pass

    @abc.abstractmethod
    def task_stop(self, **kw):
        pass


class TaskWarriorDirect(TaskWarriorBase):
    """ Interacts with taskwarrior by directly manipulating the ~/.task/ db.

    This is the deprecated implementation and will be phased out in
    time due to taskwarrior's guidelines:  http://bit.ly/16I9VN4

    See https://github.com/ralphbean/taskw/pull/15 for discussion
    and https://github.com/ralphbean/taskw/issues/30 for more.
    """

    def sync(self):
        raise NotImplementedError(
            "You must use TaskWarriorShellout to use 'sync'"
        )

    def load_tasks(self, command='all'):
        def _load_tasks(filename):
            filename = os.path.join(self.config['data']['location'], filename)
            filename = os.path.expanduser(filename)
            with open(filename, 'r') as f:
                lines = f.readlines()

            return list(map(taskw.utils.decode_task, lines))

        return dict(
            (db, _load_tasks(DataFile.filename(db)))
            for db in Command.files(command)
        )

    def get_task(self, **kw):
        line, task = self._load_task(**kw)

        id = None
        # The ID going back only makes sense if the task is pending.
        if Status.is_pending(task['status']):
            id = line

        return id, task

    def _load_task(self, **kw):
        valid_keys = set(['id', 'uuid', 'description'])
        id_keys = valid_keys.intersection(kw.keys())

        if len(id_keys) != 1:
            raise KeyError("Only 1 ID keyword argument may be specified")

        key = list(id_keys)[0]
        if key not in valid_keys:
            raise KeyError("Argument must be one of %r" % valid_keys)

        line = None
        task = dict()

        # If the key is an id, assume the task is pending (completed tasks
        # don't have IDs).
        if key == 'id':
            tasks = self.load_tasks(command=Status.PENDING)
            line = kw[key]

            if len(tasks[Status.PENDING]) >= line:
                task = tasks[Status.PENDING][line - 1]

        else:
            # Search all tasks for the specified key.
            tasks = self.load_tasks(command=Command.ALL)

            matching = list(filter(
                lambda t: t.get(key, None) == kw[key],
                sum(tasks.values(), [])
            ))

            if matching:
                task = matching[0]
                line = tasks[Status.to_file(task['status'])].index(task) + 1

        return line, task

    def task_add(self, description, tags=None, **kw):
        """ Add a new task.

        Takes any of the keywords allowed by taskwarrior like proj or prior.
        """

        task = self._stub_task(description, tags, **kw)

        task['status'] = Status.PENDING

        # TODO -- check only valid keywords

        if not 'entry' in task:
            task['entry'] = str(int(time.time()))

        if not 'uuid' in task:
            task['uuid'] = str(uuid.uuid4())

        id = self._task_add(task, Status.PENDING)
        task['id'] = id
        return task

    def task_done(self, **kw):
        """
        Marks a pending task as done, optionally specifying a completion
        date with the 'end' argument.
        """
        def validate(task):
            if not Status.is_pending(task['status']):
                raise ValueError("Task is not pending.")

        return self._task_change_status(Status.COMPLETED, validate, **kw)

    def task_update(self, task):
        line, _task = self._load_task(uuid=task['uuid'])

        if 'id' in task:
            del task['id']

        # Delete None values (treat them as deleting values)
        # https://github.com/ralphbean/taskw/pull/70
        items = list(task.items())  # listify generator for py3 support.
        for k, v in items:
            if v is None:
                task.pop(k)
                if k in _task:
                    _task.pop(k)

        _task.update(task)
        self._task_replace(line, Status.to_file(task['status']), _task)
        return line, _task

    def task_delete(self, **kw):
        """
        Marks a task as deleted, optionally specifying a completion
        date with the 'end' argument.
        """
        def validate(task):
            if task['status'] == Status.DELETED:
                raise ValueError("Task is already deleted.")

        return self._task_change_status(Status.DELETED, validate, **kw)

    def task_start(self, **kw):
        """ Marks a task as started.  """
        raise NotImplementedError()

    def task_stop(self, **kw):
        """ Marks a task as stopped.  """
        raise NotImplementedError()

    def filter_tasks(self, filter_dict):
        raise NotImplementedError()

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
        filename = DataFile.filename(category)
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

    def _task_change_status(self, status, validation, **kw):
        line, task = self._load_task(**kw)
        validation(task)
        original_status = task['status']

        task['status'] = status
        task['end'] = kw.get('end') or str(int(time.time()))

        self._task_add(task, Status.to_file(status))
        self._task_remove(line, Status.to_file(original_status))
        return task


class TaskWarriorShellout(TaskWarriorBase):
    """ Interacts with taskwarrior by invoking shell commands.

    This is currently the supported version and should be considered stable.

    See https://github.com/ralphbean/taskw/pull/15 for discussion
    and https://github.com/ralphbean/taskw/issues/30 for more.
    """
    DEFAULT_CONFIG_OVERRIDES = {
        'json': {
            'array': 'TRUE'
        },
        'verbose': 'nothing',
        'confirmation': 'no',
        'dependency': {
            'confirmation': 'no',
        },
    }

    def __init__(
        self,
        config_filename="~/.taskrc",
        config_overrides=None,
        marshal=False,
    ):
        super(TaskWarriorShellout, self).__init__(config_filename)
        self.config_overrides = config_overrides if config_overrides else {}
        self._marshal = marshal
        self.config = TaskRc(config_filename, overrides=config_overrides)

        if self.get_version() >= LooseVersion('2.4'):
            self.DEFAULT_CONFIG_OVERRIDES['verbose'] = 'new-uuid'

    def get_configuration_override_args(self):
        config_overrides = self.DEFAULT_CONFIG_OVERRIDES.copy()
        config_overrides.update(self.config_overrides)
        return taskw.utils.convert_dict_to_override_args(config_overrides)

    def _execute(self, *args):
        """ Execute a given taskwarrior command with arguments

        Returns a 2-tuple of stdout and stderr (respectively).

        """
        command = (
            [
                'task',
                'rc:%s' % self.config_filename,
            ]
            + self.get_configuration_override_args()
            + [six.text_type(arg) for arg in args]
        )

        # subprocess is expecting bytestrings only, so nuke unicode if present
        for i in range(len(command)):
            if isinstance(command[i], six.text_type):
                command[i] = command[i].encode('utf-8')

        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            raise TaskwarriorError(command, stderr, stdout, proc.returncode)

        # We should get bytes from the outside world.  Turn those into unicode
        # as soon as we can.
        stdout = stdout.decode(self.config.get('encoding', 'utf-8'))
        stderr = stderr.decode(self.config.get('encoding', 'utf-8'))

        return stdout, stderr

    def _get_json(self, *args):
        return json.loads(self._execute(*args)[0])

    def _get_task_objects(self, *args):
        json = self._get_json(*args)
        if isinstance(json, dict):
            return self._get_task_object(json)
        value = [self._get_task_object(j) for j in json]
        return value

    def _get_task_object(self, obj):
        if self._marshal:
            return Task(obj, udas=self.config.get_udas())
        return obj

    def _stub_task(self, description, tags=None, **kw):
        """ Given a description, stub out a task dict. """

        # If whitespace is not removed here, TW will do it when we pass the
        # task to it.
        task = {"description": description.strip()}

        # Allow passing "tags" in as part of kw.
        if 'tags' in kw and tags is None:
            task['tags'] = tags
            del(kw['tags'])

        if tags is not None:
            task['tags'] = tags

        task.update(kw)

        return task

    @classmethod
    def can_use(cls):
        """ Returns true if runtime requirements of experimental mode are met
        """
        try:
            return cls.get_version() > LooseVersion('2')
        except OSError:
            # OSError is raised if subprocess.Popen fails to find
            # the executable.
            return False

    @classmethod
    def get_version(cls):
        taskwarrior_version = subprocess.Popen(
            ['task', '--version'],
            stdout=subprocess.PIPE
        ).communicate()[0]
        return LooseVersion(taskwarrior_version.decode())

    def sync(self, init=False):
        if self.get_version() < LooseVersion('2.3'):
            raise UnsupportedVersionException(
                "'sync' requires version 2.3 of taskwarrior or later."
            )
        if init is True:
            self._execute('sync', 'init')
        else:
            self._execute('sync')

    def load_tasks(self, command='all'):
        """ Returns a dictionary of tasks for a list of command."""

        results = dict(
            (db, self._get_task_objects('status:%s' % db, 'export'))
            for db in Command.files(command)
        )

        # 'waiting' tasks are returned separately from 'pending' tasks
        # Here we merge the waiting list back into the pending list.
        if 'pending' in results:
            results['pending'].extend(
                self._get_task_objects('status:waiting', 'export'))

        return results

    def filter_tasks(self, filter_dict):
        """ Return a filtered list of tasks from taskwarrior.

        Filter dict should be a dictionary mapping filter constraints
        with their values.  For example, to return only pending tasks,
        you could use::

            {'status': 'pending'}

        Or, to return tasks that have the word "Abjad" in their description
        that are also pending::

            {
                'status': 'pending',
                'description.contains': 'Abjad',
            }

        Filters can be quite complex, and are documented on Taskwarrior's
        website.

        """
        query_args = taskw.utils.encode_query(filter_dict, self.get_version())
        return self._get_task_objects(
            'export',
            *query_args
        )

    def get_task(self, **kw):
        task = dict()
        task_id = None
        task_id, task = self._load_task(**kw)
        id = None

        # The ID going back only makes sense if the task is pending.
        if 'status' in task:
            if Status.is_pending(task['status']):
                id = task_id

        return id, task

    def _load_task(self, **kwargs):
        if len(kwargs) > 1:
            raise KeyError(
                "Only one keyword argument may be specified"
            )

        search = []
        for key, value in six.iteritems(kwargs):
            if key not in ['id', 'uuid', 'description']:
                search.append(
                    '%s:%s' % (
                        key,
                        value,
                    )
                )
            elif key == 'description' and '(bw)' in value:
                search.append(
                    value[4:]
                )
            else:
                search = [value]

        task = self._get_task_objects('export', *search)

        if task:
            if isinstance(task, list):
                # Multiple items returned from search, return just the 1st
                task = task[0]
            return task['id'], task

        return None, dict()

    def task_add(self, description, tags=None, **kw):
        """ Add a new task.

        Takes any of the keywords allowed by taskwarrior like proj or prior.
        """
        task = self._stub_task(description, tags, **kw)

        # Check if there are annotations, if so remove them from the
        # task and add them after we've added the task.
        annotations = self._extract_annotations_from_task(task)

        # With older versions of taskwarrior, you can specify whatever uuid you
        # want when adding a task.
        if self.get_version() < LooseVersion('2.4'):
            task['uuid'] = str(uuid.uuid4())
        elif 'uuid' in task:
            del task['uuid']

        stdout, stderr = self._execute(
            'add',
            *taskw.utils.encode_task_experimental(task)
        )

        # However, in 2.4 and later, you cannot specify whatever uuid you want
        # when adding a task.  Instead, you have to specify rc.verbose=new-uuid
        # and then parse the assigned uuid out from stdout.
        if self.get_version() >= LooseVersion('2.4'):
            task['uuid'] = stdout.strip().split()[-1].strip('.')

        id, added_task = self.get_task(uuid=task['uuid'])

        # Check if 'uuid' is in the task we just added.
        if not 'uuid' in added_task:
            raise KeyError(
                'Error encountered while creating task;'
                'STDOUT: %s; STDERR: %s' % (
                    stdout,
                    stderr,
                )
            )

        if annotations and 'uuid' in added_task:
            for annotation in annotations:
                self.task_annotate(added_task, annotation)

        id, added_task = self.get_task(uuid=added_task[six.u('uuid')])
        return added_task

    def task_annotate(self, task, annotation):
        """ Annotates a task. """
        self._execute(
            task['uuid'],
            'annotate',
            '--',
            annotation
        )
        id, annotated_task = self.get_task(uuid=task[six.u('uuid')])
        return annotated_task

    def task_denotate(self, task, annotation):
        """ Removes an annotation from a task. """
        self._execute(
            task['uuid'],
            'denotate',
            '--',
            annotation
        )
        id, denotated_task = self.get_task(uuid=task[six.u('uuid')])
        return denotated_task

    def task_done(self, **kw):
        if not kw:
            raise KeyError('No key was passed.')

        id, task = self.get_task(**kw)

        if not Status.is_pending(task['status']):
            raise ValueError("Task is not pending.")

        self._execute(id, 'done')
        return self.get_task(uuid=task['uuid'])[1]

    def task_update(self, task):
        if 'uuid' not in task:
            raise KeyError('Task must have a UUID.')
        # 'Legacy' causes us to handle this task as if it were an
        # old-style task -- just a standard dictionary
        legacy = True

        if isinstance(task, Task):
            # Let's pre-serialize taskw.task.Task instances
            task_uuid = six.text_type(task['uuid'])
            task = task.serialized_changes(keep=True)
            legacy = False
        else:
            task_uuid = task['uuid']

        id, original_task = self.get_task(uuid=task_uuid)

        if 'id' in task:
            del task['id']

        task_to_modify = copy.deepcopy(task)

        task_to_modify.pop('uuid', None)
        task_to_modify.pop('id', None)

        # Only handle annotation differences if this is an old-style
        # task, or if the task itself says annotations have changed.
        annotations_to_delete = set()
        annotations_to_create = set()
        if legacy or 'annotations' in task_to_modify:
            # Check if there are annotations, if so, look if they are
            # in the existing task, otherwise annotate the task to add them.
            ttm_annotations = taskw.utils.annotation_list_to_comparison_map(
                self._extract_annotations_from_task(task_to_modify)
            )
            original_annotations = (
                taskw.utils.annotation_list_to_comparison_map(
                    self._extract_annotations_from_task(original_task)
                )
            )

            new_annotations = set(ttm_annotations.keys())
            existing_annotations = set(original_annotations.keys())

            annotations_to_delete = existing_annotations - new_annotations
            annotations_to_create = new_annotations - existing_annotations

            if 'annotations' in task_to_modify:
                del task_to_modify['annotations']

        modification = taskw.utils.encode_task_experimental(task_to_modify)
        # Only try to modify the task if there are changes to post here
        # (changes *might* just be in annotations).
        if modification:
            self._execute(task_uuid, 'modify', *modification)

        # If there are no existing annotations, add the new ones
        if legacy or annotations_to_delete or annotations_to_create:
            ttm_annotations.update(original_annotations)
            for annotation_key in annotations_to_create:
                self.task_annotate(
                    original_task,
                    ttm_annotations[annotation_key]
                )
            for annotation_key in annotations_to_delete:
                self.task_denotate(
                    original_task,
                    ttm_annotations[annotation_key]
                )

        return self.get_task(uuid=task_uuid)

    def task_delete(self, **kw):
        """ Marks a task as deleted.  """

        id, task = self.get_task(**kw)

        if task['status'] == Status.DELETED:
            raise ValueError("Task is already deleted.")

        self._execute(id, 'delete')
        return self.get_task(uuid=task['uuid'])[1]

    def task_start(self, **kw):
        """ Marks a task as started.  """

        id, task = self.get_task(**kw)

        self._execute(id, 'start')
        return self.get_task(uuid=task['uuid'])[1]

    def task_stop(self, **kw):
        """ Marks a task as stopped.  """

        id, task = self.get_task(**kw)

        self._execute(id, 'stop')
        return self.get_task(uuid=task['uuid'])[1]

    def task_info(self, **kw):
        id, task = self.get_task(**kw)
        out, err = self._execute(id, 'info')
        if err:
            return err
        return out


class DataFile(object):
    """ Encapsulates data file names. """
    PENDING = 'pending'
    COMPLETED = 'completed'

    @classmethod
    def filename(cls, name):
        return "%s.data" % name


class Command(object):
    """ Encapsulates available commands. """
    PENDING = 'pending'
    COMPLETED = 'completed'
    ALL = 'all'

    @classmethod
    def files(cls, command):
        known_commands = {
            Command.PENDING: [DataFile.PENDING],
            Command.COMPLETED: [DataFile.COMPLETED],
            Command.ALL: [DataFile.PENDING, DataFile.COMPLETED]
        }

        if not command in known_commands:
            raise ValueError(
                "Unknown command, %s. Command must be one of %s." %
                (command, known_commands.keys()))

        return known_commands[command]


class Status(object):
    """ Encapsulates task status values. """
    PENDING = 'pending'
    COMPLETED = 'completed'
    DELETED = 'deleted'
    WAITING = 'waiting'

    @classmethod
    def is_pending(cls, status):
        """ Identifies if the specified status is a 'pending' state. """
        return status == Status.PENDING or status == Status.WAITING

    @classmethod
    def to_file(cls, status):
        """ Returns the file in which this task is stored. """
        return {
            Status.PENDING: DataFile.PENDING,
            Status.WAITING: DataFile.PENDING,
            Status.COMPLETED: DataFile.COMPLETED,
            Status.DELETED: DataFile.COMPLETED
        }[status]


class UnsupportedVersionException(object):
    pass


# It is not really experimental anymore, but we provide this rename for
# backwards compatibility.  It will eventually be removed.
TaskWarriorExperimental = TaskWarriorShellout


# Set a default based on what is available on the system.
if TaskWarriorShellout.can_use():
    TaskWarrior = TaskWarriorShellout
else:
    TaskWarrior = TaskWarriorDirect
