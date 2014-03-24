import numbers

from .base import Field


class NumericField(Field):
    def serialize(self, value):
        if not isinstance(value, numbers.Number):
            raise ValueError("Value must be numeric.")
        return value
