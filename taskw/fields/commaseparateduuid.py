from __future__ import absolute_import

import uuid

from .base import DirtyableList, Field


class CommaSeparatedUUIDField(Field):
    def deserialize(self, value):
        if not value:
            return DirtyableList([])
        return DirtyableList([uuid.UUID(v) for v in value.split(',')])

    def serialize(self, value):
        if not value:
            value = []
        if not hasattr(value, '__iter__'):
            raise ValueError("Value must be list or tuple.")
        return ','.join([str(v) for v in value])
