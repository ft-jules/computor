"""
Classe Rational : Gère les nombres rationnels (numérateur/dénominateur).
"""

class Rational:
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise MathError("Division by zero")

        if isinstance(numerator, float):
            n, d = numerator.as_integer_ratio()
            numerator = n
            denominator = denominator * d
        if isinstance(denominator, float):
            n, d = denominator.as_integer_ratio()
            numerator = numerator * d
            denominator = n

        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        a = abs(int(numerator))
        b = abs(int(denominator))
        while b:
            a, b = b, a % b
        common = a

        self.numerator = int(numerator // common)
        self.denominator = int(denominator // common)

    def __repr__(self):
        if self.denominator == 1:
            return f"{self.numerator}"
        return f"{self.numerator}/{self.denominator}"

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            other = Rational(other)
        if not isinstance(other, Rational):
            return False
        return self.numerator == other.numerator and self.denominator == other.denominator

# -------------------OPERATIONS ARITHMETIQUES------------------- #

    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Rational(other)
        new_num = self.numerator * other.denominator + other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Rational(new_num, new_den)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Rational(other)
        new_num = self.numerator * other.denominator - other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Rational(new_num, new_den)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Rational(other)
        return Rational(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = Rational(other)
        if other.numerator == 0:
            raise MathError("Division by zero")
        return Rational(self.numerator * other.denominator, self.denominator * other.numerator)

    def __pow__(self, power):
        if not isinstance(power, int):
            raise MathError("Exponent must be an interger")
        if power < 0:
            return Rational(self.denominator, self.numerator) ** -power
        return Rational(self.numerator ** power, self.denominator ** power)