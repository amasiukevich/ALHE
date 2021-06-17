from src.algorithms.hill_climbing_algoritm import HillClimbingAlgorithm
import unittest

class TestHillClimb(unittest.TestCase):


    def test_init_state(self):

        cases = [
            (2, 3, 5, [2, 1, 0, 4, 3]),
            (4, 0, 5, [4, 3, 2, 1, 0])
        ]

        for case in cases:
            begin, end, num_currs, result = case
            base_algo = HillClimbingAlgorithm(begin, end, num_currs, [])
            state = base_algo.init_state(shuffling=False)

            self.assertListEqual(state, result)


    def test_price_function(self):
        pass