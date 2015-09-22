.. module:: aur

`aur:` Python AUR interface
===========================

`aur` is a Python library that makes it easy to access and parse data from the
`Arch User Repository API`_.

.. _`Arch User Repository API`: https://wiki.archlinux.org/index.php/AurJson


Core functions
--------------

The AUR API has four query types. For each of these query types, `aur` exposes
a function that calls the API with this query type.

.. autofunction:: info
.. autofunction:: msearch
.. autofunction:: multiinfo
.. autofunction:: search


The Package class
-----------------

Most functions in this library return :py:class:`Package` objects in some form.
They essentially act as storage objects for all metadata related to a package.

.. code:: python

    >>> yturl = info('yturl')
    >>> yturl.description
    'YouTube videos on the command line'
    >>> yturl.last_modified
    datetime.datetime(2015, 9, 8, 22, 26, 24)
    >>> yturl.out_of_date
    False

.. Unfortunately Sphinx's introspection fails to get the class signature here,
   presumably because _Package is being subclassed, so we need to do our own
   work.

.. autoclass:: Package
    :inherited-members:
    :exclude-members: count, index

    Here are all of the attributes available:


Exceptions
----------

`aur` uses `requests`_ internally, so general HTTP(S) exceptions will come from
there.

There are also a number of more targeted exceptions defined in `aur` itself:

.. autoexception:: AURError
.. autoexception:: APIError
.. autoexception:: QueryTooShortError
.. autoexception:: NoSuchPackageError

.. _requests: http://docs.python-requests.org
