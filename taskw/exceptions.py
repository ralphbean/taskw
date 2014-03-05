import sys


class TaskwarriorError(Exception):
    def __init__(self, stderr, stdout, code):
        self.stderr = stderr.strip()
        self.stdout = stdout.strip()
        self.code = code
        super(TaskwarriorError, self).__init__(self.stderr)

    def __unicode__(self):
        return "#%s; stderr:\"%s\"; stdout:\"%s\"" % (
            self.code,
            self.stderr,
            self.stdout,
        )

    def __str__(self):
        return self.__unicode__().encode(sys.getdefaultencoding(), 'replace')
