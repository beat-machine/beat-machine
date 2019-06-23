import random
import unittest
from unittest.mock import patch

from beatmachine.effects.temporal import RandomizeAllBeats, SwapBeats


class TestSongEffects(unittest.TestCase):
    def setUp(self):
        self.dummy_song = list(range(1, 5))

    def test_randomize_all(self):
        seed = random.seed
        random_a = random.Random(seed)
        random_b = random.Random(seed)

        expected_result = self.dummy_song.copy()
        random_a.shuffle(expected_result)

        with patch('random.shuffle', random_b.shuffle):
            randomize_effect = RandomizeAllBeats()
            self.assertEqual(expected_result, list(randomize_effect(self.dummy_song)))

    def test_swap_beats(self):
        swap_effect = SwapBeats(x_period=2, y_period=4)
        self.assertEqual([1, 4, 3, 2], list(swap_effect(self.dummy_song)))

    def test_zero_swap_beats_disallowed(self):
        self.assertRaises(ValueError, lambda: SwapBeats(x_period=0, y_period=1))
        self.assertRaises(ValueError, lambda: SwapBeats(x_period=1, y_period=0))
        self.assertRaises(ValueError, lambda: SwapBeats(x_period=0, y_period=0))

    def test_negative_swap_beats_disallowed(self):
        self.assertRaises(ValueError, lambda: SwapBeats(x_period=-1, y_period=0))
        self.assertRaises(ValueError, lambda: SwapBeats(x_period=0, y_period=-1))
        self.assertRaises(ValueError, lambda: SwapBeats(x_period=-1, y_period=-1))

    def test_equal_swap_beats_disallowed(self):
        self.assertRaises(ValueError, lambda: SwapBeats(x_period=10, y_period=10))


if __name__ == '__main__':
    unittest.main()
