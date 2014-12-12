#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

__version__ = '0.2.0'
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


install_requires = [
    'Flask==0.10.1',
    'requests==2.2.1',
    'sarge==0.1.3',
    'beautifulsoup4==4.3.2',
    'gevent>=1.0'
]
tests_require = ['pytest==2.5.1', 'pytest-cov==1.6']
develop_require = tests_require + [
    'Sphinx>=1.2.1', 'pylint>=1.1.0'
]

setup(
    name='debot',
    version=__version__,
    description='',
    long_description=readme + '\n\n' + history,
    author='Harry Liang',
    author_email='blurrcat@gmail.com',
    url='https://github.com/blurrcat/debot.git',
    packages=find_packages(),
    scripts=[
        'scripts/test_bot.py',
    ],
    package_dir={'debot': 'debot'},
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'develop': develop_require
    },
)
