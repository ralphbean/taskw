import os
import multiprocessing
import sys
from setuptools import setup, find_packages
import uuid

f = open('README.rst')
long_description = f.read().strip()
long_description = long_description.split('split here', 1)[1]
f.close()

REQUIREMENTS_FILES = {
    'test': 'test_requirements.txt',
    'install': 'requirements.txt',
}
REQUIREMENTS = {}
for category, filename in REQUIREMENTS_FILES.items():
    requirements_path = os.path.join(
        os.path.dirname(__file__),
        filename
    )
    try:
        from pip.req import parse_requirements
        requirements = [
            str(req.req) for req in parse_requirements(
                requirements_path,
                session=uuid.uuid1()
            )
        ]
    except ImportError:
        requirements = []
        with open(requirements_path, 'r') as in_:
            requirements = [
                req for req in in_.readlines()
                if not req.startswith('-')
                and not req.startswith('#')
            ]
    REQUIREMENTS[category] = requirements

if sys.version_info < (2, 7):
    REQUIREMENTS['test'].append('unittest2')
    REQUIREMENTS['install'].append('ordereddict')

setup(name='taskw',
      version='1.0.0',
      description="Python bindings for your taskwarrior database",
      long_description=long_description,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Intended Audience :: Developers",
      ],
      keywords='taskwarrior task',
      author='Ralph Bean',
      author_email='ralph.bean@gmail.com',
      url='http://github.com/ralphbean/taskw',
      license='GPLv3+',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS['install'],
      test_suite='nose.collector',
      tests_require=REQUIREMENTS['test'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
