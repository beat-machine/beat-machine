import pytest

from beatmachine.effects.remap import RemapBeats


@pytest.mark.parametrize(
    "song,mapping,expected",
    [
        ([5, 6, 7, 8], [3, 2, 1, 0], [8, 7, 6, 5]),
        ([5, 6, 7, 8], [0, 3, 2, 1], [5, 8, 7, 6]),
        ([5, 6, 7, 8], [0, 0, 2, 2], [5, 5, 7, 7]),
        ([5, 6], [0, 3, 2, 1], [5, 6]),
    ],
)
def test_remap_beats(song, mapping, expected):
    remap_effect = RemapBeats(mapping=mapping)
    assert expected == list(remap_effect(song))
