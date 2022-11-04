import pytest

from beatmachine.effects.remove import RemoveEveryNth

from .effect_test_util import *


def test_remove_every_nth(dummy_song):
    remove_effect = RemoveEveryNth(period=2)
    assert_beat_sequences_equal([[1] * 4, [3] * 4], list(remove_effect(dummy_song)))


def test_remove_every_single_beat_disallowed(dummy_song):
    with pytest.raises(ValueError):
        _ = RemoveEveryNth(period=1)
