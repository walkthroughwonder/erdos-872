"""
Stochastic stress test for strategy v3 on configurations that exceed the
exhaustive enumeration budget. Instead of walking every reachable pre-Maker
state, we sample N independent Shortener trajectories and check the raw RSE
at every visited state.

This is a Monte Carlo lower bound on RSE failures: if no failure is found
in N samples of total depth D, the probability of any single trajectory
violating RSE is at most O(1/N).

Usage:
  python k4_avoidance_v3_sampled.py [5,4] --trials 50000
  python k4_avoidance_v3_sampled.py [4,4,2] --trials 20000
"""
from __future__ import annotations

import sys
import time
import random
import argparse
sys.path.insert(0, '.')
from multi_fiber_rse import (
    MultiState, build_edges, is_live, live_edges, phi, Q,
    breaker_moves, raw_rse, is_terminal,
)
from k4_avoidance_v3 import strategy_v3


def sample_trajectory(fibers, rng, max_depth=200):
    """Walk one Maker-Shortener trajectory under strategy v3 with random
    Shortener choices. Return (n_states_visited, n_rse_fail, first_fail_state)."""
    edges, fiber_of = build_edges(fibers)
    initial = MultiState(C=frozenset(), D_V=frozenset(), D_E=frozenset(),
                        K=frozenset(), S=0, captured_edges=frozenset())
    s = initial
    n_states = 0
    n_fail = 0
    first_fail = None
    for _ in range(max_depth):
        n_states += 1
        if is_terminal(s, edges):
            break
        live_pos = [ei for ei in live_edges(s, edges) if phi(s, ei, edges) > 0]
        if not live_pos:
            break
        ok, _ = raw_rse(s, edges)
        if not ok:
            n_fail += 1
            if first_fail is None:
                first_fail = s
        m = strategy_v3(s, edges)
        if m is None:
            break
        # Random Shortener reply
        bms = list(breaker_moves(m[2], edges))
        if not bms:
            s = m[2]
            continue
        _, _, s = rng.choice(bms)
    return n_states, n_fail, first_fail


def run_sampled(cfg, trials, seed=0):
    fibers = [list(range(1, k + 1)) for k in cfg]
    rng = random.Random(seed)
    total_states = 0
    total_fail = 0
    first_fail = None
    t0 = time.time()
    for i in range(trials):
        ns, nf, ff = sample_trajectory(fibers, rng)
        total_states += ns
        total_fail += nf
        if ff is not None and first_fail is None:
            first_fail = ff
        if i % 5000 == 0 and i > 0:
            dt = time.time() - t0
            print(f"  trial {i}/{trials}, visited {total_states} states, "
                  f"failures={total_fail}, {dt:.1f}s elapsed")
    dt = time.time() - t0
    print(f"\nConfig {cfg}: {trials} trials, {total_states} state visits, "
          f"RSE failures={total_fail} ({total_fail/max(total_states,1):.2%}), "
          f"{dt:.1f}s")
    if first_fail is not None:
        print(f"  first failing state: {first_fail}")
    return total_states, total_fail


def main():
    p = argparse.ArgumentParser()
    p.add_argument("config", help="config like [5,4] or [4,4,2]")
    p.add_argument("--trials", type=int, default=20000)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    cfg = eval(args.config)
    assert isinstance(cfg, list) and all(isinstance(x, int) for x in cfg)
    print(f"=== Stochastic v3 stress test, config={cfg}, trials={args.trials} ===")
    run_sampled(cfg, args.trials, args.seed)


if __name__ == "__main__":
    main()
