from .base_algorithm import BaseAlgorithm

class HillClimbNeightborAlgorithm(BaseAlgorithm):

    def __init__(self,
                 begin_curr_idx,
                 end_curr_idx,
                 num_currs,
                 rates_data,
                 num_iterations=420,
                 num_neighbors=2,
                 depth=2):
        super().__init__(begin_curr_idx, end_curr_idx, num_currs, rates_data)
        self.num_iterations = num_iterations
        self.num_neighbors = num_neighbors
        self.depth = depth


    def optimize(self):

        no_change_iters = 0
        state = self.init_state()

        while no_change_iters < self.num_iterations:

            tab_state = [state]
            idx = 0

            for i in range(self.depth):
                for j in range(idx, len(tab_state)):
                    for k in range(self.num_neighbors):
                        new_state = self.new_state(list(tab_state[j]))
                        tab_state.append(new_state)

                    idx += 1

            best_state = self.find_best(tab_state)

            if self.calc_price(best_state) > self.calc_price(state):
                state = best_state
                no_change_iters = 0
            else:
                no_change_iters += 1

        return state, self.calc_price(state)
