import nose
from nose.tools import eq_
import os
import shutil
import tempfile

from taskw import TaskWarriorShellout


TASK = {'description': "task 2 http://www.google.com/",
        'entry': "1325011643",
        'project': "work",
        'start': "1326079920", 'status': "pending",
        'uuid': "c1c431ea-f0dc-4683-9a20-e64fcfa65fd1"}


class TestRecursibe(object):
    def setup(self):
        if not TaskWarriorShellout.can_use():
            # Sometimes the 'task' command line tool is not installed.
            raise nose.SkipTest("taskwarrior not installed")

        # Create some temporary config stuff
        fd, fname = tempfile.mkstemp(prefix='taskw-testsrc')
        dname = tempfile.mkdtemp(prefix='taskw-tests-data')

        with open(fname, 'w') as f:
            f.writelines([
                'data.location=%s\n' % dname,
                'uda.somestring.label=Testing String\n',
                'uda.somestring.type=string\n',
                'uda.somedate.label=Testing Date\n',
                'uda.somedate.type=date\n',
                'uda.somenumber.label=Testing Number\n',
                'uda.somenumber.type=numeric\n',
            ])

        # Create empty .data files
        for piece in ['completed', 'pending', 'undo']:
            with open(os.path.sep.join([dname, piece + '.data']), 'w'):
                pass

        # Save names for .tearDown()
        self.fname, self.dname = fname, dname

        # Create the taskwarrior db object that each test will use.
        self.tw = TaskWarriorShellout(config_filename=fname, marshal=True)

    def tearDown(self):
        os.remove(self.fname)
        shutil.rmtree(self.dname)

    def test_set_dep_on_one_uuid(self):
        task1 = self.tw.task_add('task1')
        task2 = self.tw.task_add('task2', depends=[task1['uuid']])
        eq_(task2['depends'][0], task1['uuid'])

    def test_set_dep_on_two_uuid(self):
        task1 = self.tw.task_add('task1')
        task2 = self.tw.task_add('task2')
        depends = [task1['uuid'], task2['uuid']]
        task3 = self.tw.task_add('task3', depends=depends)
        eq_(task3['depends'], [task1['uuid'], task2['uuid']])
