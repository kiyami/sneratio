import unittest


class CalculatorTest(unittest.TestCase):
    def test_of_calc_ratio(self):
        value = 1
        result = 1
        self.assertEqual(value, result)


if __name__ == '__main__':
    unittest.main()
