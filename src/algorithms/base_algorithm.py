from abc import ABC, abstractmethod
from typing import List
import numpy as np


from collections import Counter


class BaseAlgorithm(ABC):


    def __init__(self, begin_curr_idx, end_curr_idx, num_currs, rates_data, random_state, next_state_method="modify"):

        self.begin_curr_idx = begin_curr_idx
        self.end_curr_idx = end_curr_idx
        self.num_currs = num_currs
        self.rates = rates_data
        self.next_state_method = next_state_method
        self.random_state = random_state

    def init_state(self, shuffling=True):

        state = [curr_num for curr_num in range(self.num_currs)]

        if shuffling:
            self.random_state.shuffle(state)

        # beginning currency number on the first position
        # ending currency number on the last position

        if state[0] == self.end_curr_idx and state[-1] == self.begin_curr_idx:
            state.reverse()

        else:
            for i in range(self.num_currs):
                if state[i] == self.begin_curr_idx:
                    state[i], state[0] = state[0], state[i]

                if state[i] == self.end_curr_idx:
                    state[i], state[-1] = state[-1], state[i]

        return state



    def calc_price(self, state: list):

        """
        :param state:   a sequence of the numbers of currencies
        :return:        float value of price function
        """
        price = 1
        for i in range(len(state) - 1):
            try:
                price *= self.rates[ state[i] ][ state[i + 1] ]
            except:
                breakpoint()

        return price


    def next_state(self, current_state: list):

        next_state = current_state.copy()

        if self.next_state_method == "shuffle":
            next_state = self.shuffle_state(next_state)
        elif self.next_state_method == "swap":
            next_state = self.make_swap(next_state)
        elif self.next_state_method == "add":
            next_state = self.add_item(next_state)
        elif self.next_state_method == "all":
            next_state = self.next_state_combined(next_state)

        return next_state



    def next_state_combined(self, state: list):

        prob = self.random_state.uniform(0, 1)
        if prob <= 0.25:
            return self.shuffle_state(state.copy())
        elif prob <= 0.5:
            return self.make_swap(state.copy())
        elif prob <= 0.75:
            return self.add_item(state.copy())
        else:
            return self.remove_item(state.copy())


    def shuffle_state(self, state: list):

        if len(state) <= 3:
            return state

        part_to_shuffle = state[1:-1]
        self.random_state.shuffle(part_to_shuffle)

        result = [state[0]] + part_to_shuffle + [state[-1]]

        return result


    def make_swap(self, state: list):

        if len(state) <= 3:
            return state

        part_to_swap = state[1: -1]

        # random
        indexes = self.random_state.randint(len(state) - 2, size=2)
        index_left, index_right = np.min(indexes), np.max(indexes)

        part_to_swap[index_left], part_to_swap[index_right] = part_to_swap[index_right], part_to_swap[index_left]

        return [state[0]] + part_to_swap + [state[-1]]


    def remove_item(self, state: list):

        if len(state) <= 2:
            return state

        part_to_remove_from = state[1: -1]
        index = self.random_state.randint(len(state) - 2)
        part_to_remove_from.pop(index)

        new_state = [state[0]] + part_to_remove_from + [state[-1]]
        new_state = self.remove_cycles(new_state)

        return new_state


    def add_item(self, state: list):

        if len(state) <= 2:
            return state

        index_to_add = self.random_state.randint(1, len(state) - 1)

        new_value = self.random_state.randint(self.num_currs)
        new_state = self.remove_cycles(state[:index_to_add] + [new_value] + state[index_to_add:])

        return new_state


    def remove_cycles(self, state: list):

        new_state = []
        outter_count = 0
        while outter_count < len(state):
            found = False

            inner_count = outter_count + 1
            while inner_count < len(state):

                if state[outter_count] == state[inner_count]:
                    found = True
                    new_state.append(state[inner_count])
                    outter_count = inner_count
                    break

                inner_count += 1

            if not found:
                new_state.append(state[outter_count])

            outter_count += 1

        return new_state



    def find_best(self, states: List[list]):

        assert len(states) >= 1

        best_state = states[0]
        best_score = (-1) * float("inf")

        for state in states:
            if self.calc_price(state) > best_score:
                best_state = state
                best_score = self.calc_price(state)

        return best_state


    @abstractmethod
    def optimize(self):
        pass