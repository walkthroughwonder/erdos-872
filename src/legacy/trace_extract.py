"""
Extract complete optimal-play game traces for small/medium n.

This shows BOTH players' optimal moves, which is needed to understand
Short's strategy and identify candidate pairings.
"""
from __future__ import annotations
import sys, time
sys.setrecursionlimit(10**7)
sys.path.insert(0, "/home/user/workspace/erdos872")

from solver_fast import precompute_kills


def best_with_choice(n: int, long_first: bool):
    """Returns (value, principal_variation) under optimal play."""
    cands, kills = precompute_kills(n)
    N = len(cands)
    full_mask = (1 << N) - 1

    memo = {}

    def best(state, turn_long):
        if state == 0: return 0, []
        key = (state, turn_long)
        if key in memo: return memo[key]
        if turn_long:
            best_val = -1; best_pv = []; best_move = None
            s = state
            while s:
                low = s & -s
                bit_idx = low.bit_length() - 1
                new_state = (state & ~kills[bit_idx]) & ~low
                sub_val, sub_pv = best(new_state, 0)
                v = 1 + sub_val
                if v > best_val:
                    best_val = v
                    best_move = cands[bit_idx]
                    best_pv = sub_pv
                s ^= low
            result = (best_val, [best_move] + best_pv)
        else:
            best_val = 10**9; best_pv = []; best_move = None
            s = state
            while s:
                low = s & -s
                bit_idx = low.bit_length() - 1
                new_state = (state & ~kills[bit_idx]) & ~low
                sub_val, sub_pv = best(new_state, 1)
                v = 1 + sub_val
                if v < best_val:
                    best_val = v
                    best_move = cands[bit_idx]
                    best_pv = sub_pv
                s ^= low
            result = (best_val, [best_move] + best_pv)
        memo[key] = result
        return result

    return best(full_mask, 1 if long_first else 0)


def main():
    for n in [15, 20, 25, 30]:
        t0 = time.time()
        val, pv = best_with_choice(n, True)
        print(f"\nn={n}, long-first, sat_L={val}, time={time.time()-t0:.1f}s")
        print(f"  PV: {pv}")
        # Annotate who plays what
        moves = []
        turn_long = True
        for m in pv:
            moves.append(("L" if turn_long else "S", m))
            turn_long = not turn_long
        print(f"  by player: {moves}")
        # Short player's moves only
        short_moves = [m for who, m in moves if who == "S"]
        print(f"  Short played: {short_moves}")

if __name__ == "__main__":
    main()
