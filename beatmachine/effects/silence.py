import numpy as np

from ..effect_registry import EffectABCMeta
from .periodic import PeriodicEffect


class SilenceEveryNth(PeriodicEffect, metaclass=EffectABCMeta):
    """
    Silence beats, retaining their lengths.
    """

    __effect_name__ = "silence"

    def __init__(self, *, period: int = 1, offset: int = 0):
        super().__init__(period=period, offset=offset)

    def process_beat(self, beat: np.ndarray) -> np.ndarray:
        return np.zeros(np.shape(beat), dtype="int16")
