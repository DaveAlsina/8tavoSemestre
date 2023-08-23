import unittest
from calc import Calculator

class TestCalculator(unittest.TestCase):
    def test_addition(self):
        result = Calculator.add(1, 2)
        self.assertEqual(result, 3)

        result = Calculator.add(-1, 2)
        self.assertEqual(result, 1)

        result = Calculator.add(2, -1)
        self.assertEqual(result, 1)

        result = Calculator.add(-1, -2)
        self.assertEqual(result, -3)
    
    def test_subtraction(self):
        result = Calculator.sub(1, 2)
        self.assertEqual(result, -1)

        result = Calculator.sub(-1, 2)
        self.assertEqual(result, -3)

        result = Calculator.sub(2, -1)
        self.assertEqual(result, 3)

        result = Calculator.sub(-1, -2)
        self.assertEqual(result, 1)

    def test_multiplication(self):
        result = Calculator.mul(1, 2)
        self.assertEqual(result, 2)

        result = Calculator.mul(-1, 2)
        self.assertEqual(result, -2)

        result = Calculator.mul(2, -1)
        self.assertEqual(result, -2)

        result = Calculator.mul(-1, -2)
        self.assertEqual(result, 2)
    
    def test_division(self):
        result = Calculator.div(1, 2)
        self.assertEqual(result, 0.5)

        result = Calculator.div(-1, 2)
        self.assertEqual(result, -0.5)

        result = Calculator.div(2, -1)
        self.assertEqual(result, -2)

        result = Calculator.div(-1, -2)
        self.assertEqual(result, 0.5)

        result = Calculator.div(-1, 0)
        self.assertEqual(result, float("inf"))

    def test_integer_division(self):
        result = Calculator.idiv(1, 2)
        self.assertEqual(result, 0)

        result = Calculator.idiv(3, 2)
        self.assertEqual(result, 1)

        result = Calculator.idiv(-1, 2)
        self.assertEqual(result, 0)

        result = Calculator.idiv(2, -1)
        self.assertEqual(result, -2)

        result = Calculator.idiv(-1, -2)
        self.assertEqual(result, 0)

        result = Calculator.idiv(-1, 0)
        self.assertEqual(result, float("inf"))

if __name__ == '__main__':
    unittest.main()