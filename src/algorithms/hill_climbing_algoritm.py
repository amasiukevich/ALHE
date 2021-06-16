from .base_algorithm import BaseAlgorithm

class HillClimbingAlgorithm(BaseAlgorithm):

    def __init__(self,
                 begin_curr_idx,
                 end_curr_idx,
                 num_currs,
                 rates_data,
                 random_state,
                 next_state_method="all",
                 num_iterations=100):
        super().__init__(begin_curr_idx, end_curr_idx, num_currs, rates_data, random_state, next_state_method)
        self.num_iterations = num_iterations
        self.random_state = random_state

    def optimize(self):

        no_change_iters = 0
        prev_state = self.init_state()

        while no_change_iters < self.num_iterations:
            curr_state = self.next_state(list(prev_state))

            if self.calc_price(curr_state) > self.calc_price(prev_state):
                prev_state = curr_state
                no_change_iters = 0
            else:
                no_change_iters += 1

        return prev_state, self.calc_price(prev_state)
