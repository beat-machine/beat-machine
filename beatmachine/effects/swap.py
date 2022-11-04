from typing import Generator, Iterable

import numpy as np

from ..effect_registry import EffectABCMeta, LoadableEffect
from ..utils import chunks


class SwapBeats(LoadableEffect, metaclass=EffectABCMeta):
    """
    Swap two beats, indicated by X and Y, every set number of beats.
    For example, X = 2 Y = 4, Group = 4 results in a "beats 2 and 4 are swapped" effect. Periods cannot be equal.
    """

    __effect_name__ = "swap"
    __effect_schema__ = {
        "x_period": {
            "type": "number",
            "minimum": 1,
            "default": 2,
            "title": "X",
            "description": "First beat to swap, starting at 1.",
        },
        "y_period": {
            "type": "number",
            "minimum": 1,
            "default": 4,
            "title": "Y",
            "description": "Second beat to swap, starting at 1 and not equal to X.",
        },
        "group_size": {
            "type": "number",
            "minimum": 4,
            "default": 4,
            "title": "Group",
            "description": "Beats per measure, or how many beats to wait before swapping again.",
        },
        "offset": {
            "type": "number",
            "minimum": 0,
            "default": 0,
            "title": "Offset",
            "description": "How many beats to wait before the first swap.",
        },
    }

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
                f"`swap` effect must have unique `x_period` and `y_period` values, " f"but both were {x_period}"
            )

        if offset < 0:
            raise ValueError(f"Offset must be >= 0, but was {offset}")

        # Historical bad decision: x/y periods were 1-indexed
        x_period_index = (x_period - 1) % group_size
        y_period_index = (y_period - 1) % group_size

        self.low_period = min(x_period_index, y_period_index)
        self.high_period = max(x_period_index, y_period_index)

        self.group_size = group_size
        self.offset = offset

    def __call__(self, beats: Iterable[np.ndarray]) -> Generator[np.ndarray, None, None]:
        beats = iter(beats)

        for _ in range(self.offset):
            yield next(beats)

        for group in chunks(beats, self.group_size):
            if len(group) > self.high_period:
                # Swap low and high beats
                (group[self.low_period], group[self.high_period]) = (
                    group[self.high_period],
                    group[self.low_period],
                )

            yield from group

    def __eq__(self, other):
        return (
            isinstance(other, SwapBeats)
            and self.low_period == other.low_period
            and self.high_period == other.high_period
            and self.group_size == other.group_size
            and self.offset == other.offset
        )
