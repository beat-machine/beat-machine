Using The CLI
=============

A CLI for ``beatmachine`` is available by executing the module::

    $ python -m beatmachine --help

    usage: beatmachine [-h] --input INPUT --effects EFFECTS --output OUTPUT

    optional arguments:
      -h, --help            show this help message and exit
      --input INPUT, -i INPUT
                            Input MP3 file
      --effects EFFECTS, -e EFFECTS
                            JSON effects to apply
      --output OUTPUT, -o OUTPUT
                            Output MP3 file

So, for example, to swap beats 2 and 4 of a song, use::

    $ python -m beatmachine -i in.mp3 -e '[{"type": "swap", "x_period": 2, "y_period": 4}]' -o out.mp3

This command is quite long, though, and writing out JSON can be annoying. To
mitigate this, a file containing the effect descriptions can be used::

    $ python -m beatmachine -i in.mp3 -e effects.json -o out.mp3
