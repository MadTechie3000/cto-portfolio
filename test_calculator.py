import unittest
from calculator import Calculator


class TestCalculatorAddition(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(self.calc.add(-1, -1), -2)

    def test_add_mixed_numbers(self):
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_add_floats(self):
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3)


class TestCalculatorSubtraction(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_subtract_positive_numbers(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_subtract_negative_result(self):
        self.assertEqual(self.calc.subtract(3, 5), -2)


class TestCalculatorMultiplication(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_multiply_positive_numbers(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)

    def test_multiply_by_zero(self):
        self.assertEqual(self.calc.multiply(5, 0), 0)

    def test_multiply_negative_numbers(self):
        self.assertEqual(self.calc.multiply(-3, -4), 12)


class TestCalculatorDivision(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_divide_positive_numbers(self):
        self.assertEqual(self.calc.divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(1, 0)

    def test_divide_floats(self):
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333333333)


if __name__ == "__main__":
    unittest.main()
