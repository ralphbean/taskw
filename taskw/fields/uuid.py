from __future__ import absolute_import

import uuid

from .base import Field


class UUIDField(Field):
    def deserialize(self, value):
        if not value:
            return value
        return uuid.UUID(value)

    def serialize(self, value):
        if isinstance(value, uuid.UUID):
            value = str(value)
        else:
            # Just to make sure it's a UUID
            uuid.UUID(value)
        return value
