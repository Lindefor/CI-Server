import unittest
import sys
import os

# Add root folder to current path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.compute_math import sum

class TestComputeMatch(unittest.TestCase):

    def test_sum_is_correct(self):
        a = 3
        b = 2
        expected_sum = 5
        actual_sum = sum(a,b)

        self.assertEqual(expected_sum, actual_sum)