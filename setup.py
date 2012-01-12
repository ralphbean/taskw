from setuptools import setup, find_packages

version = '0.2.0'

f = open('README.rst')
long_description = f.read().strip()
long_description = long_description.split('split here', 1)[1]
f.close()

setup(name='taskw',
      version=version,
      description="Python bindings for your taskwarrior database",
      long_description=long_description,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python :: 2",
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
      install_requires=[],
      test_suite='unittest2.collector',
      tests_require=['unittest2'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
