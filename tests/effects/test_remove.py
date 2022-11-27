import pytest

from beatmachine.effects.remove import RemoveEveryNth

from .effect_test_util import *


def test_remove_every_nth(song_ascending):
    remove_effect = RemoveEveryNth(period=2)
    assert_beat_sequences_equal([[1] * 4, [3] * 4], list(remove_effect(song_ascending)))


def test_remove_every_single_beat_disallowed():
    with pytest.raises(ValueError):
        _ = RemoveEveryNth(period=1)
