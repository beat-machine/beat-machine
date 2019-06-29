"""
The `effects` module provides a base effect class as well as some sample implementations of song effects.
"""

from . import base, periodic, temporal

load_from_dict = base.EffectRegistry.load_effect_from_dict
