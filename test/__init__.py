import unittest
from typing import List, Union

import numpy as np


class BeatMachineTestCase(unittest.TestCase):
    def assert_beat_sequences_equal(
        self,
        expected: Union[List[List[int]], List[np.ndarray]],
        actual: List[np.ndarray],
    ):
        self.assertEqual(
            len(expected), len(actual), msg="Beat sequence lengths were not equal"
        )
        for (e, a) in zip(expected, actual):
            np.testing.assert_array_equal(e, a)
