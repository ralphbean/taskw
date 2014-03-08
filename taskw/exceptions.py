import sys


class TaskwarriorError(Exception):
    def __init__(self, command, stderr, stdout, code):
        self.command = command
        self.stderr = stderr.strip()
        self.stdout = stdout.strip()
        self.code = code
        super(TaskwarriorError, self).__init__(self.stderr)

    def __unicode__(self):
        return "%r #%s; stderr:\"%s\"; stdout:\"%s\"" % (
            self.command,
            self.code,
            self.stderr,
            self.stdout,
        )

    def __str__(self):
        return self.__unicode__().encode(sys.getdefaultencoding(), 'replace')
