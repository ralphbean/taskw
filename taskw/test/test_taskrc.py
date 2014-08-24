import os
import sys

from taskw.taskrc import TaskRc
from taskw.fields import NumericField, ChoiceField


if sys.version_info >= (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase


class TestTaskRc(TestCase):
    def setUp(self):
        self.path_to_taskrc = os.path.join(
            os.path.dirname(__file__),
            'data/default.taskrc',
        )
        self.taskrc = TaskRc(self.path_to_taskrc)

    def test_taskrc_parsing(self):
        expected_config = {
            'data': {
                'location': '~/.task'
            },
            'alpha': {
                'one': 'yes',
                'two': '2',
            },
            'beta': {
                'one': 'FALSE',
            },
            'gamma': {
                'one': 'TRUE',
            },
            'uda': {
                'a': {
                    'type': 'numeric',
                    'label': 'Alpha',
                },
                'b': {
                    'type': 'string',
                    'label': 'Beta',
                    'values': 'Strontium-90,Hydrogen-3',
                }
            }
        }

        self.assertEqual(self.taskrc, expected_config)

    def test_get_udas(self):
        expected_udas = {
            'a': NumericField(label='Alpha'),
            'b': ChoiceField(
                label='Beta',
                choices=['Strontium-90', 'Hydrogen-3'],
            ),
        }
        actual_udas = self.taskrc.get_udas()

        self.assertEqual(actual_udas, expected_udas)

    def test_config_overrides(self):
        overrides = {
            'uda': {
                'd': {
                    'type': 'string',
                    'label': 'Delta',
                }
            },
            'alpha': {
                'two': '3',
            }
        }

        taskrc = TaskRc(self.path_to_taskrc, overrides=overrides)

        expected_config = {
            'data': {
                'location': '~/.task'
            },
            'alpha': {
                'one': 'yes',
                'two': '3',
            },
            'beta': {
                'one': 'FALSE',
            },
            'gamma': {
                'one': 'TRUE',
            },
            'uda': {
                'a': {
                    'type': 'numeric',
                    'label': 'Alpha',
                },
                'b': {
                    'type': 'string',
                    'label': 'Beta',
                    'values': 'Strontium-90,Hydrogen-3',
                },
                'd': {
                    'type': 'string',
                    'label': 'Delta',
                }
            }
        }

        self.assertEqual(taskrc, expected_config)
