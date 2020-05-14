beatmachine
===========

.. image:: https://github.com/beat-machine/beat-machine/workflows/Build/badge.svg
    :alt: Build Status
    :target: https://github.com/beat-machine/beat-machine/actions

.. image:: https://img.shields.io/pypi/v/beatmachine
    :alt: PyPI Version
    :target: https://pypi.org/project/beatmachine/

.. image:: https://readthedocs.org/projects/beatmachine/badge/?version=latest
    :target: https://beatmachine.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


The Beat Machine is a library for remixing songs by procedurally editing their beats, inspired by the creations on
`/r/BeatEdits <https://www.reddit.com/r/BeatEdits/>`_. It works both as a library and as a command-line utility.

Installation
------------

The ``beatmachine`` library is available on PyPI::

   $ pip install beatmachine

Quick Reference
---------------

CLI
~~~
A simple CLI is available that reads effects from JSON files. See the docs for
more info on how to define these.

The basic usage is::

    $ python -m beatmachine -i in.mp3 -e <JSON string or file describing effects> -o out.mp3

Python API
~~~~~~~~~~
A new ``Beats`` class is available that wraps most basic functionality. If you
want to get started quickly, this may be for you!

Here's a sample::

    import beatmachine as bm

    beats = bm.Beats.from_song('in.mp3')
    beats.apply(bm.effects.RemoveEveryNth(2)).save('out.mp3')

If you want to get more advanced, you can also convert to an ``ndarray`` at
any point::

    import beatmachine as bm
    import numpy as np

    beats = bm.Beats.from_song('in.mp3')
    y = np.flip(beats.to_ndarray())
