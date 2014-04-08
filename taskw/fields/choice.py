from .base import Field


class ChoiceField(Field):
    def __init__(
        self,
        choices=None,
        nullable=False,
        case_sensitive=False,
        **kwargs
    ):
        self._choices = choices if choices else []
        self._case_sensitive = case_sensitive
        super(ChoiceField, self).__init__(**kwargs)

    def is_valid_choice(self, value):
        if value is None and value not in self._choices:
            return False
        if value is None and value in self._choices:
            return True
        if self._case_sensitive and value in self._choices:
            return True
        elif (
            not self._case_sensitive
            and value.upper() in [v.upper() for v in self._choices if v]
        ):
            return True
        elif self._case_sensitive and value in self._choices:
            return True
        return False

    def serialize(self, value):
        if not self.is_valid_choice(value):
            raise ValueError(
                "'%s' is not a valid choice; choices: %s" % (
                    value,
                    self._choices,
                )
            )
        return value
