# beat-machine

[![Build Status](https://travis-ci.com/dhsavell/beat-machine.svg?branch=master)](https://travis-ci.com/dhsavell/beat-machine)
[![Maintainability](https://api.codeclimate.com/v1/badges/b6421f0e0edd9c8a77f4/maintainability)](https://codeclimate.com/github/dhsavell/beat-machine/maintainability)
[![PyPI](https://img.shields.io/pypi/v/beatmachine)](https://pypi.org/project/beatmachine/)

The Beat Machine is a library for playing with beats of songs, inspired by the creations over on
[/r/BeatEdits](https://www.reddit.com/r/BeatEdits/). It works both as a library and as a command-line utility that
reads effects from a JSON array.

## Installation

One of the Beat Machine's dependencies, `madmom`, requires `Cython` to be present before installation. If you encounter
an error along the lines of:

```
Command "python setup.py egg_info" failed with error code 1 in /tmp/tmp1d2dis8pbuild/madmom/
```

Try installing Cython (`pip install Cython`) beforehand as a separate build step.

## Examples

A few examples of common edits are available below. In all cases, multiple effects can be supplied. When more than
one effect is present, effects are applied in order of appearance.

### Using the CLI

The CLI has the following usage (produced by `python -m beatmachine --help`):

```text
Usage: __main__.py [OPTIONS]

Options:
  --input TEXT    File to process.  [required]
  --effects TEXT  JSON representation of effects to apply.  [required]
  --output TEXT   Output mp3 file path.  [required]
  --help          Show this message and exit.
```

Note that **the program may appear to hang** due to the time taken to locate beats.

#### Removing every other beat

The `remove` effect can't have a period of 1, because that would be silly (and result in nothing to work with).

```sh
$ python -m beatmachine \
    --input "in.mp3" \
    --output "out.mp3" \
    --effects '[{"type": "remove", "period": 2}]'
```

#### Cutting every beat in half

```sh
$ python -m beatmachine \
    --input "in.mp3" \
    --output "out.mp3" \
    --effects '[{"type": "cut", "period": 1}]'
```

#### Swapping beats 2 and 4

In the `swap` effect, the `x_period` and `y_period` fields are interchangeable, however they can't be equal.

```sh
$ python -m beatmachine \
    --input "in.mp3" \
    --output "out.mp3" \
    --effects '[{"type": "swap", "x_period": 2, "y_period": 4}]'
```

#### Halving every beat then duplicating every other beat

```sh
$ python -m beatmachine \
    --input "in.mp3" \
    --output "out.mp3" \
    --effects '[{"type": "cut", "period": 1},
                {"type": "repeat", "period": 2, "times": 2}]'
```

### Using the Python module

Note that `load_beats_by_signal` is a rather long, blocking operation (~50 seconds for a 2 minute song on a
Ryzen 5 2600 w/ 16GB of RAM). Your mileage may vary.

If slightly inaccurate results are acceptable, `load_beats_by_bpm` is also available, which is much less CPU- and
memory-intensive. This method of loading beats is not capable of handling any kind of tempo change.

#### Removing every other beat

```python
import beatmachine as bm

beats = bm.loader.load_beats_by_signal('in.mp3')  # A file-like object is also acceptable
effects = [bm.effects.periodic.RemoveEveryNth(period=2)]
result = sum(bm.editor.apply_effects(beats, effects))
result.export('out.mp3')
```

Other results come from modifying the `effects` list. See the `effects` module and its submodules for more
possibilities.

#### Implementing a custom effect

There are two ways to create a basic effect class:
 - Create a class with the metaclass `beatmachine.effects.base.EffectRegistry`
 - Inherit from `beatmachine.effects.base.BaseEffect` with metaclass `beatmachine.effects.base.EffectABCMeta`
    - This is recommended since it provides all the necessary attributes as an abstract base class
    
The resulting effect class will automatically be loadable through `beatmachine.effects.load_from_dict`. Make sure that
any configurable parameters are specified as keyword arguments, since `load_from_dict` passes fields directly to
`__init__`. 