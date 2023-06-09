#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-beeprint",
    version="0.1.0",
    author="Rodrigo Ferreira de Souza",
    author_email="rodfersou@gmail.com",
    maintainer="Rodrigo Ferreira de Souza",
    maintainer_email="rodfersou@gmail.com",
    license="Unlicense",
    url="https://github.com/hjwp/pytest-beeprint",
    description="use icdiff for better error messages in pytest assertions",
    long_description=read("README.rst") + read("HISTORY.rst"),
    long_description_content_type="text/x-rst",
    py_modules=["pytest_beeprint"],
    python_requires=">=3.7",
    install_requires=["pytest", "icdiff", "beeprint"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: Public Domain",
    ],
    entry_points={
        "pytest11": [
            "icdiff = pytest_beeprint",
        ],
    },
)
