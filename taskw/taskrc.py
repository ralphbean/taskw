import logging
import os
import re

from taskw.fields import (
    DateField,
    DurationField,
    NumericField,
    StringField
)


logger = logging.getLogger(__name__)


def sanitize(line):
    comment_position = line.find('#')
    if comment_position < 0:
        return line.strip()
    return line[:comment_position].strip()


class TaskRc(dict):
    UDA_TYPE_MAP = {
        'date': DateField,
        'duration': DurationField,
        'numeric': NumericField,
        'string': StringField,
    }

    def __init__(self, path=None):
        if path:
            self.path = os.path.normpath(
                os.path.expanduser(
                    path
                )
            )
            config = self._read(self.path)
        else:
            self.path = None
            config = {}
        config['data'] = {
            'location': self.path
        }
        super(TaskRc, self).__init__(config)

    def _read(self, path):
        config = {}
        with open(path, 'r') as config_file:
            for raw_line in config_file.readlines():
                line = sanitize(raw_line)
                if not line:
                    continue
                if line.startswith('include '):
                    try:
                        left, right = line.split(' ')
                        config.update(TaskRc(right.strip()))
                    except ValueError:
                        logger.exception(
                            "Error encountered while adding TaskRc at "
                            "'%s' (from TaskRc file at '%s')",
                            right.strip(),
                            self.path
                        )
                else:
                    try:
                        left, right = line.split('=')
                        key = left.strip()
                        value = right.strip()
                        config[key] = value
                    except ValueError:
                        logger.exception(
                            "Error encountered while processing configuration "
                            "setting '%s' (from TaskRc file at '%s')",
                            line,
                            self.path,
                        )
        return config

    def __delitem__(self, *args):
        raise TypeError('TaskRc objects are immutable')

    def __setitem__(self, item, value):
        raise TypeError('TaskRc objects are immutable')

    def update(self, value):
        raise TypeError('TaskRc objects are immutable')

    def _get_uda_data(self):
        raw_udas = {}

        uda_type = re.compile('^uda\.([^.]+)\.(type)$')
        uda_label = re.compile('^uda\.([^.]+)\.(label)$')
        uda_values = re.compile('^uda\.([^.]+)\.(values)$')
        for k, v in self.items():
            for matcher in (uda_type, uda_label, uda_values):
                matches = matcher.match(k)
                if matches:
                    if matches.group(1) not in raw_udas:
                        raw_udas[matches.group(1)] = {}
                    raw_udas[matches.group(1)][matches.group(2)] = v

        return raw_udas

    def get_udas(self):
        udas = {}

        for k, v in self._get_uda_data().items():
            tw_type = v.get('type', '')
            label = v.get('label', None)
            choices = v.get('values', None)

            kwargs = {}
            cls = self.UDA_TYPE_MAP.get(tw_type, StringField)

            if choices and cls == StringField:
                kwargs['choices'] = choices.split(',')
            if label:
                kwargs['label'] = label

            udas[k] = cls(**kwargs)

        return udas

    def add_include(self, item):
        if item not in self.includes:
            self.includes.append(item)
        self._write()

    def __unicode__(self):
        return 'TaskRc file at {path}'.format(
            path=self.path
        )

    def __str__(self):
        return self.__unicode__().encode('utf-8', 'REPLACE')
