from nose.tools import eq_, raises
import os
import shutil
import tempfile

from taskw import TaskWarrior

TASK = {'description': "task 2 http://www.google.com/",
        'entry': "1325011643",
        'project': "work",
        'start': "1326079920", 'status': "pending",
        'uuid': "c1c431ea-f0dc-4683-9a20-e64fcfa65fd1"}


class TestDB(object):
    def setup(self):
        # Create some temporary config stuff
        fd, fname = tempfile.mkstemp(prefix='taskw-testsrc')
        dname = tempfile.mkdtemp(prefix='taskw-tests-data')

        with open(fname, 'w') as f:
            f.writelines(['data.location=%s' % dname])

        # Create empty .data files
        for piece in ['completed', 'pending', 'undo']:
            with open(os.path.sep.join([dname, piece + '.data']), 'w'):
                pass

        # Save names for .tearDown()
        self.fname, self.dname = fname, dname

        # Create the taskwarrior db object that each test will use.
        self.tw = TaskWarrior(config_filename=fname)

    def tearDown(self):
        os.remove(self.fname)
        shutil.rmtree(self.dname)

    def test_has_two_categories(self):
        tasks = self.tw.load_tasks()
        eq_(len(tasks), 2)

    def test_empty_db(self):
        tasks = self.tw.load_tasks()
        eq_(len(sum(tasks.values(), [])), 0)

    def test_add(self):
        self.tw.task_add("foobar")
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 1)

    def test_unchanging_load_tasks(self):
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)

    @raises(KeyError)
    def test_completion_raising_unspecified(self):
        self.tw.task_done()

    def test_completing_task_by_id_unspecified(self):
        self.tw.task_add("foobar")
        self.tw.task_done(id=1)
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        eq_(len(tasks['completed']), 1)
        eq_(len(sum(tasks.values(), [])), 1)

    def test_completing_task_by_id_specified(self):
        self.tw.task_add("foobar")
        self.tw.task_done(id=1)
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        eq_(len(tasks['completed']), 1)
        eq_(len(sum(tasks.values(), [])), 1)

    def test_completing_task_by_id_retrieved(self):
        task = self.tw.task_add("foobar")
        self.tw.task_done(id=task['id'])
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        eq_(len(tasks['completed']), 1)
        eq_(len(sum(tasks.values(), [])), 1)

    def test_completing_task_by_uuid(self):
        self.tw.task_add("foobar")
        uuid = self.tw.load_tasks()['pending'][0]['uuid']
        self.tw.task_done(uuid=uuid)
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        eq_(len(tasks['completed']), 1)
        eq_(len(sum(tasks.values(), [])), 1)

    @raises(KeyError)
    def test_get_task_mismatch(self):
        self.tw.task_add("foobar")
        self.tw.task_add("bazbar")
        uuid = self.tw.load_tasks()['pending'][0]['uuid']
        self.tw.get_task(id=2, uuid=uuid)  # which one?

    def test_updating_task(self):
        self.tw.task_add("foobar")

        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 1)

        task = tasks['pending'][0]
        task["priority"] = "L"
        self.tw.task_update(task)

        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 1)
        eq_(tasks['pending'][0], task)

    @raises(KeyError)
    def test_update_exc(self):
        task = dict(description="lol")
        self.tw.task_update(task)
