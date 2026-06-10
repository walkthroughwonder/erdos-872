"""
Analyze the structure of optimal play in #872.
- Compute sat(n) for n up to as far as we can go in reasonable time.
- For each optimal long-first move, decode it: prime factorization, smoothness,
  number of multiples in [2..n], number of divisors in [2..n].
- For sequence of sat(n), compute deltas, ratios, and check against known
  primitive-set extremal counts (e.g., size of largest primitive set in [2..n]).
"""

import sys, time
from math import gcd
sys.path.insert(0, ".")
from solver import solve, candidates_for_n


def largest_primitive_set_size(n: int) -> int:
    """
    Maximum size of a primitive set inside {2..n}. Known classical fact:
    take {k+1, k+2, ..., 2k} where 2k <= n (so k = floor(n/2)), giving
    floor(n/2) elements. This is asymptotically optimal and exactly optimal
    for n >= 2. We just return floor(n/2).
    """
    return n // 2


def factor(x: int) -> dict[int, int]:
    f = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            f[d] = f.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        f[x] = f.get(x, 0) + 1
    return f


def describe(x: int, n: int) -> str:
    f = factor(x)
    fstr = " * ".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(f.items()))
    multiples = sum(1 for k in range(2, n+1) if k % x == 0)
    divisors = sum(1 for k in range(2, n+1) if x % k == 0)
    return f"{x} = {fstr} | mult-in-range:{multiples} divs-in-range:{divisors}"


def main():
    rows = []
    for n in range(4, 30):
        sat_L, moves_L = solve(n, long_goes_first=True)
        sat_S, moves_S = solve(n, long_goes_first=False)
        lps = largest_primitive_set_size(n)
        rows.append((n, sat_L, sat_S, lps, moves_L))
        print(f"n={n:>2}  sat_L={sat_L:>3}  sat_S={sat_S:>3}  "
              f"max_primitive_size={lps:>3}  "
              f"sat_L/max={sat_L/lps:.3f}  "
              f"opt_first_long={moves_L}")
        for m in moves_L[:3]:
            print(f"          first-move {describe(m, n)}")

    # Look at the gap: max_primitive - sat_L (how close to perfect play does
    # the long player get?)
    print()
    print(f"{'n':>3}  {'sat_L':>5}  {'max_prim':>8}  {'gap':>4}  {'gap/n':>7}")
    for n, sat_L, sat_S, lps, _ in rows:
        gap = lps - sat_L
        print(f"{n:>3}  {sat_L:>5}  {lps:>8}  {gap:>4}  {gap/n:>7.4f}")


if __name__ == "__main__":
    main()
