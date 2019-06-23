from typing import BinaryIO, Union, Generator

import numpy
import pydub
from madmom.audio import Signal
from madmom.features import DBNBeatTrackingProcessor, RNNBeatProcessor
from pydub import AudioSegment


def load_beats_by_signal(fp: Union[str, BinaryIO], audio_format: str = 'mp3', min_bpm: int = 60, max_bpm: int = 300,
                         fps: int = 100) -> Generator[AudioSegment, None, None]:
    """
    A generator that loads beats based on audio data itself, handling variations in tempo.

    :param fp: Path to or file-like object of the audio to load.
    :param audio_format: Audio data format.
    :param min_bpm: Minimum permissible BPM.
    :param max_bpm: Maximum permissible BPM.
    :param fps: Resolution to process beats at.
    :return: A generator yielding each beat of the input song as a PyDub AudioSegment. Note that the initial
             beat-finding process is comparatively time-consuming and can take up to a few minutes for longer songs.
    """

    tracker = DBNBeatTrackingProcessor(min_bpm=min_bpm, max_bpm=max_bpm, fps=fps)
    processor = RNNBeatProcessor()
    times = tracker(processor(Signal(fp)))

    audio = pydub.AudioSegment.from_file(fp, format=audio_format)

    last_time_s = 0
    for i, time_s in numpy.ndenumerate(times):
        yield audio[int(last_time_s * 1000):int(time_s * 1000)]
        last_time_s = time_s


def load_beats_by_bpm(fp: Union[str, BinaryIO], bpm: int, audio_format: str = 'mp3') -> \
        Generator[AudioSegment, None, None]:
    """
    A generator that loads beats strictly by a given BPM assuming no fluctuations in tempo. Significantly faster than
    `load_beats_by_signal` however can be less accurate, especially in live performances.

    :param fp: Path to or file-like object of the audio to load.
    :param bpm: Song BPM. This can sometimes be found online.
    :param audio_format: Audio data format.
    :return: A generator yielding each beat of the input song as a PyDub AudioSegment.
    """
    audio = pydub.AudioSegment.from_file(fp, format=audio_format)
    beat_size_ms = 60_000 // bpm
    for beat_start_ms in range(0, len(audio), beat_size_ms):
        yield audio[beat_start_ms:beat_start_ms + beat_size_ms]
