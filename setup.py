#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

__version__ = '0.2.0'
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


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
        'scripts/debot-cli',
    ],
    package_dir={'debot': 'debot'},
)
