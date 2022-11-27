import pytest

from beatmachine.effects.reverse_order import ReverseAllBeats


@pytest.mark.parametrize(
    "song,expected",
    [([10, 20, 30, 40, 50], [50, 40, 30, 20, 10]), ([1], [1])],
)
def test_remap_beats(song, expected):
    reverse_effect = ReverseAllBeats()
    assert expected == list(reverse_effect(song))
