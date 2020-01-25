from . import loader, effects
from typing import List, Callable, BinaryIO, Generator, Union
from pydub import AudioSegment
from functools import reduce


class Beats:
    """
    The Beats class is a convenient immutable wrapper for applying effects to songs.
    """

    _beats: List[AudioSegment]

    def __init__(self, beats: List[AudioSegment]):
        self._beats = beats

    def apply(self, effect: effects.base.BaseEffect) -> "Beats":
        """
        Applies a single effect and returns a new Beats object.

        :param effect: Effect to apply.
        :return: A new Beats object with the given effect applied.
        """
        return Beats(effect(self._beats))

    def apply_all(self, *effects: List[effects.base.BaseEffect]) -> "Beats":
        """
        Applies a list of effects and returns a new Beats object.

        :param effects: Effects to apply in order.
        :return: A new Beats object with the given effects applied.
        """
        return reduce(lambda beats, effect: beats.apply(effect), effects, self)

    def consolidate(self) -> AudioSegment:
        """
        Consolidates this Beats object into a PyDub AudioSegment.

        :return: A PyDub AudioSegment formed from this Beats object.
        """
        return sum(self._beats)

    @staticmethod
    def from_song(
        path_or_fp: Union[str, BinaryIO],
        loader: Callable[
            [BinaryIO], Generator[AudioSegment, None, None]
        ] = loader.load_beats_by_signal,
    ) -> "Beats":
        """
        Loads a song as a Beats object.

        :param path_or_fp: Path or file-like object to load from.
        :param loader: Callable to load and split the given path/file-like object into beats.
        """
        return Beats(list(loader(path_or_fp)))
