import json
import os

import beatmachine as bm
import argparse


def main():
    parser = argparse.ArgumentParser(prog="beatmachine")
    parser.add_argument("--input", "-i", help="Input MP3 file", required=True)
    parser.add_argument("--effects", "-e", help="JSON effects to apply", required=True)
    parser.add_argument("--output", "-o", help="Output MP3 file", required=True)
    args = parser.parse_args()

    if os.path.isfile(args.effects):
        with open(args.effects, "r") as fp:
            effects_json = json.load(fp)
    else:
        effects_json = json.loads(args.effects)

    effects = [bm.effects.load_from_dict(e) for e in effects_json]

    print("Locating beats (this may take a while)")
    beats = bm.Beats.from_song(args.input)
    effect_count = len(effects)

    for i, effect in enumerate(effects):
        print(f"Applying effect {i + 1}/{effect_count} ({effect.__effect_name__})")
        beats = beats.apply(effect)

    print("Rendering song")
    beats.consolidate().export(args.output)
    print("Wrote output to", args.output)


if __name__ == "__main__":
    main()
