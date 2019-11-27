import random
import unittest
from unittest.mock import patch

from parameterized import parameterized

from beatmachine.effects.temporal import RandomizeAllBeats, SwapBeats, RemapBeats


class TestSongEffects(unittest.TestCase):
    def setUp(self):
        self.dummy_song = list(range(1, 5))

    def test_randomize_all(self):
        seed = random.seed
        random_a = random.Random(seed)
        random_b = random.Random(seed)

        expected_result = self.dummy_song.copy()
        random_a.shuffle(expected_result)

        with patch("random.shuffle", random_b.shuffle):
            randomize_effect = RandomizeAllBeats()
            self.assertEqual(expected_result, list(randomize_effect(self.dummy_song)))

    @parameterized.expand(
        [
            (
                "Beats 2 and 4",
                (2, 4),
                4,
                [1, 2, 3, 4, 5, 6, 7, 8],
                [1, 4, 3, 2, 5, 8, 7, 6],
            ),
            (
                "Beats 1 and 3",
                (1, 3),
                4,
                [1, 2, 3, 4, 5, 6, 7, 8],
                [3, 2, 1, 4, 7, 6, 5, 8],
            ),
            (
                "Beats 2 and 4 with non-even song",
                (2, 4),
                4,
                [1, 2, 3, 4, 5],
                [1, 4, 3, 2, 5],
            ),
            (
                "Beats 1 and 3 with non-even song",
                (1, 3),
                4,
                [1, 2, 3, 4, 5],
                [3, 2, 1, 4, 5],
            ),
        ]
    )
    def test_swap_beats(self, _name, periods, beats_per_measure, song, result):
        effect = SwapBeats(
            x_period=periods[0], y_period=periods[1], group_size=beats_per_measure
        )
        self.assertEqual(result, list(effect(song)))

    @parameterized.expand(
        [
            (
                "Remap [0, 1, 2, 3] => [3, 2, 1, 0]",
                [5, 6, 7, 8],
                [3, 2, 1, 0],
                [8, 7, 6, 5],
            ),
            (
                "Remap [0, 1, 2, 3] => [0, 3, 2, 1]",
                [5, 6, 7, 8],
                [0, 3, 2, 1],
                [5, 8, 7, 6],
            ),
            (
                "Remap [0, 1, 2, 3] => [0, 0, 2, 2]",
                [5, 6, 7, 8],
                [0, 0, 2, 2],
                [5, 5, 7, 7],
            ),
            (
                "Partially remap [0, 1, 2, 3] => [3, 2, 1, 0]",
                [5, 6],
                [0, 3, 2, 1],
                [5, 6],
            ),
        ]
    )
    def test_remap_beats(self, _name, song, mapping, expected):
        remap_effect = RemapBeats(mapping=mapping)
        self.assertEqual(expected, list(remap_effect(song)))

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


if __name__ == "__main__":
    unittest.main()
