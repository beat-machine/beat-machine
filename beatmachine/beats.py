import dataclasses
import subprocess
import typing as t
from functools import reduce

import numpy as np
import soundfile as sf

from .backend import Backend
from .backends.madmom import MadmomDbnBackend
from .effect_registry import Effect


@dataclasses.dataclass
class PreprocessOpts:
    downmix: bool = False  # Downmix to mono before processing
    resample: t.Optional[int] = None  # Resample to the given sample rate before processing


_DEFAULT_BACKEND = MadmomDbnBackend(model_count=4)
_DEFAULT_PREPROCESS_OPTS = PreprocessOpts(downmix=True, resample=11000)


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
    def from_song(
        fp: t.Union[str, t.BinaryIO], backend: Backend = None, preprocess_opts: PreprocessOpts = None
    ) -> "Beats":
        backend = backend or _DEFAULT_BACKEND
        preprocess_opts = preprocess_opts or _DEFAULT_PREPROCESS_OPTS

        signal, sample_rate = sf.read(fp, dtype="float64")
        channels = 1
        if len(signal.shape) >= 1:
            channels = signal.shape[1]

        detection_signal = signal
        detection_sample_rate = sample_rate

        if preprocess_opts.downmix:
            detection_signal = np.mean(detection_signal, 1)

        if preprocess_opts.resample:
            detection_sample_rate = preprocess_opts.resample
            length = detection_signal.shape[0]
            original_t = np.arange(length)
            resample_t = np.linspace(0, length, int(length / sample_rate * detection_sample_rate))
            def interp(a):
                return np.interp(resample_t, original_t, a)
            detection_signal = np.apply_along_axis(interp, 0, detection_signal)

        beat_locations = np.array(backend.locate_beats(detection_signal, detection_sample_rate))
        beat_locations = (beat_locations / detection_sample_rate * sample_rate).astype(np.int64)

        print(sample_rate, channels, beat_locations)
        return Beats(sample_rate, channels, np.split(signal, beat_locations))
