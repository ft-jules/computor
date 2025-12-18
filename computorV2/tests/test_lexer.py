"""
Tests unitaires pour le Lexer.
"""
import unittest
from src.lexer.lexer import Lexer
from src.lexer.tokens import TokenType

class TestLexer(unittest.TestCase):
    
    def get_tokens(self, text):
        lexer = Lexer(text)
        tokens = []
        while True:
            tok = lexer.get_next_token()
            if tok.type == TokenType.EOF:
                break
            tokens.append(tok)
        return tokens

    def test_basic_assignment(self):
        # Ex: varA = 2
        tokens = self.get_tokens("varA = 2")
        self.assertEqual(tokens[0].type, TokenType.ID)
        self.assertEqual(tokens[0].value, "vara") # Doit être lowercased
        self.assertEqual(tokens[1].type, TokenType.ASSIGN)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, 2)

    def test_imaginary(self):
        # Ex: 2 * i + 3
        tokens = self.get_tokens("2 * i + 3")
        self.assertEqual(tokens[2].type, TokenType.IMAGINARY) # Le 'i' doit être détecté

    def test_matrix_syntax(self):
        # Ex: [[1,2];[3,4]]
        tokens = self.get_tokens("[[1,2];[3,4]]")
        token_types = [t.type for t in tokens]
        expected = [
            TokenType.LBRACKET, TokenType.LBRACKET, 
            TokenType.NUMBER, TokenType.COMMA, TokenType.NUMBER, 
            TokenType.RBRACKET, TokenType.SEMICOLON, TokenType.LBRACKET,
            TokenType.NUMBER, TokenType.COMMA, TokenType.NUMBER,
            TokenType.RBRACKET, TokenType.RBRACKET
        ]
        self.assertEqual(token_types, expected)

    def test_matrix_multiplication(self):
        # Ex: A ** B
        tokens = self.get_tokens("A ** B")
        self.assertEqual(tokens[1].type, TokenType.MAT_MUL)

if __name__ == '__main__':
    unittest.main()