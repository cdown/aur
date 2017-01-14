|travis| |appveyor| |coveralls| |libraries|

.. |travis| image:: https://img.shields.io/travis/cdown/aur/develop.svg?label=linux%20%2B%20mac%20tests
  :target: https://travis-ci.org/cdown/aur
  :alt: Linux and Mac tests

.. |appveyor| image:: https://img.shields.io/appveyor/ci/cdown/aur/develop.svg?label=windows%20tests
  :target: https://ci.appveyor.com/project/cdown/aur
  :alt: Windows tests

.. |coveralls| image:: https://img.shields.io/coveralls/cdown/aur/develop.svg?label=test%20coverage
  :target: https://coveralls.io/github/cdown/aur?branch=develop
  :alt: Coverage

.. |libraries| image:: https://img.shields.io/librariesio/github/cdown/aur.svg?label=dependencies
  :target: https://libraries.io/github/cdown/aur
  :alt: Dependencies

aur is a Python library that makes it easy to access and parse data from the
`Arch User Repository API`_.

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

To install the latest stable version from PyPi:

.. code::

    $ pip install -U aur

To install the latest development version directly from GitHub:

.. code::

    $ pip install -U git+https://github.com/cdown/aur.git@develop

Testing
-------

.. code::

    $ pip install tox
    $ tox
    ..........
    ----------------------------------------------------------------------
    Ran 10 tests in 4.088s
    OK
