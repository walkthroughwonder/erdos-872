"""
SAT/ILP-based min maximal primitive subset solver for {2..n}.

A subset M ⊂ {2..n} is "primitive" iff no a|b for distinct a,b in M.
M is "maximal primitive" iff for every y in {2..n}\M, some m in M
has m|y or y|m (so M ∪ {y} would no longer be primitive).

We minimize |M| subject to:
  (P) primitivity: for each comparable pair (a,b), x_a + x_b <= 1
  (M) maximality: for each y in {2..n}, x_y + sum_{m comparable to y, m!=y} x_m >= 1
      (i.e. either y is in M, or some comparable element is in M)

Uses OR-Tools CP-SAT, which handles binary problems much faster than
brute-force backtracking.
"""
import sys
import time
from ortools.sat.python import cp_model


def sieve_primes(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def pi(n):
    return len(sieve_primes(n))


def comparable_pairs(n):
    """Return dict: i -> set of j in {2..n}, j!=i, with i|j or j|i."""
    comp = {i: set() for i in range(2, n + 1)}
    for a in range(2, n + 1):
        for b in range(2 * a, n + 1, a):
            comp[a].add(b)
            comp[b].add(a)
    return comp


def min_max_primitive(n, time_limit_s=120, upper_bound=None, log=True):
    """
    Find min |M| where M is a maximal primitive subset of {2..n}.
    Returns (min_size, witness_set or None, status, elapsed_s).
    """
    comp = comparable_pairs(n)
    model = cp_model.CpModel()
    x = {i: model.NewBoolVar(f"x_{i}") for i in range(2, n + 1)}

    # Primitivity: for each comparable pair (a<b), x_a + x_b <= 1
    for a in range(2, n + 1):
        for b in comp[a]:
            if b > a:
                model.Add(x[a] + x[b] <= 1)

    # Maximality: for each y in {2..n}, x_y + sum_{m in comp[y]} x_m >= 1
    for y in range(2, n + 1):
        model.Add(x[y] + sum(x[m] for m in comp[y]) >= 1)

    # Symmetry breaking: π(n) is always feasible (primes), so |M| <= π(n)
    if upper_bound is None:
        upper_bound = pi(n)
    model.Add(sum(x[i] for i in range(2, n + 1)) <= upper_bound)

    # Objective: minimize |M|
    model.Minimize(sum(x[i] for i in range(2, n + 1)))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_search_workers = 4
    t0 = time.time()
    status = solver.Solve(model)
    elapsed = time.time() - t0

    status_name = {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE",
        cp_model.UNKNOWN: "UNKNOWN",
        cp_model.MODEL_INVALID: "MODEL_INVALID",
    }.get(status, str(status))

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sz = int(solver.ObjectiveValue())
        witness = sorted(i for i in range(2, n + 1) if solver.Value(x[i]) == 1)
        if log:
            print(f"n={n}: π(n)={pi(n)}, min|M|={sz} ({status_name}, {elapsed:.2f}s)")
            if sz < pi(n):
                print(f"  *** BREAKTHROUGH: smaller than π(n)! witness={witness}")
            elif sz == pi(n):
                print(f"  confirmed min|M|=π(n). witness={witness[:15]}{'...' if len(witness)>15 else ''}")
        return sz, witness, status_name, elapsed
    else:
        if log:
            print(f"n={n}: π(n)={pi(n)}, status={status_name} ({elapsed:.2f}s)")
        return None, None, status_name, elapsed


def main():
    n_lo = int(sys.argv[1]) if len(sys.argv) > 1 else 31
    n_hi = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    tlim = int(sys.argv[3]) if len(sys.argv) > 3 else 90

    print(f"=== Min maximal primitive subset via CP-SAT, n={n_lo}..{n_hi}, "
          f"time_limit={tlim}s/n ===", flush=True)
    results = {}
    for n in range(n_lo, n_hi + 1):
        sz, witness, status, t = min_max_primitive(n, time_limit_s=tlim, log=True)
        results[n] = {
            "pi_n": pi(n),
            "min_M": sz,
            "status": status,
            "time_s": round(t, 2),
            "witness_size": len(witness) if witness else None,
            "witness_sample": (witness[:10] if witness else None),
        }
        sys.stdout.flush()

    import json
    out_path = f"/home/user/workspace/erdos872/min_mp_sat_results_{n_lo}_{n_hi}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved results to {out_path}")


if __name__ == "__main__":
    main()
