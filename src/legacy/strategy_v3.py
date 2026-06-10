"""
Candidate Long strategy v3.

Hypothesis (after extended data n=4..40):
- sat_L(n)/n drifts toward something around 0.40, not 0.50.
- Short's wedge: she plays small numbers in [2, sqrt(n)] whose multiples
  cover many upper-half elements; this prevents Long from filling the
  full upper half.
- Long's best heuristic so far (v2): take the most-divisor-rich upper-half
  element on each turn; opening move 6 then 18.

v3 refinements:
  (a) On opening, pick the most-killing element in the lower half whose
      multiples are densest in the upper half ((n+1)/2..n).
  (b) On subsequent turns, prefer an upper-half element that has the largest
      number of its small divisors STILL LIVE (i.e., the element most at risk
      of being killed by a future Short move).
  (c) Tie-break by: among equally-threatened candidates, pick the one with
      the largest distinct-prime-factor count of x's divisors in [2, n/2]
      (so playing x removes the most lower-half threat capacity from Short).
"""
from __future__ import annotations
import sys
sys.setrecursionlimit(10**7)
sys.path.insert(0, "/home/user/workspace/erdos872")

from solver_fast import precompute_kills


def best_opening(n, cands, idx, state):
    """Pick x in [2, n/2] maximizing number of multiples of x in (n/2, n]
    that are still live; tie-break by smallest x."""
    half = n // 2
    best_x = None
    best_score = -1
    for x in range(2, half + 1):
        if x in idx and (state & (1 << idx[x])):
            count = 0
            k = 2
            while x * k <= n:
                m = x * k
                if m > half and m in idx and (state & (1 << idx[m])):
                    count += 1
                k += 1
            if count > best_score or (count == best_score and (best_x is None or x < best_x)):
                best_score = count
                best_x = x
    return best_x


def threat_score(x, n, idx, state):
    """Count of small divisors d in [2, n/2] of x that are still live;
    these are elements Short can play to kill x."""
    half = n // 2
    score = 0
    d = 2
    while d <= half:
        if x % d == 0 and d in idx and (state & (1 << idx[d])):
            score += 1
        d += 1
    return score


def long_strategy_v3(state, n, cands, idx, kills, ply=None):
    """Defend upper half, prefer most-threatened core element first."""
    half = n // 2
    full = (1 << len(cands)) - 1
    # Heuristic for "opening": when no upper-half elements are claimed yet,
    # i.e., state ∩ upper-half == upper-half (all still live).
    upper_live = sum(1 for x in range(half + 1, n + 1) if x in idx and (state & (1 << idx[x])))
    upper_total = n - half
    if upper_live == upper_total:
        # First Long move: pick the strongest opener.
        x = best_opening(n, cands, idx, state)
        if x is not None:
            return x

    # Defend most threatened upper-half core element.
    best_x = None
    best = None
    for x in range(half + 1, n + 1):
        if x in idx and (state & (1 << idx[x])):
            t = threat_score(x, n, idx, state)
            # Secondary score: distinct small divisors that are live, weighted.
            if best is None or (t, x) > best:
                best = (t, x)
                best_x = x
    if best_x is not None:
        return best_x

    # Fallback: any live element.
    s = state
    while s:
        low = s & -s
        bit_idx = low.bit_length() - 1
        return cands[bit_idx]
    return None


def short_optimal_against(long_fn, n):
    cands, kills_list = precompute_kills(n)
    idx = {v: i for i, v in enumerate(cands)}
    full_mask = (1 << len(cands)) - 1
    memo = {}

    def best(state, turn_long):
        if state == 0: return 0
        key = (state, turn_long)
        if key in memo: return memo[key]
        if turn_long:
            move = long_fn(state, n, cands, idx, kills_list)
            if move is None or not (state & (1 << idx[move])):
                low = state & -state
                bit_idx = low.bit_length() - 1
                move = cands[bit_idx]
            bi = idx[move]
            new_state = (state & ~kills_list[bi]) & ~(1 << bi)
            v = 1 + best(new_state, 0)
        else:
            v = 10**9
            s = state
            while s:
                low = s & -s
                bit_idx = low.bit_length() - 1
                new_state = (state & ~kills_list[bit_idx]) & ~low
                sub = 1 + best(new_state, 1)
                if sub < v: v = sub
                s ^= low
        memo[key] = v
        return v

    return best(full_mask, 1)


def main():
    # Optimal from solver
    optimal = {4:2,5:3,6:3,7:4,8:4,9:5,10:5,11:6,12:6,13:7,14:7,15:7,16:7,17:8,18:8,
               19:9,20:9,21:10,22:10,23:11,24:11,25:11,26:11,27:11,28:12,29:13,30:13,
               31:14,32:14,33:14,34:14,35:15,36:15,37:16,38:16,39:16,40:16}
    print(f"{'n':>3}  {'optimal':>7}  {'v3':>4}  {'gap':>4}  {'v3/opt':>7}")
    cum_gap = 0
    for n in range(10, 39):
        opt = optimal[n]
        v3 = short_optimal_against(long_strategy_v3, n)
        gap = opt - v3
        cum_gap += max(0, gap)
        print(f"{n:>3}  {opt:>7}  {v3:>4}  {gap:>+4}  {v3/opt:>7.4f}")
    print(f"\nTotal positive gap (n=10..38): {cum_gap}")
    print(f"Max gap: {max(opt-short_optimal_against(long_strategy_v3,n) for n,opt in optimal.items() if n>=10 and n<=38)}")


if __name__ == "__main__":
    main()
