import numpy as np


class BpmBackend:
    def __init__(self, bpm: float, first_beat_ms: float) -> None:
        super().__init__()
        self.bpm = bpm
        self.first_beat_ms = first_beat_ms

    def locate_beats(self, signal: np.ndarray, sample_rate: int) -> np.ndarray:
        samples_per_beat = int((60 * sample_rate) / self.bpm)
        downbeat_sample = int(sample_rate * 1000 * self.first_beat_ms)
        return np.arange(downbeat_sample, signal.shape[0], samples_per_beat)
