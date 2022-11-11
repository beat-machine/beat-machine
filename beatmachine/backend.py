import typing as t

import numpy as np


class Backend(t.Protocol):
    def locate_beats(self, signal: np.ndarray, sample_rate: int) -> np.ndarray:
        raise NotImplementedError()
