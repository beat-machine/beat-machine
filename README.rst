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

    # This takes a while with the defaults!
    beats = Beats.from_song('in.mp3')

    # The consolidate() method returns a PyDub AudioSegment, which we can use
    # however we want.
    beats.apply(bm.effects.RemoveEveryNth(2)).consolidate().export('out.mp3')

    # The Beats class is immutable, so we're free to use it again.
    beats.apply_all(bm.effects.RemoveEveryNth(2), bm.effects.CutEveryNth()).consolidate().export('out_2.mp3')

