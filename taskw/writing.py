import taskw.reading
import taskw.utils

import codecs
import os
import time
import uuid


open = lambda fname, mode : codecs.open(fname, mode, "utf-8")


def task_add(description, **kw):
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

    _task_add(task, 'pending')


def task_done(id=None, uuid=None):
    if not id and not uuid:
        raise KeyError("task_done must receive either id or uuid")

    tasks = taskw.reading.load_tasks()

    if id:
        if len(tasks['pending']) < id:
            raise ValueError("No such pending task with id %i." % id)

        task = tasks['pending'][id - 1]
    else:
        matching = filter(lambda t: t['uuid'] == uuid, tasks['pending'])
        if not matching:
            raise ValueError("No such pending task with uuid %i." % uuid)

        task = matching[0]
        id = tasks['pending'].index(task)+1

    task['status'] = 'completed'
    task['end'] = str(int(time.time()))

    _task_add(task, 'completed')
    _task_remove(id, 'pending')


def _task_remove(id, category):
    filename = category + '.data'
    config = taskw.reading.load_config()

    with open(os.path.join(config['data']['location'], filename), "r") as f:
        lines = f.readlines()

    del lines[id-1]

    with open(os.path.join(config['data']['location'], filename), "w") as f:
        f.writelines(lines)


def _task_add(task, category):
    filename = category + '.data'
    config = taskw.reading.load_config()
    location = config['data']['location']

    # Append the task
    with open(os.path.join(location, filename), "a") as f:
        f.writelines([taskw.utils.task2str(task)])

    # Add to undo.data
    with open(os.path.join(location, 'undo.data'), "a") as f:
        f.write("time %s\n" % str(int(time.time())))
        f.write("new %s" % taskw.utils.task2str(task))
        f.write("---\n")
