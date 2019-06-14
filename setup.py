"""
Setup file.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

import screamshot


HERE = os.path.abspath(os.path.dirname(__file__))


def get_requires():
    requirements_f = open("requirements.txt", "r")
    install_requires = requirements_f.read().splitlines()
    requirements_f.close()
    return install_requires


setup(
    name="screamshot",
    version=screamshot.__version__,
    author=screamshot.__author__,
    description="Python library to capture screenshots of web applications or pages",
    description_content_type="text/markdown",
    long_description_content_type="text/markdown",
    long_description=open(os.path.join(HERE, "README.md")).read()
    + "\n\n"
    + open(os.path.join(HERE, "CHANGES.md")).read(),
    include_package_data=True,
    package_data={"screamshot": ["py.typed"]},
    packages=["screamshot"],
    package_dir={"screamshot": "screamshot"},
    url="https://github.com/makinacorpus/screamshot",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=get_requires(),
    entry_points={
        "console_scripts": [
            "screamshot = screamshot.screamshot_script:main",
            "browser-manager = screamshot.browser_manager_script:main",
        ]
    },
)
