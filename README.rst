beatmachine
===========

.. image:: https://travis-ci.com/dhsavell/beat-machine.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.com/dhsavell/beat-machine

.. image:: https://img.shields.io/pypi/v/beatmachine
    :alt: PyPI
    :target: https://pypi.org/project/beatmachine/

The Beat Machine is a library for remixing songs by procedurally editing their beats, inspired by the creations over on
`/r/BeatEdits <https://www.reddit.com/r/BeatEdits/>`_. It works both as a library and as a command-line utility.

Installation
------------

The ``beatmachine`` library is available on PyPI::

   $ pip install beatmachine

Build Dependency Woes
~~~~~~~~~~~~~~~~~~~~~

One of ``beatmachine``'s dependencies, ``madmom``, requires ``Cython`` and ``numpy`` to be present at build time. For
consistent results, make sure that these packages are installed separately before.

These packages are listed as PEP-518 build dependencies, but not all tooling supports this yet. Additionally, some tools
like Pipenv will just try again after the first failure, resulting in an overall success.
