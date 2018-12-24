import random

from beatmachine.registry import loadable


@loadable('randomize')
class RandomizeAllBeats:
    """
    An effect that randomizes the order of every single beat of a song.
    """

    def __call__(self, beats):
        shuffled_beats = beats.copy()
        random.shuffle(shuffled_beats)
        yield from shuffled_beats

    def __eq__(self, other):
        return isinstance(other, RandomizeAllBeats)


@loadable('swap', required_parameters={'x_period': int, 'y_period': int})
class SwapBeats:
    """
    An effect that swaps every two specified beats. For example, specifying periods 2 and 4 would result in every
    second and fourth beats being swapped.
    """

    def __init__(self, x_period, y_period):
        if x_period <= 1 or y_period <= 1:
            raise ValueError('Attempted to create a SwapBeats effect where one or more periods are <= 1')

        if x_period == y_period:
            raise ValueError('Attempted to create a SwapBeats effect that swaps a beat with itself')

        self.low_period = min(x_period, y_period)
        self.high_period = max(x_period, y_period)

    def __call__(self, beats):
        for group_start in range(0, len(beats), self.high_period):
            group = beats[group_start:group_start + self.high_period]
            if len(group) == self.high_period:
                group[self.low_period - 1], group[self.high_period - 1] = group[self.high_period - 1], group[
                    self.low_period - 1]

            yield from group

    def __eq__(self, other):
        return isinstance(other, SwapBeats) and \
               (self.low_period, self.high_period) == (other.low_period, other.high_period)
