Using The CLI
=============

A CLI for ``beatmachine`` is available by executing the module::

    $ python -m beatmachine --help

    usage: beatmachine [-h] [--version] --input INPUT --effects EFFECTS --output
                    OUTPUT [--serialize] [--bpm BPM] [--tolerance TOLERANCE]

    optional arguments:
    -h, --help            show this help message and exit
    --version, -v         show program's version number and exit
    --input INPUT, -i INPUT
                            Input MP3 or Beat file
    --effects EFFECTS, -e EFFECTS
                            JSON effects to apply
    --output OUTPUT, -o OUTPUT
                            Output MP3 file
    --serialize, -s       Output serialized beat file (can be used in place of
                            MP3)
    --bpm BPM, -b BPM     BPM estimate
    --tolerance TOLERANCE, -t TOLERANCE
                            BPM drift tolerance, only used if --bpm is set

So, for example, to swap beats 2 and 4 of a song, use::

    $ python -m beatmachine -i in.mp3 -e '[{"type": "swap", "x_period": 2, "y_period": 4}]' -o out.mp3

This command is quite long, though, and writing out JSON can be annoying. To
mitigate this, a file containing the effect descriptions can be used::

    $ python -m beatmachine -i in.mp3 -e effects.json -o out.mp3

Serialization
-------------

Instead of re-locating beats every single time, partial results can be cached
for later use. To pickle the intermediate ``Beats`` object into a ``.beat``
file, use the ``--serialize/-s`` flag like so::

    $ python -m beatmachine -i in.mp3 -s -o in.beat
    $ python -m beatmachine -i in.beat -e effects.json -o out.mp3

Preprocessing songs in this manner is highly recommended for repeated use.
