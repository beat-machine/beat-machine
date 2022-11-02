import abc
from typing import Generator, List, Optional

import numpy as np

from beatmachine.effect_registry import LoadableEffect


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

    @abc.abstractmethod
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
