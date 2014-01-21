import nose
from nose.tools import eq_, ok_, raises
import os
import sys
import shutil
import tempfile

from taskw import TaskWarriorDirect, TaskWarriorShellout


TASK = {'description': "task 2 http://www.google.com/",
        'entry': "1325011643",
        'project': "work",
        'start': "1326079920", 'status': "pending",
        'uuid': "c1c431ea-f0dc-4683-9a20-e64fcfa65fd1"}


class _BaseTestDB(object):
    def setup(self):

        # Sometimes the 'task' command line tool is not installed.
        if self.should_skip():
            raise nose.SkipTest(
                "%r unsupported on this system" % (self.class_to_test)
            )

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
        self.tw = self.class_to_test(config_filename=fname)

    def tearDown(self):
        os.remove(self.fname)
        shutil.rmtree(self.dname)

    def test_has_two_categories(self):
        tasks = self.tw.load_tasks()
        eq_(len(tasks), 2)
        ok_('pending' in tasks)
        ok_('completed' in tasks)

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
        ok_(tasks['completed'][0]['end'] is not None)
        eq_(tasks['completed'][0]['status'], 'completed')

    def test_completing_task_by_id_specified(self):
        self.tw.task_add("foobar")
        self.tw.task_done(id=1)
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        eq_(len(tasks['completed']), 1)
        eq_(len(sum(tasks.values(), [])), 1)
        eq_(tasks['completed'][0]['status'], 'completed')

    def test_completing_task_by_id_retrieved(self):
        task = self.tw.task_add("foobar")
        self.tw.task_done(id=task['id'])
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        eq_(len(tasks['completed']), 1)
        eq_(len(sum(tasks.values(), [])), 1)
        eq_(tasks['completed'][0]['status'], 'completed')

    def test_completing_task_by_uuid(self):
        self.tw.task_add("foobar")
        uuid = self.tw.load_tasks()['pending'][0]['uuid']
        self.tw.task_done(uuid=uuid)
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        eq_(len(tasks['completed']), 1)
        eq_(len(sum(tasks.values(), [])), 1)
        eq_(tasks['completed'][0]['status'], 'completed')

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

        # For compatibility with the direct and shellout modes.
        # Shellout returns more information.
        try:
            # Shellout mode returns the correct urgency, so,
            # let's just not compare for now.
            del tasks['pending'][0]['urgency']
            del task['urgency']

            # Also, experimental mode returns the id.  So, avoid comparing.
            del tasks['pending'][0]['id']
            # Task 2.2.0 adds a "modified" field, so delete this.
            del tasks['pending'][0]['modified']
        except:
            pass

        eq_(tasks['pending'][0], task)

    @raises(KeyError)
    def test_update_exc(self):
        task = dict(description="lol")
        self.tw.task_update(task)

    def test_add_complicated(self):
        self.tw.task_add(
            "foobar",
            uuid="1234-1234",
            project="some_project"
        )
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 1)

    @raises(ValueError)
    def test_completing_completed_task(self):
        task = self.tw.task_add("foobar")
        self.tw.task_done(uuid=task['uuid'])
        self.tw.task_done(uuid=task['uuid'])

    def test_updating_completed_task(self):
        task = self.tw.task_add("foobar")
        task = self.tw.task_done(uuid=task['uuid'])
        task['priority'] = 'L'
        id, task = self.tw.task_update(task)
        eq_(task['priority'], 'L')

    def test_get_task_completed(self):
        task = self.tw.task_add("foobar")
        task = self.tw.task_done(uuid=task['uuid'])

        id, _task = self.tw.get_task(uuid=task['uuid'])
        eq_(id, None)
        eq_(_task['uuid'], task['uuid'])

    def test_load_task_pending_command(self):
        tasks = self.tw.load_tasks(command='pending')
        eq_(len(tasks), 1)
        ok_('pending' in tasks)

    def test_load_task_completed_command(self):
        tasks = self.tw.load_tasks(command='completed')
        eq_(len(tasks), 1)
        ok_('completed' in tasks)

    @raises(ValueError)
    def test_load_task_with_unknown_command(self):
        tasks = self.tw.load_tasks(command='foobar')

    def test_updating_deleted_task(self):
        task = self.tw.task_add("foobar")
        task = self.tw.task_delete(uuid=task['uuid'])
        task['priority'] = 'L'
        id, task = self.tw.task_update(task)
        eq_(task['priority'], 'L')

    def test_delete(self):
        task = self.tw.task_add("foobar")
        self.tw.task_delete(uuid=task['uuid'])
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        # The shellout and direct methods behave differently here
        #eq_(len(tasks['completed']), 1)
        #ok_(not tasks['completed'][0]['end'] is None)
        #eq_(tasks['completed'][0]['status'], 'deleted')

    def test_delete_completed(self):
        task = self.tw.task_add("foobar")
        task = self.tw.task_done(uuid=task['uuid'])
        self.tw.task_delete(uuid=task['uuid'])
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 0)
        eq_(len(tasks['completed']), 1)
        #eq_(tasks['completed'][0]['status'], 'deleted')

    @raises(ValueError)
    def test_delete_already_deleted(self):
        task = self.tw.task_add("foobar")
        self.tw.task_delete(uuid=task['uuid'])
        self.tw.task_delete(uuid=task['uuid'])

    def test_load_tasks_with_one_each(self):
        task1 = self.tw.task_add("foobar1")
        task2 = self.tw.task_add("foobar2")
        task2 = self.tw.task_done(uuid=task2['uuid'])
        tasks = self.tw.load_tasks()
        eq_(len(tasks['pending']), 1)
        eq_(len(tasks['completed']), 1)

        # For issue #26, I thought this would raise an exception...
        task = self.tw.get_task(description='foobar1')


class TestDBDirect(_BaseTestDB):
    class_to_test = TaskWarriorDirect

    def should_skip(self):
        return False


class TestDBShellout(_BaseTestDB):
    class_to_test = TaskWarriorShellout

    def should_skip(self):
        """ If 'task' is not installed, we can't run these tests. """
        return not TaskWarriorShellout.can_use()
