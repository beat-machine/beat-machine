from abc import ABC, abstractmethod
from pydub import AudioSegment

from beatmachine.effect_loader import register_effect


class PeriodicEffect(ABC):
    """
    A PeriodicEffect is an effect that gets applied to beats at a fixed interval, i.e. every other beat. A
    PeriodicEffect with a period of 1 gets applied to every single beat.
    """

    def __init__(self, period=1):
        """
        Initializes this PeriodicEffect.
        :param period: Period of applying this effect to beats. Beats whose indices (starting at 1) are multiples of
                       this value will have the effect applied to them.
        """
        if period <= 0:
            raise ValueError(f'Invalid period {period} for periodic effect')

        self.period = period

    @abstractmethod
    def apply_effect_to_beat(self, beat_audio):
        """
        Applies this PeriodicEffect to a single beat.
        :param beat_audio: Single beat to apply this effect to.
        :return: Beat audio with the effect applied.
        """
        raise NotImplementedError

    def __call__(self, beats):
        """
        Applies this PeriodicEffect to a song, represented as a list of AudioSegments (each beat).
        :param beats: Song as a list of beats to apply this PeriodicEffect to.
        :return: A generator yielding beats of the modified song.
        """
        if self.period > len(beats):
            yield from beats
        elif self.period == 1:
            yield from map(self.apply_effect_to_beat, beats)
        else:
            for i, beat in enumerate(beats):
                result = self.apply_effect_to_beat(beat) if (i - 1) % self.period == 0 else beat
                if result is not None:
                    yield result

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.period == other.period


@register_effect('silence', optional_parameters={'period': int})
class SilenceEveryNth(PeriodicEffect):
    """
    A periodic effect that silences beats, retaining their length.
    """

    def __init__(self, period=1, silence_producer=AudioSegment.silent):
        """
        Initializes this SilenceEveryNth effect.
        :param period: Period of applying this effect to beats. Beats whose indices (starting at 1) are multiples of
                       this value will have the effect applied to them.
        :param silence_producer: Method used to produce silent beats.
        """
        super().__init__(period)
        self.silence_producer = silence_producer

    def apply_effect_to_beat(self, beat_audio):
        return self.silence_producer(len(beat_audio))

    def __eq__(self, other):
        return super(SilenceEveryNth, self).__eq__(other) and self.silence_producer == other.silence_producer


@register_effect('remove', optional_parameters={'period': int})
class RemoveEveryNth(PeriodicEffect):
    """
    A periodic effect that completely removes beats.
    """

    def __init__(self, period=2):
        super().__init__(period)
        if period <= 1:
            raise ValueError('Attempted to remove every single beat of a song')

    def apply_effect_to_beat(self, beat_audio):
        return None


@register_effect('cut', optional_parameters={'period': int})
class CutEveryNthInHalf(PeriodicEffect):
    """
    A periodic effect that cuts beats in half.
    """

    def apply_effect_to_beat(self, beat_audio):
        return beat_audio[:(len(beat_audio) // 2)]


@register_effect('reverse', optional_parameters={'period': int})
class ReverseEveryNth(PeriodicEffect):
    """
    A periodic effect that reverses beats.
    """

    def apply_effect_to_beat(self, beat_audio):
        return beat_audio.reverse()


@register_effect('repeat', optional_parameters={'period': int, 'times': int})
class RepeatEveryNth(PeriodicEffect):
    """
    A periodic effect that repeats beats a specified number of times.
    """

    def __init__(self, period=1, times=2):
        super().__init__(period)
        if times == 1:
            raise ValueError('Attempted to create an ineffective RepeatEveryNth effect (x1)')
        if times < 1:
            raise ValueError(f'Attempted to create an invalid RepeatEveryNth effect (x{times})')

        self.times = times

    def apply_effect_to_beat(self, beat_audio):
        return beat_audio * self.times

    def __eq__(self, other):
        return super(RepeatEveryNth, self).__eq__(other) and self.times == other.times
