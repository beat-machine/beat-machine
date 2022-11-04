import pytest

from beatmachine.effects.swap import SwapBeats


@pytest.mark.parametrize(
    "periods, beats_per_measure, song, result",
    [
        ((2, 4), 4, [1, 2, 3, 4, 5, 6, 7, 8], [1, 4, 3, 2, 5, 8, 7, 6]),
        ((1, 3), 4, [1, 2, 3, 4, 5, 6, 7, 8], [3, 2, 1, 4, 7, 6, 5, 8]),
        ((2, 4), 4, [1, 2, 3, 4, 5], [1, 4, 3, 2, 5]),
        ((1, 3), 4, [1, 2, 3, 4, 5], [3, 2, 1, 4, 5]),
        ((4, 5), 4, [1, 2, 3, 4, 5], [4, 2, 3, 1, 5]),
    ],
)
def test_swap_beats(periods, beats_per_measure, song, result):
    effect = SwapBeats(x_period=periods[0], y_period=periods[1], group_size=beats_per_measure)
    assert result == list(effect(song))


def test_swap_beats_offset():
    effect = SwapBeats(x_period=2, y_period=4, group_size=4, offset=1)
    assert [0, 1, 4, 3, 2] == list(effect([0, 1, 2, 3, 4]))


def test_zero_swap_beats_disallowed():
    with pytest.raises(ValueError):
        _ = SwapBeats(x_period=0, y_period=1)
    with pytest.raises(ValueError):
        _ = SwapBeats(x_period=1, y_period=0)
    with pytest.raises(ValueError):
        _ = SwapBeats(x_period=0, y_period=0)


def test_negative_swap_beats_disallowed():
    with pytest.raises(ValueError):
        _ = SwapBeats(x_period=-1, y_period=0)
    with pytest.raises(ValueError):
        _ = SwapBeats(x_period=0, y_period=-1)
    with pytest.raises(ValueError):
        _ = SwapBeats(x_period=-1, y_period=-1)


def test_equal_swap_beats_disallowed():
    with pytest.raises(ValueError):
        _ = SwapBeats(x_period=10, y_period=10)
