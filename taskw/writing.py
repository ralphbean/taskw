import taskw.reading

import os
import time
import uuid

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


def task_done(id):
    tasks = taskw.reading.load_tasks()

    if len(tasks['pending']) < id:
        raise ValueError("No such pending task.")

    task = tasks['pending'][id - 1]
    task['status'] = 'completed'
    task['end'] = str(int(time.time()))

    _task_add(task, 'completed')
    _task_remove(id, 'pending')


def task2str(task):
    return "[%s]\n" % " ".join([
        "%s:\"%s\"" % (k, v) for k, v in task.iteritems()
    ])


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

    # Append the task
    with open(os.path.join(config['data']['location'], filename), "a") as f:
        f.writelines([task2str(task)])
