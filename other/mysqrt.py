#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Racine carrée par Newton "safeguardé" (avec repli bissection).
- Robuste: on conserve toujours un encadrement [lo, hi] de sqrt(x).
- Rapide: on accepte les pas de Newton quand ils contractent bien.
- Sûr numériquement: on compare z <= x/z plutôt que z*z <= x.

Utilisation rapide:
    python3 sqrt_newton.py 10
    python3 sqrt_newton.py --test
"""

from __future__ import annotations
import math
import random
import sys
from typing import Tuple


def _handle_special(x: float) -> Tuple[bool, float]:
    """Traite les cas spéciaux; renvoie (handled, value)."""
    if math.isnan(x):
        return True, math.nan
    if x < 0:
        raise ValueError("sqrt_newton_safe: x < 0 (pas de racine réelle).")
    if x == 0.0:
        return True, 0.0
    if math.isinf(x):
        # à ce stade x ne peut être que +inf (car x<0 déjà géré)
        return True, math.inf
    return False, 0.0


def sqrt_newton_safe(
    x: float,
    tol_rel: float = 1e-12,
    tol_abs: float = 0.0,
    max_iter: int = 100,
    accept_factor: float = 0.90,
) -> float:
    """
    Calcule sqrt(x) avec Newton "safeguardé".

    Invariants:
      - lo <= sqrt(x) <= hi
      - mise à jour via test sûr: z <= x/z  <=>  z*z <= x  (si z>0)

    Critère d'arrêt:
      hi - lo <= max(tol_abs, tol_rel * hi)

    Paramètres:
      tol_rel: tolérance relative visée (~1e-12 pour des float64)
      tol_abs: tolérance absolue (laisser 0.0 pour des x d'ordre >= 1)
      max_iter: garde-fou pour éviter boucles infinies
      accept_factor: exige une contraction (<= accept_factor * (hi - lo))
                     pour accepter le pas de Newton (0.9 recommandé).

    Exceptions:
      ValueError si x < 0.
    """
    handled, y = _handle_special(x)
    if handled:
        return y

    # Encadrement initial robuste
    if x >= 1.0:
        lo, hi = 1.0, x
    else:  # 0 < x < 1
        lo, hi = x, 1.0

    # Point de départ positif => pas de division par zéro
    y = 0.5 * (lo + hi)

    for _ in range(max_iter):
        # Arrêt si l'intervalle est suffisamment petit
        if (hi - lo) <= max(tol_abs, tol_rel * hi):
            return 0.5 * (lo + hi)

        # Proposition de Newton (Heron)
        zN = 0.5 * (y + x / y)  # y>0 garanti

        # Newton n'est accepté que s'il reste dans [lo, hi] ET contracte assez
        good = (zN > lo) and (zN < hi)
        if good:
            # contraction maximale résiduelle si l'on prenait zN
            resid = max(zN - lo, hi - zN)
            good = resid <= accept_factor * (hi - lo)

        z = zN if good else 0.5 * (lo + hi)  # repli bissection si "pas bon"

        # Mise à jour d'encadrement par comparaison sûre (évite z*z)
        if z <= x / z:
            lo = z
        else:
            hi = z

        y = z  # nouveau point pour l’itération suivante

    # Si on atteint max_iter, on renvoie le milieu (encore valide et précis)
    return 0.5 * (lo + hi)


# --- Référence pour tests: bissection "pure" (lente mais très sûre) ---
def sqrt_bisect_ref(x: float, tol_rel: float = 1e-15, tol_abs: float = 0.0) -> float:
    handled, y = _handle_special(x)
    if handled:
        return y

    if x >= 1.0:
        lo, hi = 1.0, x
    else:
        lo, hi = x, 1.0

    while (hi - lo) > max(tol_abs, tol_rel * hi):
        m = 0.5 * (lo + hi)
        if m <= x / m:  # test sûr
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


# --- Mini banc de tests -------------------------------------------------------
def _relative_error(a: float, b: float) -> float:
    if a == b:
        return 0.0
    denom = max(1.0, abs(a), abs(b))
    return abs(a - b) / denom


def run_tests(verbose: bool = False) -> None:
    # Cas déterministes
    cases = [
        0.0, 1.0, 2.0, 10.0, 1e-12, 1e-6, 1e-3, 0.5, 0.25, 0.1,
        1e6, 1e12, 1e300,
        math.inf,  # NaN testé à part (comparaison spéciale)
    ]
    for x in cases:
        y = sqrt_newton_safe(x)
        y_ref = sqrt_bisect_ref(x)
        assert y_ref == y_ref  # pas NaN
        err = _relative_error(y, y_ref)
        if verbose:
            print(f"x={x:g}\t y={y:.17g}\t y_ref={y_ref:.17g}\t rel_err={err:.3e}")
        assert err <= 5e-13, f"Erreur relative trop grande pour x={x}: {err}"

    # NaN
    y_nan = sqrt_newton_safe(math.nan)
    assert math.isnan(y_nan)

    # Aléatoires (uniformes et log-uniformes)
    rng = random.Random(1234)
    for _ in range(200):
        x = rng.random() * 1e6  # [0, 1e6]
        y = sqrt_newton_safe(x)
        y_ref = sqrt_bisect_ref(x)
        assert _relative_error(y, y_ref) <= 5e-13

    for _ in range(200):
        # log-uniforme dans [1e-300, 1e300]
        e = rng.uniform(-300.0, 300.0)
        x = 10.0 ** e
        y = sqrt_newton_safe(x)
        y_ref = sqrt_bisect_ref(x)
        assert _relative_error(y, y_ref) <= 5e-13

    # Erreur attendue sur négatifs
    try:
        sqrt_newton_safe(-1.0)
        raise AssertionError("Devrait lever ValueError pour x<0.")
    except ValueError:
        pass

    if verbose:
        print("Tous les tests ont réussi.")


# --- Interface CLI simple -----------------------------------------------------
def _main(argv=None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Racine carrée par Newton safeguardé.")
    p.add_argument("x", type=float, nargs="?", help="valeur non négative dont calculer sqrt(x)")
    p.add_argument("--tol-rel", type=float, default=1e-12, help="tolérance relative")
    p.add_argument("--tol-abs", type=float, default=0.0, help="tolérance absolue")
    p.add_argument("--max-iter", type=int, default=100, help="itérations max")
    p.add_argument("--accept", type=float, default=0.90, help="seuil de contraction pour accepter Newton")
    p.add_argument("--test", action="store_true", help="exécute le banc de tests")
    p.add_argument("--verbose", action="store_true", help="sortie verbeuse (tests)")
    args = p.parse_args(argv)

    if args.test:
        run_tests(verbose=args.verbose)
        print("OK")
        return 0

    if args.x is None:
        p.error("Veuillez fournir x (ou --test).")

    y = sqrt_newton_safe(
        args.x, tol_rel=args.tol_rel, tol_abs=args.tol_abs,
        max_iter=args.max_iter, accept_factor=args.accept
    )
    print(f"sqrt_newton_safe({args.x}) = {y:.17g}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
