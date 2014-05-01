import copy
import sys

import six


class Field(object):
    def __init__(self, label=None, read_only=False):
        self._label = label
        self._read_only = read_only
        super(Field, self).__init__()

    @property
    def read_only(self):
        return self._read_only

    @property
    def label(self):
        return self._label

    def deserialize(self, value):
        return value

    def serialize(self, value):
        return value

    def __str__(self):
        if sys.version_info >= (3, ):
            return self.label
        return self.__unicode__().encode(sys.getdefaultencoding(), 'replace')

    def __unicode__(self):
        return self.label

    def __repr__(self):
        return "<{cls} '{label}'>".format(
            cls=six.text_type(self.__class__.__name__),
            label=six.text_type(self) if self._label else '(No Label)',
        )

    def __eq__(self, other):
        if self.label != other.label:
            return False
        if self.read_only != other.read_only:
            return False
        if self.__class__ != other.__class__:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class Dirtyable(object):
    """ Superclass for all objects implementing trackability."""

    def __init__(self, value=None):
        self._original_value = copy.deepcopy(value)
        super(Dirtyable, self).__init__(value)

    def get_changes(self, keep=False):
        if self._original_value == self:
            return {}
        result = (self._original_value, self)
        if not keep:
            self._original_value = copy.deepcopy(self)
        return result


class DirtyableList(Dirtyable, list):
    pass


class DirtyableDict(Dirtyable, list):
    pass
