import sys
import re
from bonus_part import pars_terms


def _ft_sqrt(nombre):
    return nombre ** 0.5

def solve(polynomial, degree):
    a = polynomial.get(2, 0)
    b = polynomial.get(1, 0)
    c = polynomial.get(0, 0)
    # ax^2+bx+c

    # 4 * X^0 = 0 ou 2 * X^0 = 2 * X^0
    if degree == 0:
        if c == 0:
            print("Every real number is a solution.")
        else:
            print("No solution.")

    # 2 * X^1 + 4 * X^0 = 0 -> X = -c / b
    elif degree == 1:
        res = -c / b
        print(f"The solution is:\n{res}")

    # 3 * X^2 + 2 * X^1 + 4 * X^0 = 0
    elif degree == 2:
        delta = (b * b) - (4 * a * c)

        if delta > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            sqrt_delta = _ft_sqrt(delta)

            # (-b ± √Δ) / 2a
            sol1 = (-b - sqrt_delta) / (2 * a)
            sol2 = (-b + sqrt_delta) / (2 * a)

            print(f"{sol1}\n{sol2}")

        elif delta == 0:
            print("Discriminant is zero, the solution is:")
            # -b / 2a
            sol = -b / (2 * a)
            print(f"{sol}")

        else: # delta < 0
            print("Discriminant is strictly negative, the two complex solutions are:")
            sqrt_delta = _ft_sqrt(-delta)
            reel = -b / (2 * a)
            imag = sqrt_delta / (2 * a)

            # "X + i * Y"
            print(f"{reel} - i * {abs(imag)}")
            print(f"{reel} + i * {abs(imag)}")
def main():

    # ----------PARSING----------

    if len(sys.argv) != 2:
        print("Usage: python3 computor.py \"5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0\"")
        return

    equation = sys.argv[1].replace(" ", "")
    
    try:
        lhs, rhs = equation.split('=')
    except ValueError:
        print("Erreur de format : il faut un signe '='")
        return
    
    # Définition du motif (Pattern)
    # 1. ([-+]?\d*\.?\d+) : Capture le nombre (entier ou décimal, positif ou négatif)
    # 2. \*X\^            : Cherche littéralement "*X^"
    # 3. (\d+)            : Capture l'exposant (un nombre entier)
    pattern = r"([-+]?\d*\.?\d+)\*X\^(\d+)"

    lhs_terms = re.findall(pattern, lhs)
    rhs_terms = re.findall(pattern, rhs)

    #print(f"left terms : {lhs_terms}")
    #print(f"rigth terms : {rhs_terms}")


    # ----------REDUCTION----------

    # Dictionnaire { degré (int) : coeff (float) }
    polynomial = {}

    def add_term(coeff, exposant, signe_global=1):
        degree = int(exposant)
        valeur = float(coeff) * signe_global
        
        if degree in polynomial:
            polynomial[degree] += valeur
        else:
            polynomial[degree] = valeur

    for coeff, exposant in lhs_terms:
        add_term(coeff, exposant, 1)

    for coeff, exposant in rhs_terms:
        add_term(coeff, exposant, -1)

    #print(f"Reducted polynomial : {polynomial}")
    

    # ----------CALCUL DU DEGRÉ----------
    
    degree = 0
    for d in polynomial:
        if polynomial[d] != 0:
            if d > degree:
                degree = d

    print(f"Polynomial degree: {degree}")

    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return

    solve(polynomial, degree)


if __name__ == "__main__":
    main()