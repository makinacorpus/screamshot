"""
Setup file.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

import screamshot


HERE = os.path.abspath(os.path.dirname(__file__))


setup(
    name="screamshot",
    version=screamshot.__version__,
    author=screamshot.__author__,
    description="Python library to capture screenshots of web applications or pages",
    long_description=open(os.path.join(HERE, "README.md")).read()
    + "\n\n"
    + open(os.path.join(HERE, "CHANGES.md")).read(),
    include_package_data=True,
    package_data={"screamshot": ["py.typed"]},
    packages=["screamshot"],
    url="https://github.com/makinacorpus/screamshot",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["pyppeteer", "requests"],
    entry_points={
        "console_scripts": [
            "screamshot = screamshot.screamshot_script:main",
            "browser-manager = screamshot.browser_manager_script:main",
        ]
    },
)
