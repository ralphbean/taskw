import tempfile
import os
import shutil
from unittest import TestCase

from taskw.warrior import TaskWarrior


class TestTaskWarrior(TestCase):
    def setUp(self):
        self.taskdata = tempfile.mkdtemp()
        taskrc = os.path.join(os.path.dirname(__file__), 'data/empty.taskrc')
        self.taskwarrior = TaskWarrior(
            config_filename=taskrc,
            config_overrides={'data.location': self.taskdata})
        # Just a sanity check to make sure that after the setup, the list of
        # tasks is empty, otherwise we are probably using the current user's
        # TASKDATA and we should not continue.
        assert self.taskwarrior.load_tasks() == {'completed': [], 'pending': []}

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.taskdata)

    def test_add_task_foobar(self):
        """ Add a task with description 'foobar' and checks that the task is
        indeed created """
        self.taskwarrior.task_add("foobar")
        tasks = self.taskwarrior.load_tasks()
        assert len(tasks['pending']) == 1
        assert tasks['pending'][0]['description'] == 'foobar'

    def test_add_task_null_char(self):
        """ Try adding a task where the description contains a NULL character
        (0x00). This should not fail but instead simply add a task with the
        same description minus the NULL character """
        self.taskwarrior.task_add("foo\x00bar")
        tasks = self.taskwarrior.load_tasks()
        assert len(tasks['pending']) == 1
        assert tasks['pending'][0]['description'] == 'foobar'

    def test_add_task_recurs(self):
        """ Try adding a task with `recur` to ensure the uuid can be parsed """
        self.taskwarrior.task_add("foobar weekly", due="tomorrow", recur="weekly")
        tasks = self.taskwarrior.load_tasks()

        assert len(tasks['pending']) == 1
        assert tasks['pending'][0]['description'] == 'foobar weekly'
        assert tasks['pending'][0]['recur'] == 'weekly'
        assert tasks['pending'][0]['parent'] is not None

