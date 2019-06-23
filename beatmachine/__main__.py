import json

from click import command, option

import beatmachine as bm


@command()
@option('--input', help='File to process.', required=True)
@option('--effects', help='JSON representation of effects to apply.', required=True)
@option('--output', help='Output mp3 file path.', required=True)
def main(input, effects, output):
    beats = bm.loader.load_beats_by_signal(input)
    effects = [bm.effects.load_from_dict(e) for e in json.loads(effects)]
    result = bm.editor.apply_effects(beats, effects)
    return sum(result).export(output)


if __name__ == '__main__':
    main()
