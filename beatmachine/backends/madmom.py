import typing as t

import numpy as np
from madmom.audio import Signal
from madmom.features import DBNBeatTrackingProcessor, RNNBeatProcessor

from ..backend import Backend

class MadmomDbnBackend(Backend):
    def __init__(self, min_bpm: int = 60, max_bpm: int = 300, fps: int = 100) -> None:
        super().__init__()
        self.min_bpm = min_bpm
        self.max_bpm = max_bpm
        self.fps = fps

    def locate_beats(self, signal: np.ndarray, sr: int = 44100) -> t.Iterable[int]:
        madmom_signal = Signal(signal, sr)
        tracker = DBNBeatTrackingProcessor(min_bpm=self.min_bpm, max_bpm=self.max_bpm, fps=self.fps)
        processor = RNNBeatProcessor()
        # tracker returns positions in sec
        return (tracker(processor(madmom_signal)) * madmom_signal.sample_rate).astype(np.int64)
