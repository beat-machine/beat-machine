import typing as t
import numpy as np
import dataclasses

class Backend(t.Protocol):
    def locate_beats(self, signal: np.ndarray, sample_rate: int) -> t.Iterable[int]:
        raise NotImplementedError()
