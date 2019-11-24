"""
The ``editor`` module contains high-level beat editing functions.
"""

from typing import Iterable, Generator
from pydub import AudioSegment
from beatmachine.effects.base import BaseEffect


def apply_effects(
    beats: Iterable[AudioSegment], effects: Iterable[BaseEffect]
) -> Generator[AudioSegment, None, None]:
    """
    Applies a collection of effects to a song represented by a collection of beats.

    :param beats: Beats to apply the given effects to
    :param effects: Effects to apply to the song
    :return: A generator yielding beats with the given effects applied
    """
    for effect in effects:
        beats = effect(beats)

    yield from beats
