# beat-machine

The Beat Machine is a free tool for creating "every other beat is missing" remixes -- and many other kind of beat
edits, too.

To use The Beat Machine from your browser, try the official web interface at https://beatmachine.branchpanic.me.

## Installation

![PyPI Version](https://img.shields.io/pypi/v/beatmachine)

TBM is available on PyPI and can be installed with `pip install beatmachine`.

## Usage

TBM is built on *effects*, which modify on the beats of a song. For example, the `swap` effect swaps beats and can be
used to create the "beats 2 and 4 are swapped" sound.

The easiest way to get started is to download some of the presets from the [`examples`][examples] directory.
You can use them like so:

```sh
$ python -m beatmachine -i in.mp3 -e swap_2_4.json -o out.mp3
```

The CLI reads effects as an array of JSON objects. Each object represents an effect, and effects are applied
sequentially. You can either specify this inline or provide a path to a JSON file. For example, to swap beats 2 and 4:

```sh
$ python -m beatmachine -i in.mp3 -e '[{"type": "swap", "x_period": 2, "y_period": 4}]' -o out.mp3
```

Using `python -m beatmachine.dump_schema`, you can generate a JSON schema that describes the effects array. This
includes definitions of all valid effects.

You can also look at the individual classes in `beatmachine.effects` to see their parameters. For example, [here is
the source for the remove effect](https://github.com/beat-machine/beat-machine/blob/3885a531006c297d579bf7530cc9f9e344587f70/beatmachine/effects/periodic.py#L88). The JSON object for an effect must have a key called `type` with the value of
`__effect_name__`. It can have additional keys for parameters defined in `__effect_schema__`. So, some examples of
valid `remove` effects are `{ "type": "remove" }` and `{ "type": "remove", "period": 4 }`.

(TODO: add a human-readable list of effects and their parameters.)

(TODO: document the `--serialize` flag, which can be used to speed up repeated processing. See [#54].)

## API

The `beatmachine.Beats` class lets you modify beats using a Python script.

```python
import beatmachine as bm

beats = bm.Beats.from_song('in.mp3')
beats.apply(bm.effects.RemoveEveryNth(2)).save('out.mp3')
```

This opens up some interesting possibilities, like turning beats into a NumPy array that you can modify further.

```python
import beatmachine as bm
import numpy as np

beats = bm.Beats.from_song('in.mp3')
y = np.flip(beats.to_ndarray())
```

Be warned that the API is largely untested outside of the core `from_song` -> `apply` -> `save` path.

(TODO: more detailed docs will eventually live on the [wiki].)

## Attribution

The default beat detector is powered by [CPJKU/madmom](https://github.com/CPJKU/madmom). View its license
[here][madmom_license].

[madmom_license]: https://github.com/CPJKU/madmom/blob/3bc8334099feb310acfce884ebdb76a28e01670d/LICENSE
[examples]: https://github.com/beat-machine/beat-machine/tree/main/examples
[#54]: https://github.com/beat-machine/beat-machine/issues/54
[wiki]: https://github.com/beat-machine/beat-machine/wiki
