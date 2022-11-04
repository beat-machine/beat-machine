import numpy as np
import pytest


@pytest.fixture(scope="module")
def dummy_song():
    return [np.full(4, 1), np.full(4, 2), np.full(4, 3), np.full(4, 4)]


def assert_beat_sequences_equal(expected, actual):
    __tracebackhide__ = True
    assert len(expected) == len(actual)
    for (e, a) in zip(expected, actual):
        np.testing.assert_array_equal(e, a)
