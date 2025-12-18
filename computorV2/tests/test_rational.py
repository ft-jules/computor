import unittest
from src.core.rational import Rational

class TestRational(unittest.TestCase):
    def test_simplification(self):
        r = Rational(2, 4)
        self.assertEqual(r.numerator, 1)
        self.assertEqual(r.denominator, 2)

    def test_sign(self):
        r = Rational(1, -2)
        self.assertEqual(r.numerator, -1)
        self.assertEqual(r.denominator, 2)
        
        r2 = Rational(-1, -2)
        self.assertEqual(r2.numerator, 1)

    def test_addition(self):
        # 1/2 + 1/3 = 5/6
        r = Rational(1, 2) + Rational(1, 3)
        self.assertEqual(r.numerator, 5)
        self.assertEqual(r.denominator, 6)

    def test_operations(self):
        r1 = Rational(1, 2)
        r2 = Rational(2, 1) # 2
        
        # Mul: 1/2 * 2 = 1
        res = r1 * r2
        self.assertEqual(res.numerator, 1)
        self.assertEqual(res.denominator, 1)

if __name__ == '__main__':
    unittest.main()