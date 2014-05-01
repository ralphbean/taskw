import logging

import six

from taskw.utils import encode_replacements_experimental
from .base import Field


logger = logging.getLogger(__name__)


class StringField(Field):
    def deserialize(self, value):
        # If value is None, let's just let it pass through
        if not value:
            return value
        if not isinstance(value, six.string_types):
            value = six.text_type(value)
        for left, right in six.iteritems(encode_replacements_experimental):
            value = value.replace(right, left)
        return value

    def serialize(self, value):
        if not isinstance(value, six.string_types):
            string_value = six.text_type(value)
            logger.warning(
                "Value %s serialized to string as '%s'",
                repr(value),
                string_value
            )
            value = string_value
        for left, right in six.iteritems(encode_replacements_experimental):
            value = value.replace(left, right)
        return value
