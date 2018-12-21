# beat-machine

> A program that rearranges and/or applies effects to each beat of a song.

## Usage

Python 3.6+ is required!

For a brief overview, run `python -m beatmachine --help`. Note that all inputs and outputs are expected to be MP3 files.

See the section below or `effect_loader.py` for a loose guideline on how JSON effect descriptions can be written. This
system is a work in progress.

### Examples

```sh
# Remove every other beat
$ python -m beatmachine --input in.mp3 --effects "{\"effects\":[{\"type\":\"remove\",\"every\":2}]}" --output out.mp3

# Cut every beat in half
$ python -m beatmachine --input in.mp3 --effects "{\"effects\":[{\"type\":\"cut_in_half\"}]}" --output out.mp3
```

## Effects

The Beat Machine uses two different types of effects: **beat effects** and **song effects**. Beat effects transform a
single beat, and can't be used on their own. Song effects apply to an entire song, and can either be composed of beat
effects or do their own work entirely.

### Beat Effects

Beat effects can be described with one of the following objects:

```json
{
  "type": "replace_with_silence"
},

{
  "type": "replace_with_silence",
  "every": 2
}
```

#### Replace With Silence (`replace_with_silence`)
Replaces a beat with silence of equal length.

#### Remove (`remove`)
Removes a beat entirely.

#### Cut In Half (`cut_in_half`)
Cuts a beat in half.

#### Reverse (`reverse`)
Reverses a beat.

### Song Effects

Song effects can be described simply by specifying their type:

```json
{
  "type": "sort_by_loudness"
}
```

#### Randomize All (`randomize_all`)
Randomizes the order of all beats in the song.

#### Sort By Loudness (`sort_by_loudness`)
Sorts all beats by their average loudness.

#### Sort By Average Frequency (`sort_by_average_frequency`)
Sorts all beats by their average frequency.

#### Swap Beats (`swap`)
**Requires 2 additional parameters**: `x` and `y`. Both are integers where `y` > `x`.

Swaps every *x*th and *y*th beat.