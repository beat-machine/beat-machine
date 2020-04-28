import json
import os
import sys
import pickle
import beatmachine as bm
import argparse

def main():
    parser = argparse.ArgumentParser(prog="beatmachine")
    parser.add_argument("--input", "-i", help="Input MP3 or beats file", required=True)
    parser.add_argument("--effects", "-e", help="JSON effects to apply", required=True)
    parser.add_argument("--output", "-o", help="Output MP3 file", required=True)
    parser.add_argument("--beat", "-b", help="Output beats file (can be used in place of the MP3)", required=False, action='store_true')
    args = parser.parse_args()

    if os.path.isfile(args.effects):
        with open(args.effects, "r") as fp:
            effects_json = json.load(fp)
    else:
        effects_json = json.loads(args.effects)

    effects = [bm.effects.load_from_dict(e) for e in effects_json]
    effect_count = len(effects)
    filename = os.path.splitext(args.input.lower())
    if os.path.isfile(args.input):
        if filename[1]=='.mp3':
            print("Locating beats (this may take a while)")
            beats = bm.Beats.from_song(args.input)
            if args.beat is True:
                with open(filename[0]+".beat", "wb") as fp:
                    fp.write(pickle.dumps(beats))
                    fp.close()
                    print("Wrote beats out to "+filename[0]+".beat. Use this instead of the MP3 to speed up processing.")
        elif filename[1]=='.beat':
            with open(args.input, "rb") as fp:
                try:
                    beats = pickle.load(fp)
                    fp.close()
                except Exception:
                    print("Something is wrong with your previously generated beats file. Please try rebuilding it from the MP3.")
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
    beats.consolidate().export(args.output)
    print("Wrote output to", args.output)

if __name__ == "__main__":
    main()
