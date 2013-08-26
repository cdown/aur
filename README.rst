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
    [Package({'category_id': 12, 'name': 'yturl-git', 'out_of_date': False, 'version': '20130824041733.85d42ac-3', ...}), ...]
    >>> package = client.info("tzupdate-git")
    Package({'category_id': 16, 'name': 'tzupdate-git', 'out_of_date': False, 'version': '20130823150922.47977f2-1', ...})
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
