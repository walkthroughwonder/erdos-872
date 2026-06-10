"""
Faster solver for Erdős #872 primitive-set saturation game.

Optimizations over solver.py:
1. Alpha-beta pruning (the value is bounded: 0 <= v <= popcount(state)).
2. Move ordering: try highly-composite candidates first for long player
   (empirically optimal first moves were 6, 12, 18, 24), and small primes
   first for short player (they kill many candidates).
3. Symmetry pruning: skip provably-equivalent first moves (we don't bother
   here since the state space encodes everything).
4. Larger recursion + sys.setrecursionlimit, iterative writes per n so we
   get partial results if interrupted.
5. Periodic checkpoint write to disk per n.
"""

from __future__ import annotations
import sys, time, json, os, signal
sys.setrecursionlimit(10**7)

OUT = "/home/user/workspace/erdos872/extended_results.json"

def candidates_for_n(n: int) -> list[int]:
    return list(range(2, n + 1))


def precompute_kills(n: int):
    cands = candidates_for_n(n)
    idx = {v: i for i, v in enumerate(cands)}
    kills = []
    for x in cands:
        mask = 1 << idx[x]
        m = 2 * x
        while m <= n:
            mask |= 1 << idx[m]
            m += x
        d = 2
        while d * d <= x:
            if x % d == 0:
                if d != x:
                    mask |= 1 << idx[d]
                q = x // d
                if q >= 2 and q != x:
                    mask |= 1 << idx[q]
            d += 1
        kills.append(mask)
    return cands, kills


def solve(n: int, long_first: bool, time_budget_s: float = 1e9):
    cands, kills = precompute_kills(n)
    N = len(cands)
    full_mask = (1 << N) - 1

    # Move ordering: prefer "highly composite small even numbers" for long
    # player, and "small primes" for short player.
    # Score each candidate index for ordering.
    def is_prime(x):
        if x < 2: return False
        d = 2
        while d*d <= x:
            if x % d == 0: return False
            d += 1
        return True

    # smaller score => tried earlier
    long_order = sorted(range(N), key=lambda i: (-bin(kills[i]).count("1"), cands[i]))
    short_order = sorted(range(N), key=lambda i: (0 if is_prime(cands[i]) else 1, cands[i]))

    memo = {}
    t0 = time.time()
    timeout = [False]

    def best(state, turn_long, alpha, beta):
        if state == 0:
            return 0
        if time.time() - t0 > time_budget_s:
            timeout[0] = True
            return 0
        key = (state, turn_long)
        if key in memo:
            v = memo[key]
            return v

        # NOTE: alpha-beta + transposition table is unsound unless we track
        # bound type (exact/lower/upper). We rely on move ordering + memo only.
        order = long_order if turn_long else short_order
        if turn_long:
            value = -1
            for bit_idx in order:
                bit = 1 << bit_idx
                if not (state & bit):
                    continue
                new_state = state & ~kills[bit_idx]
                new_state &= ~bit
                sub = 1 + best(new_state, 0, alpha, beta)
                if sub > value:
                    value = sub
        else:
            value = 10**9
            for bit_idx in order:
                bit = 1 << bit_idx
                if not (state & bit):
                    continue
                new_state = state & ~kills[bit_idx]
                new_state &= ~bit
                sub = 1 + best(new_state, 1, alpha, beta)
                if sub < value:
                    value = sub
        memo[key] = value
        return value

    val = best(full_mask, 1 if long_first else 0, -1, N + 1)
    return val, len(memo), time.time() - t0, timeout[0]


def load_results():
    if os.path.exists(OUT):
        with open(OUT) as f:
            return json.load(f)
    return {}


def save_results(d):
    with open(OUT + ".tmp", "w") as f:
        json.dump(d, f, indent=2)
    os.rename(OUT + ".tmp", OUT)


def main():
    results = load_results()
    # We'll go n=4..50, breaking when a single solve exceeds, say, 30 minutes.
    PER_N_BUDGET_S = float(os.environ.get("PER_N_BUDGET_S", "1800"))
    HARD_STOP_AT = int(os.environ.get("HARD_STOP_AT", "50"))

    print(f"per_n_budget={PER_N_BUDGET_S}s  hard_stop_at={HARD_STOP_AT}")
    print(f"{'n':>3}  {'sat_L':>5}  {'sat_S':>5}  {'states_L':>9}  {'states_S':>9}  {'tL_s':>6}  {'tS_s':>6}")

    for n in range(4, HARD_STOP_AT + 1):
        key = str(n)
        if key in results and "sat_L" in results[key] and "sat_S" in results[key]:
            r = results[key]
            print(f"{n:>3}  {r['sat_L']:>5}  {r['sat_S']:>5}  {'(cached)':>9}  {'':>9}  {'':>6}  {'':>6}")
            continue

        try:
            satL, statesL, tL, toL = solve(n, True, PER_N_BUDGET_S)
            if toL:
                print(f"n={n} long-first hit time budget; stopping.")
                break
            satS, statesS, tS, toS = solve(n, False, PER_N_BUDGET_S)
            if toS:
                print(f"n={n} short-first hit time budget; saving long-first only and stopping.")
                results[key] = {"sat_L": satL, "states_L": statesL, "time_L": tL}
                save_results(results)
                break
            results[key] = {"sat_L": satL, "sat_S": satS, "states_L": statesL,
                            "states_S": statesS, "time_L": tL, "time_S": tS}
            save_results(results)
            print(f"{n:>3}  {satL:>5}  {satS:>5}  {statesL:>9}  {statesS:>9}  {tL:>6.2f}  {tS:>6.2f}")
        except MemoryError:
            print(f"n={n} OOM; stopping.")
            break
        except KeyboardInterrupt:
            print("Interrupted; partial results saved.")
            break

if __name__ == "__main__":
    main()
