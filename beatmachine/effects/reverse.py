import numpy as np

from ..effect_registry import EffectABCMeta
from .periodic import PeriodicEffect


class ReverseEveryNth(PeriodicEffect, metaclass=EffectABCMeta):
    """
    Reverse beats.
    """

    __effect_name__ = "reverse"

    def process_beat(self, beat: np.ndarray) -> np.ndarray:
        return np.flip(beat)
