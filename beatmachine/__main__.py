from click import command, option

from beatmachine.beat_effects import *
from beatmachine.effect_loader import load_all_effects
from beatmachine.processor import apply_effects, remove_leading_silence, estimate_bpm


@command()
@option('--input', help='File to process.', required=True, default="E:\Projects\src\\beat-machine\\uptown.mp3")
@option('--bpm', help='BPM of the input audio.', type=int)
@option('--effects', help='JSON representation of effects to apply.', required=True)
@option('--output', help='Output mp3 file path.', required=True, default="E:\Projects\src\\beat-machine\\uptown2.mp3")
def main(input, bpm, effects, output):
    audio = remove_leading_silence(AudioSegment.from_mp3(input))

    if not bpm:
        print('Auto-detecting BPM. This is not particularly accurate! Specify one with --bpm if you can.')
        bpm = estimate_bpm(audio)

    return apply_effects(audio, int(bpm), load_all_effects(effects)).export(output, format='mp3')


if __name__ == '__main__':
    main()
