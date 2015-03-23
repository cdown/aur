===
aur
===

.. image:: https://img.shields.io/travis/cdown/aur/master.svg?label=linux
        :target: https://travis-ci.org/cdown/aur

.. image:: https://img.shields.io/appveyor/ci/cdown/aur/master.svg?label=windows
        :target: https://ci.appveyor.com/project/cdown/aur

.. image:: https://img.shields.io/coveralls/cdown/aur/master.svg
        :target: https://coveralls.io/r/cdown/aur

.. image:: https://landscape.io/github/cdown/aur/master/landscape.svg
        :target: https://landscape.io/github/cdown/aur/master

.. image:: https://img.shields.io/requires/github/cdown/aur.svg?label=deps
        :target: https://requires.io/github/cdown/aur/requirements/?branch=master

aur is a Python library that makes it easy to access and parse data
from the `Arch User Repository API`_.

.. _Arch User Repository API: https://wiki.archlinux.org/index.php/AurJson

Usage
-----

.. code:: python

    >>> import aur
    >>> list(aur.search("yturl"))
    [<Package: 'yturl-git'>, <Package: 'yturl'>]
    >>> package = aur.info("cower")
    >>> package.description
    'A simple AUR agent with a pretentious name'

Installation
------------

From pip:

.. code::

    pip install aur

Manually:

.. code::

    python setup.py install


Testing
-------

.. code::

    python setup.py test
