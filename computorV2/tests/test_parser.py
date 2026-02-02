"""
Tests unitaires pour le Parser.
"""

import unittest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.core.rational import Rational
from src.core.complex import Complex
from src.core.matrix import Matrix

class TestParser(unittest.TestCase):
    
    def evaluate(self, text):
        lexer = Lexer(text)
        parser = Parser(lexer)
        return parser.parse()

    def test_basic_arithmetic(self):
        # 1 + 2 * 3 = 7 (Priorité respectée)
        res = self.evaluate("1 + 2 * 3")
        self.assertEqual(res, Rational(7))

    def test_parentheses(self):
        # (1 + 2) * 3 = 9
        res = self.evaluate("(1 + 2) * 3")
        self.assertEqual(res, Rational(9))

    def test_complex_parsing(self):
        # 1 + 2i
        res = self.evaluate("1 + 2 * i")
        self.assertEqual(res, Complex(1, 2))

    def test_matrix_parsing(self):
        # [[1, 2]; [3, 4]]
        res = self.evaluate("[[1, 2]; [3, 4]]")
        self.assertIsInstance(res, Matrix)
        self.assertEqual(res.rows, 2)
        # Vérif calcul dans matrice
        res2 = self.evaluate("[[1 + 1]]")
        self.assertEqual(str(res2.data[0][0]), "2")

    def test_matrix_mult(self):
        # [[1, 2]] ** [[3]; [4]]  (1*3 + 2*4 = 11)
        res = self.evaluate("[[1, 2]] ** [[3]; [4]]")
        self.assertEqual(str(res.data[0][0]), "11")

if __name__ == '__main__':
    unittest.main()