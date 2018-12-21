import unittest

from beatmachine.beat_effects import remove, cut_in_half


class TestBeatEffects(unittest.TestCase):
    def test_remove(self):
        self.assertIsNone(remove([1]))

    def test_cut_in_half(self):
        self.assertEqual([1, 2], cut_in_half([1, 2, 3, 4]))
        self.assertEqual([], cut_in_half([1]))


if __name__ == '__main__':
    unittest.main()
