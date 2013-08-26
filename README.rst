pyaur
=====

.. image:: https://travis-ci.org/cdown/pyaur.png?branch=master  
    :target: https://travis-ci.org/cdown/pyaur
.. image:: https://pypip.in/v/pyaur/badge.png   
    :target: https://crate.io/packages/pyaur

**pyaur** is a Python library that makes it easy to access and parse data from
the Arch User Repository API.

Search for packages, get package info, maintainer info, and more. pyaur wraps
the official `AurJson API <https://wiki.archlinux.org/index.php/AurJson>`__ so
that you can focus on using AUR data, not retrieving or parsing it.

.. code:: python

    >>> import aur
    >>> client = aur.AURClient()
    >>> list(client.search("yturl"))
    [<Package: yturl-git>, <Package: yturl>]
    >>> package = client.info("tzupdate-git")
    >>> package.description
    'Set the local timezone based on IP geolocation.'
    >>> package.last_modified
    datetime.datetime(2013, 8, 23, 21, 11, 6)

Installation
------------

To install pyaur, simply run:

::

    $ pip install pyaur

License
-------

pyaur is MIT licensed. See the `LICENSE file
<https://github.com/cdown/pyaur/blob/master/LICENSE>`__ for full details.
