import copy
import datetime
import io
import uuid
from unittest import TestCase

import pytz
from dateutil.tz import tzutc

from taskw.task import Task


class TestTaskDirtyability(TestCase):
    def setUp(self):
        self.task = Task({
            'uuid': str(uuid.uuid4()),
            'description': 'Something important',
            'due': (
                datetime.datetime.now().replace(tzinfo=pytz.UTC)
                + datetime.timedelta(hours=1)
            ).strftime('%Y%m%dT%H%M%SZ'),
            'tags': ['one', 'two', 'three'],
        })

    def test_append_when_absent(self):
        self.task['annotations'] = []
        self.task['annotations'].append('awesome')
        self.assertEqual(self.task['annotations'], ['awesome'])

    def test_append_when_absent_but_with_tags(self):
        self.task = Task({'uuid': str(uuid.uuid4()), 'description': 'Test'})
        self.task['tags'] = []
        self.task['tags'].append('awesome')
        self.assertEqual(self.task['tags'], ['awesome'])

    def test_marks_date_changed(self):
        original_due_date = self.task['due']
        new_due_date = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        self.task['due'] = new_due_date

        expected_changes = {'due': (original_due_date, new_due_date)}
        actual_changes = self.task.get_changes()

        self.assertEqual(list(actual_changes.keys()), ['due'])

        # Use assertAlmostEqual to allow for millisecond loss when
        # converting to string in setUp
        self.assertAlmostEqual(
            expected_changes['due'][0],
            actual_changes['due'][0],
            delta=datetime.timedelta(seconds=1)
        )
        self.assertAlmostEqual(
            expected_changes['due'][1],
            actual_changes['due'][1],
            delta=datetime.timedelta(seconds=1)
        )

    def test_marks_tags_changed(self):
        original_tags = copy.deepcopy(self.task['tags'])
        new_tag = 'alpha'
        self.task['tags'].append(new_tag)

        expected_tags = copy.deepcopy(original_tags)
        expected_tags.append(new_tag)

        expected_changes = {'tags': [original_tags, expected_tags]}
        actual_changes = self.task.get_changes()

        self.assertEqual(actual_changes, expected_changes)

    def test_does_not_mark_unchanged(self):
        self.task['description'] = self.task['description']

        expected_changes = {}
        actual_changes = self.task.get_changes()

        self.assertEqual(actual_changes, expected_changes)

    def test_does_not_allow_changing_id(self):
        with self.assertRaises(ValueError):
            self.task['id'] = 10


class TestTaskMarshalling(TestCase):
    def test_serialize(self):
        arbitrary_serialized_data = {
            'depends': ','.join([
                str(uuid.uuid4()),
                str(uuid.uuid4()),
            ]),
            'description': '&open;Something important',
            'due': (
                datetime.datetime.now().replace(tzinfo=pytz.UTC)
                + datetime.timedelta(hours=1)
            ).strftime('%Y%m%dT%H%M%SZ'),
            'tags': ['one', 'two', 'three'],
            'urgency': 10,
            'uuid': str(uuid.uuid4()),
        }
        task = Task(arbitrary_serialized_data)
        expected_result = arbitrary_serialized_data
        actual_result = task.serialized()

        self.assertEqual(actual_result, expected_result)

    def test_deserialize(self):
        arbitrary_depends_uuids = [uuid.uuid4(), uuid.uuid4()]
        arbitrary_description = '[one'
        arbitrary_due_date = (
            datetime.datetime.now().replace(tzinfo=pytz.UTC)
            + datetime.timedelta(hours=1)
        )
        arbitrary_tags = ['one', 'two', ]
        arbitrary_urgency = 10
        arbitrary_uuid = uuid.uuid4()

        serialized = {
            'depends': ','.join([str(u) for u in arbitrary_depends_uuids]),
            'description': arbitrary_description.replace('[', '&open;'),
            'due': arbitrary_due_date.strftime('%Y%m%dT%H%M%SZ'),
            'tags': arbitrary_tags,
            'urgency': arbitrary_urgency,
            'uuid': str(arbitrary_uuid)
        }
        task = Task(serialized)

        self.assertEqual(task['depends'], arbitrary_depends_uuids)
        self.assertEqual(task['description'], arbitrary_description)
        # Loss of milliseconds when converting to string
        self.assertAlmostEqual(
            task['due'],
            arbitrary_due_date,
            delta=datetime.timedelta(seconds=1)
        )
        self.assertEqual(task['tags'], arbitrary_tags)
        self.assertEqual(task['urgency'], arbitrary_urgency)
        self.assertEqual(task['uuid'], arbitrary_uuid)

    def test_composition(self):
        arbitrary_serialized_data = {
            'depends': ','.join([
                str(uuid.uuid4()),
                str(uuid.uuid4()),
            ]),
            'description': '&open;Something important',
            'due': (
                datetime.datetime.now().replace(tzinfo=pytz.UTC)
                + datetime.timedelta(hours=1)
            ).strftime('%Y%m%dT%H%M%SZ'),
            'tags': ['one', 'two', 'three'],
            'urgency': 10,
            'uuid': str(uuid.uuid4()),
        }
        expected_result = arbitrary_serialized_data

        after_composition = Task(
            Task(
                Task(
                    arbitrary_serialized_data
                ).serialized()
            ).serialized()
        ).serialized()

        self.assertEqual(after_composition, expected_result)

    def test_from_input(self):
        input_add_data = io.StringIO(
            '{'
            '"description":"Go to Camelot",'
            '"entry":"20180618T030242Z",'
            '"status":"pending",'
            '"start":"20181012T110605Z",'
            '"uuid":"daa3ff05-f716-482e-bc35-3e1601e50778"'
            '}')

        input_modify_data = io.StringIO(
            '\n'.join([
                input_add_data.getvalue(),
                (
                    '{'
                    '"description":"Go to Camelot again",'
                    '"entry":"20180618T030242Z",'
                    '"status":"pending",'
                    '"start":"20181012T110605Z",'
                    '"uuid":"daa3ff05-f716-482e-bc35-3e1601e50778"'
                    '}'
                ),
            ]),
        )

        on_add_task = Task.from_input(input_file=input_add_data)
        assert on_add_task.get('description') == "Go to Camelot"
        assert on_add_task.get('entry') == datetime.datetime(2018, 6, 18, 3, 2, 42, tzinfo=tzutc())
        assert on_add_task.get('status') == "pending"
        assert on_add_task.get('start') == datetime.datetime(2018, 10, 12, 11, 6, 5, tzinfo=tzutc())
        assert on_add_task.get('uuid') == uuid.UUID("daa3ff05-f716-482e-bc35-3e1601e50778")

        on_modify_task = Task.from_input(input_file=input_modify_data, modify=True)
        assert on_modify_task.get('description') == "Go to Camelot again"
        assert on_modify_task.get('entry') == datetime.datetime(2018, 6, 18, 3, 2, 42, tzinfo=tzutc())
        assert on_modify_task.get('status') == "pending"
        assert on_modify_task.get('start') == datetime.datetime(2018, 10, 12, 11, 6, 5, tzinfo=tzutc())
        assert on_modify_task.get('uuid') == uuid.UUID("daa3ff05-f716-482e-bc35-3e1601e50778")
