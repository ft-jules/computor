"""
Tests unitaires pour les nombres complexes.
"""

import unittest
from src.core.complex import Complex
from src.core.rational import Rational

class TestComplex(unittest.TestCase):
    
    def test_init_display(self):
        # 0 + 1i -> "i"
        self.assertEqual(str(Complex(0, 1)), "i")
        # 2 + 0i -> "2"
        self.assertEqual(str(Complex(2, 0)), "2")
        # 2 - 3i -> "2 - 3i"
        self.assertEqual(str(Complex(2, -3)), "2 - 3i")

    def test_add(self):
        c1 = Complex(1, 2) # 1 + 2i
        c2 = Complex(3, 4) # 3 + 4i
        res = c1 + c2
        self.assertEqual(str(res), "4 + 6i")

    def test_mul_i(self):
        # i * i = -1
        i = Complex(0, 1)
        res = i * i
        self.assertEqual(str(res), "-1")

    def test_div(self):
        # (1 + 2i) / (1 + i)
        # Attendu : 3/2 + 1/2i
        c1 = Complex(1, 2)
        c2 = Complex(1, 1)
        res = c1 / c2
        self.assertEqual(res.real, Rational(3, 2))
        self.assertEqual(res.imaginary, Rational(1, 2))
        self.assertEqual(str(res), "3/2 + 1/2i")

    def test_pow(self):
        # i^2 = -1
        i = Complex(0, 1)
        self.assertEqual(str(i**2), "-1")
        # i^3 = -i
        self.assertEqual(str(i**3), "-i")
        # i^4 = 1
        self.assertEqual(str(i**4), "1")

if __name__ == '__main__':
    unittest.main()