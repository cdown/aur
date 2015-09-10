===
aur
===

.. image:: https://travis-ci.org/cdown/aur.svg?branch=develop
  :target: https://travis-ci.org/cdown/aur
  :alt: Test status

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
