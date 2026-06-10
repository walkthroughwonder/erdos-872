"""
Third independent solver - simplest possible code, used as ground truth tiebreaker.
Game state = frozenset of remaining legal candidates.
No bitmasks, no memoization tricks - just clean recursion with @lru_cache.
"""
from functools import lru_cache
import sys
sys.setrecursionlimit(10**7)

def solve_naive(n: int, long_first: bool) -> int:
    # Pre-build divisibility relation
    cands = list(range(2, n+1))
    # For each candidate x, the set of candidates that become illegal once x is played:
    # multiples of x in cands, divisors of x in cands, and x itself.
    blocked_by = {}
    for x in cands:
        s = set()
        s.add(x)
        for y in cands:
            if y != x and (y % x == 0 or x % y == 0):
                s.add(y)
        blocked_by[x] = frozenset(s)

    @lru_cache(maxsize=None)
    def best(remaining: frozenset, turn_long: bool) -> int:
        if not remaining:
            return 0
        if turn_long:
            v = -1
            for x in remaining:
                new_rem = remaining - blocked_by[x]
                sub = 1 + best(new_rem, False)
                if sub > v: v = sub
            return v
        else:
            v = 10**9
            for x in remaining:
                new_rem = remaining - blocked_by[x]
                sub = 1 + best(new_rem, True)
                if sub < v: v = sub
            return v

    return best(frozenset(cands), long_first)


if __name__ == "__main__":
    import time
    for n in range(4, 22):
        t0 = time.time()
        sL = solve_naive(n, True)
        sS = solve_naive(n, False)
        print(f"n={n:>2}  sat_L={sL}  sat_S={sS}  ({time.time()-t0:.2f}s)")
