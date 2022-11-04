import numpy as np

from beatmachine.effects.reverse import ReverseEveryNth

from .effect_test_util import *


def test_reverse_every_nth():
    forward_beat = np.ndarray([1, 2, 3, 4])
    reversed_beat = np.flip(forward_beat)
    reverse_effect = ReverseEveryNth(period=2)

    assert_beat_sequences_equal([forward_beat, reversed_beat] * 2, list(reverse_effect([forward_beat] * 4)))
