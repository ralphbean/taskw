import os
import shutil
import tempfile
import datetime
import dateutil.tz

import pytest

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
            pytest.skip(
                "%r unsupported on this system" % (self.class_to_test)
            )

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
        self.tw = self.class_to_test(config_filename=fname)

        # Create a taskwarrior db object for tests where marshal=True,
        # but only for TaskwarriorShellout
        if self.class_to_test == TaskWarriorShellout:
            self.tw_marshal = self.class_to_test(config_filename=fname,
                                                 marshal=True)

    def tearDown(self):
        os.remove(self.fname)
        shutil.rmtree(self.dname)

    def test_has_two_categories(self):
        tasks = self.tw.load_tasks()
        assert len(tasks) == 2
        assert 'pending' in tasks
        assert 'completed' in tasks

    def test_empty_db(self):
        tasks = self.tw.load_tasks()
        assert len(sum(tasks.values(), [])) == 0

    def test_add(self):
        self.tw.task_add("foobar")
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 1

    def test_unchanging_load_tasks(self):
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 0
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 0

    def test_completion_raising_unspecified(self):
        with pytest.raises(KeyError):
            self.tw.task_done()

    def test_completing_task_by_id_unspecified(self):
        self.tw.task_add("foobar")
        self.tw.task_done(id=1)
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 0
        assert len(tasks['completed']) == 1
        assert len(sum(tasks.values(), [])) == 1
        assert tasks['completed'][0]['end'] is not None
        assert tasks['completed'][0]['status'] == 'completed'

    def test_completing_task_by_id_specified(self):
        self.tw.task_add("foobar")
        self.tw.task_done(id=1)
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 0
        assert len(tasks['completed']) == 1
        assert len(sum(tasks.values(), [])) == 1
        assert tasks['completed'][0]['status'] == 'completed'

    def test_completing_task_by_id_retrieved(self):
        task = self.tw.task_add("foobar")
        self.tw.task_done(id=task['id'])
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 0
        assert len(tasks['completed']) == 1
        assert len(sum(tasks.values(), [])) == 1
        assert tasks['completed'][0]['status'] == 'completed'

    def test_completing_task_by_uuid(self):
        self.tw.task_add("foobar")
        uuid = self.tw.load_tasks()['pending'][0]['uuid']
        self.tw.task_done(uuid=uuid)
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 0
        assert len(tasks['completed']) == 1
        assert len(sum(tasks.values(), [])) == 1
        assert tasks['completed'][0]['status'] == 'completed'

    def test_get_task_mismatch(self):
        self.tw.task_add("foobar")
        self.tw.task_add("bazbar")
        uuid = self.tw.load_tasks()['pending'][0]['uuid']
        with pytest.raises(KeyError):
            self.tw.get_task(id=2, uuid=uuid)  # which one?

    def test_updating_task(self):
        self.tw.task_add("foobar")

        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 1

        task = tasks['pending'][0]
        task["priority"] = "L"
        self.tw.task_update(task)

        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 1
        assert tasks['pending'][0]['priority'] == 'L'

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
        except Exception:
            pass

        # But Task 2.4.0 puts the modified field in earlier
        if 'modified' in task:
            del task['modified']

        assert tasks['pending'][0] == task

    def test_update_exc(self):
        task = dict(description="lol")
        with pytest.raises(KeyError):
            self.tw.task_update(task)

    def test_add_complicated(self):
        self.tw.task_add(
            "foobar",
            uuid="1234-1234",
            project="some_project"
        )
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 1

    def test_add_timestamp(self):
        self.tw.task_add(
            "foobar",
            uuid="1234-1234",
            project="some_project",
            entry="20110101T000000Z",
        )
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 1
        assert tasks['pending'][0]['entry'] == "20110101T000000Z"

    def test_add_datetime(self):
        self.tw.task_add(
            "foobar",
            uuid="1234-1234",
            project="some_project",
            entry=datetime.datetime(2011, 1, 1, tzinfo=dateutil.tz.tzutc()),
        )
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 1
        # The exact string we get back is dependent on your current TZ
        # ... we'll just "roughly" test it instead of mocking.
        assert(tasks['pending'][0]['entry'].startswith("20110101T"))

    def test_add_with_uda_string(self):
        self.tw.task_add(
            "foobar",
            somestring="this is a uda",
        )
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 1
        task = tasks['pending'][0]

        assert task['somestring'] == "this is a uda"

    def test_add_with_uda_date(self):
        self.tw.task_add(
            "foobar",
            somedate=datetime.datetime(2011, 1, 1, tzinfo=dateutil.tz.tzutc()),
        )
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 1
        task = tasks['pending'][0]

        assert(task['somedate'].startswith("20110101T"))

    def test_remove_uda_string(self):
        # Check that a string UDA is removed from a task when its
        # value is set to None
        task = self.tw.task_add(
            "foobar",
            somestring='this is a uda',
        )
        task['somestring'] = None
        id, task = self.tw.task_update(task)
        with pytest.raises(KeyError):
            task['somestring']

    def test_remove_uda_date(self):
        # Check that a date UDA is removed from a task when its
        # value is set to None
        task = self.tw.task_add(
            "foobar",
            somedate=datetime.datetime(2011, 1, 1),
        )
        task['somedate'] = None
        id, task = self.tw.task_update(task)
        with pytest.raises(KeyError):
            task['somedate']

    def test_remove_uda_numeric(self):
        # Check that a numeric UDA is removed from a task when its
        # value is set to None
        task = self.tw.task_add(
            "foobar",
            somenumber=15,
        )
        task['somenumber'] = None
        id, task = self.tw.task_update(task)
        with pytest.raises(KeyError):
            task['somenumber']

    def test_completing_completed_task(self):
        task = self.tw.task_add("foobar")
        self.tw.task_done(uuid=task['uuid'])
        with pytest.raises(ValueError):
            self.tw.task_done(uuid=task['uuid'])

    def test_updating_completed_task(self):
        task = self.tw.task_add("foobar")
        task = self.tw.task_done(uuid=task['uuid'])
        task['priority'] = 'L'
        id, task = self.tw.task_update(task)
        assert task['priority'] == 'L'

    def test_get_task_completed(self):
        task = self.tw.task_add("foobar")
        task = self.tw.task_done(uuid=task['uuid'])

        id, _task = self.tw.get_task(uuid=task['uuid'])
        assert id is None
        assert _task['uuid'] == task['uuid']

    def test_load_task_pending_command(self):
        tasks = self.tw.load_tasks(command='pending')
        assert len(tasks) == 1
        assert 'pending' in tasks

    def test_load_task_completed_command(self):
        tasks = self.tw.load_tasks(command='completed')
        assert len(tasks) == 1
        assert 'completed' in tasks

    def test_load_task_with_unknown_command(self):
        with pytest.raises(ValueError):
            self.tw.load_tasks(command='foobar')

    def test_updating_deleted_task(self):
        task = self.tw.task_add("foobar")
        task = self.tw.task_delete(uuid=task['uuid'])
        task['priority'] = 'L'
        id, task = self.tw.task_update(task)
        assert task['priority'] == 'L'

    def test_delete(self):
        task = self.tw.task_add("foobar")
        self.tw.task_delete(uuid=task['uuid'])
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 0

    def test_delete_already_deleted(self):
        task = self.tw.task_add("foobar")
        self.tw.task_delete(uuid=task['uuid'])
        with pytest.raises(ValueError):
            self.tw.task_delete(uuid=task['uuid'])

    def test_load_tasks_with_one_each(self):
        self.tw.task_add("foobar1")
        task2 = self.tw.task_add("foobar2")
        task2 = self.tw.task_done(uuid=task2['uuid'])
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 1
        assert len(tasks['completed']) == 1

        # For issue #26, I thought this would raise an exception...
        self.tw.get_task(description='foobar1')


class TestDBDirect(_BaseTestDB):
    class_to_test = TaskWarriorDirect

    def test_delete_completed(self):
        task = self.tw.task_add("foobar")
        task = self.tw.task_done(uuid=task['uuid'])
        self.tw.task_delete(uuid=task['uuid'])
        tasks = self.tw.load_tasks()
        assert len(tasks['pending']) == 0
        assert len(tasks['completed']) == 1

    def should_skip(self):
        return False


class TestDBShellout(_BaseTestDB):
    class_to_test = TaskWarriorShellout

    def should_skip(self):
        """ If 'task' is not installed, we can't run these tests. """
        return not TaskWarriorShellout.can_use()

    def test_filtering_simple(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        tasks = self.tw.filter_tasks({
            'description.contains': 'foobar2',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 2

    def test_filtering_brace(self):
        self.tw.task_add("[foobar1]")
        self.tw.task_add("[foobar2]")
        tasks = self.tw.filter_tasks({
            'description.contains': '[foobar2]',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 2

    def test_filtering_quote(self):
        self.tw.task_add("[foobar1]")
        self.tw.task_add("\"foobar2\"")
        tasks = self.tw.filter_tasks({
            'description.contains': '"foobar2"',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 2

    def test_filtering_plus(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        self.tw.task_add("foobar+")
        tasks = self.tw.filter_tasks({
            'description.contains': '"foobar+"',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 3

    def test_filtering_minus(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        self.tw.task_add("foobar-")
        tasks = self.tw.filter_tasks({
            'description.contains': '"foobar-"',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 3

    def test_filtering_colon(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        self.tw.task_add("foobar:")
        tasks = self.tw.filter_tasks({
            'description.contains': 'foobar:',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 3

    def test_filtering_qmark(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foo?bar")
        tasks = self.tw.filter_tasks({
                'description.contains': 'oo?ba',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 2

    def test_filtering_qmark_not_contains(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foo?bar")
        tasks = self.tw.filter_tasks({
                'description': 'foo?bar',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 2

    def test_filtering_semicolon(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        self.tw.task_add("foo;bar")
        tasks = self.tw.filter_tasks({
            'description.contains': 'foo;bar',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 3

    def test_filtering_question_mark(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        self.tw.task_add("foo?bar")
        tasks = self.tw.filter_tasks({
            'description.contains': 'foo?bar',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 3

    def test_filtering_slash(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        self.tw.task_add("foo/bar")
        tasks = self.tw.filter_tasks({
            'description.contains': '"foo/bar"',
        })
        assert len(tasks) == 1
        assert tasks[0]['id'] == 3

    def test_filtering_logic_disjunction(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        self.tw.task_add("foobar3")
        tasks = self.tw.filter_tasks({
            'or': [
                ('description.has', 'foobar1'),
                ('description.has', 'foobar3'),
            ]
        })
        assert len(tasks) == 2
        assert tasks[0]['id'] == 1
        assert tasks[1]['id'] == 3

    def test_filtering_logic_conjunction(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        self.tw.task_add("foobar3")
        tasks = self.tw.filter_tasks({
            'and': [
                ('description.has', 'foobar1'),
                ('description.has', 'foobar3'),
            ]
        })
        assert len(tasks) == 0

    def test_filtering_logic_conjunction_junction_whats_your_function(self):
        self.tw.task_add("foobar1")
        self.tw.task_add("foobar2")
        self.tw.task_add("foobar3")
        tasks = self.tw.filter_tasks({
            'and': [
                ('description', 'foobar1'),
            ],
            'or': [
                ('status', 'pending'),
                ('status', 'waiting'),
            ]
        })
        assert len(tasks) == 1

    def test_annotation_escaping(self):
        original = {'description': 're-opening the issue'}

        self.tw.task_add('foobar')
        task = self.tw.load_tasks()['pending'][0]
        task['annotations'] = [original]
        self.tw.task_update(task)

        task = self.tw.load_tasks()['pending'][0]
        self.tw.task_update(task)

        assert len(task['annotations']) == 1
        assert task['annotations'][0]['description'] == original['description']

    def test_remove_uda_string_marshal(self):
        # Check that a string UDA is removed from a task when its
        # value is set to None
        task = self.tw_marshal.task_add(
            "foobar",
            somestring='this is a uda',
        )
        task['somestring'] = None
        id, task = self.tw_marshal.task_update(task)
        with pytest.raises(KeyError):
            task['somestring']

    def test_remove_uda_date_marshal(self):
        # Check that a date UDA is removed from a task when its
        # value is set to None
        task = self.tw_marshal.task_add(
            "foobar",
            somedate=datetime.datetime(2011, 1, 1),
        )
        task['somedate'] = None
        id, task = self.tw_marshal.task_update(task)
        with pytest.raises(KeyError):
            task['somedate']

    def test_remove_uda_numeric_marshal(self):
        # Check that a numeric UDA is removed from a task when its
        # value is set to None
        task = self.tw_marshal.task_add(
            "foobar",
            somenumber=15,
        )
        task['somenumber'] = None
        id, task = self.tw_marshal.task_update(task)
        with pytest.raises(KeyError):
            task['somenumber']

    def test_add_and_retrieve_uda_string_url(self):
        arbitrary_url = "http://www.someurl.com/1084/"

        self.tw.config_overrides['uda'] = {
            'someurl': {
                'label': 'Some URL',
                'type': 'string'
            }
        }
        self.tw.task_add(
            "foobar",
            someurl=arbitrary_url,
        )
        results = self.tw.filter_tasks({
            'someurl.is': arbitrary_url
        })
        assert len(results) == 1
        task = results[0]
        assert task['someurl'] == arbitrary_url

    def test_add_and_retrieve_uda_string_url_in_parens(self):
        arbitrary_url = "http://www.someurl.com/1084/"

        self.tw.config_overrides['uda'] = {
            'someurl': {
                'label': 'Some URL',
                'type': 'string'
            }
        }
        self.tw.task_add(
            "foobar",
            someurl=arbitrary_url,
        )
        results = self.tw.filter_tasks({
            'and': [
                ('someurl.is', arbitrary_url),
            ],
        })
        assert len(results) == 1
        task = results[0]
        assert task['someurl'] == arbitrary_url
