import abc
from typing import Generator, Iterable

from pydub import AudioSegment


class EffectRegistry(type):
    effects = {}

    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)
        try:
            if name not in mcs.effects:
                mcs.effects[cls.__effect_name__] = cls
        except AttributeError as e:
            raise AttributeError('Attempted to register an effect class without an __effect_name__ attribute') from e
        return cls

    @staticmethod
    def load_effect_from_dict(effect: dict) -> 'BaseEffect':
        if 'type' not in effect:
            raise KeyError('Effect definition missing `type` key')

        effect_type = effect['type']

        try:
            kwargs = effect.copy()
            del kwargs['type']
            return EffectRegistry.effects[effect_type](**kwargs)
        except KeyError as e:
            raise KeyError(f'Unknown effect `{effect_type}`') from e
        except ValueError as e:
            raise ValueError(f'An effect of type `{effect_type}` failed to load') from e


class EffectABCMeta(EffectRegistry, abc.ABCMeta):
    pass


class BaseEffect:
    __abstract__ = True

    @property
    @abc.abstractmethod
    def __effect_name__(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def __call__(self, beats: Iterable[AudioSegment]) -> Generator[AudioSegment, None, None]:
        """
        Applies this effect to a given list of beats.
        :param beats: An iterable of beats to process.
        :return: A generator that yields modified beats, potentially in a different order.
        """
        raise NotImplementedError
