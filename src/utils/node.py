import numpy as np

class Node:

    def __init__(self, new_curr=None, rate=None, heur=None, old_obj=None):

        if new_curr is None:
            raise Exception("Empty node")

        if old_obj is None:
            self.history = [new_curr]
            self.cost = rate
            self.value = rate * heur
        else:
            self.history = list(old_obj.history)
            self.history.append(new_curr)
            self.cost = old_obj.cost * rate
            self.value = self.cost * heur

    def push_back(self, new_curr, rate, heuristic):

        self.history.append(new_curr)
        self.cost *= rate
        self.value = self.cost * heuristic

    def is_acceptable(self, fin):
        return self.history[-1] == fin

    def is_invalid(self):
        last_in_history = self.history[-1]
        return any([elem == last_in_history for elem in self.history])

    def get_history(self):
        return np.array(self.history)

    def get_current(self):
        return self.history[-1]

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self,other):
        return self.value <= other.value

    def __ne__(self, other):
        return self.value != other.value

    def __eq__(self, other):
        return self.value == other.value
