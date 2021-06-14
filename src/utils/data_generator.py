import numpy as np

def generate_data(n_currs):

    currs = np.zeros(shape=(n_currs, n_currs))
    for i in range(n_currs):
        for j in range(n_currs):
            if i == j:
                currs[i][j] = np.random.random()
            else:
                currs[i][j] = (1 / currs[j][i]) - np.random.random()

    return currs
