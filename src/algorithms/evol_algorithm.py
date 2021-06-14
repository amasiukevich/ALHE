from .base_algorithm import BaseAlgorithm

import numpy as np

class EvolAlgorithm(BaseAlgorithm):

    def __init__(self,
                 begin_curr_idx,
                 end_curr_idx,
                 num_currs,
                 rates_data,
                 num_iterations=1000,
                 population_size=10,
                 selection_type="prop"
                 ):

        super().__init__(begin_curr_idx, end_curr_idx, num_currs, rates_data)
        self.selection_type = selection_type
        self.num_iterations = num_iterations
        self.population_size = population_size
        self.population = self.generate_population()
        self.log = self.population.copy(deep=True)

    def generate_population(self):

        population = []
        for i in range(self.population_size):
            population.append(self.init_state())

        return population

    def crossover(self, state1: list, state2: list, first=-1):

        split_idx = np.random.randint(1, min(len(state1), len(state2)) - 1)

        if first == -1:
            first = np.random.choice([1, 2])

        if first == 1:
            new_state = state1[:split_idx] + state2[split_idx:]
        else:
            new_state = state2[:split_idx] + state1[split_idx:]

        # eliminate cycles
        tab = [-1] * self.num_currs
        left, right = len(new_state), 0

        for i in range(len(new_state)):
            if tab[new_state[i]] == -1:
                tab[new_state[i]] = i
            else:
                left = min(left, tab[new_state[i]])
                right = max(right, i)

            if left < right:
                new_state = new_state[:left] + new_state[right:]

        return new_state


    def selection(self, pool):

        if self.selection_type == "tournament":
            return self.tournament_selection(pool)
        elif self.selection_type == "roulette":
            return self.roulette_wheel_selection(pool)
        else:
            return self.proportional_selection(pool)

    def proportional_selection(self, pool):

        new_population = []
        np.shuffle(pool)

        suma = np.sum([self.calc_price(state) for state in pool])

        probs = [self.calc_price(state) / suma for state in pool]
        # TODO: tickets here
        count = 0
        while count < self.population_size:

            x = np.random.uniform(0, 2 / self.num_population)
            if x < probs[i]:
                new_population.append(pool[i])

            i = (i + 1) % len(pool)

    def roulette_wheel_selection(self, pool):
        pass

    def tournament_selection(self, pool):
        pass


    def optimize(self):


        for i in range(self.num_iterations):
            new_population = []
            if np.random.uniform() < 0.2:
                idx = np.random.randint(0, len(self.population) - 1)
                while idx == i:
                    idx = np.random.randint(0, len(self.population) - 1)

                new_population.append(
                    self.next_state(
                        list(self.crossover(self.population[i], self.population[idx]))
                    )
                )

            else:
                new_population.append(self.next_state(list(self.population[i])))

            pool = self.population + new_population

            self.population = self.selection(pool)
            self.log += self.population

        best_state = self.find_best(self.log)

        return best_state, self.calc_price(best_state)