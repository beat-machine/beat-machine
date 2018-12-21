import unittest

from beatmachine.song_effects import *


def dummy_effect(_):
    return 'Applied'


class TestSongEffects(unittest.TestCase):
    def test_every_beat(self):
        self.assertEqual(['Applied', 'Applied', 'Applied'], every_beat(dummy_effect)([1, 2, 3]))

    def test_every_nth_beat(self):
        self.assertEqual([0, 'Applied', 2, 'Applied', 4], every_nth_beat(2, dummy_effect)([0, 1, 2, 3, 4]))

    def test_swap_beats(self):
        self.assertEqual([1, 4, 3, 2, 5, 8, 7, 6], swap_beats(2, 4)([1, 2, 3, 4, 5, 6, 7, 8]))


if __name__ == '__main__':
    unittest.main()
