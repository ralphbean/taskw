from .base import DirtyableList, Field


class ArrayField(Field):
    def deserialize(self, value):
        if not value:
            value = DirtyableList([])
        return DirtyableList(value)

    def serialize(self, value):
        if not value:
            value = []
        if not hasattr(value, '__iter__'):
            raise ValueError("Value must be list or tuple.")
        return value
