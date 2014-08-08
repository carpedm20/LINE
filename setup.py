# -*- coding: utf-8 -*-
"""
Line -- May the LINE be with you...
=========================================

If you're reading this code, you should know what LINE is.

Just play. Have fun. Enjoy the LINE!
```````````````````````````

::

    >>> from line import Client

Links
`````

* `GitHub repository <http://github.com/carpedm20/line>`_
* `development version
  <http://github.com/carpedm20/line/zipball/master>`_


"""
from __future__ import with_statement
import re

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

# detect the current version
with open('line/__init__.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+?)\'', f.read()).group(1)
assert version

setup(
    name='line',
    packages=['line'],
    version=version,
    description='May the LINE be with you...',
    long_description=open('README.rst').read(),
    license='BSD License',
    author='Taehoon Kim',
    author_email='carpedm20@gmail.com',
    url='http://carpedm20.github.io/line',
    keywords=['line'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Communications :: Chat',
    ],
    install_requires=[
        'requests',
        'curve',
        'rsa'
    ],
)
