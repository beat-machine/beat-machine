from ..effect_registry import EffectABCMeta, LoadableEffect


class ReverseAllBeats(LoadableEffect, metaclass=EffectABCMeta):
    """
    Reverses beat order, so the last beat of the song will play first, etc.
    """

    __effect_name__ = "reverseb"
    __effect_schema__ = {}

    def __call__(self, beats):
        beat_list = list(beats)
        beat_list.reverse()
        yield from beat_list

    def __eq__(self, other):
        return isinstance(other, ReverseAllBeats)
