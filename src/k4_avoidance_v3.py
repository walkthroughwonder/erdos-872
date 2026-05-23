"""
Refined trap-aware Maker strategy v3.

The remaining failures after v2 share signature:
  fiber has Phi=8 live edge (all 3 slot vertices captured)
  Maker's gain is 0 (capturing or scoring adds nothing to vertices)
  Breaker edge-deletes the Phi=8 edge for a loss of 8

The fix: BEFORE any Maker move that would create a Phi=8 live edge, prefer
either (a) a move in a different fiber, or (b) an alternate-scoring move that
removes the dangerous edge instead of strengthening it.

We define:

  is_dangerous_capture(state, ei): capturing edge ei would either
    (i) raise some live edge's Phi to 8, or
    (ii) leave a live edge with Phi >= 4 and adjacent capturable slots.

  is_dangerous_score(state, ei): scoring removes ei from live but does not
    alter Phi elsewhere. Score is always safe in terms of NEW Phi=8 creation.
    But score consumes the edge without gain, so we only score when no safe
    capture is available.

Strategy v3:
  1. Find all live edges. Group by fiber.
  2. For each live edge ei, classify:
       SAFE_CAPTURE: ordinary capture, no fiber becomes near-trap after.
       SAFE_SCORE:   alternate-scoring (always allowed).
       UNSAFE:       capture creates near-trap or Phi=8.
  3. Prefer SAFE_CAPTURE with max gain. If none exists, prefer SAFE_SCORE
     with max gain. If neither, fall back to least-bad UNSAFE_CAPTURE.

Definition of "fiber becomes near-trap": after the capture, the fiber has
  - 0 vertex deletions in fiber
  - >= 1 ordinary capture in fiber (counting this one)
  - >= 1 live edge with Phi >= 4 (post-capture)
  - no scored edge in fiber to break the geometry.

Equivalently: the post-capture fiber state is on the path to the K_k trap.
"""
from __future__ import annotations

import sys
import time
sys.path.insert(0, '.')
from multi_fiber_rse import (
    MultiState, build_edges, is_live, live_edges, phi, Q,
    m_capture, m_score, b_del_v, b_del_e, b_score_e, breaker_moves,
    raw_rse, is_terminal, signature_of, find_isolated_violations,
    strategy_max_gain,
)


def fiber_of_edge(edges, ei):
    return edges[ei][0][0]


def fiber_state(state, edges, f):
    fe = [ei for ei in range(len(edges)) if fiber_of_edge(edges, ei) == f]
    live = [ei for ei in fe if is_live(state, ei, edges)]
    captured = [ei for ei in fe if ei in state.captured_edges]
    scored_in_f = [ei for ei in fe if ei in state.K]
    n_dv = sum(1 for v in state.D_V if v[0] == f)
    max_phi = max((phi(state, ei, edges) for ei in live), default=0)
    return len(live), len(captured), len(scored_in_f), n_dv, max_phi


def is_post_state_near_trap(after_state, edges, f):
    n_live, n_cap, n_score, n_dv, max_phi = fiber_state(after_state, edges, f)
    if n_dv > 0:
        return False
    if n_score > 0:
        return False
    if n_cap >= 1 and n_live >= 1 and max_phi >= 4:
        return True
    return False


def post_capture_creates_phi8(after_state, edges, f):
    """Does any live edge in fiber f have Phi == 8 after the move?"""
    fe = [ei for ei in range(len(edges)) if fiber_of_edge(edges, ei) == f]
    for ei in fe:
        if is_live(after_state, ei, edges) and phi(after_state, ei, edges) >= 8:
            return True
    return False


def strategy_v3(state, edges):
    Q0 = Q(state, edges)
    live_now = live_edges(state, edges)
    safe_caps = []
    unsafe_caps = []
    safe_scores = []

    for ei in live_now:
        f = fiber_of_edge(edges, ei)
        # Try capture
        after = m_capture(state, ei, edges)
        gain = Q(after, edges) - Q0
        if post_capture_creates_phi8(after, edges, f):
            unsafe_caps.append((gain, ei, after, "phi8"))
        elif is_post_state_near_trap(after, edges, f):
            unsafe_caps.append((gain, ei, after, "near_trap"))
        else:
            safe_caps.append((gain, ei, after))
        # Try score (always safe in terms of new Phi=8)
        after_s = m_score(state, ei)
        gain_s = Q(after_s, edges) - Q0
        safe_scores.append((gain_s, ei, after_s))

    # Prefer safe capture with max gain
    if safe_caps:
        safe_caps.sort(reverse=True, key=lambda t: t[0])
        gain, ei, after = safe_caps[0]
        return ("capture", ei, after)
    # Else safe score with max gain
    if safe_scores:
        safe_scores.sort(reverse=True, key=lambda t: t[0])
        gain, ei, after = safe_scores[0]
        return ("score", ei, after)
    # Should not happen but fall through to unsafe
    if unsafe_caps:
        unsafe_caps.sort(reverse=True, key=lambda t: t[0])
        gain, ei, after, reason = unsafe_caps[0]
        return ("capture", ei, after)
    return None


def run(fibers, strategy, name, max_states=2_000_000):
    edges, fiber_of = build_edges(fibers)
    bad_sigs = find_isolated_violations(edges, fiber_of)
    initial = MultiState(C=frozenset(), D_V=frozenset(), D_E=frozenset(),
                        K=frozenset(), S=0, captured_edges=frozenset())
    visited = {initial}
    queue = [initial]
    n_fail = 0
    sig_hits = 0
    fail_examples = []
    t0 = time.time()
    while queue:
        if len(visited) > max_states:
            print(f"  hit max_states={max_states}")
            break
        s = queue.pop()
        if is_terminal(s, edges):
            continue
        if not any(phi(s, ei, edges) > 0 for ei in live_edges(s, edges)):
            continue
        ok, _ = raw_rse(s, edges)
        if not ok:
            n_fail += 1
            if len(fail_examples) < 3:
                fail_examples.append(s)
        for f in range(len(fibers)):
            sig = signature_of(s, edges, fiber_of, f)
            if sig is not None and sig in bad_sigs:
                sig_hits += 1
                break
        m = strategy(s, edges)
        if m is None:
            continue
        for b_act, b_tg, after_b in breaker_moves(m[2], edges):
            if after_b not in visited:
                visited.add(after_b)
                queue.append(after_b)
    dt = time.time() - t0
    print(f"  {name}: {len(visited)} states in {dt:.2f}s, RSE failures={n_fail}, isolated-K_k-sig hits={sig_hits}")
    return n_fail, sig_hits, fail_examples


def main():
    for cfg in [[4, 2], [4, 3], [4, 4], [3, 3, 3], [4, 3, 2]]:
        fibers = [list(range(1, k + 1)) for k in cfg]
        print(f"\n=== Config {cfg} ===")
        run(fibers, strategy_max_gain, "max_gain  (baseline)")
        run(fibers, strategy_v3, "v3 trap+phi8 aware")


if __name__ == "__main__":
    main()
