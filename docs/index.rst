`aur` is a Python library that makes it easy to access and parse data from the
`Arch User Repository API`_.

.. _`Arch User Repository API`: https://wiki.archlinux.org/index.php/AurJson


Core functions
--------------

The AUR API has four query types. For each of these query types, `aur` exposes
a function that calls the API with this query type.

.. module:: aur
.. autofunction:: info
.. autofunction:: msearch
.. autofunction:: multiinfo
.. autofunction:: search

The Package class
-----------------


.. Unfortunately Sphinx's introspection fails to get the class signature here,
   presumably because _Package is being subclassed, so we need to do our own
   work.

.. autoclass:: Package
    :inherited-members:
    :exclude-members: count, index

    Here are all of the attributes available:
