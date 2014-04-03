from .string import StringField


class DurationField(StringField):
    """ In the future this will handle transforming recurrence patterns.

    See https://github.com/taskwarrior/task/blob/2.3.0/src/Duration.cpp#L41

    """
    pass
