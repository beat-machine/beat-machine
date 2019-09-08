import unittest

from parameterized import parameterized

import beatmachine.effects as fx


class TestEffectLoading(unittest.TestCase):
    @parameterized.expand(
        [
            (
                "Silence every 2",
                {"type": "silence", "period": 2},
                fx.periodic.SilenceEveryNth(period=2),
            ),
            (
                "Remove every 2",
                {"type": "remove", "period": 2},
                fx.periodic.RemoveEveryNth(period=2),
            ),
            (
                "Cut every 2",
                {"type": "cut", "period": 2},
                fx.periodic.CutEveryNth(period=2),
            ),
            (
                "Cut every 1 in 1/3 taking 3rd part",
                {"type": "cut", "period": 1, "denominator": 3, "take_index": 2},
                fx.periodic.CutEveryNth(period=1, denominator=3, take_index=2),
            ),
            (
                "Reverse every 2",
                {"type": "reverse", "period": 2},
                fx.periodic.ReverseEveryNth(period=2),
            ),
            (
                "Repeat every 2 twice",
                {"type": "repeat", "period": 2, "times": 2},
                fx.periodic.RepeatEveryNth(period=2, times=2),
            ),
            (
                "Randomize all beats",
                {"type": "randomize"},
                fx.temporal.RandomizeAllBeats(),
            ),
            (
                "Swap 2 and 4",
                {"type": "swap", "x_period": 2, "y_period": 4},
                fx.temporal.SwapBeats(x_period=2, y_period=4),
            ),
            (
                "Remap [0, 1, 2, 3] => [3, 1, 2, 0]",
                {"type": "remap", "mapping": [3, 1, 2, 0]},
                fx.temporal.RemapBeats(mapping=[3, 1, 2, 0]),
            ),
        ]
    )
    def test_load_registered_effect_simple(self, _name, definition, result):
        self.assertEqual(
            result, fx.base.EffectRegistry.load_effect_from_dict(definition)
        )


if __name__ == "__main__":
    unittest.main()
