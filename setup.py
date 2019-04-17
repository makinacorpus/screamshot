"""
Setup file.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

import screamshot


HERE = os.path.abspath(os.path.dirname(__file__))


setup(
    name='screamshot',

    version=screamshot.__version__,

    author=screamshot.__author__,

    description='Python library to capture screenshots of web applications or pages',

    long_description=open(os.path.join(HERE, 'README.md')).read() + '\n\n' +
    open(os.path.join(HERE, 'CHANGES.md')).read(),

    include_package_data=True,
    package_data={'package_c-stubs': ['__init__.pyi', 'generate_bytes_img.pyi']},
    packages=find_packages(),

    url='https://github.com/makinacorpus/screamshot',

    classifiers=[
        'Programming Language :: Python',
        'License :: BSD 2-Clause License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Screenshot',
    ],

    install_requires=[
        'pyppeteer',
    ],
)
