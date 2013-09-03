#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "pyaur",
    version = "0.9.0",
    description = "Arch User Repository API library",
    url = "https://github.com/cdown/pyaur/",

    author = "Chris Down",
    author_email = "chris@chrisdown.name",
    license = "MIT",

    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],

    packages = [ "aur" ],
    requires = [ "requests" ],
)
