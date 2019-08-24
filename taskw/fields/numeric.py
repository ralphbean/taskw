import numbers

from .base import Field


class NumericField(Field):
    def serialize(self, value):
        if not isinstance(value, numbers.Number):
            if value:
                raise ValueError("Value must be numeric.")
        return value

    def deserialize(self, value):
        if value is None:
            return value
        elif isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                pass
            try:
                return float(value)
            except ValueError:
                pass
        elif isinstance(value, int) or isinstance(value, float):
            # already desialized
            return value
        else:
            raise ValueError("Unhandled type [{}] passed during deserialization for value [{}]"
                             .format(type(value), value))

        # If we've made it this far, somehow Taskwarrior has
        # a non-numeric value stored in this field; this shouldn't
        # happen, but it's probably inappropriate to blow up.
        return value
