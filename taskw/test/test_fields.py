import datetime
import sys
import uuid

from dateutil.tz import tzlocal
from pytz import UTC, timezone

from taskw import fields

if sys.version_info >= (3, ):
    from unittest import TestCase
else:
    from unittest2 import TestCase


class TestArrayField(TestCase):
    def setUp(self):
        self.field = fields.ArrayField()

    def test_serialize_none(self):
        actual_result = self.field.serialize(None)
        expected_result = []

        self.assertEqual(actual_result, expected_result)

    def test_serialize_not_ok(self):
        arbitrary_inappropriate_value = 1

        with self.assertRaises(ValueError):
            self.field.serialize(arbitrary_inappropriate_value)

    def test_serialize_ok(self):
        arbitrary_list = [1, 2, 3]

        actual_result = self.field.serialize(arbitrary_list)
        expected_result = arbitrary_list

        self.assertEqual(actual_result, expected_result)


class TestChoiceField(TestCase):
    def test_serialize_ok(self):
        field = fields.ChoiceField(
            choices=['A', 'B', 'C'],
            nullable=False,
            case_sensitive=True,
        )
        acceptable_value = 'A'

        actual_value = field.serialize(acceptable_value)
        expected_value = acceptable_value

        self.assertEqual(actual_value, expected_value)

    def test_serialize_wrong_case(self):
        field = fields.ChoiceField(
            choices=['A', 'B', 'C'],
            nullable=False,
            case_sensitive=True,
        )
        unacceptable_wrong_case = 'a'

        with self.assertRaises(ValueError):
            field.serialize(unacceptable_wrong_case)

    def test_serialize_none_unacceptable(self):
        field = fields.ChoiceField(
            choices=['A', 'B', 'C'],
            nullable=False,
            case_sensitive=True,
        )
        unacceptable_none_value = None

        with self.assertRaises(ValueError):
            field.serialize(unacceptable_none_value)

    def test_serialize_none_acceptable(self):
        field = fields.ChoiceField(
            choices=[None, 'A', 'B', 'C'],
            case_sensitive=True,
        )
        acceptable_none_value = None

        actual_value = field.serialize(acceptable_none_value)
        expected_value = acceptable_none_value

        self.assertEqual(actual_value, expected_value)

    def test_serialize_case_insensitive(self):
        field = fields.ChoiceField(
            choices=['A', 'B', 'C'],
            nullable=False,
            case_sensitive=False,
        )
        value_wrong_case = 'a'

        actual_value = field.serialize(value_wrong_case)
        expected_value = value_wrong_case

        self.assertEqual(actual_value, expected_value)


class TestCommaSeparatedUUIDField(TestCase):
    def setUp(self):
        self.field = fields.CommaSeparatedUUIDField()

    def test_serialize_single_uuid(self):
        single_uuid = [uuid.uuid4()]

        actual_value = self.field.serialize(single_uuid)
        expected_value = str(single_uuid[0])

        self.assertEqual(actual_value, expected_value)

    def test_serialize_mulitple_values(self):
        many_uuids = [
            uuid.uuid4(),
            uuid.uuid4(),
            uuid.uuid4(),
        ]

        actual_value = self.field.serialize(many_uuids)
        expected_value = ','.join([str(u) for u in many_uuids])

        self.assertEqual(actual_value, expected_value)

    def test_deserialize_uuid_string(self):
        arbitrary_uuids = [uuid.uuid4(), uuid.uuid4()]
        uuid_strings = ','.join([str(u) for u in arbitrary_uuids])

        actual_value = self.field.deserialize(uuid_strings)
        expected_value = arbitrary_uuids

        self.assertEqual(actual_value, expected_value)

    def test_deserialize_uuid_string_undashed(self):
        arbitrary_uuids = [uuid.uuid4(), uuid.uuid4()]
        uuid_strings = ','.join([u.hex for u in arbitrary_uuids])

        actual_value = self.field.deserialize(uuid_strings)
        expected_value = arbitrary_uuids

        self.assertEqual(actual_value, expected_value)


class TestDateField(TestCase):
    def setUp(self):
        self.field = fields.DateField()

    def test_deserialize_none(self):
        actual_value = self.field.deserialize(None)
        expected_value = None

        self.assertEqual(actual_value, expected_value)

    def test_deserialize_naive(self):
        arbitrary_year = 2014
        arbitrary_month = 3
        arbitrary_day = 2
        arbitrary_hour = 9
        arbitrary_minute = 10
        arbitrary_second = 3

        naive_date_string = (
            '{year}-{month}-{day}T{hour}:{minute}:{second}'.format(
                year=arbitrary_year,
                month=arbitrary_month,
                day=arbitrary_day,
                hour=arbitrary_hour,
                minute=arbitrary_minute,
                second=arbitrary_second,
            )
        )

        actual_value = self.field.deserialize(naive_date_string)
        expected_value = datetime.datetime(
            arbitrary_year,
            arbitrary_month,
            arbitrary_day,
            arbitrary_hour,
            arbitrary_minute,
            arbitrary_second,
            tzinfo=UTC
        )

        self.assertEqual(actual_value, expected_value)

    def test_deserialize_nonnaive(self):
        arbitrary_year = 2014
        arbitrary_month = 3
        arbitrary_day = 2
        arbitrary_hour = 9
        arbitrary_minute = 10
        arbitrary_second = 3

        nonnaive_date_string = (
            '{year}-{month}-{day}T{hour}:{minute}:{second}Z'.format(
                year=arbitrary_year,
                month=arbitrary_month,
                day=arbitrary_day,
                hour=arbitrary_hour,
                minute=arbitrary_minute,
                second=arbitrary_second,
            )
        )

        actual_value = self.field.deserialize(nonnaive_date_string)
        expected_value = datetime.datetime(
            arbitrary_year,
            arbitrary_month,
            arbitrary_day,
            arbitrary_hour,
            arbitrary_minute,
            arbitrary_second,
            tzinfo=UTC
        )

        self.assertEqual(actual_value, expected_value)

    def test_serialize_none(self):
        actual_value = self.field.serialize(None)
        expected_value = None

        self.assertEqual(actual_value, expected_value)

    def test_serialize_naive(self):
        arbitrary_year = 2014
        arbitrary_month = 3
        arbitrary_day = 2
        arbitrary_hour = 9
        arbitrary_minute = 10
        arbitrary_second = 3

        arbitrary_date = datetime.datetime(
            arbitrary_year,
            arbitrary_month,
            arbitrary_day,
            arbitrary_hour,
            arbitrary_minute,
            arbitrary_second,
        )

        actual_value = self.field.serialize(arbitrary_date)
        expected_value = UTC.normalize(
            arbitrary_date.replace(tzinfo=tzlocal())
        ).strftime('%Y%m%dT%H%M%SZ')

        self.assertEqual(actual_value, expected_value)

    def test_serialize_nonnaive(self):
        arbitrary_year = 2014
        arbitrary_month = 3
        arbitrary_day = 2
        arbitrary_hour = 9
        arbitrary_minute = 10
        arbitrary_second = 3

        arbitrary_date = datetime.datetime(
            arbitrary_year,
            arbitrary_month,
            arbitrary_day,
            arbitrary_hour,
            arbitrary_minute,
            arbitrary_second,
            tzinfo=timezone('America/Los_Angeles')
        )

        actual_value = self.field.serialize(arbitrary_date)
        expected_value = UTC.normalize(
            arbitrary_date
        ).strftime('%Y%m%dT%H%M%SZ')

        self.assertEqual(actual_value, expected_value)


class TestNumericField(TestCase):
    def setUp(self):
        self.field = fields.NumericField()

    def test_numeric_value(self):
        arbitrary_numeric_value = 10

        actual_value = self.field.serialize(arbitrary_numeric_value)
        expected_value = arbitrary_numeric_value

        self.assertEqual(actual_value, expected_value)

    def test_nonnumeric_value(self):
        arbitrary_nonnumeric_value = 'alpha'

        with self.assertRaises(ValueError):
            self.field.serialize(arbitrary_nonnumeric_value)


class TestStringField(TestCase):
    def setUp(self):
        self.field = fields.StringField()

    def test_deserialize_string(self):
        serialized_string = '&open;hello&close;'

        actual_value = self.field.deserialize(serialized_string)
        expected_value = '[hello]'

        self.assertEqual(actual_value, expected_value)

    def test_serialize_string(self):
        unserialized_string = '[hello]'

        actual_value = self.field.serialize(unserialized_string)
        expected_value = '&open;hello&close;'

        self.assertEqual(actual_value, expected_value)


class TestUUIDField(TestCase):
    def setUp(self):
        self.field = fields.UUIDField()

    def test_serialize(self):
        arbitrary_uuid = uuid.uuid4()

        actual_result = self.field.serialize(arbitrary_uuid)
        expected_result = str(arbitrary_uuid)

        self.assertEqual(actual_result, expected_result)

    def test_deserialize_dashed(self):
        arbitrary_uuid = uuid.uuid4()
        dashed_uuid = str(arbitrary_uuid)

        actual_result = self.field.deserialize(dashed_uuid)
        expected_result = arbitrary_uuid

        self.assertEqual(actual_result, expected_result)

    def test_deserialize_undashed(self):
        arbitrary_uuid = uuid.uuid4()
        dashed_uuid = arbitrary_uuid.hex

        actual_result = self.field.deserialize(dashed_uuid)
        expected_result = arbitrary_uuid

        self.assertEqual(actual_result, expected_result)
