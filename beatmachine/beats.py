from __future__ import annotations

from . import loader, effects
from typing import List, Callable, BinaryIO, Generator, Union
from pydub import AudioSegment


class Beats:
    """
    The Beats class provides a convenient wrapper for most common functions
    involving songs.
    """

    _beats: List[AudioSegment]

    def __init__(self, beats: List[AudioSegment]):
        self._beats = beats

    def apply_effect(self, effect: effects.base.BaseEffect) -> Beats:
        return Beats(effect(self._beats))

    def consolidate(self) -> AudioSegment:
        return sum(self._beats)

    @staticmethod
    def from_song(
        path_or_fp: Union[str, BinaryIO],
        loader: Callable[
            [BinaryIO], Generator[AudioSegment, None, None]
        ] = loader.load_beats_by_signal,
    ) -> Beats:
        return Beats(list(loader(path_or_fp)))
