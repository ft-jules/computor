"""
Tests unitaires pour les opérations matricielles.
"""
import unittest
from src.core.matrix import Matrix
from src.core.complex import Complex
from src.utils.errors import MathError

class TestMatrix(unittest.TestCase):

    def test_init(self):
        # Création basique
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.cols, 2)
        # Vérifie que c'est bien converti en Complex
        self.assertIsInstance(m.data[0][0], Complex)

    def test_invalid_shape(self):
        # Matrice pas rectangulaire
        with self.assertRaises(MathError):
            Matrix([[1, 2], [3]])

    def test_add(self):
        m1 = Matrix([[1, 2]])
        m2 = Matrix([[3, 4]])
        res = m1 + m2
        # [1+3, 2+4] = [4, 6]
        self.assertEqual(str(res.data[0][0]), "4")
        self.assertEqual(str(res.data[0][1]), "6")

    def test_scalar_mul(self):
        m = Matrix([[1, 2], [3, 4]])
        res = m * 2
        # [[2, 4], [6, 8]]
        self.assertEqual(str(res.data[0][0]), "2")
        self.assertEqual(str(res.data[1][1]), "8")

    def test_matrix_mul(self):
        # Multiplication matricielle
        # A (2x3)  * B (3x2)  =  C (2x2)
        # [1 2 3]     [7 8]
        # [4 5 6]     [9 1]
        #             [2 3]
        
        # Calcul case (0,0) : 1*7 + 2*9 + 3*2 = 7 + 18 + 6 = 31
        
        m1 = Matrix([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix([[7, 8], [9, 1], [2, 3]])
        
        res = m1 * m2
        
        self.assertEqual(res.rows, 2)
        self.assertEqual(res.cols, 2)
        self.assertEqual(str(res.data[0][0]), "31")

    def test_matrix_mul_error(self):
        # Dimensions incompatibles (2x2) * (3x2) -> Impossible
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[1, 2], [3, 4], [5, 6]])
        with self.assertRaises(MathError):
            m1 * m2

if __name__ == '__main__':
    unittest.main()