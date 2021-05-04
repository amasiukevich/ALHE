# Getting data
from utils.data_generator import generate_data
from utils.data_loader import load_rates

# Algorithms
from algorithms.a_star import AStar
from algorithms.evol_algorithm import EvolAlgorithm
from algorithms.hill_climbing_algoritm import HillClimbingAlgoritm
from algorithms.hill_climb_neighbor import HillClimbNeightborAlgorithm
from algorithms.symulated_heating import SymulatedHeating

import numpy as np

if __name__ == "__main__":

    rates, n_currs = load_rates("data/data3_small.txt")