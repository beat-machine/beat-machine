import unittest

from parameterized import parameterized

from beatmachine.effects.periodic import *
from . import BeatMachineTestCase


class TestPeriodicEffects(BeatMachineTestCase):
    def setUp(self):
        self.dummy_song = [np.full(4, 1), np.full(4, 2), np.full(4, 3), np.full(4, 4)]

    def test_silence_every_nth(self):
        silence_effect = SilenceEveryNth(period=2)
        self.assert_beat_sequences_equal(
            [[1] * 4, [0] * 4, [3] * 4, [0] * 4], list(silence_effect(self.dummy_song))
        )

    def test_remove_every_nth(self):
        remove_effect = RemoveEveryNth(period=2)
        self.assert_beat_sequences_equal(
            [[1] * 4, [3] * 4], list(remove_effect(self.dummy_song))
        )

    def test_remove_every_single_beat_disallowed(self):
        self.assertRaises(ValueError, lambda: RemoveEveryNth(period=1))

    @parameterized.expand(
        [
            (
                "1st part of every 1/2",
                [[1, -1], [2, -2], [3, -3], [4, -4]],
                CutEveryNth(period=1, denominator=2, take_index=0),
                [[1], [2], [3], [4]],
            ),
            (
                "2nd part of every 1/2",
                [[1, -1], [2, -2], [3, -3], [4, -4]],
                CutEveryNth(period=1, denominator=2, take_index=0),
                [[-1], [-2], [-3], [-4]],
            ),
            (
                "1st part of every 1/3",
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                CutEveryNth(period=1, denominator=3, take_index=0),
                [[1], [4], [7]],
            ),
            (
                "3rd part of every 1/3",
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                CutEveryNth(period=1, denominator=3, take_index=0),
                [[3], [6], [9]],
            ),
        ]
    )
    def test_cut_every_nth(self, _name, song, effect, expected):
        pass

    def test_reverse_every_nth(self):
        forward_beat = np.ndarray([1, 2, 3, 4])
        reversed_beat = np.flip(forward_beat)
        reverse_effect = ReverseEveryNth(period=2)

        self.assert_beat_sequences_equal(
            [forward_beat, reversed_beat] * 2, list(reverse_effect([forward_beat] * 4))
        )

    def test_repeat_every_nth(self):
        repeat_effect = RepeatEveryNth(period=2, times=2)
        self.assert_beat_sequences_equal(
            [[1] * 4, [2] * 8, [3] * 4, [4] * 8], list(repeat_effect(self.dummy_song))
        )

    def test_useless_repeat_effect_disallowed(self):
        self.assertRaises(ValueError, lambda: RepeatEveryNth(times=1))

    def test_invalid_repeat_effect_disallowed(self):
        self.assertRaises(ValueError, lambda: RepeatEveryNth(times=0))
        self.assertRaises(ValueError, lambda: RepeatEveryNth(times=-1))

    def test_zero_period_disallowed(self):
        self.assertRaises(ValueError, lambda: RemoveEveryNth(period=0))

    def test_negative_period_disallowed(self):
        self.assertRaises(ValueError, lambda: RemoveEveryNth(period=-1))


if __name__ == "__main__":
    unittest.main()
