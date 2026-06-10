"""
Compute an UPPER BOUND on sat_S(n) by simulating Short's "play-all-primes-then-stop"
strategy against Long's worst-case response.

The idea: if Short can guarantee that the game ends as some maximal primitive
set of size <= f(n), then sat_S(n) <= f(n). We exhibit Short's strategy
explicitly (greedy: pick the candidate that minimizes the resulting min-max-prim
bound) and let Long play optimally.

For tractability we use a heuristic Long: Long picks the move that maximizes
the future "available count" greedily (since exact maximization is expensive).
This gives an UPPER BOUND on sat_S (since Long is suboptimal => possibly
larger terminal set => upper bound on what Short can force is loose),
WAIT: this gives sat_S(n) <= terminal_size only if Long is OPTIMAL. So
we cannot upper-bound sat_S this way.

Correct approach for an upper bound on sat_S:
  sat_S(n) <= max_{game play with Short adversarial, Long greedy/random/optimal} |A_final|
  = max over Long strategies of terminal size with Short adversarial.

What we can compute: Short plays "primes only", Long plays optimally (depth-limited).
The resulting terminal size T is an *upper bound* on sat_S(n) because Short has
a (possibly suboptimal) strategy that forces |A| <= T.

So: sat_S(n) <= max_{Long plays optimally against Short=primes} |A_final|

We compute this by treating Short's strategy as FIXED (play primes in order,
or play the smallest available prime each turn). Long maximizes.

Long's optimization is a one-player game tree we can solve exactly up to ~50.
"""
import sys
import time
import json
from functools import lru_cache
sys.setrecursionlimit(10**7)


def sieve_primes(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def precompute(n):
    cands = list(range(2, n + 1))
    idx = {v: i for i, v in enumerate(cands)}
    N = len(cands)
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
    return cands, idx, kills


def short_strategy_smallest_available_prime(n, cands, idx, kills, primes):
    """
    Short plays the smallest available prime each turn (starting with 2).
    Returns a function that picks a move given the current state.
    """
    prime_bits = [1 << idx[p] for p in primes if p <= n]

    def picker(state):
        for pb in prime_bits:
            if state & pb:
                return pb
        # No primes left; pick smallest available
        b = state & -state
        return b

    return picker


def short_strategy_smallest_available(n, cands, idx, kills):
    """Short plays smallest available (this is what 'play primes first' becomes
    after the smallest primes are exhausted)."""
    def picker(state):
        return state & -state
    return picker


def long_max_with_fixed_short(n, short_picker, time_budget_s=300.0):
    """
    Compute max terminal A-size when Long plays optimally and Short plays
    according to short_picker.

    State: bitmask of remaining candidates. Long's turn => maximize over moves.
    Short's turn => move dictated by short_picker.

    Returns (max_terminal_size, optimal_long_play_trace).
    """
    cands, idx, kills = precompute(n)
    N = len(cands)

    memo = {}
    t0 = time.time()

    def search(state, turn_long):
        if state == 0:
            return 0, []
        if time.time() - t0 > time_budget_s:
            raise TimeoutError()
        key = (state, turn_long)
        if key in memo:
            return memo[key]

        if turn_long:
            best_val = -1
            best_trace = None
            s = state
            while s:
                bit = s & -s
                s &= s - 1
                bit_idx = bit.bit_length() - 1
                new_state = state & ~kills[bit_idx]
                new_state &= ~bit
                sub, trace = search(new_state, False)
                val = 1 + sub
                if val > best_val:
                    best_val = val
                    best_trace = [(cands[bit_idx], "L")] + trace
            memo[key] = (best_val, best_trace)
            return best_val, best_trace
        else:
            # Short plays dictated move; BOTH players add to A.
            bit = short_picker(state)
            bit_idx = bit.bit_length() - 1
            new_state = state & ~kills[bit_idx]
            new_state &= ~bit
            sub, trace = search(new_state, True)
            val = 1 + sub  # Short's pick is added to A
            memo[key] = (val, [(cands[bit_idx], "S")] + trace)
            return val, [(cands[bit_idx], "S")] + trace

    try:
        # Short moves first
        result, trace = search((1 << N) - 1, False)
        return result, trace, False
    except TimeoutError:
        return None, None, True


def main():
    n_lo = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    n_hi = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    tlim = float(sys.argv[3]) if len(sys.argv) > 3 else 60.0

    print(f"=== Upper bound on sat_S(n) via Short=smallest-prime strategy ===")
    print(f"n={n_lo}..{n_hi}, time_limit={tlim}s/n")
    print(f"{'n':>3} {'π(n)':>5} {'sat_S_upper':>12} {'gap':>5} {'time':>7}")

    results = {}
    for n in range(n_lo, n_hi + 1):
        primes = sieve_primes(n)
        cands, idx, kills = precompute(n)
        picker = short_strategy_smallest_available_prime(n, cands, idx, kills, primes)
        t0 = time.time()
        try:
            ub, trace, _ = long_max_with_fixed_short(n, picker, time_budget_s=tlim)
        except RecursionError:
            ub, trace = None, None
        elapsed = time.time() - t0
        pn = len(primes)
        if ub is not None:
            gap = ub - pn
            print(f"{n:>3} {pn:>5} {ub:>12} {gap:>5} {elapsed:>6.2f}s")
            results[n] = {"pi_n": pn, "sat_S_upper": ub, "gap": gap, "time_s": round(elapsed, 2)}
        else:
            print(f"{n:>3} {pn:>5} {'TIMEOUT':>12} {'?':>5} {elapsed:>6.2f}s")
            results[n] = {"pi_n": pn, "sat_S_upper": None, "gap": None, "time_s": round(elapsed, 2)}

    out = f"/home/user/workspace/erdos872/short_strategy_upper_{n_lo}_{n_hi}.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
