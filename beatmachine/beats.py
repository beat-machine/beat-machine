import subprocess
from functools import reduce
from typing import List, BinaryIO, Union, Iterable

import numpy as np
import soundfile

from . import loader, effects


class Beats:
    """
    The Beats class is a convenient immutable wrapper for applying effects to songs.
    """

    _sr: int
    _beats: Iterable[np.ndarray]

    def __init__(self, sr: int, beats: Iterable[np.ndarray]):
        self._sr = sr
        self._beats = beats

    def apply(self, effect: effects.base.Effect) -> "Beats":
        """
        Applies a single effect and returns a new Beats object.

        :param effect: Effect to apply.
        :return: A new Beats object with the given effect applied.
        """
        return Beats(self._sr, effect(self._beats))

    def apply_all(self, *effects_list: List[effects.base.Effect]) -> "Beats":
        """
        Applies a list of effects and returns a new Beats object.

        :param effects_list: Effects to apply in order.
        :return: A new Beats object with the given effects applied.
        """
        return reduce(lambda beats, effect: beats.apply(effect), effects_list, self)

    def to_ndarray(self) -> np.ndarray:
        """
        Consolidates this Beats object into an array.

        :return: A PyDub AudioSegment formed from this Beats object.
        """
        return np.concatenate(list(self._beats))

    def save(self, filename: str, extra_ffmpeg_args: List[str] = None):
        extra_ffmpeg_args = extra_ffmpeg_args or []
        p = subprocess.Popen(
            [
                'ffmpeg',
                '-y',
                '-f', 'wav',
                '-i', '-',
                *extra_ffmpeg_args,
                filename
            ], stdin=subprocess.PIPE
        )

        soundfile.write(p.stdin, self.to_ndarray(), samplerate=self._sr, format='wav')
        p.stdin.close()
        p.wait()

    @property
    def sr(self):
        """
        :return: The sample rate of the audio in this Beats object.
        """
        return self._sr

    @staticmethod
    def from_song(
            path_or_fp: Union[str, BinaryIO],
            beat_loader: loader.BeatLoader = loader.load_beats_by_signal,
    ) -> "Beats":
        """
        Loads a song as a Beats object.

        :param path_or_fp: Path or file-like object to load from.
        :param beat_loader: Callable to load and split the given path/file-like object into beats.
        """
        sr, beats = beat_loader(path_or_fp)
        return Beats(sr, beats)
