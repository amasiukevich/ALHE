from .base_algorithm import BaseAlgorithm

import numpy as np

class SimulatedAnnealing(BaseAlgorithm):


    def __init__(self,
                 begin_curr_idx,
                 end_curr_idx,
                 num_currs,
                 rates_data,
                 random_state,
                 next_state_method="all",
                 num_iterations=1000,
                 population_size=10,
                 heat=10):

        super().__init__(begin_curr_idx, end_curr_idx, num_currs, rates_data, random_state, next_state_method)
        self.num_iterations = num_iterations
        self.population_size = population_size
        self.heat = heat
        self.random_state = random_state
        self.population = self.generate_population()
        self.log = list(self.population)
        self.best_state = self.find_best(self.population)


    def calc_heat(self, price1, price2):
        return np.exp((-1) * (np.abs(price1 - price2) / self.heat))


    def generate_population(self):

        population = []

        for i in range(self.population_size):
            population.append(self.init_state())

        return population


    def optimize(self):

        for i in range(self.num_iterations):

            new_state = self.next_state(list(self.best_state))

            if self.calc_price(new_state) > self.calc_price(self.best_state):
                self.best_state = list(new_state)
            elif self.random_state.uniform() < self.calc_heat(
                self.calc_price(new_state),
                self.calc_price(self.best_state)
            ):
                self.best_state = list(new_state)

            self.log.append(new_state)

        best_state = self.find_best(self.log)

        return best_state, self.calc_price(best_state)