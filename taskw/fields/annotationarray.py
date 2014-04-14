from .array import ArrayField
from .base import DirtyableList


class AnnotationArrayField(ArrayField):
    """ A special case of the ArrayField handling idiosyncrasies of Annotations

    Taskwarrior will currently return to you a dictionary of values --
    the annotation's date and description -- for each annotation, but
    given that we cannot create annotations with a date, let's pretend
    that they aren't giving us a date.  It'll simplify things a bit.

    """
    def deserialize(self, value):
        if not value:
            value = DirtyableList([])

        elements = []
        for annotation in value:
            if isinstance(annotation, dict):
                elements.append(annotation['description'])
            else:
                elements.append(annotation)

        return super(AnnotationArrayField, self).deserialize(elements)
