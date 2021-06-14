from src.utils.data_loader import load_rates, save_rates
import numpy as np
import unittest


class TestDataLoader(unittest.TestCase):



    def saving_loading_rates(self, data_portion, test_filename):

        save_rates(data_portion, test_filename)
        new_rates = load_rates(test_filename)[0]


        return all([
            [np.isclose(data_portion[i][j], new_rates[i][j]) for j in range(len(data_portion[0]))]
        ] for i in range(len(data_portion)))


    def test_data1(self):

        test1 = [
             [0,    2,    4  ],
             [0.4,  0,    1.9],
             [0.2,  0.5,  0  ]
        ]
        new_rates = self.saving_loading_rates(test1, "../../data/test_data1.txt")
        self.assertEqual(np.array(test1), new_rates)



    def test_data2(self):

        test2 = [
            [0, 0.19, 0.22, 0.26],
            [5.24, 0, 1.15, 1.38],
            [4.54, 0.86, 0, 1.20],
            [3.79, 0.72, 0.83, 0]
        ]
        new_rates = self.saving_loading_rates(test2, "../../data/test_data2.txt")
        self.assertEqual(np.array(test2), new_rates)



    def test_data3(self):

        test3 = [
            [0, 0.19, 0.22, 0.26, 19.85],
            [5.24, 0, 1.15, 1.38, 104.03],
            [4.54, 0.86, 0, 1.20, 90.50],
            [3.79, 0.72, 0.83, 0, 75.29],
            [0.05, 0.0096, 0.011, 0.013, 0]
        ]

        new_rates = self.saving_loading_rates(test3, "../../data/test_data3.txt")
        self.assertEqual(np.array(test3), new_rates)
