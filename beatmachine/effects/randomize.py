import random

from ..effect_registry import EffectABCMeta, LoadableEffect


class RandomizeAllBeats(LoadableEffect, metaclass=EffectABCMeta):
    """
    Completely randomize the order of every single beat.
    """

    __effect_name__ = "randomize"
    __effect_schema__ = {}

    def __call__(self, beats):
        shuffled_beats = list(beats)
        random.shuffle(shuffled_beats)
        yield from shuffled_beats

    def __eq__(self, other):
        return isinstance(other, RandomizeAllBeats)
