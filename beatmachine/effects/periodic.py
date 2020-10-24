"""
The `periodic` module contains effects that update beats independently of others at regular intervals, i.e. removing
every other beat.
"""

import abc
from typing import Optional, List, Generator

import numpy as np

from beatmachine.effects.base import LoadableEffect, EffectABCMeta


class PeriodicEffect(LoadableEffect, abc.ABC):
    """
    A PeriodicEffect is an effect that gets applied to beats at a fixed interval, i.e. every other beat. A
    PeriodicEffect with a period of 1 gets applied to every single beat.
    """

    __effect_schema__ = {
        "period": {
            "type": "integer",
            "minimum": 1,
            "default": 1,
            "title": "Period",
            "description": "How often to apply this effect.",
        },
        "offset": {
            "type": "integer",
            "minimum": 0,
            "default": 0,
            "title": "Offset",
            "description": "How many beats to wait before applying this effect.",
        },
    }

    def __init__(self, *, period: int = 1, offset: int = 0):
        """
        :param period: Period (>= 1) to apply this effect on
        :param offset: How many beats to wait before applying this effect every ``period`` beats
        """
        if period <= 0:
            raise ValueError(f"Effect period must be > 0, but was {period}")

        if offset < 0:
            raise ValueError(f"Offset must be >= 0, but was {offset}")

        self.period = period
        self.offset = offset

    def process_beat(self, beat: np.ndarray) -> Optional[np.ndarray]:
        """
        Processes a single beat.

        :param beat: Beat to process.
        :return: Updated beat or None if it should be removed.
        """
        raise NotImplementedError

    def __call__(self, beats: List[np.ndarray]) -> Generator[np.ndarray, None, None]:
        for i, beat in enumerate(beats):
            if i < self.offset:
                yield beat
            else:
                i -= self.offset
                result = self.process_beat(beat) if (i - 1) % self.period == 0 else beat
                if result is not None:
                    yield result

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.period == other.period


class SilenceEveryNth(PeriodicEffect, metaclass=EffectABCMeta):
    """
    Silence beats, retaining their lengths.
    """

    __effect_name__ = "silence"

    def __init__(self, *, period: int = 1, offset: int = 0):
        super().__init__(period=period, offset=offset)

    def process_beat(self, beat: np.ndarray) -> np.ndarray:
        return np.zeros(np.shape(beat), dtype="int16")


class RemoveEveryNth(PeriodicEffect, metaclass=EffectABCMeta):
    """
    Completely remove beats.
    """

    __effect_name__ = "remove"
    __effect_schema__ = {
        "period": {
            "type": "integer",
            "minimum": 2,
            "default": 2,
            "title": "Period",
            "description": "How often to apply this effect. For Remove, this must be at least 2.",
        },
        "offset": {
            "type": "integer",
            "minimum": 0,
            "default": 0,
            "title": "Offset",
            "description": "How many beats to wait before applying this effect.",
        },
    }

    def __init__(self, *, period: int = 2, offset: int = 0):
        if period < 2:
            raise ValueError(f"`remove` effect period must be >= 2, but was {period}")
        super().__init__(period=period, offset=offset)

    def process_beat(self, beat: np.ndarray) -> Optional[np.ndarray]:
        return None


class CutEveryNth(PeriodicEffect, metaclass=EffectABCMeta):
    """
    Keeps one piece of each beat. For example, Denominator = 2, Take = 0 takes the first half and Denominator = 2, Take = 1 keeps the second half.
    """

    __effect_name__ = "cut"
    __effect_schema__ = {
        **PeriodicEffect.__effect_schema__,
        "denominator": {
            "type": "integer",
            "minimum": 2,
            "default": 2,
            "title": "Denominator",
            "description": "How many pieces to cut each beat into.",
        },
        "take_index": {
            "type": "integer",
            "minimum": 0,
            "default": 0,
            "title": "Take",
            "description": "Which piece, starting at 0, to keep.",
        },
    }

    def __init__(
        self,
        *,
        period: int = 1,
        denominator: int = 2,
        take_index: int = 0,
        offset: int = 0,
    ):
        super().__init__(period=period, offset=offset)
        self.denominator = denominator
        self.take_index = take_index

    def process_beat(self, beat: np.ndarray) -> np.ndarray:
        size = len(beat) // self.denominator
        offset = self.take_index * size
        return beat[offset : offset + size, ...]

    def __eq__(self, other):
        return (
            isinstance(other, CutEveryNth)
            and other.period == self.period
            and other.denominator == self.denominator
            and other.take_index == self.take_index
        )


class ReverseEveryNth(PeriodicEffect, metaclass=EffectABCMeta):
    """
    Reverse beats.
    """

    __effect_name__ = "reverse"

    def process_beat(self, beat: np.ndarray) -> np.ndarray:
        return np.flip(beat)


class RepeatEveryNth(PeriodicEffect, metaclass=EffectABCMeta):
    """
    Repeat beats.
    """

    __effect_name__ = "repeat"
    __effect_schema__ = {
        **PeriodicEffect.__effect_schema__,
        "times": {
            "type": "number",
            "minimum": 2,
            "default": 2,
            "title": "How many times each affected beat should be played. Must be at least 2, because a value of 1 would do nothing.",
        },
    }

    def __init__(self, *, period: int = 1, offset: int = 0, times: int = 2):
        if times < 2:
            raise ValueError(
                f"Repeat effect must have `times` >= 2, but instead got {times}"
            )
        super().__init__(period=period, offset=offset)

        self.times = times

    def process_beat(self, beat: np.ndarray) -> np.ndarray:
        return np.concatenate(self.times * [beat], axis=0)

    def __eq__(self, other):
        return super(RepeatEveryNth, self).__eq__(other) and self.times == other.times
