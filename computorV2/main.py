"""
Point d'entrée du programme. Lance le shell interactif.
"""

"""
BONUS:
division par des fractions avec la sous couche de rationels Expression
pas avec methode float sale car (2^1/2)^2 = 1.99999999

faire une interface pour le projet
"""

import sys
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.core.context import Context
from src.core.polynomial import Polynomial
from src.core.rational import Rational
from src.core.complex import Complex
from src.utils.errors import MathError, ParseError

def hanlde_equation(line, context):
    expression_text = line.replace('?', '')
    if '=' not in expression_text:
        print("Synthax Error: Equation must contain '='")
        return
    parts = expression_text.split('=')
    if len(parts) != 2:
        print("Synthax Error: Equation must have two parts separated by '='")
        return
    left.str = parts[0]
    right.str = parts[1]

    import copy
    equation_ctx = copy.deepcopy(context)
    X = Polynomial({1: 1})
    equation_ctx.set_variable('x', X)
    equation_ctx.set_variable('X', X)

    try:
        lexer_l = Lexer(left_str)
        parser_l = Parser(lexer_l, equation_ctx)
        left_val = parser_l.parse()
        lexer_r = Lexer(right_str)
        parser_r = Parser(lexer_r, equation_ctx)
        right_val = parser_r.parse()
        final_poly = left_val - right_val
        if not isinstance(final_poly, Polynomial):
            final_poly = Polynomial({0: final_poly})
        final_poly.solve()
    except (MathError, ParseError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def main():
    print("Welcome to ComputorV2!")
    print("Type 'exit' to quit.")

    global_context = Context()

    while True:
        try:
            text = input("> ").strip()
            if not text:
                continue
            if text.lower() in ["exit", "quit"]:
                break
            if '?' in text:
                hanlde_equation(text, global_context)
            else:
                lexer = Lexer(text)
                parser = Parser(lexer, global_context)
                result = parser.parse()
                if result is not None:
                    print(result)
        except (MathError, ParseError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
