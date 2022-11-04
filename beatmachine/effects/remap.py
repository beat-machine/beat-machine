from typing import Generator, Iterable, List

import numpy as np

from ..effect_registry import EffectABCMeta, LoadableEffect
from ..utils import chunks


class RemapBeats(LoadableEffect, metaclass=EffectABCMeta):
    """
    An effect that remaps beats based on a list of target indices. For example, a remap effect with mapping [0, 3, 2, 1]
    behaves identically to a swap effect with periods 2 and 4.

    Most effects can be emulated through Remap.
    """

    __effect_name__ = "remap"
    __effect_schema__ = {
        "mapping": {
            "type": "array",
            "items": {"type": "number"},
            "title": "Mapping",
            "description": "New order of beats, starting at 0. For example, the mapping [0, 3, 2, 1] swaps beats 2 and 4 every 4 beats. The mapping [0, 1, 1, 1] replaces beats 3 and 4 with beat 2.",
        }
    }

    def __init__(self, *, mapping: List[int]):
        if any(m < 0 or m >= len(mapping) for m in mapping):
            raise ValueError(
                f"values of `remap` effect with {len(mapping)} values must be within range "
                f"[0, {len(mapping) - 1}], however the following values fall outside of it: "
                f"{[m for m in mapping if m < 0 or m >= len(mapping)]}"
            )

        self.mapping = mapping

    def __call__(self, beats: Iterable[np.ndarray]) -> Generator[np.ndarray, None, None]:
        for group in chunks(beats, len(self.mapping)):
            group_size = len(group)
            remapped_group = []

            for beat_idx in self.mapping:
                if beat_idx < group_size:
                    remapped_group.append(group[beat_idx])

            yield from remapped_group

    def __eq__(self, other):
        return isinstance(other, RemapBeats) and self.mapping == other.mapping
