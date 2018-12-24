def beats_of(audio, bpm):
    """
    Splits a given AudioSegment into a list of beats and their indices. Each beat is represented as a Beat object.

    :param audio: The AudioSegment to split into beats.
    :param bpm: BPM of the given audio.
    :return: A generator yielding each beat and its index.
    """
    beat_size_ms = 60_000 // bpm
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


def apply_effects(audio, bpm, song_effects):
    """
    Processes an MP3 file with a collection of given transformers. Transformers are merely functions that consume a
    Beat and then return a (potentially) changed Beat.

    :param audio: The AudioSegment to process.
    :param bpm: BPM of the given audio.
    :param song_effects: A collection of transformers to apply.
    :return: An AudioSegment that has been processed with the given transformers.
    """
    beats = list(beats_of(audio, bpm))

    for song_effect in song_effects:
        beats = song_effect(beats)

    return sum(beats)
