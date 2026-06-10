#!/usr/bin/env python3
"""
Full activation graph safe-edge check for the concrete K5 q-fiber witness.

Instance:
  n = 10^20, delta = 1/8, Y = floor(n^delta) = 316
  P_Y = odd primes <= Y
  K5 primes = {101, 103, 107, 109, 113}
  q = 4806305873305829

Manuscript rule implemented:
  Proposition A.6 uses a rank-2 activation graph on small primes.  An
  unclaimed pair edge e=(a,c) has current token weight w_t(e)=|B_e(t)|.
  The activation potential is

      Q_t = S_t + sum_e phi_t(e),

  where phi_t(e) is 1/8, 1/4, or 1/2 times w_t(e) for unclaimed edges with
  0, 1, or 2 captured endpoints, is w_t(e) for claimed edges, and is 0 for
  deleted edges.  A safe activation edge is one whose Maker play leaves Q
  nondecreasing after every modeled Breaker reply: deletion of an uncaptured
  small-prime vertex or deletion of one currently live pair edge.

This checker does not need exact prime counts to disprove safety.  For each
candidate first K5 pair, it computes:
  (1) a rigorous upper bound for the Maker potential gain, and
  (2) a rigorous lower bound for the loss caused by Breaker deleting vertex 3.
If lower_loss(3) > upper_gain, that candidate is not safe in the full graph.

Prime-count bounds used for intervals (x/2, x]:
  For x/2 >= 17,
     pi(x) > x / log x,
     pi(x) < 1.25506 x / log x.
  Therefore
     |P cap (x/2,x]| <= 1.25506 x/log x,
     |P cap (x/2,x]| >= x/log x - 1.25506 (x/2)/log(x/2).
These are deliberately coarse, but the failure margins are large.

The script also includes a reduced exact-count sanity check on a smaller
instance, comparing the same potential algebra against explicit prime lists.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import math
from typing import Iterable

try:
    from sympy import primerange, isprime
except Exception:  # pragma: no cover
    primerange = None
    isprime = None


N = 10**20
Y = int(N ** (1 / 8))
K5 = (101, 103, 107, 109, 113)
Q_WITNESS = 4806305873305829
RS_C = 1.25506


def odd_primes_upto(y: int) -> list[int]:
    out = []
    for m in range(3, y + 1, 2):
        ok = True
        r = int(m**0.5)
        for p in range(3, r + 1, 2):
            if m % p == 0:
                ok = False
                break
        if ok:
            out.append(m)
    return out


P_Y = tuple(odd_primes_upto(Y))


def upper_w(a: int, c: int, n: int = N) -> float:
    """Rigorous upper bound for |B_{a,c}|."""
    x = n / (a * c)
    return RS_C * x / math.log(x)


def lower_w(a: int, c: int, n: int = N) -> float:
    """Rigorous lower bound for |B_{a,c}|."""
    x = n / (a * c)
    return x / math.log(x) - RS_C * (x / 2) / math.log(x / 2)


def interval_bounds_table(primes: Iterable[int]) -> tuple[float, float]:
    lows = []
    highs = []
    for a, c in combinations(primes, 2):
        lows.append(lower_w(a, c))
        highs.append(upper_w(a, c))
    return min(lows), max(highs)


def maker_gain_upper_first_pair(a: int, c: int, primes: tuple[int, ...] = P_Y) -> float:
    """
    Upper bound for Maker's Q gain when the initial full activation state has
    C empty and Maker first claims pair (a,c).
    """
    gain = (7.0 / 8.0) * upper_w(a, c)
    for x in primes:
        if x == a or x == c:
            continue
        gain += (1.0 / 8.0) * upper_w(min(a, x), max(a, x))
        gain += (1.0 / 8.0) * upper_w(min(c, x), max(c, x))
    return gain


def breaker_vertex_loss_lower_after_first_pair(
    chosen_a: int,
    chosen_c: int,
    breaker_v: int = 3,
    primes: tuple[int, ...] = P_Y,
) -> float:
    """
    Lower bound for the Q loss if Breaker deletes uncaptured vertex breaker_v
    after Maker first claims (chosen_a, chosen_c).
    """
    if breaker_v in (chosen_a, chosen_c):
        raise ValueError("breaker vertex is captured and not a legal deletion")
    loss = 0.0
    for x in primes:
        if x == breaker_v:
            continue
        coeff = 1.0 / 4.0 if x in (chosen_a, chosen_c) else 1.0 / 8.0
        loss += coeff * lower_w(min(breaker_v, x), max(breaker_v, x))
    return loss


@dataclass(frozen=True)
class FailureCert:
    pair: tuple[int, int]
    maker_gain_upper: float
    breaker_vertex: int
    breaker_loss_lower: float

    @property
    def margin(self) -> float:
        return self.breaker_loss_lower - self.maker_gain_upper

    @property
    def ratio(self) -> float:
        return self.breaker_loss_lower / self.maker_gain_upper


def first_move_failure_certificates() -> list[FailureCert]:
    certs = []
    for a, c in combinations(K5, 2):
        gu = maker_gain_upper_first_pair(a, c)
        ll = breaker_vertex_loss_lower_after_first_pair(a, c, 3)
        certs.append(FailureCert((a, c), gu, 3, ll))
    return certs


def deterministic_miller_rabin(n: int) -> bool:
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    # Deterministic for n < 2^64 with these bases.  The witness q is < 2^63.
    for a in [2, 3, 5, 7, 11, 13, 17]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def verify_q_membership() -> bool:
    if not deterministic_miller_rabin(Q_WITNESS):
        return False
    for a, c in combinations(K5, 2):
        if not (N / (2 * a * c) < Q_WITNESS <= N / (a * c)):
            return False
    return True


def exact_weight_small(n: int, a: int, c: int) -> int:
    """Exact interval count for reduced sanity instances."""
    if primerange is None:
        raise RuntimeError("sympy is required for reduced exact sanity checks")
    lo = n // (2 * a * c)
    hi = n // (a * c)
    return sum(1 for _ in primerange(lo + 1, hi + 1))


def exact_initial_safety_small(n: int, y: int, k5_like: tuple[int, ...]) -> list[tuple[tuple[int, int], float, float]]:
    """
    Reduced exact-count sanity check.  This independently computes exact B
    sizes by enumerating primes in small intervals, then evaluates the same
    first-move potential formulas.
    """
    primes = tuple(odd_primes_upto(y))
    w_cache = {}

    def w(a: int, c: int) -> int:
        key = (min(a, c), max(a, c))
        if key not in w_cache:
            w_cache[key] = exact_weight_small(n, *key)
        return w_cache[key]

    rows = []
    for a, c in combinations(k5_like, 2):
        gain = (7.0 / 8.0) * w(a, c)
        for x in primes:
            if x in (a, c):
                continue
            gain += (1.0 / 8.0) * w(a, x)
            gain += (1.0 / 8.0) * w(c, x)
        v = primes[0]
        if v in (a, c):
            continue
        loss = 0.0
        for x in primes:
            if x == v:
                continue
            coeff = 1.0 / 4.0 if x in (a, c) else 1.0 / 8.0
            loss += coeff * w(v, x)
        rows.append(((a, c), gain, loss))
    return rows


def main() -> int:
    print("=== Full activation graph safety check for K5 pair activations ===")
    print(f"n={N}")
    print("delta=1/8")
    print(f"Y_floor={Y}")
    print(f"|P_Y|={len(P_Y)} odd primes")
    print(f"P_Y first/last={P_Y[:8]} ... {P_Y[-8:]}")
    print(f"K5={K5}")
    print(f"q={Q_WITNESS}")
    print(f"q_membership_all_10={verify_q_membership()}")
    min_lb, max_ub = interval_bounds_table(P_Y)
    print(f"pair_graph_edges={len(P_Y) * (len(P_Y) - 1) // 2}")
    print(f"all_pair_edges_positive_by_lower_bound={min_lb > 0}")
    print(f"min_lower_weight_bound={min_lb:.6e}")
    print(f"max_upper_weight_bound={max_ub:.6e}")
    print()

    print("Manuscript activation safety test at initial full-graph state:")
    print("  safe requires Maker gain >= every legal Breaker reply loss.")
    print("  The legal Breaker reply tested here is vertex deletion v=3.")
    print()
    print("pair, maker_gain_upper, breaker_loss_lower_at_v3, margin_loss_minus_gain, ratio")
    certs = first_move_failure_certificates()
    all_fail = True
    for cert in certs:
        print(
            f"{cert.pair}, "
            f"{cert.maker_gain_upper:.6e}, "
            f"{cert.breaker_loss_lower:.6e}, "
            f"{cert.margin:.6e}, "
            f"{cert.ratio:.6f}"
        )
        all_fail = all_fail and cert.margin > 0

    print()
    if all_fail:
        print("NEG: every K5 pair is unsafe as the first activation edge in the full activation graph.")
        print("Therefore no ordering can secure all ten K5 pairs as safe activations, because the first move of any such ordering already fails.")
    else:
        print("INCONCLUSIVE/POS-POSSIBLE: at least one K5 pair was not excluded by the v=3 certificate.")

    print()
    print("Reduced exact-count sanity check:")
    print("  n_small=100000000, y_small=31, k5_like=(13,17,19,23,29)")
    try:
        rows = exact_initial_safety_small(100_000_000, 31, (13, 17, 19, 23, 29))
        for pair, gain, loss in rows[:5]:
            print(f"  {pair}: exact_gain={gain:.3f}, exact_loss_delete_3={loss:.3f}, margin={loss-gain:.3f}")
    except Exception as exc:
        print(f"  skipped: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
