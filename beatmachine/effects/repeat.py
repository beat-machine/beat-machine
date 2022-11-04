import numpy as np

from ..effect_registry import EffectABCMeta
from .periodic import PeriodicEffect


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
            raise ValueError(f"Repeat effect must have `times` >= 2, but instead got {times}")
        super().__init__(period=period, offset=offset)

        self.times = times

    def process_beat(self, beat: np.ndarray) -> np.ndarray:
        return np.concatenate(self.times * [beat], axis=0)

    def __eq__(self, other):
        return super(RepeatEveryNth, self).__eq__(other) and self.times == other.times
