import numpy as np
import pytest

from beatmachine.effects.cut import CutEveryNth

from .effect_test_util import *


@pytest.mark.parametrize(
    "song,effect,expected",
    [
        (
            [
                np.array([1, -1]),
                np.array([2, -2]),
                np.array([3, -3]),
                np.array([4, -4]),
            ],
            CutEveryNth(period=1, denominator=2, take_index=0),
            [[1], [2], [3], [4]],
        ),
        (
            [
                np.array([1, -1]),
                np.array([2, -2]),
                np.array([3, -3]),
                np.array([4, -4]),
            ],
            CutEveryNth(period=1, denominator=2, take_index=1),
            [[-1], [-2], [-3], [-4]],
        ),
        (
            [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9])],
            CutEveryNth(period=1, denominator=3, take_index=0),
            [[1], [4], [7]],
        ),
        (
            [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9])],
            CutEveryNth(period=1, denominator=3, take_index=2),
            [[3], [6], [9]],
        ),
    ],
)
def test_cut_every_nth(song, effect, expected):
    assert_beat_sequences_equal(expected, list(effect(song)))
