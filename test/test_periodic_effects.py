import pytest
import numpy as np

from beatmachine.effects.periodic import *
from typing import *


@pytest.fixture
def dummy_song():
    return [np.full(4, 1), np.full(4, 2), np.full(4, 3), np.full(4, 4)]


def assert_beat_sequences_equal(
    expected: Union[List[List[int]], List[np.ndarray]], actual: List[np.ndarray]
):
    __tracebackhide__ = True
    assert len(expected) == len(actual)
    for (e, a) in zip(expected, actual):
        np.testing.assert_array_equal(e, a)


def test_silence_every_nth(dummy_song):
    silence_effect = SilenceEveryNth(period=2)
    assert_beat_sequences_equal(
        [[1] * 4, [0] * 4, [3] * 4, [0] * 4], list(silence_effect(dummy_song))
    )


def test_remove_every_nth(dummy_song):
    remove_effect = RemoveEveryNth(period=2)
    assert_beat_sequences_equal([[1] * 4, [3] * 4], list(remove_effect(dummy_song)))


def test_remove_every_single_beat_disallowed(dummy_song):
    with pytest.raises(ValueError):
        _ = RemoveEveryNth(period=1)


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


def test_reverse_every_nth():
    forward_beat = np.ndarray([1, 2, 3, 4])
    reversed_beat = np.flip(forward_beat)
    reverse_effect = ReverseEveryNth(period=2)

    assert_beat_sequences_equal(
        [forward_beat, reversed_beat] * 2, list(reverse_effect([forward_beat] * 4))
    )


def test_repeat_every_nth(dummy_song):
    repeat_effect = RepeatEveryNth(period=2, times=2)
    assert_beat_sequences_equal(
        [[1] * 4, [2] * 8, [3] * 4, [4] * 8], list(repeat_effect(dummy_song))
    )


def test_useless_repeat_effect_disallowed():
    with pytest.raises(ValueError):
        _ = RepeatEveryNth(times=1)


def test_invalid_repeat_effect_disallowed():
    with pytest.raises(ValueError):
        _ = RepeatEveryNth(times=0)

    with pytest.raises(ValueError):
        _ = RepeatEveryNth(times=-1)


def test_zero_period_disallowed():
    with pytest.raises(ValueError):
        _ = RemoveEveryNth(period=0)


def test_negative_period_disallowed():
    with pytest.raises(ValueError):
        _ = RemoveEveryNth(period=-1)
