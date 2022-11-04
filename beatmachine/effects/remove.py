from typing import Optional

import numpy as np

from ..effect_registry import EffectABCMeta
from .periodic import PeriodicEffect


class RemoveEveryNth(PeriodicEffect, metaclass=EffectABCMeta):
    """
    Completely remove beats.
    """

    __effect_name__ = "remove"
    __effect_schema__ = {
        "period": {
            "type": "integer",
            "minimum": 2,
            "default": 2,
            "title": "Period",
            "description": "How often to apply this effect. For Remove, this must be at least 2.",
        },
        "offset": {
            "type": "integer",
            "minimum": 0,
            "default": 0,
            "title": "Offset",
            "description": "How many beats to wait before applying this effect.",
        },
    }

    def __init__(self, *, period: int = 2, offset: int = 0):
        if period < 2:
            raise ValueError(f"`remove` effect period must be >= 2, but was {period}")
        super().__init__(period=period, offset=offset)

    def process_beat(self, beat: np.ndarray) -> Optional[np.ndarray]:
        return None
