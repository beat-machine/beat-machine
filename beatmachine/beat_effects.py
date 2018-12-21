from pydub import AudioSegment


def replace_with_silence(beat):
    """
    Replaces a beat with silence.

    :param beat: Beat to transform.
    :return: Silence of the same length as the given audio.
    """
    return AudioSegment.silent(len(beat))


def remove(_):
    """
    "Removes" a beat by returning None.

    :param _: Beat to transform.
    :return: Always None.
    """
    return None


def cut_in_half(beat):
    """
    Returns the first half of a beat.

    :param beat: Beat to transform.
    :return: A beat with the same index but only the first half of its audio.
    """
    result = beat[:(len(beat) // 2)]
    return result


def reverse(beat):
    """
    Reverses a given beat.

    :param beat: Beat to transform.
    :return: A reversed version of the given beat.
    """
    return beat.reverse()
