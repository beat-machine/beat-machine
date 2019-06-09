import unittest

from beatmachine.effects.periodic import CutEveryNthInHalf, RepeatEveryNth
from beatmachine.effects.song import SwapBeats
from beatmachine.effect_loader import load_effect


class TestEffectLoading(unittest.TestCase):
    def test_load_registered_effect_simple(self):
        obj = {
            'type': 'cut',
            'period': 2
        }

        self.assertEqual(CutEveryNthInHalf(period=2), load_effect(obj))

    def test_load_registered_effect_without_specifying_optional(self):
        obj = {
            'type': 'repeat'
        }

        self.assertEqual(RepeatEveryNth(), load_effect(obj))

    def test_load_registered_effect_with_required(self):
        obj = {
            'type': 'swap',
            'x_period': 2,
            'y_period': 4
        }

        self.assertEqual(SwapBeats(2, 4), load_effect(obj))

    def test_load_unregistered_effect_fails(self):
        obj = {
            'type': 'an invalid effect',
            'foo': 'bar'
        }

        self.assertRaises(ValueError, load_effect, obj)

    def test_load_registered_effect_missing_required_fails(self):
        obj = {
            'type': 'swap'
        }

        self.assertRaises(ValueError, load_effect, obj)

    def test_load_registered_effect_with_invalid_values(self):
        obj = {
            'type': 'swap',
            'x_period': 'not an integer',
            'y_period': 'also not an integer'
        }

        self.assertRaises(ValueError, load_effect, obj)


if __name__ == '__main__':
    unittest.main()
