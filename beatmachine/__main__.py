import argparse
import json
import os
import sys
import pickle
import beatmachine as bm


def main():
    parser = argparse.ArgumentParser(prog="beatmachine")
    parser.add_argument("--version", "-v", action="version", version=bm.__version__)
    parser.add_argument("--input", "-i", help="Input MP3 or Beat file", required=True)
    parser.add_argument("--effects", "-e", help="JSON effects to apply", default="[]")
    parser.add_argument("--output", "-o", help="Output MP3 file", required=True)
    parser.add_argument(
        "--serialize",
        "-s",
        help="Output serialized beat file (can be used in place of MP3)",
        required=False,
        action="store_true",
    )
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
    filename = os.path.splitext(args.input)
    if args.bpm is not None:
        if filename[1].lower() == ".beat":
            print(
                "BPM already encoded in beat file. If you want to change this, please use the MP3."
            )
            sys.exit()
        else:

            def loader(f):
                return bm.loader.load_beats_by_signal(
                    f,
                    min_bpm=args.bpm - args.tolerance,
                    max_bpm=args.bpm + args.tolerance,
                )

    effect_count = len(effects)
    if os.path.isfile(args.input):
        if filename[1].lower() == ".mp3":
            print("Locating beats (this may take a while)")
            beats = bm.Beats.from_song(args.input, beat_loader=loader)
            if args.serialize is True:
                with open(filename[0] + ".beat", "wb") as fp:
                    fp.write(pickle.dumps(beats))
                    fp.close()
                    print(
                        "Wrote beats out to "
                        + filename[0]
                        + ".beat. Use this instead of the MP3 to speed up processing."
                    )
        elif filename[1].lower() == ".beat":
            with open(args.input, "rb") as fp:
                try:
                    beats = pickle.load(fp)
                    fp.close()
                except Exception:
                    print(
                        "Something is wrong with your previously generated beats file. Please try rebuilding it from the MP3."
                    )
                    fp.close()
                    sys.exit()
        else:
            print("Please specify either an MP3 or a previously generated beats file.")
            sys.exit()
    else:
        print("Please specify either an MP3 or a previously generated beats file.")
        sys.exit()

    for i, effect in enumerate(effects):
        print(f"Applying effect {i + 1}/{effect_count} ({effect.__effect_name__})")
        beats = beats.apply(effect)

    print("Rendering song")
    beats.save(args.output)
    print("Wrote output to", args.output)


if __name__ == "__main__":
    main()
