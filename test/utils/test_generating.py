import unittest
from src.utils.data_generator import generate_test_by_path

class TestGenerating(unittest.TestCase):

    def test_generating_by_path(self):

        tab = generate_test_by_path(pocz=3, kon=5, n=3, currencyNumber=10)

        with open("../../data/paths_prepared.txt", "w") as paths_file:
            for tab_chunk in tab:
                str_tab = " ".join([str(elem) for elem in tab_chunk])
                str_tab += "\n"
                paths_file.write(str_tab)
