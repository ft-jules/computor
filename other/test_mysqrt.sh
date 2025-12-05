#!/usr/bin/env bash
# test_mysqrt.sh — tests CLI pour mysqrt.py (sans pytest)
# Dépendances: bash, awk, python3|python
# Usage:
#   chmod +x test_mysqrt.sh
#   ./test_mysqrt.sh
set -u  # pas -e: on doit pouvoir capturer des échecs attendus
FAILS=0
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MYSQRT="$HERE/mysqrt.py"

# Trouver Python
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else
  echo "Python introuvable (python3/python)."
  exit 1
fi

if [[ ! -f "$MYSQRT" ]]; then
  echo "mysqrt.py introuvable à côté du script."
  exit 1
fi

ok(){ echo "OK  : $*"; }
fail(){ echo "FAIL: $*"; FAILS=$((FAILS+1)); }

# Lance une commande, capture sortie et code de retour
run_capture(){
  # usage: run_capture VAROUT cmd args...
  local __var="$1"; shift
  local __out
  __out="$("$@" 2>&1)"; local __rc=$?
  printf -v "$__var" "%s" "$__out"
  return $__rc
}

# Vérifs numériques via awk
residual_ok(){ # y, x, tol
  awk -v y="$1" -v x="$2" -v tol="$3" 'BEGIN{
    if (y != y) exit 1            # NaN
    if (y ~ /inf/) exit 1         # inf
    r = y*y - x; if (r<0) r=-r
    scale = (x>=1.0? x:1.0)
    exit (r <= tol*scale ? 0:1)
  }'
}

is_close(){ # a, b, rel, abs
  awk -v a="$1" -v b="$2" -v rel="$3" -v abs="$4" 'BEGIN{
    if (a != a || b != b) exit 1
    diff = a-b; if (diff<0) diff=-diff
    aa=(a<0?-a:a); bb=(b<0?-b:b)
    scale=1.0; if (aa>scale) scale=aa; if (bb>scale) scale=bb
    tol = abs; reltol = rel*scale; if (reltol>tol) tol = reltol
    exit (diff <= tol ? 0:1)
  }'
}

# ---------- TESTS FONCTIONNELS ----------
test_newton_residual(){
  local TOL=1e-12
  local xs=(0 1 4 9 0.5 2 3 10 1000000 1e-12 1e-8 1e-3)
  for x in "${xs[@]}"; do
    local out rc
    run_capture out "$PY" "$MYSQRT" --method newton -x "$x"
    rc=$?
    if [[ $rc -ne 0 ]]; then fail "newton -x $x (rc=$rc)"; continue; fi
    if residual_ok "$out" "$x" "$TOL"; then ok "résidu newton x=$x"
    else fail "résidu newton x=$x (y=$out)"; fi
  done
}

test_bisect_residual(){
  local TOL=1e-12
  local xs=(0 1 4 9 2 3 10 1000000)
  for x in "${xs[@]}"; do
    local out rc
    run_capture out "$PY" "$MYSQRT" --method bisect -x "$x"
    rc=$?
    if [[ $rc -ne 0 ]]; then fail "bisect -x $x (rc=$rc)"; continue; fi
    if residual_ok "$out" "$x" "$TOL"; then ok "résidu bisect x=$x"
    else fail "résidu bisect x=$x (y=$out)"; fi
  done
}

test_methods_agree(){
  local REL=1e-11 ABS=1e-14
  local xs=(0.3 2 123.456 1e-12 1e12)
  for x in "${xs[@]}"; do
    local a b rcA rcB
    run_capture a "$PY" "$MYSQRT" --method newton -x "$x"; rcA=$?
    run_capture b "$PY" "$MYSQRT" --method bisect -x "$x"; rcB=$?
    if [[ $rcA -ne 0 || $rcB -ne 0 ]]; then fail "newton≈bisect x=$x (rcA=$rcA rcB=$rcB)"; continue; fi
    if is_close "$a" "$b" "$REL" "$ABS"; then ok "newton≈bisect x=$x"
    else fail "newton≈bisect x=$x (a=$a b=$b)"; fi
  done
}

test_nan_inf(){
  local out rc
  run_capture out "$PY" "$MYSQRT" --method newton -x nan; rc=$?
  [[ $rc -eq 0 && "${out,,}" == "nan" ]] && ok "newton NaN -> nan" || fail "newton NaN (rc=$rc out=$out)"

  run_capture out "$PY" "$MYSQRT" --method bisect -x nan; rc=$?
  [[ $rc -eq 0 && "${out,,}" == "nan" ]] && ok "bisect NaN -> nan" || fail "bisect NaN (rc=$rc out=$out)"

  run_capture out "$PY" "$MYSQRT" --method newton -x inf; rc=$?
  [[ $rc -eq 0 && "${out,,}" == "inf" ]] && ok "newton +inf -> inf" || fail "newton +inf (rc=$rc out=$out)"

  run_capture out "$PY" "$MYSQRT" --method bisect -x inf; rc=$?
  [[ $rc -eq 0 && "${out,,}" == "inf" ]] && ok "bisect +inf -> inf" || fail "bisect +inf (rc=$rc out=$out)"
}

test_isqrt(){
  local out rc
  run_capture out "$PY" "$MYSQRT" --method isqrt -x 16; rc=$?
  [[ $rc -eq 0 && "$out" == "4" ]] && ok "isqrt 16 -> 4" || fail "isqrt 16 (rc=$rc out=$out)"

  run_capture out "$PY" "$MYSQRT" --method isqrt -x 0x100; rc=$?
  [[ $rc -eq 0 && "$out" == "16" ]] && ok "isqrt 0x100 -> 16" || fail "isqrt 0x100 (rc=$rc out=$out)"

  run_capture out "$PY" "$MYSQRT" --method isqrt -x 1000000000000; rc=$?
  [[ $rc -eq 0 && "$out" == "1000000" ]] && ok "isqrt 1e12 -> 1e6" || fail "isqrt 1e12 (rc=$rc out=$out)"
}

# ---------- TESTS CLI INTEGRES ----------
test_cli_builtin_tests(){
  local rc
  "$PY" "$MYSQRT" --test >/dev/null 2>&1; rc=$?
  [[ $rc -eq 0 ]] && ok "--test intégré -> rc=0" || fail "--test intégré (rc=$rc)"
}

test_cli_complex_and_errors(){
  local out rc
  run_capture out "$PY" "$MYSQRT" --method newton --allow-complex -x -4; rc=$?
  [[ $rc -eq 0 && "$out" == "2j" ]] && ok "newton --allow-complex -4 -> 2j" || fail "newton complex -4 (rc=$rc out=$out)"

  run_capture out "$PY" "$MYSQRT" --method bisect --allow-complex -x -4; rc=$?
  if [[ $rc -eq 2 && "$out" == *"bisect"* && "${out,,}" == *"complex"* ]]; then
    ok "bisect --allow-complex -4 -> rc=2 + msg"
  else
    fail "bisect --allow-complex -4 (rc=$rc, out=$out)"
  fi
}

echo "=== Tests fonctionnels ==="
test_newton_residual
test_bisect_residual
test_methods_agree
test_nan_inf
test_isqrt

echo
echo "=== Tests CLI intégrés ==="
test_cli_builtin_tests
test_cli_complex_and_errors

echo
if [[ $FAILS -eq 0 ]]; then
  echo "Résumé: SUCCESS"
  exit 0
else
  echo "Résumé: $FAILS échec(s)"
  exit 1
fi
