#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import free_audio_books
version = free_audio_books.__version__

setup(
    name='free_audio_books',
    version=version,
    author="Patrick Forringer",
    author_email='patrick@forringer.com',
    packages=[
        'free_audio_books',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.7.4',
    ],
    zip_safe=False,
    scripts=['free_audio_books/manage.py'],
)
