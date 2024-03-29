import subprocess
import typing as t
from functools import reduce
from pathlib import Path

import numpy as np
from madmom.audio import Signal

from .backend import Backend
from .backends.madmom import MadmomDbnBackend
from .effect_registry import Effect

_DEFAULT_BACKEND = MadmomDbnBackend(model_count=4)  # TODO: 2 might be sufficient, test more


def _load_audio(path: Path) -> t.Tuple[int, np.array]:
    # TODO: Revisit python-soundfile once it bundles a recent version of libsndfile on linux:
    #       https://github.com/bastibe/python-soundfile/issues/353. (Most distros still have a libsndfile version
    #       that doesn't support MP3. Users could always build from source but we don't want that to be a requirement.)
    s = Signal(str(path), sample_rate=None, num_channels=None, dtype=np.float64)
    return s, s.sample_rate


class Beats:
    """
    The Beats class is a convenient immutable wrapper for applying effects to songs.
    """

    _sample_rate: int
    _channels: int
    _beats: t.List[np.ndarray]

    def __init__(self, sample_rate: int, channels: int, beats: t.List[np.ndarray]):
        self._sample_rate = sample_rate
        self._channels = channels
        self._beats = beats

    def apply(self, effect: Effect) -> "Beats":
        """
        Applies a single effect and returns a new Beats object.

        :param effect: Effect to apply.
        :return: A new Beats object with the given effect applied.
        """
        return Beats(self._sample_rate, self._channels, list(effect(self._beats)))

    def apply_all(self, *effects_list: t.List[Effect]) -> "Beats":
        """
        Applies a list of effects and returns a new Beats object.
        This is the best way to apply multiple effects, since it only collects
        them into a list at the very end.

        :param effects_list: Effects to apply in order.
        :return: A new Beats object with the given effects applied.
        """
        return Beats(
            self._sample_rate,
            self._channels,
            reduce(lambda beats, effect: effect(beats), effects_list, self._beats),
        )

    def to_ndarray(self) -> np.ndarray:
        """
        Consolidates this Beats object into an array with shape (samples, channels).

        :return: An ndarray with shape (samples, channels).
        """
        return np.concatenate(list(self._beats), axis=0)

    def _create_ffmpeg_command(self, dst: str, out_format: str = None, extra_args: t.List[str] = None):
        cmd = [
            # fmt: off
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "panic",
            "-y",
            "-f", "f64le",
            "-ar", str(self._sample_rate),
            "-ac", str(self._channels),
            "-i", "-",
            # fmt: on
        ]

        if out_format is not None:
            cmd.extend(["-f", out_format])

        if extra_args is not None:
            cmd.extend(extra_args)

        cmd.append(dst)
        return cmd

    def _save_to_file(self, filename: str, out_format: str = None, extra_ffmpeg_args: t.List[str] = None):
        p = subprocess.Popen(
            self._create_ffmpeg_command(filename, out_format, extra_ffmpeg_args),
            stdin=subprocess.PIPE,
        )
        p.communicate(input=self.to_ndarray().tobytes())
        p.stdin.close()
        p.wait()

    def _save_to_binary_io(self, fp: t.BinaryIO, out_format: str = None, extra_ffmpeg_args: t.List[str] = None):
        if not out_format:
            raise ValueError("out_format is required when writing to file-like object")

        p = subprocess.Popen(
            self._create_ffmpeg_command("pipe:", out_format, extra_ffmpeg_args),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        stdout, _ = p.communicate(input=self.to_ndarray().tobytes())
        p.stdin.close()
        p.wait()

        return fp.write(stdout)

    def save(self, fp, out_format=None, extra_ffmpeg_args: t.List[str] = None):
        if isinstance(fp, str):
            return self._save_to_file(fp, out_format, extra_ffmpeg_args)
        else:
            return self._save_to_binary_io(fp, out_format, extra_ffmpeg_args)

    @property
    def sample_rate(self):
        """
        :return: Audio sample rate.
        """
        return self._sample_rate

    @property
    def channels(self):
        """
        :return: Number of audio channels.
        """
        return self._channels

    @staticmethod
    def from_song(fp: t.Union[str, t.BinaryIO], backend: Backend = None) -> "Beats":
        backend = backend or _DEFAULT_BACKEND

        signal, sample_rate = _load_audio(fp)

        channels = 1
        if len(signal.shape) >= 1:
            channels = signal.shape[1]

        beat_locations = np.array(backend.locate_beats(signal, sample_rate)).astype(np.int64)

        return Beats(sample_rate, channels, np.split(signal, beat_locations))
