import unittest

from numpy.random import RandomState

class TestRandomState(unittest.TestCase):

    def test_random_state(self):

        my_random = RandomState(42)
        random_list = [-4, 9, 4, 0, -3, -4, 8, 0, 0, -7]
        gen_random_list = []

        for i in range(10):
            gen_random_list.append(my_random.randint(-10, 10))

        print(gen_random_list)
        self.assertListEqual(gen_random_list, random_list)
