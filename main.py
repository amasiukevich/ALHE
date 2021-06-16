# Getting data
from numpy.random import RandomState

from src.utils.data_loader import load_rates

# Algorithms

from src.algorithms.a_star import AStar
from src.algorithms.base_algorithm import BaseAlgorithm
from src.algorithms.evol_algorithm import EvolAlgorithm
from src.algorithms.hill_climbing_algoritm import HillClimbingAlgorithm
from src.algorithms.hill_climb_neighbor import HillClimbNeightborAlgorithm
from src.algorithms.simulated_annealing import SimulatedAnnealing

# for the reports
import pandas as pd



def test_algorithms():

    data_sources = {
        1: ("data/data3_small.txt", 1, 4),
        2: ("data/paths_prepared.txt", 3, 5)
    }

    random_seeds = [42]

    selection_ways = [ "threshold", "tournament", "roulette"]
    mutation_ways = ["shuffle", "swap", "add", "all"]

    num_iterations = [10, 50, 100, 200, 500, 1000]
    temperatures = [1, 2, 3, 5, 8, 13, 21]
    population_sizes = [2, 5, 10, 20, 50, 100]

    num_neighbors = [1, 2, 3, 4]
    depths = [1, 2, 3]

    a_star_data = []
    evol_data = []
    climbing_data = []
    climbing_neighbor_data = []
    annealing_data = []

    i = 0
    print("testing annealing")
    # simulated_annealing
    for number, source_data in data_sources.items():
        filename = source_data[0]
        begin, end = source_data[1], source_data[2]

        rates, num_currs = load_rates(filename)

        for state_mutation in mutation_ways:
            for temperature in temperatures:
                for population_size in population_sizes:
                    for num_iteration in num_iterations:

                        for random_seed in random_seeds:

                            random_state = RandomState(random_seed)
                            algo = SimulatedAnnealing(
                                begin_curr_idx=begin,
                                end_curr_idx=end,
                                num_currs=num_currs,
                                rates_data=rates,
                                next_state_method=state_mutation,
                                heat=temperature,
                                population_size=population_size,
                                num_iterations=num_iteration,
                                random_state=random_state
                            )
                            i += 1
                            best_state, best_result = algo.optimize()
                            print(i)
                            annealing_data.append({
                                "source": number,
                                "mutation_method": state_mutation,
                                "temperature": temperature,
                                "population_size": population_size,
                                "num_iterations": num_iteration,
                                "best_state": best_state,
                                "best_score": best_result
                            })


    print("Testing Astar")
    # Astar

    for number, source_data in data_sources.items():
        filename = source_data[0]
        begin, end = source_data[1], source_data[2]

        rates, num_currs = load_rates(filename)

        for state_mutation in mutation_ways:

            for random_seed in random_seeds:
                random_state = RandomState(random_seed)
                algo = AStar(
                    begin_curr_idx=begin,
                    end_curr_idx=end,
                    num_currs=num_currs,
                    rates_data=rates,
                    random_state=random_state,
                    next_state_method=state_mutation
                )

                best_state, best_result = algo.optimize()

                a_star_data.append({
                    "source": number,
                    "mutation_method": state_mutation,
                    "best_state": best_state,
                    "best_score": best_result
                })


    # print("Testing evolutionary")
    #
    # i = 0
    # # evolutionary
    # for number, source_data in data_sources.items():
    #
    #     filename = source_data[0]
    #     begin, end = source_data[1], source_data[2]
    #
    #     rates, num_currs = load_rates(filename)
    #     for selection_way in selection_ways:
    #         for state_mutation in mutation_ways:
    #             for num_iteration in num_iterations:
    #                 for population_size in population_sizes:
    #                     for random_seed in random_seeds:
    #
    #                         random_state = RandomState(random_seed)
    #
    #                         evol = EvolAlgorithm(
    #                             begin_curr_idx=begin,
    #                             end_curr_idx=end,
    #                             num_currs=num_currs,
    #                             rates_data=rates,
    #                             next_state_method=state_mutation,
    #                             num_iterations=num_iteration,
    #                             population_size=population_size,
    #                             selection_type=selection_way,
    #                             random_state=random_state
    #                         )
    #
    #                         best_state, best_score = evol.optimize()
    #                         i += 1
    #                         print(i)
    #                         evol_data.append({
    #                             "source": number,
    #                             "mutation_method": state_mutation,
    #                             "num_iterations": num_iterations,
    #                             "population_size": population_size,
    #                             "selection_type": selection_way,
    #                             "best_state": best_state,
    #                             "best_score": best_score
    #                         })
    #
    # print("Testing hill climbing")

    # hill_climbing
    for number, source_data in data_sources.items():
        filename = source_data[0]
        begin, end = source_data[1], source_data[2]

        rates, num_currs = load_rates(filename)

        for state_mutation in mutation_ways:
            for num_iteration in num_iterations:
                for random_seed in random_seeds:

                    random_state = RandomState(random_seed)
                    algo = HillClimbingAlgorithm(
                        begin_curr_idx=begin,
                        end_curr_idx=end,
                        num_currs=num_currs,
                        rates_data=rates,
                        next_state_method=state_mutation,
                        num_iterations=num_iteration,
                        random_state=random_state
                    )

                    best_state, best_result = algo.optimize()

                    climbing_data.append({
                        "source": number,
                        "mutation_method": state_mutation,
                        "num_iterations": num_iteration,
                        "best_state": best_state,
                        "best_score": best_result
                    })

    print("Testing hill climbing neighbor")


    # hill_climbing_neighbor
    for number, source_data in data_sources.items():
        filename = source_data[0]
        begin, end = source_data[1], source_data[2]

        rates, num_currs = load_rates(filename)

        for state_mutation in mutation_ways:
            for num_iteration in num_iterations:
                for depth in depths:
                    for num_neighbor in num_neighbors:
                        for random_seed in random_seeds:

                            random_state = RandomState(random_seed)
                            algo = HillClimbNeightborAlgorithm(
                                begin_curr_idx=begin,
                                end_curr_idx=end,
                                num_currs=num_currs,
                                rates_data=rates,
                                next_state_method=state_mutation,
                                num_iterations=num_iteration,
                                depth=depth,
                                num_neighbors=num_neighbor,
                                random_state=random_state
                            )

                            best_state, best_result = algo.optimize()

                            climbing_neighbor_data.append({
                                "source": number,
                                "mutation_method": state_mutation,
                                "num_iterations": num_iteration,
                                "depth": depth,
                                "num_neighbors": num_neighbor,
                                "best_state": best_state,
                                "best_score": best_result
                            })


    a_star_df = pd.DataFrame(a_star_data)
    evol_df = pd.DataFrame(evol_data)
    climbing_df = pd.DataFrame(climbing_data)
    climbing_neighbor_df = pd.DataFrame(climbing_neighbor_data)
    annealing_df = pd.DataFrame(annealing_data)

    a_star_df.to_csv("result_data/a_star_data.csv")
    evol_df.to_csv("result_data/evol_data.csv")
    climbing_df.to_csv("result_data/climbing_data.csv")
    climbing_neighbor_df.to_csv("result_data/climbing_neighbor_data.csv")
    annealing_df.to_csv("result_data/annealing_data.csv")


if __name__ == "__main__":
    test_algorithms()