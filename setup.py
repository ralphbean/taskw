import multiprocessing
import logging
import sys
from setuptools import setup, find_packages

version = '0.8.4'

f = open('README.rst')
long_description = f.read().strip()
long_description = long_description.split('split here', 1)[1]
f.close()

install_requires = [
    "six",
    "python-dateutil",
    "pytz",
]
tests_require = [
    'nose',
]

if sys.version_info < (3, ):
    tests_require.append('unittest2')

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    install_requires.extend([
        'ordereddict',
    ])

setup(name='taskw',
      version=version,
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
      install_requires=install_requires,
      test_suite='nose.collector',
      tests_require=tests_require,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
