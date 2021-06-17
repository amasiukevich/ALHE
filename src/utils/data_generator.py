import numpy as np
from random import sample

def generate_data(n_currs):

    currs = np.zeros(shape=(n_currs, n_currs))
    for i in range(n_currs):
        for j in range(n_currs):
            if i == j:
                currs[i][j] = np.random.random()
            else:
                currs[i][j] = (1 / currs[j][i]) - np.random.random()

    return currs


def generate_test_by_path(pocz, kon, n, currencyNumber):
    tab = np.array([0.1])
    tab.resize([currencyNumber, currencyNumber])
    tab.fill(0.5)
    for i in range(n):
        x = np.random.randint(0,currencyNumber-1)
        ciag = sample(range(currencyNumber), x)

        if pocz in ciag:
            ciag.remove(pocz)
        if kon in ciag:
            ciag.remove(kon)
        ciag.insert(0,pocz)
        ciag.append(kon)
        print(ciag)
        for j in range(len(ciag)-1):
            tab[ciag[j]][ciag[j+1]] = i

    return tab