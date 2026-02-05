import unittest
from src.core.polynomial import Polynomial
from src.core.complex import Complex

class TestPolynomial(unittest.TestCase):
    def test_reduction(self):
        # Simulation de : (x + 1) * (x - 1)
        # x est un Polynome de degré 1 : {1: 1}
        X = Polynomial({1: 1}) 
        
        # (X + 1)
        term1 = X + 1
        # (X - 1)
        term2 = X - 1
        
        # Multiplication : x^2 - 1
        res = term1 * term2
        
        # On s'attend à {2: 1, 0: -1}
        self.assertEqual(res.coeffs[2], Complex(1))
        self.assertEqual(res.coeffs[0], Complex(-1))
        self.assertNotIn(1, res.coeffs) # Pas de terme en x

    def test_solve_degree_2(self):
        # x^2 + 2x + 1 = 0  -> (x+1)^2 -> x = -1
        # Coeffs: {2:1, 1:2, 0:1}
        poly = Polynomial({2: 1, 1: 2, 0: 1})
        # Pour tester solve, on regarde juste s'il ne crash pas (car il fait des prints)
        poly.solve()

if __name__ == '__main__':
    unittest.main()