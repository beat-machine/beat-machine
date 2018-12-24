import unittest

from beatmachine.effects.periodic import *


class TestPeriodicEffects(unittest.TestCase):
    def setUp(self):
        self.dummy_song = [
            [1] * 4,
            [2] * 4,
            [3] * 4,
            [4] * 4
        ]

    def test_silence_every_nth(self):
        silence_effect = SilenceEveryNth(period=2, silence_producer=lambda n: [0] * n)
        self.assertEqual([
            [1] * 4,
            [0] * 4,
            [3] * 4,
            [0] * 4
        ], list(silence_effect(self.dummy_song)))

    def test_remove_every_nth(self):
        remove_effect = RemoveEveryNth(period=2)
        self.assertEqual([
            [1] * 4,
            [3] * 4
        ], list(remove_effect(self.dummy_song)))

    def test_remove_every_single_beat_disallowed(self):
        self.assertRaises(ValueError, lambda: RemoveEveryNth(period=1))

    def test_cut_every_nth_in_half(self):
        cut_effect = CutEveryNthInHalf(period=1)
        self.assertEqual([
            [1] * 2,
            [2] * 2,
            [3] * 2,
            [4] * 2
        ], list(cut_effect(self.dummy_song)))

    def test_reverse_every_nth(self):
        try:
            snare_drum = AudioSegment.from_mp3('resources/philharmonia_snare_025.mp3')
        except FileNotFoundError:
            raise unittest.SkipTest('Failed to load test audio!')

        reversed_snare_drum = snare_drum.reverse()
        ordered_dummy_song = [snare_drum] * 4
        reverse_effect = ReverseEveryNth(period=2)
        self.assertEqual([
            snare_drum,
            reversed_snare_drum,
            snare_drum,
            reversed_snare_drum
        ], list(reverse_effect(ordered_dummy_song)))

    def test_repeat_every_nth(self):
        repeat_effect = RepeatEveryNth(period=2, times=2)
        self.assertEqual([
            [1] * 4,
            [2] * 8,
            [3] * 4,
            [4] * 8
        ], list(repeat_effect(self.dummy_song)))

    def test_useless_repeat_effect_disallowed(self):
        self.assertRaises(ValueError, lambda: RepeatEveryNth(times=1))

    def test_invalid_repeat_effect_disallowed(self):
        self.assertRaises(ValueError, lambda: RepeatEveryNth(times=0))
        self.assertRaises(ValueError, lambda: RepeatEveryNth(times=-1))

    def test_zero_period_disallowed(self):
        self.assertRaises(ValueError, lambda: RemoveEveryNth(period=0))

    def test_negative_period_disallowed(self):
        self.assertRaises(ValueError, lambda: RemoveEveryNth(period=-1))


if __name__ == '__main__':
    unittest.main()

