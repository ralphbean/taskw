import logging

from taskw.utils import encode_replacements_experimental
from .base import Field


logger = logging.getLogger(__name__)


class StringField(Field):
    def deserialize(self, value):
        # If value is None, let's just let it pass through
        if not value:
            return value
        if not isinstance(value, str):
            value = str(value)
        for left, right in encode_replacements_experimental.items():
            value = value.replace(right, left)
        return value

    def serialize(self, value):
        # If value is None let it pass through
        if not value:
            return value
        if not isinstance(value, str):
            string_value = str(value)
            logger.debug(
                "Value %s serialized to string as '%s'",
                repr(value),
                string_value
            )
            value = string_value
        for left, right in encode_replacements_experimental.items():
            value = value.replace(left, right)
        return value
