"""
Tests unitaires pour les Variables.
"""

import unittest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.core.context import Context
from src.core.rational import Rational

class TestVariables(unittest.TestCase):
    def test_assignment_and_retrieval(self):
        ctx = Context()
        
        # 1. On assigne x = 10
        lexer = Lexer("x = 10")
        parser = Parser(lexer, ctx)
        res = parser.parse()
        self.assertEqual(res, Rational(10))
        
        # 2. On utilise x dans un calcul : x * 2
        lexer = Lexer("x * 2")
        parser = Parser(lexer, ctx) # On passe le MÊME contexte
        res = parser.parse()
        self.assertEqual(res, Rational(20))

    def test_unknown_variable(self):
        ctx = Context()
        lexer = Lexer("y + 1")
        parser = Parser(lexer, ctx)
        with self.assertRaises(Exception): # MathError
            parser.parse()

if __name__ == '__main__':
    unittest.main()