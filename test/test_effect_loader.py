import unittest

from beatmachine.effect_loader import load_effect, load_all_effects
from beatmachine.song_effects import *


class EffectLoaderTest(unittest.TestCase):
    def test_load_beat_effect(self):
        remove_every_2 = load_effect({
            'type': 'remove',
            'every': 2
        })

        remove_all = load_effect({
            'type': 'remove'
        })

        self.assertEqual([1, 3, 5, 7, 9], remove_every_2([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual([], remove_all([1, 2, 3, 4, 5, 6, 7, 8, 9]))

    def test_load_song_effect(self):
        self.assertEqual(randomize_all, load_effect({'type': 'randomize_all'}))
        self.assertEqual(sort_by_loudness, load_effect({'type': 'sort_by_loudness'}))
        self.assertEqual(sort_by_average_frequency, load_effect({'type': 'sort_by_average_frequency'}))

    def test_load_swap_beats(self):
        self.assertEqual([1, 4, 3, 2], load_effect({'type': 'swap', 'x': 2, 'y': 4})([1, 2, 3, 4]))

    def test_load_all_effects(self):
        self.assertEqual([randomize_all, sort_by_loudness], load_all_effects({
            'effects': [
                {
                    'type': 'randomize_all'
                },
                {
                    'type': 'sort_by_loudness'
                }
            ]
        }))


if __name__ == '__main__':
    unittest.main()
