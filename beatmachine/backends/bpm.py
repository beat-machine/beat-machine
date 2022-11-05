import typing as t

import numpy as np

from ..backend import Backend

class BpmBackend(Backend):
    def __init__(self, bpm: float, downbeat_ms: float) -> None:
        super().__init__()
        self.bpm = bpm
        self.downbeat_ms = downbeat_ms

    def locate_beats(self, signal: np.ndarray, sample_rate: int) -> t.Iterable[int]:
        samples_per_beat = int((60 * sample_rate) / self.bpm)
        downbeat_sample = int(sample_rate * 1000 * self.downbeat_ms)
        return np.arange(downbeat_sample, signal.shape[0], samples_per_beat)
