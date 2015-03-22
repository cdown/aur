|Build status| |Coverage| |Code quality| |Dependencies|

pyaur is a Python library that makes it easy to access and parse data
from the `Arch User Repository API`_.

.. code:: python

    >>> import aur
    >>> list(aur.search("yturl"))
    [<Package: 'yturl-git'>, <Package: 'yturl'>]
    >>> package = aur.info("cower")
    >>> package.description
    'A simple AUR agent with a pretentious name'

Installation
------------

::

    $ pip install pyaur

Installing dependencies
-----------------------

If you install by `pip`_, these will be installed automatically, but
otherwise:

::

    $ pip install -r requirements.txt

Testing
-------

::

    $ pip install -r tests/requirements.txt
    $ nosetests

License
-------

pyaur is `ISC licensed`_. See the LICENSE file for full details.

.. _Arch User Repository API: https://wiki.archlinux.org/index.php/AurJson
.. _pip: https://pypi.python.org/pypi/pip
.. _ISC licensed: http://en.wikipedia.org/wiki/ISC_license

.. |Build status| image:: https://img.shields.io/travis/cdown/pyaur/master.svg
   :target: https://travis-ci.org/cdown/pyaur
.. |Coverage| image:: https://img.shields.io/coveralls/cdown/pyaur/master.svg
   :target: https://coveralls.io/r/cdown/pyaur
.. |Code quality| image:: https://img.shields.io/scrutinizer/g/cdown/pyaur.svg
   :target: https://scrutinizer-ci.com/g/cdown/pyaur/code-structure/master/hot-spots
.. |Dependencies| image:: https://img.shields.io/requires/github/cdown/pyaur.svg
   :target: https://requires.io/github/cdown/pyaur/requirements/?branch=master
