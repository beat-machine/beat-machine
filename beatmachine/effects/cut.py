import numpy as np

from ..effect_registry import EffectABCMeta
from .periodic import PeriodicEffect


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
