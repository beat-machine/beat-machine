"""
The `effects` module provides a base effect class as well as some common effects to play with.
"""

from . import base, periodic, temporal

load_effect = base.EffectRegistry.load_effect
load_effect_chain = base.EffectRegistry.load_effect_chain

from .periodic import *
from .temporal import *
