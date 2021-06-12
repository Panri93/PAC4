import unittest
from utils import exercici_1

class TestExercici1(unittest.TestCase):
    def test_exercici1(self):
        self.assertEqual(exercici_1(path="/home/datasci/PycharmProjects/PAC4/data/covid_approval_polls.csv"), None)

if __name__ == '__main__':
    unittest.main()

