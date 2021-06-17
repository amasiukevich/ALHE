from .base_algorithm import BaseAlgorithm
from src.utils.node import Node
from queue import PriorityQueue


class AStar(BaseAlgorithm):

    def __init__(self,
                 begin_curr_idx,
                 end_curr_idx,
                 num_currs,
                 rates_data):
        super().__init__(begin_curr_idx, end_curr_idx, num_currs, rates_data, random_state=None)

        self.queue = PriorityQueue()

    def optimize(self):

        visited = [-1] * self.num_currs

        self.queue.put((-1, Node(
            self.begin_curr_idx,
            1,
            self.heuristic(self.begin_curr_idx)
        )))

        while not self.queue.empty():
            node = self.queue.get()[1]

            if node.is_invalid():
                continue
            if node.is_acceptable(self.end_curr_idx):
                return node.history, node.cost

            for i in range(len(self.rates)):
                value = self.rates[node.get_current()][i] * node.cost

                if value > visited[i]:
                    visited[i] = value
                    value *= (-1) * self.heuristic(i)
                    self.queue.put((value, Node(
                        i,
                        self.rates[node.get_current()][i],
                        self.heuristic(i),
                        node
                    )))

    def heuristic(self, currency):
        return self.rates[currency][self.end_curr_idx]