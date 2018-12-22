import random


def every_nth_beat(n, beat_effect):
    """
    Returns a song effect based on the given beat effect, only applying to beats that are a multiple of n. Beat counting
    starts at 1, so the first beat of the song would not be matched when n = 2.

    :param n: The factor to filter beats by.
    :param beat_effect: The function to apply every nth beat.
    :return: A song effect that applies the given function to every nth beat of the song.
    """
    if n <= 0:
        raise ValueError('Invalid value of n for nth beat effect: ' + n)

    def song_effect(beats):
        modified_beats = []
        for i, beat in enumerate(beats):
            result = beat_effect(beat) if (i + 1) % n == 0 else beat
            if result is not None:
                modified_beats.append(result)
        return modified_beats

    return song_effect


def every_beat(beat_effect):
    """
    Returns a song effect that applies to every beat based on the given beat effect.
    :param beat_effect: The function to apply to every beat.
    :return: A song effect that applies the given function to every beat of the song.
    """
    return every_nth_beat(1, beat_effect)


def randomize_all(beats):
    """
    Randomizes the position of every given beat.
    :param beats: Beats to randomize.
    :return: The given beats in random order.
    """
    return random.shuffle(beats)


def sort_by_loudness(beats):
    """
    Sorts the given beats by loudness.

    I thought this would be more interesting, but oh well...

    :param beats: Beats to sort.
    :return: The given beats, sorted by average loudness.
    """
    return sorted(beats, key=lambda b: b.dBFS)


def sort_by_average_frequency(beats):
    """
    Sorts the given beats by average frequency.

    I also thought this one would be more interesting. :(

    :param beats: Beats to sort.
    :return: The given beats, sorted by average frequency.
    """
    return sorted(beats, key=lambda b: sum(b.raw_data) / len(b.raw_data))


def swap_beats(x, y):
    """
    Returns a song effect that swaps every xth and yth beat. As with every_nth_beat, beat numbering starts at 1.

    For example, pretend we have a list of beats [A, B, C, D]. Swapping every 2nd with every 4th beat would result in
    the list [A, D, C, B].

    :param x: First beat to swap. Must be less than y.
    :param y: Second beat to swap.
    :return: A song effect that swaps every xth and yth beat.
    """
    if x >= y:
        raise ValueError('First beat swap parameter must be less than the second!')

    if x <= 0 or y <= 0:
        raise ValueError(f'Invalid beat swap values: x={x}, y={y}')

    def song_effect(beats):
        result = []
        for group_start in range(0, len(beats), y):
            group = beats[group_start:group_start + y]
            if len(group) == y:
                group[x - 1], group[y - 1] = group[y - 1], group[x - 1]
            result.extend(group)
        return result

    return song_effect
