===
aur
===

aur is a Python library that makes it easy to access and parse data
from the `Arch User Repository API`_.

.. _Arch User Repository API: https://wiki.archlinux.org/index.php/AurJson

Usage
-----

.. code:: python

    >>> yturl = aur.info('yturl')
    >>> yturl.description
    'YouTube videos on the command line'
    >>> poco = aur.search('poco')
    >>> poco
    [<Package: poco>, <Package: flopoco>, <Package: libpoco-basic>]


Documentation
-------------

Documentation is available on ReadTheDocs_.

.. _ReadTheDocs: https://aur.readthedocs.org

Installation
------------

From pip:

.. code::

    pip install aur

Manually:

.. code::

    python setup.py install


Documentation
-------------

.. code::

    pydoc aur


Testing
-------

.. image:: https://travis-ci.org/cdown/aur.svg?branch=develop
  :target: https://travis-ci.org/cdown/aur
  :alt: Test status

.. code::

    python setup.py test
