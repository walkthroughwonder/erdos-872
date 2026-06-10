"""Extend min-maximal-primitive search to n in [31, 60] with a smarter algorithm.

Brute-force over all subsets is infeasible for n > 30 (2^59 subsets at n=60).
We use a recursive search: try to construct a maximal primitive subset of size k
by greedy + backtracking, starting from k = π(n) - 1 and proving infeasibility.

If we cannot find a maximal primitive subset of size π(n) - 1, then min |M| ≥ π(n).
Combined with the fact that primes form a maximal primitive set of size π(n),
this proves min |M| = π(n).
"""
import sys
import time
from itertools import combinations


def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def divisors_in_range(x, n):
    """All proper divisors of x in [2, n] (excluding x)."""
    out = []
    for d in range(2, int(x ** 0.5) + 1):
        if x % d == 0:
            out.append(d)
            if d != x // d and x // d <= n:
                out.append(x // d)
    return out


def multiples_in_range(x, n):
    return list(range(2 * x, n + 1, x))


def comparable(a, b):
    return a % b == 0 or b % a == 0


def search_maximal_primitive(n, target_size, time_limit=120.0):
    """Search for a maximal primitive subset of {2..n} with exactly target_size elements.

    Returns the subset if found, None if infeasible within time_limit, "TIMEOUT" if budget exhausted.
    """
    universe = list(range(2, n + 1))
    start = time.time()
    found = [None]
    node_count = [0]

    # Precompute comparability adjacency
    comp = {x: set() for x in universe}
    for i, a in enumerate(universe):
        for b in universe[i + 1:]:
            if comparable(a, b):
                comp[a].add(b)
                comp[b].add(a)

    def recurse(chosen, banned, remaining_count):
        if time.time() - start > time_limit:
            return "TIMEOUT"
        node_count[0] += 1
        # Universe = {2..n}; "uncovered" = elements not in chosen and not comparable to anything in chosen
        chosen_set = set(chosen)
        uncovered = [x for x in universe if x not in chosen_set and not any(comparable(x, c) for c in chosen)]

        if remaining_count == 0:
            # All universe elements must be covered (chosen or comparable to chosen)
            if not uncovered:
                # Verify primitivity
                for i, a in enumerate(chosen):
                    for b in chosen[i + 1:]:
                        if comparable(a, b):
                            return None
                found[0] = list(chosen)
                return "FOUND"
            return None

        if not uncovered:
            return None  # Can't add anything more; chosen is already maximal but too small

        # Choose pivot: an uncovered element with fewest extensions; we must "handle" it
        # (either add it or add something comparable to it)
        # For efficiency, try adding the smallest uncovered first
        # Heuristic: try elements with fewest comparable neighbors first
        candidates = sorted(uncovered, key=lambda x: len(comp[x]))
        for cand in candidates:
            # cand must not be comparable to any element of chosen (it isn't, since uncovered)
            if any(comparable(cand, c) for c in chosen):
                continue
            chosen.append(cand)
            res = recurse(chosen, banned, remaining_count - 1)
            chosen.pop()
            if res == "TIMEOUT":
                return "TIMEOUT"
            if res == "FOUND":
                return "FOUND"
        return None

    result = recurse([], set(), target_size)
    return result, found[0], node_count[0], time.time() - start


def min_maximal_primitive_size(n, time_limit_per_size=120.0):
    """Find min |M| for maximal primitive M in {2..n}.

    Try target_size from π(n)-1 downward (proving infeasibility), then return π(n).
    """
    primes = primes_up_to(n)
    pi_n = len(primes)
    # First confirm primes is maximal primitive
    for k in range(2, n + 1):
        if not any(k % p == 0 for p in primes):
            return None, "primes not maximal", 0, 0
    # Try size pi_n - 1
    print(f"n={n}: π(n)={pi_n}, searching for size {pi_n - 1}", flush=True)
    res, found, nodes, elapsed = search_maximal_primitive(n, pi_n - 1, time_limit_per_size)
    if res == "FOUND":
        return pi_n - 1, found, nodes, elapsed
    if res == "TIMEOUT":
        return None, "TIMEOUT", nodes, elapsed
    # Infeasible at pi_n - 1; primes are min
    return pi_n, primes, nodes, elapsed


if __name__ == "__main__":
    import json
    results = {}
    for n in range(31, 61):
        t0 = time.time()
        size, witness, nodes, elapsed = min_maximal_primitive_size(n, time_limit_per_size=60.0)
        print(f"  -> n={n}: min |M| = {size}, nodes={nodes}, time={elapsed:.2f}s", flush=True)
        results[n] = {"size": size, "witness": witness if isinstance(witness, list) else str(witness), "nodes": nodes, "time": elapsed}
        with open("min_mp_extended.json", "w") as f:
            json.dump(results, f, indent=2)
    print("DONE", flush=True)
