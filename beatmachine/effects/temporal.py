import random

from beatmachine.effects.base import BaseEffect, EffectABCMeta


class RandomizeAllBeats(BaseEffect, metaclass=EffectABCMeta):
    """
    An effect that randomizes the order of every single beat of a song.
    """

    __effect_name__ = "randomize"

    def __call__(self, beats):
        shuffled_beats = list(beats)
        random.shuffle(shuffled_beats)
        yield from shuffled_beats

    def __eq__(self, other):
        return isinstance(other, RandomizeAllBeats)


class SwapBeats(BaseEffect, metaclass=EffectABCMeta):
    """
    An effect that swaps every two specified beats. For example, specifying periods 2 and 4 would result in every
    second and fourth beats being swapped.
    """

    __effect_name__ = "swap"

    def __init__(self, *, x_period: int = 2, y_period: int = 4):
        if x_period < 1 or y_period < 1:
            raise ValueError(
                f"`swap` effect must have `x_period` and `y_period` both >= 1, "
                f"but got {x_period} and {y_period} respectively"
            )

        if x_period == y_period:
            raise ValueError(
                f"`swap` effect must have unique `x_period` and `y_period` values, "
                f"but both were {x_period}"
            )

        self.low_period = min(x_period, y_period)
        self.high_period = max(x_period, y_period)

    def __call__(self, beats):  # TODO: Creating a list of beats can probably be avoided
        beat_list = list(beats)

        for group_start in range(0, len(beat_list), self.high_period):
            group = beat_list[group_start : group_start + self.high_period]
            if len(group) == self.high_period:
                group[self.low_period - 1], group[self.high_period - 1] = (
                    group[self.high_period - 1],
                    group[self.low_period - 1],
                )

            yield from group

    def __eq__(self, other):
        return isinstance(other, SwapBeats) and (self.low_period, self.high_period) == (
            other.low_period,
            other.high_period,
        )
