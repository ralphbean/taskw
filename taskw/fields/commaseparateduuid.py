from distutils.version import LooseVersion

import uuid

from .base import DirtyableList, Field


class CommaSeparatedUUIDField(Field):
    version = LooseVersion('2.4')

    def deserialize(self, value):
        if not value:
            return DirtyableList([])

        # In task-2.5, this moved from a comma-separated string to a real list.
        # here we allow a migration path where old splitable strings are
        # handled as well as newschool lists.
        if hasattr(value, 'split'):
            value = value.split(',')

        return DirtyableList([uuid.UUID(v) for v in value])

    def serialize(self, value):
        if not value:
            value = []

        if not hasattr(value, '__iter__'):
            raise ValueError("Value must be list or tuple, not %r." % value)

        if self.version < LooseVersion('2.5'):
            return ','.join([str(v) for v in value])
        else:
            # We never hit this second code branch now.  taskwarrior changed
            # API slightly in version 2.5, but we're just going to go with
            # backwards compatibility for now.
            # Some day we should switch wholesale to the new path.
            return [str(v) for v in value]
