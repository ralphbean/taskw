import logging

import six

from taskw.fields import (
    AnnotationArrayField,
    ArrayField,
    ChoiceField,
    CommaSeparatedUUIDField,
    DateField,
    DurationField,
    Field,
    NumericField,
    StringField,
    UUIDField,
)
from taskw.fields.base import Dirtyable, DirtyableList, DirtyableDict

# Sentinel value for not specifying a default
UNSPECIFIED = object()


logger = logging.getLogger(__name__)


class Task(dict):
    FIELDS = {
        'annotations': AnnotationArrayField(label='Annotations'),
        'depends': CommaSeparatedUUIDField(label='Depends Upon'),
        'description': StringField(label='Description'),
        'due': DateField(label='Due'),
        'end': DateField(label='Ended'),
        'entry': DateField(label='Entered'),
        'id': NumericField(label='ID', read_only=True),
        'imask': NumericField(label='Imask', read_only=True),
        'mask': StringField(label='Mask', read_only=True),
        'modified': DateField(label='Modified'),
        'parent': StringField(label='Parent'),
        'priority': ChoiceField(
            choices=[None, 'H', 'M', 'L', ],
            case_sensitive=False,
            label='Priority'
        ),
        'project': StringField(label='Project'),
        'recur': DurationField(label='Recurrence'),
        'scheduled': DateField(label='Scheduled'),
        'start': DateField(label='Started'),
        'status': ChoiceField(
            choices=[
                'pending',
                'completed',
                'deleted',
                'waiting',
                'recurring',
            ],
            case_sensitive=False,
            label='Status',
        ),
        'tags': ArrayField(label='Tags'),
        'until': DateField(label='Until'),
        'urgency': NumericField(label='Urgency', read_only=True),
        'uuid': UUIDField(label='UUID'),
        'wait': DateField(label='Wait'),
    }

    def __init__(self, data, udas=None):
        self._fields = self.FIELDS.copy()
        if udas:
            self._fields.update(udas)
        self._changes = []

        processed = {}
        for k, v in six.iteritems(data):
            processed[k] = self._deserialize(k, v)

        super(Task, self).__init__(processed)

    def _get_converter_for_field(self, field, default=None):
        converter = self._fields.get(field, None)
        if not converter:
            return default if default else Field()
        return converter

    def _deserialize(self, key, value):
        """ Marshal incoming data into Python objects."""
        converter = self._get_converter_for_field(key)
        return converter.deserialize(value)

    def _serialize(self, key, value):
        """ Marshal outgoing data into Taskwarrior's JSON format."""
        converter = self._get_converter_for_field(key)
        return converter.serialize(value)

    def _field_is_writable(self, key):
        converter = self._get_converter_for_field(key)
        if converter.read_only:
            return False
        return True

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def _record_change(self, key, from_, to):
        self._changes.append((key, from_, to))

    def get_changes(self, serialized=False, keep=False):
        """ Get a journal of changes that have occurred

        :param `serialized`:
            Return changes in the serialized format used by TaskWarrior.
        :param `keep_changes`:
            By default, the list of changes is reset after running
            ``.get_changes``; set this to `True` if you would like to
            keep the changes recorded following running this command.

        :returns: A dictionary of 2-tuples of changes, where the key is the
            name of the field that has changed, and the value is a 2-tuple
            containing the original value and the final value respectively.

        """
        results = {}

        # Check for explicitly-registered changes
        for k, f, t in self._changes:
            if k not in results:
                results[k] = [f, None]
            results[k][1] = self._serialize(k, t) if serialized else t

        # Check for changes on subordinate items
        for k, v in six.iteritems(self):
            if isinstance(v, Dirtyable):
                result = v.get_changes(keep=keep)
                if result:
                    if not k in results:
                        results[k] = [result[0], None]
                    results[k][1] = (
                        self._serialize(k, result[1])
                        if serialized else result[1]
                    )

        # Clear out recorded changes
        if not keep:
            self._changes = []

        return results

    def update(self, values, force=False):
        """ Update this task dictionary

        :returns: A dictionary mapping field names specified to be updated
            and a boolean value indicating whether the field was changed.

        """
        results = {}
        for k, v in six.iteritems(values):
            results[k] = self.__setitem__(k, v, force=force)
        return results

    def set(self, key, value):
        """ Set a key's value regardless of whether a change is seen."""
        return self.__setitem__(key, value, force=True)

    def serialized(self):
        """ Returns a serialized representation of this task."""
        serialized = {}
        for k, v in six.iteritems(self):
            serialized[k] = self._serialize(k, v)
        return serialized

    def serialized_changes(self, keep=False):
        serialized = {}
        for k, v in six.iteritems(self.get_changes(keep=keep)):
            # Here, `v` is a 2-tuple of the field's original value
            # and the field's new value.
            _, to = v
            serialized[k] = self._serialize(k, to)
        return serialized

    def __setitem__(self, key, value, force=False):
        if isinstance(value, dict) and not isinstance(value, DirtyableDict):
            value = DirtyableDict(value)
        elif isinstance(value, list) and not isinstance(value, DirtyableList):
            value = DirtyableList(value)

        existing_value = self.get(key)
        if force or value != existing_value:
            if force or existing_value or value:
                # Do not attempt to record changes if both the existing
                # and previous values are Falsy.  We cannot distinguish
                # between `''` and `None` for...reasons.
                self._record_change(
                    key,
                    self.get(key),
                    value,
                )

            # Serialize just to make sure we can; it's better to throw
            # this error early.
            self._serialize(key, value)

            # Also make sure we raise an error if this field isn't
            # writable at all.
            if not self._field_is_writable(key):
                raise ValueError("%s is a read-only field", key)

            super(Task, self).__setitem__(key, value)
            return True
        return False
