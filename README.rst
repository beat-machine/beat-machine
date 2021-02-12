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


The Beat Machine is a library for remixing songs by procedurally editing their
beats, inspired by the creations on `/r/BeatEdits <https://www.reddit.com/r/BeatEdits/>`_.
It works both as a library and as a command-line utility.

Installation
------------

The ``beatmachine`` library is available on PyPI::

   $ pip install beatmachine

Usage
-----

CLI
~~~
When called from the command line, the ``beatmachine`` module will operate on
a given song with a JSON array of effects.

Its basic usage is::

    $ python -m beatmachine -i in.mp3 -e '[{"type": "swap", "x_period": 2, "y_period": 4}]' -o out.mp3

A complete list of effects can be found by browsing the documentation for the
``effects`` package. The general format of an effect object is::

    {
        "type": "value of __effect_name__",

        "kwarg1": true,
        "kwarg2": 2,
        "kwarg3": "etc..."
    }

As of 3.2.0, ``beatmachine`` also offers a `JSON schema <https://json-schema.org/>`_
for the effects array. It can be accessed through::

    $ python -m beatmachine.dump_schema

This command always provides the latest output, and reflects local
modifications.

Python
~~~~~~
The ``beatmachine.Beats`` class provides a simple interface for working with songs::

    import beatmachine as bm

    beats = bm.Beats.from_song('in.mp3')
    beats.apply(bm.effects.RemoveEveryNth(2)).save('out.mp3')

All of the effects are located in the ``effects`` package and its sub-modules.
For custom operations, ``to_ndarray()`` is available to expose the underlying
NumPy array::

    import beatmachine as bm
    import numpy as np

    beats = bm.Beats.from_song('in.mp3')
    y = np.flip(beats.to_ndarray())
