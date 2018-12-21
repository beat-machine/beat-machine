from pydub.silence import detect_nonsilent


def split_into_beats(audio, beat_size_ms):
    """
    Splits a given AudioSegment into a list of beats and their indices. Each beat is represented as a Beat object.

    :param audio: The AudioSegment to split into beats.
    :param beat_size_ms: The length of one beat (in milliseconds).
    :return: A generator yielding each beat and its index.
    """
    for beat_start_ms in range(0, len(audio), beat_size_ms):
        yield audio[beat_start_ms:beat_start_ms + beat_size_ms]


def remove_leading_silence(audio, check_size_ms=10, threshold=-60):
    """
    Removes leading silence from a given audio segment.

    Adapted from: https://gist.github.com/sotelo/be57571a1d582d44f3896710b56bc60d

    :param audio: The AudioSegment to remove leading silence from.
    :param check_size_ms: Resolution of the check. Smaller values will look at smaller intervals, but take longer.
    :param threshold: Threshold of what is considered silence.
    :return: The AudioSegment with silence trimmed.
    """
    trim_amount = 0
    while audio[trim_amount:trim_amount + check_size_ms].dBFS < threshold:
        trim_amount += check_size_ms

    return audio[trim_amount:]


def estimate_bpm(audio):
    """
    Estimates the BPM of a given audio segment.

    Adapted from: https://gist.github.com/jiaaro/faa96fabd252b8552066

    :param audio: The AudioSegment to estimate the BPM of.
    :return: An approximate BPM of the given AudioSegment.
    """
    bass = audio.low_pass_filter(120)
    beat_loudness = bass.dBFS

    minimum_silence = int(60_000 / 240)
    nonsilent_times = detect_nonsilent(bass, minimum_silence, beat_loudness)

    spaces_between_beats = []
    last_t = nonsilent_times[0][0]

    for peak_start, _ in nonsilent_times[1:]:
        spaces_between_beats.append(peak_start - last_t)
        last_t = peak_start

    spaces_between_beats = sorted(spaces_between_beats)
    space = spaces_between_beats[len(spaces_between_beats) // 2]

    return 60_000 / space


def apply_effects(audio, bpm, song_effects):
    """
    Processes an MP3 file with a collection of given transformers. Transformers are merely functions that consume a
    Beat and then return a (potentially) changed Beat.

    :param audio: The AudioSegment to process.
    :param bpm: BPM of the given audio.
    :param song_effects: A collection of transformers to apply.
    :return: An AudioSegment that has been processed with the given transformers.
    """
    beats = list(split_into_beats(audio, 60_000 // bpm))
    print(f'Processing {len(beats)} beats')

    for song_effect in song_effects:
        beats = song_effect(beats)

    print('Done.')
    return sum(beats)
