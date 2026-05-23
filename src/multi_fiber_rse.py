"""
Multi-fiber rank-3 slot game.

Setup: F disjoint fibers, each over a distinct large prime q_f. Fiber f has
its own set of small primes P_f (subsets of a common pool P), and edges
e_{f, a, c} = {q_f, a*q_f, c*q_f} for a, c in P_f, a < c. Vertices across
different fibers are completely disjoint (q_f and a*q_f only).

This models the case where the residual hypergraph is composed of multiple
fiber components, and Maker can choose between fibers globally.

We check: under any of three strategies (max_gain global, dominant global,
lookahead-1 global), can Breaker force a fiber to the K_4 trap state?

If the answer is YES for some configuration, RSE on T_* fails.
If NO for all reasonable configurations we test, that's strong evidence
for RSE-on-T2 (since real T_* is composed of many such fiber-like pieces).
"""
from __future__ import annotations

import argparse
import itertools
import time
from typing import NamedTuple


class MultiState(NamedTuple):
    # Per-fiber, we encode a state. We label vertices globally.
    # Vertex id (f, 0)=q_f, (f, p)=p*q_f for p in small primes of fiber f.
    C: frozenset           # captured vertices
    D_V: frozenset         # deleted vertices
    D_E: frozenset         # deleted edges (by global edge index)
    K: frozenset           # scored edges (by global edge index)
    S: int                 # total scored weight
    captured_edges: frozenset  # ordinary-captured edges


def build_edges(fibers: list[list[int]]) -> tuple[list[tuple], list[set]]:
    """Each fiber f is a list of small primes [p_1, ..., p_kf]. Vertices in
    fiber f: (f, 0), (f, p_1), ..., (f, p_kf). Edges in fiber f:
    e_{f, i, j} = {(f,0), (f, p_i), (f, p_j)} for i < j.
    Returns (edges_list, fiber_of_edge_list)."""
    edges = []
    fiber_of = []
    for f, ps in enumerate(fibers):
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                edges.append(((f, 0), (f, ps[i]), (f, ps[j])))
                fiber_of.append(f)
    return edges, fiber_of


def is_live(state: MultiState, e_idx: int, edges) -> bool:
    if e_idx in state.D_E or e_idx in state.K or e_idx in state.captured_edges:
        return False
    for v in edges[e_idx]:
        if v in state.D_V:
            return False
    return True


def live_edges(state: MultiState, edges) -> list[int]:
    return [i for i in range(len(edges)) if is_live(state, i, edges)]


def phi(state: MultiState, e_idx: int, edges) -> int:
    return 1 << sum(1 for v in edges[e_idx] if v in state.C)


def Q(state: MultiState, edges) -> int:
    val = 8 * state.S
    for i in range(len(edges)):
        if is_live(state, i, edges):
            val += phi(state, i, edges)
    return val


def m_capture(state: MultiState, e_idx: int, edges) -> MultiState:
    e = edges[e_idx]
    return MultiState(
        C=state.C | set(e),
        D_V=state.D_V,
        D_E=state.D_E,
        K=state.K,
        S=state.S + 1,
        captured_edges=state.captured_edges | {e_idx},
    )


def m_score(state: MultiState, e_idx: int) -> MultiState:
    return MultiState(
        C=state.C,
        D_V=state.D_V,
        D_E=state.D_E,
        K=state.K | {e_idx},
        S=state.S + 1,
        captured_edges=state.captured_edges,
    )


def b_del_v(state, v):
    return MultiState(C=state.C, D_V=state.D_V | {v}, D_E=state.D_E,
                      K=state.K, S=state.S, captured_edges=state.captured_edges)


def b_del_e(state, e_idx):
    return MultiState(C=state.C, D_V=state.D_V, D_E=state.D_E | {e_idx},
                      K=state.K, S=state.S, captured_edges=state.captured_edges)


def b_score_e(state, e_idx):
    return MultiState(C=state.C, D_V=state.D_V, D_E=state.D_E,
                      K=state.K | {e_idx}, S=state.S + 1,
                      captured_edges=state.captured_edges)


def maker_moves(state, edges):
    moves = []
    for ei in live_edges(state, edges):
        moves.append(("capture", ei, m_capture(state, ei, edges)))
        moves.append(("score", ei, m_score(state, ei)))
    return moves


def breaker_moves(state, edges):
    live = live_edges(state, edges)
    if not live:
        return []
    moves = []
    cand_v = set()
    for ei in live:
        for v in edges[ei]:
            if v not in state.C and v not in state.D_V:
                cand_v.add(v)
    for v in sorted(cand_v):
        moves.append(("del_v", v, b_del_v(state, v)))
    for ei in live:
        moves.append(("del_e", ei, b_del_e(state, ei)))
    for ei in live:
        moves.append(("score_e", ei, b_score_e(state, ei)))
    return moves


def post_capture_E(state, edges):
    best = 0
    for i in range(len(edges)):
        if is_live(state, i, edges):
            best = max(best, phi(state, i, edges))
    return best


def post_capture_V(state, edges):
    cand = set()
    for i in range(len(edges)):
        if is_live(state, i, edges):
            for v in edges[i]:
                if v not in state.C and v not in state.D_V:
                    cand.add(v)
    best = 0
    for v in cand:
        s = 0
        for i in range(len(edges)):
            if is_live(state, i, edges) and v in edges[i]:
                s += phi(state, i, edges)
        best = max(best, s)
    return best


def raw_rse(state, edges):
    Q0 = Q(state, edges)
    for action, ei, after_m in maker_moves(state, edges):
        ok = True
        for b_act, b_target, after_b in breaker_moves(after_m, edges):
            if Q(after_b, edges) < Q0:
                ok = False
                break
        if ok:
            return True, (action, ei)
    return False, None


def is_terminal(state, edges):
    return not any(is_live(state, i, edges) for i in range(len(edges)))


def strategy_max_gain(state, edges):
    Q0 = Q(state, edges)
    best = None
    best_gain = None
    for ei in live_edges(state, edges):
        after = m_capture(state, ei, edges)
        gain = Q(after, edges) - Q0
        if best_gain is None or gain > best_gain:
            best_gain = gain
            best = ("capture", ei, after)
    return best


def strategy_dominant(state, edges):
    Q0 = Q(state, edges)
    best = None
    best_slack = None
    for ei in live_edges(state, edges):
        after = m_capture(state, ei, edges)
        G = Q(after, edges) - Q0
        E = post_capture_E(after, edges)
        V = post_capture_V(after, edges)
        if G >= E and G >= V:
            slack = G - max(E, V)
            if best_slack is None or slack > best_slack:
                best_slack = slack
                best = ("capture", ei, after)
    if best is not None:
        return best
    return strategy_max_gain(state, edges)


def strategy_lookahead(state, edges):
    """Pick Maker move maximizing min_breaker Q(after_breaker)."""
    best = None
    best_min = None
    for action, ei, after_m in maker_moves(state, edges):
        worst = None
        for b_act, b_tg, after_b in breaker_moves(after_m, edges):
            v = Q(after_b, edges)
            if worst is None or v < worst:
                worst = v
        if worst is None:
            worst = Q(after_m, edges)
        if best_min is None or worst > best_min:
            best_min = worst
            best = (action, ei, after_m)
    return best


STRATEGIES = {
    "max_gain": strategy_max_gain,
    "dominant": strategy_dominant,
    "lookahead": strategy_lookahead,
}


def find_isolated_violations(edges, fiber_of):
    """For each fiber, enumerate isolated single-fiber states and find raw-RSE
    failures. Returns set of global states corresponding to those violations
    (restricted to one fiber)."""
    from collections import defaultdict
    from fiber_rse_check import (
        State as FState, edges_for_k, enumerate_pre_maker_states, raw_rse as f_raw_rse,
        is_terminal as f_is_terminal, live_edges as f_live, phi as f_phi,
    )

    # Group edges by fiber
    by_fiber = defaultdict(list)
    for ei, f in enumerate(fiber_of):
        by_fiber[f].append(ei)
    violation_signatures = []
    for f, fiber_edges in by_fiber.items():
        # The isolated game over this fiber has k = (number of distinct small
        # primes in the fiber) vertices besides q_f. We re-use Phase 4 logic.
        ks = set()
        for ei in fiber_edges:
            v0, v1, v2 = edges[ei]
            ks.add(v1[1])
            ks.add(v2[1])
        k = len(ks)
        if k >= 2:
            # enumerate isolated game on K_k
            fedges = edges_for_k(k)
            visited, order = enumerate_pre_maker_states(k, 200_000)
            for fs in order:
                if f_is_terminal(fs, fedges):
                    continue
                if not any(f_phi(fs, ei, fedges) > 0 for ei in f_live(fs, fedges)):
                    continue
                ok, _ = f_raw_rse(fs, fedges, k)
                if not ok:
                    # signature = (|C|, |D_E|, |captured_edges|, sorted phi tuple)
                    sig = (
                        len(fs.C), len(fs.D_E), len(fs.D_V), len(fs.captured_edges),
                        tuple(sorted([f_phi(fs, ei, fedges) for ei in f_live(fs, fedges)])),
                        f,
                    )
                    violation_signatures.append(sig)
    return set(violation_signatures)


def signature_of(state, edges, fiber_of, f):
    """Restrict state to fiber f and compute its signature."""
    fiber_edges = [ei for ei, ff in enumerate(fiber_of) if ff == f]
    fiber_verts = set()
    for ei in fiber_edges:
        for v in edges[ei]:
            fiber_verts.add(v)
    C_f = state.C & fiber_verts
    D_V_f = state.D_V & fiber_verts
    D_E_f = state.D_E & set(fiber_edges)
    K_f = state.K & set(fiber_edges)
    captured_f = state.captured_edges & set(fiber_edges)
    live_in_f = [ei for ei in fiber_edges if is_live(state, ei, edges)]
    if not live_in_f:
        return None
    if not any(phi(state, ei, edges) > 0 for ei in live_in_f):
        return None
    sig = (
        len(C_f), len(D_E_f), len(D_V_f), len(captured_f),
        tuple(sorted([phi(state, ei, edges) for ei in live_in_f])),
        f,
    )
    return sig


def run_strategy_check(fibers, strategy_name, max_states=2_000_000):
    edges, fiber_of = build_edges(fibers)
    print(f"  Built {len(edges)} edges across {len(fibers)} fibers: {fibers}")
    print(f"  Identifying isolated-fiber violation signatures...")
    bad_sigs = find_isolated_violations(edges, fiber_of)
    print(f"  Identified {len(bad_sigs)} isolated-fiber violation signatures.")

    initial = MultiState(
        C=frozenset(), D_V=frozenset(), D_E=frozenset(),
        K=frozenset(), S=0, captured_edges=frozenset(),
    )
    visited = {initial}
    queue = [initial]
    n_rse_fail = 0
    rse_fail_examples = []
    t0 = time.time()
    strategy = STRATEGIES[strategy_name]
    sig_hits = 0
    sig_hit_examples = []
    while queue:
        if len(visited) > max_states:
            print(f"  [stop] hit max_states={max_states}")
            break
        s = queue.pop()
        if is_terminal(s, edges):
            continue
        live = live_edges(s, edges)
        if not any(phi(s, ei, edges) > 0 for ei in live):
            continue
        # Check raw RSE on this state
        ok, witness = raw_rse(s, edges)
        if not ok:
            n_rse_fail += 1
            if len(rse_fail_examples) < 3:
                rse_fail_examples.append(s)
        # Check fiber signatures
        for f in range(len(fibers)):
            sig = signature_of(s, edges, fiber_of, f)
            if sig is not None and sig in bad_sigs:
                sig_hits += 1
                if len(sig_hit_examples) < 3:
                    sig_hit_examples.append((s, f))
                break
        # Apply strategy
        m = strategy(s, edges)
        if m is None:
            continue
        action, ei, after_m = m
        for b_act, b_tg, after_b in breaker_moves(after_m, edges):
            if after_b not in visited:
                visited.add(after_b)
                queue.append(after_b)
    dt = time.time() - t0
    print(f"  Strategy={strategy_name}: visited {len(visited)} states in {dt:.2f}s.")
    print(f"    states where multi-fiber RSE fails: {n_rse_fail}")
    print(f"    states matching isolated-fiber violation signature: {sig_hits}")
    return n_rse_fail, sig_hits, rse_fail_examples, sig_hit_examples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default="33", help="comma-list of fiber sizes (e.g. '4,4' or '3,3,3' or '4,2')")
    args = ap.parse_args()
    sizes = [int(x) for x in args.config.split(",")]
    fibers = []
    for f, k in enumerate(sizes):
        # use small primes labeled 1..k, distinct per fiber via the (f, p) tuple, so pool can be shared
        fibers.append(list(range(1, k + 1)))
    print(f"=== Multi-fiber RSE check, config = {sizes} ===")
    for strat in ["max_gain", "dominant", "lookahead"]:
        print(f"\n--- Strategy: {strat} ---")
        run_strategy_check(fibers, strat)


if __name__ == "__main__":
    main()
