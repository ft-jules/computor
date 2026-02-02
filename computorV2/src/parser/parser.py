"""
Analyse la liste de tokens et construit l'AST (Abstract Syntax Tree).
"""

from src.lexer.tokens import TokenType
from src.utils.errors import ParseError
from src.core.rational import Rational
from src.core.complex import Complex
from src.core.matrix import Matrix

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise ParseError("Invalid synthax")

    def eat(self, token_type): #compare avec type attendu, avance ou error
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    # NIVEAU 1 : Nombres, Parentheses
    def factor(self):
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Rational(token.value)
        
        if token.type == TokenType.IMAGINARY:
            self.eat(TokenType.IMAGINARY)
            return Complex(0, 1)

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        if token.type == TokenType.LBRACKET:
            return self.matrix()
        
        self.error()

    # GESTION DES MATRICES
    def matrix(self):
        self.eat(TokenType.LBRACKET)
        data = []

        while self.current_token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            row = []
            row.append(self.expr())

            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                row.append(self.expr())

            self.eat(TokenType.RBRACKET)
            data.append(row)

            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
        
        self.eat(TokenType.RBRACKET)
        return Matrix(data)


    # NIVEAU 2 : Puissances
    def power(self):
        node = self.factor()

        while self.current_token.type == TokenType.POW:
            token = self.current_token
            self.eat(TokenType.POW)
            node = node ** self.factor()

        return node

    # NIVEAU 3 : Termes(*, /, %, **)
    def term(self):
        node = self.power()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV, TokenType.MOD, TokenType.MAT_MUL):
            token = self.current_token

            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                node = node * self.power()
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
                node = node / self.power()
            elif token.type == TokenType.MOD:
                self.eat(TokenType.MOD)
                #node = node % self.power()
                self.error()
            elif token.type == TokenType.MAT_MUL:
                self.eat(TokenType.MAT_MUL)
                node = node * self.power()
        return node

    # NIVEAU 4 : Expresssions (+, -)
    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                node = node + self.term()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                node = node - self.term()
        return node

    def parse(self):
        return self.expr()