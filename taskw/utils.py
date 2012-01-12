""" Various utilties """

replacements = {
    '"': '&dquot;',
    '[': '&open;',
    ']': '&close;',
    '/': '\\/',
}


def clean_task(task):
    """ Clean a task by replacing any dangerous characters """
    for k in task:
        for unsafe, safe in replacements.iteritems():
            task[k] = task[k].replace(unsafe, safe)
    return task


def task2str(task):
    """ Convert a dict-like task to its string representation """
    # First, clean the task:
    task = clean_task(task)

    # Then, format it as a string
    return "[%s]\n" % " ".join([
        "%s:\"%s\"" % (k, v) for k, v in task.iteritems()
    ])
