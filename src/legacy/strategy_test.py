"""
Test a candidate Long strategy against optimal Short.

Strategy hypothesis (after the trace analysis): Long should
1. First move: play 6 (or 18 for larger n) -- kills 2, 3, 6, 12, 18, ...
2. Then: claim the largest unclaimed prime in the upper-half core
   to prevent Short from stealing it; otherwise claim the smallest
   prime power that an unplayed-divisor Short attack threatens.
3. Pre-commit: against Short's "small divisor" attacks {4, 5, 7, 11, 13, ...},
   prefer claiming a number of the form 2p where p is the next dangerous prime,
   so playing 2p kills both 2 (already done) and p (the threat) preemptively.

We compare this strategy's game-length against optimal Short to the true sat_L(n).
If our strategy achieves sat_L(n) (or close), it's a candidate for a provable bound.
"""
from __future__ import annotations
import sys, time
sys.setrecursionlimit(10**7)
sys.path.insert(0, "/home/user/workspace/erdos872")

from solver_fast import precompute_kills


def is_prime(x):
    if x < 2: return False
    d = 2
    while d*d <= x:
        if x % d == 0: return False
        d += 1
    return True


def long_strategy_v1(state_mask, n, cands, idx, kills):
    """A simple heuristic: play 6 first if available, then largest unclaimed
    upper-half element, then smallest claimable element."""
    half = n // 2
    # First move preference order
    pref = [6, 12, 18, 24]
    for p in pref:
        if p in idx and (state_mask & (1 << idx[p])):
            return p
    # Largest in upper half that is still legal
    for x in range(n, half, -1):
        if x in idx and (state_mask & (1 << idx[x])):
            return x
    # Smallest legal
    for x in range(2, n+1):
        if x in idx and (state_mask & (1 << idx[x])):
            return x
    return None


def long_strategy_v2(state_mask, n, cands, idx, kills):
    """V2: play the highly-composite first move (depending on n),
    then defend the core by playing the most-threatened core element.

    Most-threatened = largest popcount of kills intersected with state."""
    # Choose first move: 6 if n < 28, else 18
    if 6 in idx and (state_mask & (1 << idx[6])):
        # only play 6 if it's still good (most large multiples present)
        # else fall through
        return 6
    if 18 in idx and (state_mask & (1 << idx[18])):
        return 18

    half = n // 2
    # Play the upper-half core element that, if Short claimed something small next,
    # would have died. = upper-half element with most small divisors in [2, n/2]
    # that are STILL LIVE candidates Short could play.
    best_x = None
    best_score = -1
    for x in range(half+1, n+1):
        if x in idx and (state_mask & (1 << idx[x])):
            # divisors of x in [2, n/2]
            score = 0
            d = 2
            while d <= half:
                if x % d == 0 and d in idx and (state_mask & (1 << idx[d])):
                    score += 1
                d += 1
            if score > best_score:
                best_score = score
                best_x = x
    if best_x is not None:
        return best_x

    # Fallback
    for x in range(2, n+1):
        if x in idx and (state_mask & (1 << idx[x])):
            return x
    return None


def short_optimal_against(long_fn, n):
    """Compute optimal Short play against the fixed Long strategy long_fn.

    Returns (game_length_under_optimal_Short).
    Long maximizes by playing long_fn; Short minimizes by optimal recursion.
    """
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
                # No legal move from this strategy -- treat as pass-equivalent: end.
                # But strictly the game can't be passed; if state has bits, there's a move.
                # So fall back to any legal move.
                # Pick lowest bit
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
    # Known optimal values from solver_fast
    optimal = {4:2,5:3,6:3,7:4,8:4,9:5,10:5,11:6,12:6,13:7,14:7,15:7,16:7,17:8,18:8,
               19:9,20:9,21:10,22:10,23:11,24:11,25:11,26:11,27:11,28:12,29:13,30:13,
               31:14,32:14,33:14,34:14,35:15,36:15,37:16,38:16,39:16,40:16}
    print(f"{'n':>3}  {'optimal':>7}  {'v1':>4}  {'v2':>4}  {'v1_gap':>6}  {'v2_gap':>6}")
    for n in range(10, 39):
        opt = optimal.get(n)
        v1 = short_optimal_against(long_strategy_v1, n)
        v2 = short_optimal_against(long_strategy_v2, n)
        g1 = opt - v1 if opt else "?"
        g2 = opt - v2 if opt else "?"
        print(f"{n:>3}  {opt!s:>7}  {v1:>4}  {v2:>4}  {g1!s:>6}  {g2!s:>6}")


if __name__ == "__main__":
    main()
