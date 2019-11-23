import json

import beatmachine as bm
import argparse


def main():
    parser = argparse.ArgumentParser(prog="beatmachine")
    parser.add_argument("--input", "-i", help="Input MP3 file", required=True)
    parser.add_argument("--effects", "-e", help="JSON effects to apply", required=True)
    parser.add_argument("--output", "-o", help="Output MP3 file", required=True)
    args = parser.parse_args()

    beats = bm.loader.load_beats_by_signal(args.input)
    effects = [bm.effects.load_from_dict(e) for e in json.loads(args.effects)]
    result = bm.editor.apply_effects(beats, effects)
    return sum(result).export(args.output)


if __name__ == "__main__":
    main()
