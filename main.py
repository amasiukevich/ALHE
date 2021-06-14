# Getting data
from src.utils.data_loader import load_rates

# Algorithms

from src.algorithms.a_star import AStar
from src.algorithms.base_algorithm import BaseAlgorithm
from src.algorithms.evol_algorithm import EvolAlgorithm
from src.algorithms.hill_climbing_algoritm import HillClimbingAlgoritm
from src.algorithms.hill_climb_neighbor import HillClimbNeightborAlgorithm
from src.algorithms.simulated_annealing import SimulatedAnnealing

if __name__ == "__main__":

    rates, n_currs = load_rates("data/data3_small.txt")
    starting_curr = 1
    ending_curr = 4

    base_algo = BaseAlgorithm(
        starting_curr,
        ending_curr,
        n_currs,
        rates
    )