.. image:: https://travis-ci.org/cdown/pyaur.png?branch=master
    :target: https://travis-ci.org/cdown/pyaur
.. image:: https://coveralls.io/repos/cdown/pyaur/badge.png?branch=master
    :target: https://coveralls.io/r/cdown/pyaur?branch=master

pyaur
=====

**pyaur** is a Python library that makes it easy to access and parse data from
the Arch User Repository API.

Search for packages, get package info, maintainer info, and more. pyaur wraps
the official `AurJson API <https://wiki.archlinux.org/index.php/AurJson>`__ so
that you can focus on using AUR data, not retrieving or parsing it.

.. code:: python

    >>> import aur
    >>> list(aur.search("yturl"))
    [<Package: 'yturl-git'>, <Package: 'yturl'>]
    >>> package = aur.info("cower")
    >>> package.description
    'A simple AUR agent with a pretentious name'
    >>> package.last_modified
    datetime.datetime(2013, 4, 5, 0, 18, 46)

Installation
------------

To install pyaur, simply run:

::

    $ pip install pyaur

License
-------

pyaur is MIT licensed. See the `LICENSE file
<https://github.com/cdown/pyaur/blob/master/LICENSE>`__ for full details.
