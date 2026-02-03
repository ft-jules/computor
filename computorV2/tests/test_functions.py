import unittest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.core.context import Context
from src.core.rational import Rational

class TestFunctions(unittest.TestCase):
    def test_full_flow(self):
        ctx = Context()
        
        # 1. Définition : f(x) = 2 * x + 1
        lexer = Lexer("f(x) = 2 * x + 1")
        parser = Parser(lexer, ctx)
        parser.parse()
        
        # Vérifions que c'est stocké
        func = ctx.get_function('f')
        self.assertIsNotNone(func)
        self.assertEqual(func.param_name, 'x')

        # 2. Appel : y = f(3)  -> (2*3 + 1 = 7)
        lexer = Lexer("y = f(3)")
        parser = Parser(lexer, ctx)
        res = parser.parse()
        self.assertEqual(res, Rational(7))
        
        # 3. Utilisation de la variable créée par la fonction
        lexer = Lexer("y + 3") # 7 + 3 = 10
        parser = Parser(lexer, ctx)
        res = parser.parse()
        self.assertEqual(res, Rational(10))

    def test_function_in_function(self):
        # Test avancé : g(x) = f(x) + 2
        ctx = Context()
        
        # f(x) = x * 2
        Parser(Lexer("f(x) = x * 2"), ctx).parse()
        
        # g(y) = f(y) + 1  (Note le changement de nom de paramètre pour tester l'isolation)
        Parser(Lexer("g(y) = f(y) + 1"), ctx).parse()
        
        # g(4) -> f(4) + 1 -> (4*2) + 1 -> 9
        res = Parser(Lexer("g(4)"), ctx).parse()
        self.assertEqual(res, Rational(9))

if __name__ == '__main__':
    unittest.main()