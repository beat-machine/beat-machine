import pytest

import beatmachine.effects as fx


@pytest.mark.parametrize(
    "definition,expected",
    [
        ({"type": "silence", "period": 2}, fx.SilenceEveryNth(period=2)),
        ({"type": "remove", "period": 2}, fx.RemoveEveryNth(period=2)),
        ({"type": "cut", "period": 2}, fx.CutEveryNth(period=2)),
        (
            {"type": "cut", "period": 1, "denominator": 3, "take_index": 2},
            fx.CutEveryNth(period=1, denominator=3, take_index=2),
        ),
        ({"type": "reverse", "period": 2}, fx.ReverseEveryNth(period=2)),
        (
            {"type": "repeat", "period": 2, "times": 2},
            fx.RepeatEveryNth(period=2, times=2),
        ),
        ({"type": "randomize"}, fx.RandomizeAllBeats()),
        (
            {"type": "swap", "x_period": 2, "y_period": 4},
            fx.SwapBeats(x_period=2, y_period=4),
        ),
        (
            {"type": "remap", "mapping": [3, 1, 2, 0]},
            fx.RemapBeats(mapping=[3, 1, 2, 0]),
        ),
    ],
)
def test_load_effect(definition, expected):
    assert fx.load_effect(definition) == expected
