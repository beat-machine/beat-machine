import argparse
import json
import os

import beatmachine as bm


def main():
    parser = argparse.ArgumentParser(prog="beatmachine")
    parser.add_argument("--version", "-v", action="version", version=bm.__version__)
    parser.add_argument("--input", "-i", help="Input MP3 file", required=True)
    parser.add_argument("--effects", "-e", help="JSON effects to apply", required=True)
    parser.add_argument("--output", "-o", help="Output MP3 file", required=True)
    parser.add_argument("--bpm", "-b", type=int, help="BPM estimate")
    parser.add_argument(
        "--tolerance",
        "-t",
        type=int,
        help="BPM drift tolerance, only used if --bpm is set",
        default=15,
    )
    args = parser.parse_args()

    if os.path.isfile(args.effects):
        with open(args.effects, "r") as fp:
            effects_json = json.load(fp)
    else:
        effects_json = json.loads(args.effects)

    effects = [bm.effects.load_from_dict(e) for e in effects_json]

    loader = bm.loader.load_beats_by_signal

    if args.bpm is not None:

        def loader(f):
            return bm.loader.load_beats_by_signal(
                f, min_bpm=args.bpm - args.tolerance, max_bpm=args.bpm + args.tolerance
            )

    print("Locating beats (this may take a while)")
    beats = bm.Beats.from_song(args.input, beat_loader=loader)
    effect_count = len(effects)

    for i, effect in enumerate(effects):
        print(f"Applying effect {i + 1}/{effect_count} ({effect.__effect_name__})")
        beats = beats.apply(effect)

    print("Rendering song")
    beats.save(args.output)
    print("Wrote output to", args.output)


if __name__ == "__main__":
    main()
