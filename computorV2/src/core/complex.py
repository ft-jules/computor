"""
Classe Complex : Gère les nombres complexes (partie réelle + imaginaire).
"""
from .rational import Rational
from src.utils.errors import MathError

class Complex:
    def __init__(self, real, imaginary=0):
        if not isinstance(real, Rational):
            real = Rational(real)
        if not isinstance(imaginary, Rational):
            imaginary = Rational(imaginary)
        self.real = real
        self.imaginary
        