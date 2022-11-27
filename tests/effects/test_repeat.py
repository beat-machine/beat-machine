import pytest

from beatmachine.effects.repeat import RepeatEveryNth

from .effect_test_util import *


def test_repeat_every_nth(song_ascending):
    repeat_effect = RepeatEveryNth(period=2, times=2)
    assert_beat_sequences_equal([[1] * 4, [2] * 8, [3] * 4, [4] * 8], list(repeat_effect(song_ascending)))


def test_useless_repeat_effect_disallowed():
    with pytest.raises(ValueError):
        _ = RepeatEveryNth(times=1)


def test_invalid_repeat_effect_disallowed():
    with pytest.raises(ValueError):
        _ = RepeatEveryNth(times=0)

    with pytest.raises(ValueError):
        _ = RepeatEveryNth(times=-1)
