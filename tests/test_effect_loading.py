import unittest

from parameterized import parameterized

import beatmachine.effects
import beatmachine.effects.periodic
from beatmachine.effects.base import EffectRegistry


class TestEffectLoading(unittest.TestCase):

    @parameterized.expand([
        ('Silence every 2', {'type': 'silence', 'period': 2}, beatmachine.effects.periodic.SilenceEveryNth(period=2)),
        ('Remove every 2', {'type': 'remove', 'period': 2}, beatmachine.effects.periodic.RemoveEveryNth(period=2)),
        ('Cut every 2', {'type': 'cut', 'period': 2}, beatmachine.effects.periodic.CutEveryNthInHalf(period=2)),
        ('Reverse every 2', {'type': 'reverse', 'period': 2}, beatmachine.effects.periodic.ReverseEveryNth(period=2)),
        ('Repeat every 2 twice', {'type': 'repeat', 'period': 2, 'times': 2},
         beatmachine.effects.periodic.RepeatEveryNth(period=2, times=2)),
    ])
    def test_load_registered_effect_simple(self, name, definition, result):
        self.assertEqual(result, EffectRegistry.load_effect_from_dict(definition))


if __name__ == '__main__':
    unittest.main()
