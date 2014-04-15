import sys

from dateutil.parser import parse
import six

from .array import ArrayField
from .base import DirtyableList


class Annotation(object):
    """ A special type of string that we'll use for storing annotations.

    This is, for all intents and purposes, really just a string, but
    it does allow us to store additional information if we have it -- in
    this application: the annotation's entry date.

    """
    def __init__(self, description, entry=None):
        self._description = description
        self._entry = entry
        super(Annotation, self).__init__()

    @property
    def entry(self):
        if self._entry:
            return parse(self._entry)
        return self._entry

    def __str__(self):
        if six.PY3:
            return six.text_type(self._description)
        return self.__unicode__().encode(sys.getdefaultencoding())

    def __eq__(self, other):
        value = other
        if isinstance(other, Annotation):
            value = other._description
        return self._description == value

    def __ne__(self, other):
        value = other
        if isinstance(other, Annotation):
            value = other._description
        return self._description != value

    def __unicode__(self):
        return six.text_type(self._description)

    def __repr__(self):
        return repr(six.text_type(self._description))


class AnnotationArrayField(ArrayField):
    """ A special case of the ArrayField handling idiosyncrasies of Annotations

    Taskwarrior will currently return to you a dictionary of values --
    the annotation's date and description -- for each annotation, but
    given that we cannot create annotations with a date, let's instead
    return something that behaves like a string (but from which you can
    extract an entry date if one exists).

    """
    def deserialize(self, value):
        if not value:
            value = DirtyableList([])

        elements = []
        for annotation in value:
            if isinstance(annotation, dict):
                elements.append(
                    Annotation(
                        annotation['description'],
                        annotation['entry'],
                    )
                )
            else:
                elements.append(Annotation(annotation))

        return super(AnnotationArrayField, self).deserialize(elements)

    def serialize(self, value):
        if not value:
            value = []
        return super(AnnotationArrayField, self).serialize(
            [six.text_type(entry) for entry in value]
        )
