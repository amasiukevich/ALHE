import numpy as np
import pandas as pd

def load_rates(filename):
    rates = []
    n_currs = 0
    with open(filename, "r") as currs_file:
        for line in currs_file:
            tab = [float(x) for x in line.split()]
            rates.append(tab)
            n_currs += 1

    rates = np.array(rates)
    return rates, n_currs


def save_rates(rates, filename):
    with open(filename, "w") as currs_file:
        for t in rates:
            currs_file.write(f'{" ".join([str(elem) for elem in t])}\n')

def load_csv(filename):

    data = pd.read_csv(filename, sep=";").values
    data = [list([float(elem) for elem in data_chunk[0].split(",")]) for data_chunk in data]

    return data, len(data)