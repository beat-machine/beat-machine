"""
The `temporal` module contains effects that modify beats by rearranging them over the entire song.
"""

import itertools
import random
from typing import Iterable, Generator, List, T

import numpy as np

from beatmachine.effects.base import LoadableEffect, EffectABCMeta


class RandomizeAllBeats(LoadableEffect, metaclass=EffectABCMeta):
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


def _chunks(iterable: Iterable[T], size: int = 10) -> Generator[List[T], None, None]:
    iterator = iter(iterable)
    for first in iterator:
        yield list(itertools.chain([first], itertools.islice(iterator, size - 1)))


class SwapBeats(LoadableEffect, metaclass=EffectABCMeta):
    """
    SwapBeats swaps every two specified beats. For example, specifying periods 2 and 4 would result in every second and
    fourth beats being swapped.
    """

    __effect_name__ = "swap"

    def __init__(
        self,
        *,
        x_period: int = 2,
        y_period: int = 4,
        group_size: int = 4,
        offset: int = 0,
    ):
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

        if offset < 0:
            raise ValueError(f"Offset must be >= 0, but was {offset}")

        self.low_period = (min(x_period, y_period) - 1) % group_size + 1
        self.high_period = (max(x_period, y_period) - 1) % group_size + 1
        self.group_size = group_size
        self.offset = offset

    def __call__(
        self, beats: Iterable[np.ndarray]
    ) -> Generator[np.ndarray, None, None]:
        beats = iter(beats)

        for _ in range(self.offset):
            yield next(beats)

        for group in _chunks(beats, self.group_size):
            if len(group) >= self.high_period:
                # Swap low and high beats
                (group[self.low_period - 1], group[self.high_period - 1]) = (
                    group[self.high_period - 1],
                    group[self.low_period - 1],
                )

            yield from group

    def __eq__(self, other):
        return isinstance(other, SwapBeats) and (self.low_period, self.high_period) == (
            other.low_period,
            other.high_period,
        )


class RemapBeats(LoadableEffect, metaclass=EffectABCMeta):
    """
    An effect that remaps beats based on a list of target indices. For example, a remap effect with mapping [0, 3, 2, 1]
    behaves identically to a swap effect with periods 2 and 4.
    """

    __effect_name__ = "remap"

    def __init__(self, *, mapping: List[int]):
        if any(m < 0 or m >= len(mapping) for m in mapping):
            raise ValueError(
                f"values of `remap` effect with {len(mapping)} values must be within range "
                f"[0, {len(mapping) - 1}], however the following values fall outside of it: "
                f"{[m for m in mapping if m < 0 or m >= len(mapping)]}"
            )

        self.mapping = mapping

    def __call__(
        self, beats: Iterable[np.ndarray]
    ) -> Generator[np.ndarray, None, None]:
        for group in _chunks(beats, len(self.mapping)):
            group_size = len(group)
            remapped_group = []

            for beat_idx in self.mapping:
                if beat_idx < group_size:
                    remapped_group.append(group[beat_idx])

            yield from remapped_group

    def __eq__(self, other):
        return isinstance(other, RemapBeats) and self.mapping == other.mapping
