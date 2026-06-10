"""
Erdős Problem #872: Primitive-set saturation game.

Two players alternately pick integers from {2,...,n} into a shared set A,
subject to A remaining primitive (no element divides another).
Game ends when no legal move exists.

Long player: wants total moves maximized.
Short player: wants total moves minimized.

We compute the optimal game length (sat(n)) under perfect play, for both
"who goes first" variants. Erdős did not specify, so both are interesting.

Strategy: retrograde DP over the set of REMAINING LEGAL CANDIDATES.

Key insight: the game state can be encoded by the set of elements still
legally playable. Adding an element x to A invalidates exactly the
multiples and divisors of x within the candidate set. So the state shrinks
monotonically. We don't even need to track the set A explicitly; we only
need the set of remaining candidates and whose turn it is.

The number of moves made so far = (initial candidate count - some count)
isn't quite right because some candidates get removed without being played.
So we track (remaining_candidates_bitmask, turn) -> (best_total_moves_from_now).
The total game length we want is moves_played_so_far + recursion_value.

We compute recursion_value(state) = optimal additional moves under perfect
play from this state with the given player to move. Then sat(n) = recursion
from the full candidate set with the chosen first-player.
"""

from __future__ import annotations
from functools import lru_cache
import sys
import time

sys.setrecursionlimit(10**7)


def candidates_for_n(n: int) -> list[int]:
    """Initial legal elements: {2, ..., n}."""
    return list(range(2, n + 1))


def precompute_kills(n: int) -> dict[int, int]:
    """
    For each element x in {2..n}, the bitmask of elements (by index in
    candidates_for_n) that become illegal once x is played:
    namely x itself, all multiples of x in [2..n], and all proper divisors
    of x in [2..n]. (Plays of x also remove x itself.)
    """
    cands = candidates_for_n(n)
    idx = {v: i for i, v in enumerate(cands)}
    kills = {}
    for x in cands:
        mask = 1 << idx[x]
        # multiples of x in [2..n]
        m = 2 * x
        while m <= n:
            mask |= 1 << idx[m]
            m += x
        # divisors of x in [2..n] (proper, since x itself already counted)
        d = 2
        while d * d <= x:
            if x % d == 0:
                if d >= 2 and d != x:
                    mask |= 1 << idx[d]
                q = x // d
                if q >= 2 and q != x:
                    mask |= 1 << idx[q]
            d += 1
        kills[x] = mask
    return kills


def solve(n: int, long_goes_first: bool = True) -> tuple[int, list[int]]:
    """
    Returns (optimal_game_length, optimal_first_moves_for_player_to_move).

    Encoding: state = bitmask of remaining candidate INDICES.
    We do retrograde DP via memoized recursion.
    Player to move is implicit in parity of moves_played, but we need
    the parity to know which player optimizes. Since we want the TOTAL
    game length (which is a count, not a signed sum), we track:
        best(state, turn_long) = additional moves under optimal play.
    Long maximizes, Short minimizes this value.
    """
    cands = candidates_for_n(n)
    idx = {v: i for i, v in enumerate(cands)}
    kills = precompute_kills(n)
    # Re-key kills by index for speed
    kills_by_idx = [kills[v] for v in cands]
    full_mask = (1 << len(cands)) - 1

    memo: dict[tuple[int, int], int] = {}

    def best(state: int, turn_long: int) -> int:
        if state == 0:
            return 0
        key = (state, turn_long)
        if key in memo:
            return memo[key]
        # Enumerate legal moves: every bit set in state is a legal candidate.
        s = state
        if turn_long:
            val = -1
            while s:
                low = s & -s
                bit_idx = low.bit_length() - 1
                # Playing this element removes everything in kills_by_idx[bit_idx]
                # that is still in state (we AND it out).
                new_state = state & ~kills_by_idx[bit_idx]
                # The played element itself is in kills_by_idx[bit_idx] (we set
                # the self-bit when building it... wait, we did NOT set the
                # self-bit. Let's set it explicitly:
                new_state &= ~low
                sub = 1 + best(new_state, 1 - turn_long)
                if sub > val:
                    val = sub
                s ^= low
        else:
            val = 10**9
            while s:
                low = s & -s
                bit_idx = low.bit_length() - 1
                new_state = state & ~kills_by_idx[bit_idx]
                new_state &= ~low
                sub = 1 + best(new_state, 1 - turn_long)
                if sub < val:
                    val = sub
                s ^= low
        memo[key] = val
        return val

    turn_long_init = 1 if long_goes_first else 0
    total = best(full_mask, turn_long_init)

    # Recover an optimal first-move list (all moves that achieve the optimum)
    s = full_mask
    optimal_first_moves = []
    while s:
        low = s & -s
        bit_idx = low.bit_length() - 1
        new_state = full_mask & ~kills_by_idx[bit_idx]
        new_state &= ~low
        sub = 1 + best(new_state, 1 - turn_long_init)
        if sub == total:
            optimal_first_moves.append(cands[bit_idx])
        s ^= low

    return total, optimal_first_moves


def main():
    print(f"{'n':>3}  {'sat(n)_Lfirst':>14}  {'sat(n)_Sfirst':>14}  "
          f"{'ratio_L/n':>10}  {'ratio_L/(n/2)':>14}  "
          f"{'time_s':>8}  optimal_first_moves_Lfirst")
    for n in range(4, 32):
        t0 = time.time()
        sat_L, moves_L = solve(n, long_goes_first=True)
        sat_S, moves_S = solve(n, long_goes_first=False)
        t = time.time() - t0
        ratio_n = sat_L / n
        ratio_half = sat_L / (n / 2)
        print(f"{n:>3}  {sat_L:>14}  {sat_S:>14}  "
              f"{ratio_n:>10.4f}  {ratio_half:>14.4f}  "
              f"{t:>8.2f}  {moves_L}")


if __name__ == "__main__":
    main()
