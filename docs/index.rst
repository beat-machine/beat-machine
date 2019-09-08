.. beatmachine documentation master file, created by
   sphinx-quickstart on Sun Sep  8 18:32:12 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. include:: ../README.rst

.. toctree::
   :maxdepth: 2

Installation
============

The ``beatmachine`` library is available on PyPI::

   pip install beatmachine

Cython woes
-----------

One of ``beatmachine``'s dependencies, ``madmom``, requires ``Cython`` to be
present at the time of installation. ``beatmachine`` lists it as a PEP-518
build dependency, but not all tooling supports this yet. Additionally, some
tools like Pipenv will just try again after the first failure, resulting in
a success.

For consistent results, make sure that ``Cython`` is installed in a separate
stage before installing ``beatmachine``.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
