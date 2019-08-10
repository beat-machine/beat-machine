import random
import unittest
from unittest.mock import patch

from parameterized import parameterized

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

    @parameterized.expand([
        ('Beats 2 and 4', [1, 4, 3, 2] * 2, 2, 4, [1, 2, 3, 4] * 2),
        ('Beats 1 and 3', [3, 2, 1, 4] * 2, 1, 3, [1, 2, 3, 4] * 2),
        ('Beats 1 and 4', [4, 2, 3, 1] * 2, 1, 4, [1, 2, 3, 4] * 2)
    ])
    def test_swap_beats(self, _name, song, x, y, expected):
        swap_effect = SwapBeats(x_period=x, y_period=y)
        self.assertEqual(expected, list(swap_effect(song)))

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
