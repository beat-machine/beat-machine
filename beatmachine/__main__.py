from click import command, option
from pydub import AudioSegment

from beatmachine.processor import apply_effects, remove_leading_silence
from beatmachine.registry import load_all_effects


@command()
@option('--input', help='File to process.', required=True)
@option('--bpm', help='BPM of the input audio.', type=int, required=True)
@option('--effects', help='JSON representation of effects to apply.', required=True)
@option('--output', help='Output mp3 file path.', required=True)
def main(input, bpm, effects, output):
    audio = remove_leading_silence(AudioSegment.from_mp3(input))
    return apply_effects(audio, int(bpm), load_all_effects(effects)).export(output, format='mp3')


if __name__ == '__main__':
    main()
