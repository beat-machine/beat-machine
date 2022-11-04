from typing import Optional

import numpy as np
import pytest

from beatmachine.effects.periodic import PeriodicEffect


class _NoOpEffect(PeriodicEffect):
    __effect_name__: str = "nothing"

    def process_beat(self, beat: np.ndarray) -> Optional[np.ndarray]:
        return beat


def test_zero_period_disallowed():
    with pytest.raises(ValueError):
        _ = _NoOpEffect(period=0)


def test_negative_period_disallowed():
    with pytest.raises(ValueError):
        _ = _NoOpEffect(period=-1)
