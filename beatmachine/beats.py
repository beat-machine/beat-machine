import subprocess
from functools import reduce
from typing import List, BinaryIO, Union

import numpy as np

from . import loader, effects


class Beats:
    """
    The Beats class is a convenient immutable wrapper for applying effects to songs.
    """

    _sr: int
    _channels: int
    _beats: List[np.ndarray]

    def __init__(self, sr: int, channels: int, beats: List[np.ndarray]):
        self._sr = sr
        self._channels = channels
        self._beats = beats

    def apply(self, effect: effects.base.Effect) -> "Beats":
        """
        Applies a single effect and returns a new Beats object.

        :param effect: Effect to apply.
        :return: A new Beats object with the given effect applied.
        """
        return Beats(self._sr, self._channels, list(effect(self._beats)))

    def apply_all(self, *effects_list: List[effects.base.Effect]) -> "Beats":
        """
        Applies a list of effects and returns a new Beats object.
        This is the best way to apply multiple effects, since it only collects
        them into a list at the very end.

        :param effects_list: Effects to apply in order.
        :return: A new Beats object with the given effects applied.
        """
        return Beats(
            self._sr,
            reduce(lambda beats, effect: effect(beats), effects_list, self._beats),
        )

    def to_ndarray(self) -> np.ndarray:
        """
        Consolidates this Beats object into an array with shape (samples, channels).

        :return: An ndarray with shape (samples, channels).
        """
        return np.concatenate(list(self._beats), axis=0)

    def save(self, filename: str, extra_ffmpeg_args: List[str] = None):
        extra_ffmpeg_args = extra_ffmpeg_args or []
        p = subprocess.Popen(
            [
                # fmt: off
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "panic",
                "-y",
                "-f", "s16le",
                "-ar", str(self._sr),
                "-ac", str(self._channels),
                "-i", "-",
                *extra_ffmpeg_args,
                filename,
                # fmt: on
            ],
            stdin=subprocess.PIPE,
        )
        p.communicate(input=self.to_ndarray().tobytes())
        p.stdin.close()
        p.wait()

    @property
    def sr(self):
        """
        :return: Audio sample rate.
        """
        return self._sr

    @property
    def channels(self):
        """
        :return: Number of audio channels.
        """
        return self._channels

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
        sr, channels, beats = beat_loader(path_or_fp)
        return Beats(sr, channels, list(beats))
