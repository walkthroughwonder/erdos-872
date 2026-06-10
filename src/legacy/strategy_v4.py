"""
Strategy v4: v2 framework + per-turn shallow lookahead.

The fixed-policy v2 has gap <=2 on n=10..38. We try to close the gap by
giving Long a 2-ply tactical lookahead: pick the move that maximizes
1 + min_over_Short_responses(future_game_length_under_v2).
This still runs in time O(branching * v2_inner) because v2 is deterministic
once it's Long's turn after Short's response.
"""
from __future__ import annotations
import sys
sys.setrecursionlimit(10**7)
sys.path.insert(0, "/home/user/workspace/erdos872")

from solver_fast import precompute_kills
from strategy_test import long_strategy_v2


def play_one(state, n, idx, kills, move):
    bi = idx[move]
    return (state & ~kills[bi]) & ~(1 << bi)


def long_strategy_v4(state, n, cands, idx, kills):
    """1-ply lookahead: try each legal move; for each, simulate Short's best response
    and then continue under the fixed v2 policy. Pick the move with max final length."""
    # Enumerate candidate Long moves: live cells.
    moves = []
    s = state
    while s:
        low = s & -s
        bit_idx = low.bit_length() - 1
        moves.append(cands[bit_idx])
        s ^= low
    # Bound moves by a heuristic ordering: prefer v2's pick first, then upper-half.
    moves.sort(key=lambda x: (-x, ))
    # Heuristic prune: at most top 6 moves
    PRUNE = 8
    moves = moves[:PRUNE]

    best_move = None
    best_value = -1
    for m in moves:
        s1 = play_one(state, n, idx, kills, m)
        # Short minimizes; she plays her best response among live cells.
        # Then continue with deterministic v2 policy.
        # Compute Short's best response via 1-ply min.
        if s1 == 0:
            val = 1
        else:
            worst = 10**9
            ss = s1
            while ss:
                low = ss & -ss
                bit_idx = low.bit_length() - 1
                short_move = cands[bit_idx]
                ss ^= low
                s2 = play_one(s1, n, idx, kills, short_move)
                # Now continue with v2 against optimal Short -- we approximate by playing
                # v2 forward; full optimal recursion would be expensive.
                length = 2 + simulate_v2_vs_v2(s2, n, cands, idx, kills, turn_long=True)
                if length < worst:
                    worst = length
            val = worst
        if val > best_value:
            best_value = val
            best_move = m
    return best_move


def simulate_v2_vs_v2(state, n, cands, idx, kills, turn_long):
    """Simulate: Long plays v2, Short plays the move that minimizes the
    final length under a 1-ply heuristic (most-restrictive: kill the most
    upper-half elements)."""
    cnt = 0
    while state != 0:
        if turn_long:
            move = long_strategy_v2(state, n, cands, idx, kills)
            if move is None or not (state & (1 << idx[move])):
                low = state & -state
                bit_idx = low.bit_length() - 1
                move = cands[bit_idx]
        else:
            # Short heuristic: pick the live cell whose kills mask has the most live bits.
            best = None
            best_score = -1
            s = state
            while s:
                low = s & -s
                bit_idx = low.bit_length() - 1
                killed = bin(state & kills[bit_idx]).count("1")
                if killed > best_score:
                    best_score = killed
                    best = cands[bit_idx]
                s ^= low
            move = best
        state = play_one(state, n, idx, kills, move)
        cnt += 1
        turn_long = not turn_long
    return cnt


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
    optimal = {4:2,5:3,6:3,7:4,8:4,9:5,10:5,11:6,12:6,13:7,14:7,15:7,16:7,17:8,18:8,
               19:9,20:9,21:10,22:10,23:11,24:11,25:11,26:11,27:11,28:12,29:13,30:13,
               31:14,32:14,33:14,34:14,35:15,36:15,37:16,38:16,39:16,40:16}
    print(f"{'n':>3}  {'optimal':>7}  {'v4':>4}  {'gap':>4}")
    for n in range(10, 36):
        opt = optimal[n]
        v4 = short_optimal_against(long_strategy_v4, n)
        print(f"{n:>3}  {opt:>7}  {v4:>4}  {opt-v4:>+4}")


if __name__ == "__main__":
    main()
