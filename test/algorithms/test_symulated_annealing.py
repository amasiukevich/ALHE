import unittest
from src.utils.data_loader import load_rates
from src.algorithms.simulated_annealing import SimulatedAnnealing

class TestSymulatedAnnealing(unittest.TestCase):

    def test_creation(self):

        begin = 1
        end = 4
        rates_data, num_currs = load_rates('../../data/data3_small.txt')

        optimizer = SimulatedAnnealing(
            begin_curr_idx=begin,
            end_curr_idx=end,
            num_currs=num_currs,
            rates_data=rates_data
        )

        best_state, best_cost = optimizer.optimize()

        print(best_state, best_cost)
