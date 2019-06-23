from typing import Iterable, Generator

from pydub import AudioSegment

from beatmachine.effects.base import BaseEffect


def apply_effects(beats: Iterable[AudioSegment], effects: Iterable[BaseEffect]) -> Generator[AudioSegment, None, None]:
    for effect in effects:
        beats = effect(beats)

    yield from beats
