import typing as t
import glob

import numpy as np

from madmom.audio import Signal
from madmom.features.beats import DBNBeatTrackingProcessor, RNNBeatProcessor
from madmom.models import MODEL_PATH as MADMOM_MODEL_PATH

from ..backend import Backend


class MadmomDbnBackend(Backend):
    def __init__(self, min_bpm: int = 60, max_bpm: int = 300, fps: int = 100, model_count: int = 8) -> None:
        super().__init__()
        self.min_bpm = min_bpm
        self.max_bpm = max_bpm
        self.fps = fps
        self.model_count = model_count

    def _get_nn_files(self) -> t.Iterable[str]:
        return sorted(glob.glob(f'{MADMOM_MODEL_PATH}/beats/2015/beats_blstm_[1-{self.model_count}].pkl'))

    def locate_beats(self, signal: np.ndarray, sr: int = 44100) -> t.Iterable[int]:
        madmom_signal = Signal(signal, sr)
        tracker = DBNBeatTrackingProcessor(min_bpm=self.min_bpm, max_bpm=self.max_bpm, fps=self.fps)
        processor = RNNBeatProcessor(nn_files=self._get_nn_files())
        # tracker returns positions in sec
        return (tracker(processor(madmom_signal)) * madmom_signal.sample_rate).astype(np.int64)
