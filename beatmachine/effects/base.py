"""
The `base` module contains a base effect class as well as a metaclass-based registry for simple, batteries-included
deserialization of effects.
"""

import abc
from typing import Callable, Iterable

import numpy as np

Effect = Callable[[Iterable[np.ndarray]], Iterable[np.ndarray]]


class EffectRegistry(type):
    """
    The EffectRegistry is a metaclass that serves to track all loadable effects.
    """

    effects = {}

    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)
        try:
            if name not in mcs.effects:
                mcs.effects[getattr(cls, "__effect_name__")] = cls
        except AttributeError as e:
            raise AttributeError(
                "Attempted to register an effect class without an __effect_name__ attribute"
            ) from e
        return cls

    @staticmethod
    def load_effect_from_dict(effect: dict) -> "LoadableEffect":
        """
        Loads an effect based on a key-value definition. This is represented as a Python dictionary but could be loaded
        from anywhere, i.e. JSON data.

        A "type" key is required to determine which effect to load. All other values are passed directly as keyword
        arguments to the effect constructor.

        :param effect: Effect representation to load.
        :raises KeyError: if no effect with the given name was found.
        :raises ValueError: if the effect failed to load, likely due to an invalid/missing parameter.
        :return: An effect based on the given definition.
        """
        if "type" not in effect:
            raise KeyError("Effect definition missing `type` key")

        effect_type = effect["type"]

        try:
            kwargs = effect.copy()
            del kwargs["type"]
            return EffectRegistry.effects[effect_type](**kwargs)
        except KeyError as e:
            raise KeyError(f"Unknown effect `{effect_type}`") from e
        except ValueError as e:
            raise ValueError(f"An effect of type `{effect_type}` failed to load") from e


class EffectABCMeta(EffectRegistry, abc.ABCMeta):
    """
    EffectABCMeta is a metaclass combining EffectRegistry and ABCMeta.
    """

    pass


class LoadableEffect(abc.ABC):
    """
    LoadableEffect is an abstract base for a valid effect loadable by the EffectRegistry.
    """

    __abstract__ = True

    @property
    @abc.abstractmethod
    def __effect_name__(self) -> str:
        """
        __effect_name__ is the name of this effect.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __call__(self, beats: Iterable[np.ndarray]) -> Iterable[np.ndarray]:
        """
        Applies this effect to a given list of beats.

        :param beats: An iterable of beats to process.
        :return: A generator that yields modified beats, potentially in a different order or with a different length.
        """
        raise NotImplementedError
