from beatmachine.effects.silence import SilenceEveryNth

from .effect_test_util import *


def test_silence_every_nth(song_ascending):
    silence_effect = SilenceEveryNth(period=2)
    assert_beat_sequences_equal([[1] * 4, [0] * 4, [3] * 4, [0] * 4], list(silence_effect(song_ascending)))
