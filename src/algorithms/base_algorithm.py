from abc import ABC, abstractmethod

import numpy as np


class BaseAlgorithm(ABC):


    def __init__(self, begin_curr_idx, end_curr_idx, num_currs, rates_data):

        self.begin_curr_idx = begin_curr_idx
        self.end_curr_idx = end_curr_idx
        self.num_currs = num_currs
        self.rates = rates_data

    def init_state(self, shuffling=True):

        state = [curr_num for curr_num in range(self.num_currs)]

        if shuffling:
            np.random.shuffle(state)

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
            price *= self.rates[ state[i] ][ state[i + 1] ]

        return price


    def next_state_big(self, state: list):

        prob = np.random.uniform()

        if prob < 0.333:    # TODO: bug for big states???
            temp = state[1: -1]
            np.shuffle(temp)
            next_state = [state[0]] + temp + [state[-1]]
        elif prob < 0.666:     # removing random number of currencies, but less than len // 2

            num_currs_to_remove = np.random.randint(1, len(state // 2))
            for i in range(num_currs_to_remove):
                idx = np.random.randint(1, len(state) - 2)
                del state[idx]

        else:   # Random number of swaps

            num_swaps = np.random.randint(1, len(state) // 4)
            for i in range(num_swaps):
                idx1, idx2 = np.random.randint(1, len(state - 2)), np.random.randint(1, len(state) - 2)
                state[idx1], state[idx2] = state[idx2], state[idx1]

        return state


    def next_state_small(self, state: list):

        prob = np.random.uniform()

        if prob < 0.333 and len(state) >= 4:    # random swap
            idx1, idx2 = np.random.randint(1, len(state) - 2), np.random.randint(1, len(state) - 2)

            while idx1 == idx2:
                idx2 = np.random.randint(1, len(state) - 2)
            state[idx1] , state[idx2] = state[idx2], state[idx1]

        elif prob < 0.666 and len(state) > 2:
            idx = np.random.randint(1, len(state) - 2)
            del state[idx]

        elif len(state) != self.num_currs:
            temp = [x for x in range(self.num_currs)]
            for item in state:
                temp[item] = -1
            temp2 = []
            for elem in temp:
                if elem != -1:
                    temp2.append(elem)

            idx1 = np.random.randint(0, len(temp2) - 1)
            idx2 = np.random.randint(1, len(state) - 1)

            state.insert(idx2, temp2[idx1])

        return state


    def next_state(self, state: list):
        return self.next_state_small(state) if len(state) < 10 else self.next_state_big(state)

    def find_best(self, states: list[list]):
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