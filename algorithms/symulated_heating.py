from .base_algorithm import BaseAlgorithm

import numpy as np

class SymulatedHeating(BaseAlgorithm):


    def __init__(self, heat=10):
        self.heat = heat
        self.log = []


    def calc_heat(self, price1, price2):
        return np.exp((-1) * (np.abs(price1 - price2) / self.heat))


    def optimize(self):
        pass