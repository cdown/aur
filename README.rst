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

Usage
-----

Full documentation is available on ReadTheDocs_.

If you know how to use the `Arch User Repository API`_, you know how to use
this module. The only difference is that `PascalCase`_ package attributes are
converted to confirm to Python conventions (for example, :code:`OutOfDate`
becomes :code:`out_of_date`, and :code:`FirstSubmitted` becomes
:code:`first_submitted`).

.. _PascalCase: https://en.wikipedia.org/wiki/PascalCase
.. _ReadTheDocs: https://aur.readthedocs.org

.. code:: python

    >>> yturl = aur.info('yturl')
    >>> yturl.description
    'YouTube videos on the command line'
    >>> poco = aur.search('poco')
    >>> poco
    [<Package: flopoco>, <Package: poco-git>, <Package: poco>, <Package: libpoco-basic>]
    >>> poco[0].first_submitted
    datetime.datetime(2013, 8, 21, 21, 3, 9)
    >>> aur.multiinfo(['tzupdate', 'xinput-toggle'])
    {'tzupdate': <Package: tzupdate>, 'xinput-toggle': <Package: xinput-toggle>}

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

.. _Arch User Repository API: https://wiki.archlinux.org/index.php/AurJson
