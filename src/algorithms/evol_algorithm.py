from .base_algorithm import BaseAlgorithm
import numpy as np

from random import sample

class EvolAlgorithm(BaseAlgorithm):

    def __init__(self,
                 begin_curr_idx,
                 end_curr_idx,
                 num_currs,
                 rates_data,
                 random_state,
                 num_iterations=1000,
                 population_size=10,
                 next_state_method="all",
                 selection_type="threshold"
                 ):

        super().__init__(begin_curr_idx, end_curr_idx, num_currs, rates_data, random_state, next_state_method)
        self.selection_type = selection_type
        self.num_iterations = num_iterations
        self.population_size = population_size
        self.random_state = random_state
        self.population = self.generate_population()
        self.log = self.population.copy()



    def generate_population(self):

        population = []
        for i in range(self.population_size):
            population.append(self.init_state())

        return population


    def crossover(self, state1: list, state2: list, first=-1):

        if min(len(state1), len(state2)) - 1 <= 1:
            best_fitnessed = state1 if self.calc_price(state1) > self.calc_price(state2) else state2
            return best_fitnessed

        split_idx = self.random_state.randint(1, min(len(state1), len(state2)) - 1)


        if first == -1:
            first = self.random_state.choice([1, 2])

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

        left = max(left, 1)
        right = min(right, len(new_state) - 1)
        if left < right:
            new_state = new_state[:left] + new_state[right:]

        return new_state


    def selection(self, pool):

        if self.selection_type == "tournament":
            return self.tournament_selection(pool)
        elif self.selection_type == "roulette":
            return self.roulette_wheel_selection(pool)
        else:
            return self.threshold_selection(pool)


    def threshold_selection(self, pool, threshold=0):

        strong_elements = []
        weak_elements = []

        for elem in pool:
            if self.calc_price(elem) > threshold:
                strong_elements.append(elem)
            else:
                weak_elements.append(elem)

        # if too small number of elements
        if len(strong_elements) < self.population_size:

            for i in range(self.population_size - len(strong_elements)):
                idx = self.random_state.choice([i for i in range(len(weak_elements))])
                strong_elements.append(weak_elements[idx])

        # if too big number of elements
        elif len(strong_elements) > self.population_size:

            for i in range(len(strong_elements) - self.population_size):
                idx = self.random_state.choice([i for i in range(len(strong_elements))])
                strong_elements.pop(idx)


        return strong_elements


    def roulette_wheel_selection(self, pool):

        new_population = []
        scores = [self.calc_price(elem) for elem in pool]
        probs = [100 * (score / np.sum(scores)) for score in scores]

        hashes_pool = {
            hash(id(pool[i])): pool[i]
            for i in range(len(pool))
        }

        probs_dict = {
            hash(id(pool[i])): probs[i]
            for i in range(len(probs))
        }

        # creating a lottery
        tickets = []
        for ticket, prob in probs_dict.items():
            for i in range(int(prob * 10)):
                tickets.append(ticket)

        self.random_state.shuffle(tickets)

        # if self.num_iterations == 10 and self.population_size == 5 and
        for i in range(self.population_size):

            if len(tickets) > 0:

                chosen_ticket = self.random_state.choice(tickets)
                new_population.append(hashes_pool[chosen_ticket])

                # new_population.append()

                # removing all the unnecessary tickets
                tickets = [ticket for ticket in filter(lambda elem: elem != chosen_ticket, tickets)]
            else:

                weak_elements = [elem for elem in pool if self.calc_price(elem) == 0]

                for i in range(self.population_size - len(new_population)):
                    idx = self.random_state.choice([i for i in range(len(weak_elements))])
                    new_population.append(weak_elements[idx])
                break

        return new_population


    def tournament_selection(self, pool, tour_size=2):

        new_population = []

        # new_population_hashes = []
        new_pool = [
            (hash(id(pool_elem)), self.calc_price(pool_elem), pool_elem)
            for pool_elem in pool
        ]

        while len(new_population) < self.population_size:

            smpl = sample(new_pool, tour_size)
            smpl.sort(key=lambda subset: subset[1])

            winner = smpl[0]

            new_population.append(winner[2])
            # new_population_hashes.append(winner[0])

            new_pool.remove(winner)

        return new_population



    def optimize(self):

        for e in range(self.num_iterations):

            new_population = []
            for i in range(self.population_size):
                if self.random_state.uniform() < 0.2:

                    idx = self.random_state.randint(0, len(self.population) - 1)

                    if idx == i:
                        idx = (idx + 1) % len(self.population)

                    new_population.append(
                        self.next_state(
                            list(self.crossover(self.population[i], self.population[idx]))
                        )
                    )

                else:
                    try:
                        new_population.append(self.next_state(list(self.population[i])))
                    except:
                        breakpoint()

            pool = self.population + new_population

            self.population = self.selection(pool)
            self.log += self.population

        best_state = self.find_best(self.log)

        return best_state, self.calc_price(best_state)