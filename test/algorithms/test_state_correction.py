import unittest
from src.algorithms.hill_climbing_algoritm import HillClimbingAlgorithm

class TestStateCorrection(unittest.TestCase):

    def test_cycles_removal(self):

        begin, end, num_currs = 1, 5, 5

        cases = [
            ([1, 2, 3, 2, 4, 5], [1, 2, 4, 5]),
            ([1, 2, 3, 4, 2, 3, 5], [1, 2, 3, 5]),
            ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
            ([1, 2, 1, 3, 4, 5], [1, 3, 4, 5]),
            ([1, 2, 3, 5, 4, 5], [1, 2, 3, 5])
        ]

        base_algo = HillClimbingAlgorithm(begin, end, num_currs, [])

        for case in cases:

            old_state = case[0]
            result = case[1]

            new_state = base_algo.remove_cycles(old_state)
            self.assertListEqual(result, new_state)
