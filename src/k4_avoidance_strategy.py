"""
K_4-trap-aware Maker strategy.

Hypothesis: a Maker strategy that explicitly DETECTS the impending K_4 trap
and re-routes can satisfy RSE on multi-fiber configurations.

A "near-trap" state is one where some fiber f has:
  - exactly 2 ordinary captured edges in fiber f
  - 0 vertex deletions in fiber f
  - 2 or 3 live edges remaining in fiber f, each with potential >= 4
  - Maker about to play in fiber f.

If Maker is in such a state, the trap is one Breaker move away. Maker should
SWITCH to a different fiber or play a move that breaks the trap geometry
(e.g., a score-move that doesn't add vertices to C).

This file implements two trap-avoiding strategies:

  trap_aware_score: when in near-trap fiber, Maker uses alternate-scoring
    rather than ordinary capture. Score doesn't add to C, so the "all 5
    slots in C" condition for Phi=8 never arises.

  trap_aware_switch: when in near-trap fiber AND another fiber has positive
    weight, Maker switches to the other fiber.

We then re-run multi-fiber enumeration and count RSE failures.
"""
from __future__ import annotations

import time
import sys
sys.path.insert(0, '.')
from multi_fiber_rse import (
    MultiState, build_edges, is_live, live_edges, phi, Q,
    m_capture, m_score, b_del_v, b_del_e, b_score_e, maker_moves, breaker_moves,
    raw_rse, is_terminal, signature_of, find_isolated_violations,
    strategy_max_gain, post_capture_E, post_capture_V,
)


def fiber_of_edge(edges, e_idx) -> int:
    """Recover the fiber index from edges[e_idx] = ((f,0), (f,p), (f,p'))."""
    return edges[e_idx][0][0]


def fiber_state(state, edges, f):
    """Return (n_live, n_captured_edges, n_vertex_deletions, max_phi_of_live)."""
    fe = [ei for ei in range(len(edges)) if fiber_of_edge(edges, ei) == f]
    live = [ei for ei in fe if is_live(state, ei, edges)]
    captured = [ei for ei in fe if ei in state.captured_edges]
    # vertex deletions hitting this fiber
    n_dv_in_f = sum(1 for v in state.D_V if v[0] == f)
    max_phi = max((phi(state, ei, edges) for ei in live), default=0)
    return len(live), len(captured), n_dv_in_f, max_phi


def is_near_trap(state, edges, f) -> bool:
    """Detect any K_k trap signature for k >= 3.

    The K_k trap pattern: in fiber f, 0 vertex deletions, >= 1 ordinary capture
    already, no scored edges in fiber, and the maximum live-edge potential in
    fiber is >= 4 (i.e., at least 2 slot vertices are already in C).
    Once 2 captures land and no vertex was deleted, the K_4 trap is one
    Breaker move away. We extend the detector to also cover K_3 (k=3) and
    K_5+ cases."""
    n_live, n_cap, n_dv, max_phi = fiber_state(state, edges, f)
    if n_dv > 0:
        return False  # vertex deletion already broke the fiber geometry
    if n_cap >= 1 and n_live >= 1 and max_phi >= 4:
        return True
    return False


def strategy_trap_aware_score(state, edges):
    """If Maker is about to play in a near-trap fiber, prefer alternate-scoring
    over capture. Otherwise default to max-gain capture."""
    Q0 = Q(state, edges)
    # Group live edges by fiber
    by_fiber = {}
    for ei in live_edges(state, edges):
        by_fiber.setdefault(fiber_of_edge(edges, ei), []).append(ei)
    safe_fibers = [f for f in by_fiber if not is_near_trap(state, edges, f)]
    # Prefer a capture in a non-trap fiber, max gain
    candidates = []
    if safe_fibers:
        for f in safe_fibers:
            for ei in by_fiber[f]:
                gain = Q(m_capture(state, ei, edges), edges) - Q0
                candidates.append((gain, "capture", ei))
    else:
        # all fibers are near-trap; use score moves
        for ei in live_edges(state, edges):
            gain = Q(m_score(state, ei), edges) - Q0
            candidates.append((gain, "score", ei))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    gain, action, ei = candidates[0]
    if action == "capture":
        return ("capture", ei, m_capture(state, ei, edges))
    else:
        return ("score", ei, m_score(state, ei))


def strategy_trap_aware_switch(state, edges):
    """If a fiber is near-trap and another fiber has positive-weight live edges,
    play in the other fiber. Else fall back to max-gain capture."""
    Q0 = Q(state, edges)
    by_fiber = {}
    for ei in live_edges(state, edges):
        by_fiber.setdefault(fiber_of_edge(edges, ei), []).append(ei)
    safe_fibers = [f for f in by_fiber if not is_near_trap(state, edges, f)]
    if safe_fibers:
        best = None
        best_gain = None
        for f in safe_fibers:
            for ei in by_fiber[f]:
                gain = Q(m_capture(state, ei, edges), edges) - Q0
                if best_gain is None or gain > best_gain:
                    best_gain = gain
                    best = ("capture", ei, m_capture(state, ei, edges))
        return best
    # all near-trap: score the highest-potential edge
    best = None
    best_gain = None
    for ei in live_edges(state, edges):
        gain = Q(m_score(state, ei), edges) - Q0
        if best_gain is None or gain > best_gain:
            best_gain = gain
            best = ("score", ei, m_score(state, ei))
    return best


def run_check(fibers, strategy_func, name, max_states=2_000_000):
    edges, fiber_of = build_edges(fibers)
    bad_sigs = find_isolated_violations(edges, fiber_of)
    initial = MultiState(C=frozenset(), D_V=frozenset(), D_E=frozenset(),
                        K=frozenset(), S=0, captured_edges=frozenset())
    visited = {initial}
    queue = [initial]
    n_rse_fail = 0
    sig_hits = 0
    fail_examples = []
    t0 = time.time()
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
        ok, witness = raw_rse(s, edges)
        if not ok:
            n_rse_fail += 1
            if len(fail_examples) < 2:
                fail_examples.append(s)
        for f in range(len(fibers)):
            sig = signature_of(s, edges, fiber_of, f)
            if sig is not None and sig in bad_sigs:
                sig_hits += 1
                break
        m = strategy_func(s, edges)
        if m is None:
            continue
        action, ei, after_m = m
        for b_act, b_tg, after_b in breaker_moves(after_m, edges):
            if after_b not in visited:
                visited.add(after_b)
                queue.append(after_b)
    dt = time.time() - t0
    print(f"  Strategy {name}: visited {len(visited)} states in {dt:.2f}s")
    print(f"    multi-fiber RSE failures: {n_rse_fail}")
    print(f"    states matching isolated K_k trap signature: {sig_hits}")
    return n_rse_fail, sig_hits


def main():
    for config in [[4, 4], [4, 2], [4, 3]]:
        fibers = [list(range(1, k + 1)) for k in config]
        print(f"\n=== Config {config} ===")
        run_check(fibers, strategy_max_gain, "max_gain (baseline)")
        run_check(fibers, strategy_trap_aware_score, "trap_aware_score")
        run_check(fibers, strategy_trap_aware_switch, "trap_aware_switch")


if __name__ == "__main__":
    main()
