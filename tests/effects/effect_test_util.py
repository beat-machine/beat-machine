import numpy as np


def assert_beat_sequences_equal(expected, actual):
    __tracebackhide__ = True
    assert len(expected) == len(actual)
    for (e, a) in zip(expected, actual):
        np.testing.assert_array_equal(e, a)
