"""
The `base` module contains a base effect class as well as a metaclass-based registry for simple, batteries-included
deserialization of effects.
"""

import abc
import re

from typing import Callable, Iterable

import numpy as np
from jsonschema import validate
from deprecation import deprecated
from inspect import getdoc

Effect = Callable[[Iterable[np.ndarray]], Iterable[np.ndarray]]


class EffectRegistry(type):
    """
    The EffectRegistry is a metaclass that serves to track all loadable effects. Effects may define zero or more of
    the following two attributes to control how they are loaded:

    ``__effect_name__`` explicitly sets the name used to recognize an effect. It defaults to the lowercased class name.

    ``__effect_schema__`` is an optional schema describing the effect's properties. During validation, this is placed
    within the "properties" field of an object in a Draft 7 JSON schema.
    """

    effects = {}
    schemas = {}

    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)
        if name not in mcs.effects:
            effect_name = getattr(cls, "__effect_name__", name.lower())
            mcs.effects[effect_name] = cls
            mcs.schemas[effect_name] = getattr(cls, "__effect_schema__", None)
        return cls

    @staticmethod
    def dump_schema(root: bool = False) -> dict:
        """
        Dumps a Draft 7 JSON schema describing a valid effect object. This includes all registered effects, so custom
        effects that define ``__effect_schema__`` will be included.
        """
        any_of = []
        for e, s in EffectRegistry.schemas.items():
            properties = {"type": {"const": e, "default": e, "format": "hidden"}}
            if s:
                properties.update(s)
            any_of.append(
                {
                    "type": "object",
                    "properties": properties,
                    "title": e.capitalize(),
                    "description": re.sub(
                        "\\s+", " ", getdoc(EffectRegistry.effects[e])
                    ),
                    "required": ["type"],
                    "additionalProperties": False,
                }
            )

        schema = {"title": "Effect", "anyOf": any_of}
        if root:
            schema["$schema"] = "http://json-schema.org/draft-07/schema#"

        return schema

    @staticmethod
    def dump_list_schema(root: bool = False) -> dict:
        """
        Dumps a Draft 7 JSON schema describing a valid effect chain.
        """

        schema = {
            "title": "Effect Chain",
            "type": "array",
            "items": EffectRegistry.dump_schema(),
        }
        if root:
            schema["$schema"] = "http://json-schema.org/draft-07/schema#"

        return schema

    @staticmethod
    def load_effect(effect: dict) -> "LoadableEffect":
        """
        Loads an effect from a key-value definition.

        A "type" key is required to determine which effect to load. All other values are passed directly as keyword
        arguments to the effect constructor. If an effect defines ``__effect_schema__``, the given schema will be used
        to validate parameters.

        :param effect: Effect representation to load.
        :return: An effect based on the given definition.
        """
        validate(instance=effect, schema=EffectRegistry.dump_schema(root=True))

        kwargs = effect.copy()
        del kwargs["type"]

        return EffectRegistry.effects[effect["type"]](**kwargs)

    @staticmethod
    def load_effect_chain(effects: Iterable[dict]):
        return [EffectRegistry.load_effect(e) for e in effects]

    @staticmethod
    @deprecated(
        deprecated_in="3.2.0",
        removed_in="4.0.0",
        details="Prefer ``EffectRegistry.load_effect`` or ``beatmachine.effects.load_effect``.",
    )
    def load_effect_from_dict(effect: dict) -> "LoadableEffect":
        return EffectRegistry.load_effect(effect)


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
