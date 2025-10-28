#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mysqrt.py — Implémentations "maison" de la racine carrée + tests intégrés.
- sqrt_newton: méthode de Newton/Babylone (flottants, option complexes)
- sqrt_bisect: bissection robuste (flottants)
- isqrt_binary: racine carrée entière (grands entiers)
Exécution:
  - Calcul direct:      python mysqrt.py --method newton --x 2
  - Laisser par défaut: python mysqrt.py -x 2
  - Tests intégrés:     python mysqrt.py --test
Sans import de bibliothèque mathématique. Utilise uniquement les opérations de base.
"""

from __future__ import annotations
import argparse
import sys

# --------- Petites utilitaires sans "math" ----------
def is_nan(x: float) -> bool:
    # Détecte NaN sans import: NaN != NaN est True en IEEE-754
    return x != x
 
def is_close(a: float, b: float, rel: float = 1e-12, abs_: float = 1e-15) -> bool:
    # Proche "maison" (type math.isclose) pour les tests
    diff = a - b
    if diff < 0:
        diff = -diff
    aa = a if a >= 0 else -a
    bb = b if b >= 0 else -b
    scale = 1.0
    if aa > scale:
        scale = aa
    if bb > scale:
        scale = bb
    tol = abs_
    reltol = rel * scale
    if reltol > tol:
        tol = reltol
    return diff <= tol

# --------- Implémentations racine carrée ----------

def sqrt_newton(x: float, tol: float = 1e-12, max_iter: int = 100, allow_complex: bool = False):
    """
    Racine carrée par Newton/Babylone.
    - Pas d'import math, uniquement opérations de base.
    - Convergence rapide pour x >= 0.
    - allow_complex=True -> retourne un complex pour x < 0 (0 + i*sqrt(|x|)).
    """
    # Gestion bool -> cohérent avec int(bool)
    if isinstance(x, bool):
        x = 1.0 if x else 0.0

    # Propagation des NaN/Inf
    if is_nan(x):
        return x
    if x == float('inf'):
        return x
    if x == float('-inf'):
        return float('nan')

    # Négatifs
    if x < 0.0:
        if allow_complex:
            r = sqrt_newton(-x, tol=tol, max_iter=max_iter, allow_complex=False)
            return complex(0.0, r if isinstance(r, float) else float(r))
        raise ValueError("sqrt_newton: racine carrée d’un nombre négatif (allow_complex=False)")

    # Cas triviaux
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0

    # Point de départ: évite divisions instables pour 0 < x < 1
    y = x if x >= 1.0 else 1.0

    for _ in range(max_iter):
        if y == 0.0:
            # Sécurité (ne devrait pas arriver avec nos choix)
            y = 1.0
        y_next = 0.5 * (y + (x / y))
        # Critère d'arrêt relatif+absolu
        dy = y_next - y
        if dy < 0:
            dy = -dy
        scale = y_next if y_next >= 1.0 else 1.0
        if dy <= tol * scale:
            return y_next
        y = y_next

    return y  # meilleure approx après max_iter


def sqrt_bisect(x: float, tol: float = 1e-12, max_iter: int = 200):
    """
    Racine carrée par bissection, sans overflow:
    On évite mid*mid en comparant mid <= x/mid quand mid>0.
    """
    if isinstance(x, bool):
        x = 1.0 if x else 0.0
    if is_nan(x):
        return x
    if x == float('inf'):
        return x
    if x == float('-inf'):
        return float('nan')
    if x < 0.0:
        raise ValueError("sqrt_bisect: x négatif")
    if x == 0.0 or x == 1.0:
        return x

    lo = 0.0
    hi = x if x >= 1.0 else 1.0

    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        # Arrêt sur largeur d’intervalle
        width = hi - lo
        if width <= tol * (hi if hi >= 1.0 else 1.0):
            return mid
        if mid == 0.0:
            lo = mid  # continue à avancer
            continue
        # Test monotone sans mid*mid: mid^2 <= x  <=>  mid <= x/mid (mid>0)
        if mid <= (x / mid):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def isqrt_binary(n: int) -> int:
    """
    Racine carrée entière: renvoie r = floor(sqrt(n)) pour n >= 0.
    Fonctionne pour des entiers très grands (arithmétique Python illimitée).
    """
    if not isinstance(n, int):
        raise TypeError("isqrt_binary: n doit être un int")
    if n < 0:
        raise ValueError("isqrt_binary: n négatif")
    if n < 2:
        return n
    lo, hi = 1, n // 2 + 1
    while lo < hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == n:
            return mid
        if sq < n:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1  # plus grand entier t.q. r^2 <= n


# --------- Interface CLI ----------
def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Racines carrées maison + tests")
    p.add_argument("-x", "--x", type=str, help="Valeur pour laquelle calculer la racine (float ou int)")
    p.add_argument("--method", choices=["newton", "bisect", "isqrt"], default="newton",
                   help="Méthode de calcul (newton par défaut)")
    p.add_argument("--tol", type=float, default=1e-12, help="Tolérance relative (flottants)")
    p.add_argument("--max-iter", type=int, default=100, help="Itérations max (newton/bisect)")
    p.add_argument("--allow-complex", action="store_true", help="Autoriser les complexes pour x<0 (newton)")
    p.add_argument("--test", action="store_true", help="Exécuter les tests intégrés et quitter")
    return p.parse_args(argv)


# --------- Tests intégrés (sans unittest/pytest) ----------
def _residual_ok(y: float, x: float, tol: float) -> bool:
    # Valide y comme sqrt(x) via résidu: |y^2 - x| petit.
    # Attention overflow si |y| très grand; ici on utilise des cas de test raisonnables.
    r = y * y - x
    if r < 0:
        r = -r
    scale = x if x >= 1.0 else 1.0
    return r <= tol * scale

def run_tests(verbose: bool = True) -> int:
    ok = True
    def check(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            if verbose:
                print("FAIL:", msg)
        elif verbose:
            print("OK  :", msg)

    # Cas simples
    for val in [0.0, 1.0, 4.0, 9.0, 1e-8, 1e-3, 2.0, 3.0, 10.0, 1e6]:
        y = sqrt_newton(val)
        check(_residual_ok(y, val, 1e-12), f"sqrt_newton résidu pour x={val}")

    for val in [0.0, 1.0, 4.0, 9.0, 2.0, 3.0, 10.0, 1e6]:
        y = sqrt_bisect(val)
        check(_residual_ok(y, val, 1e-12), f"sqrt_bisect résidu pour x={val}")

    # Accord entre méthodes
    for val in [1e-8, 1e-6, 0.5, 2.0, 3.0, 7.5, 123.456, 1e6]:
        a = sqrt_newton(val, tol=1e-13, max_iter=200)
        b = sqrt_bisect(val, tol=1e-13, max_iter=400)
        check(is_close(a, b, rel=1e-12, abs_=1e-14), f"newton≈bisect pour x={val}")

    # Négatifs
    try:
        _ = sqrt_newton(-4.0)
        check(False, "sqrt_newton(-4) aurait dû lever")
    except ValueError:
        check(True, "sqrt_newton(-4) lève bien ValueError")

    z = sqrt_newton(-4.0, allow_complex=True)
    check((isinstance(z, complex) and is_close(z.real, 0.0) and is_close(z.imag, 2.0)),
          "sqrt_newton(-4, complex) == 2i")

    # NaN / Inf
    nan = float('nan')
    inf = float('inf')
    n1 = sqrt_newton(nan); n2 = sqrt_bisect(nan)
    check(is_nan(n1), "sqrt_newton(NaN) -> NaN")
    check(is_nan(n2), "sqrt_bisect(NaN) -> NaN")

    check(sqrt_newton(inf) == inf, "sqrt_newton(+inf) -> +inf")
    check(sqrt_bisect(inf) == inf, "sqrt_bisect(+inf) -> +inf")

    # isqrt_binary
    ints = [0, 1, 2, 3, 4, 15, 16, 24, 25, 10**12, (10**12)-1]
    for n in ints:
        r = isqrt_binary(n)
        cond = (r * r <= n) and ((r + 1) * (r + 1) > n)
        check(cond, f"isqrt_binary n={n} -> r={r} OK")

    if verbose:
        print("\nRésumé des tests:", "SUCCESS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    args = parse_args(argv)

    if args.test:
        sys.exit(run_tests(verbose=True))

    if args.x is None:
        print("Erreur: Fournis une valeur avec -x/--x (ex: -x 2.0). Ou lance --test pour les tests.")
        return 2

    # Parsing de x selon la méthode
    if args.method == "isqrt":
        try:
            n = int(args.x, 0) if isinstance(args.x, str) else int(args.x)  # supporte '0x...' etc.
        except Exception:
            print("Erreur: isqrt attend un entier (ex: --method isqrt -x 123456).")
            return 2
        r = isqrt_binary(n)
        print(r)
        return 0
    else:
        # Méthodes flottantes
        try:
            # Autorise "nan", "inf", "-inf"
            x = float(args.x)
        except Exception:
            print("Erreur: newton/bisect attend un flottant (ex: -x 2.5).")
            return 2

        if args.method == "newton":
            y = sqrt_newton(x, tol=args.tol, max_iter=args.max_iter, allow_complex=args.allow_complex)
        else:
            if x < 0 and args.allow_complex:
                print("Attention: bisect ne gère pas les complexes. Utilise --method newton --allow-complex.")
                return 2
            y = sqrt_bisect(x, tol=args.tol, max_iter=args.max_iter)

        # Affichage compact
        print(y)
        return 0


if __name__ == "__main__":
    sys.exit(main())
