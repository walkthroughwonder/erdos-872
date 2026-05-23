"""
T2-restricted reachability check.

Question: when Maker plays an optimal strategy (e.g. max-gain capture, or our
proposed dominant-capture witness), can Breaker still force the fiber into one
of the 216 RSE-violation states identified by fiber_rse_check.py?

We check three different Maker strategies:
  (S1) Greedy max-gain capture: Maker always plays the ordinary capture with
       maximum G_sigma(f).
  (S2) Dominant-capture witness: Maker plays an f satisfying Dom(sigma,f) if
       one exists; else fall back to greedy.
  (S3) Lookahead-1 raw safe-edge: Maker plays the move (capture or score) that
       maximizes min over Breaker reply of Q.

For each, we do BFS over the state space where the transitions are:
  state -> (Maker move from chosen strategy) -> Breaker explores all replies.

If we reach any of the 216 violation states, the strategy is NOT a witness for
RSE on T2-states. If we never reach a violation state, that strategy DOES
satisfy RSE (Buddhdev calls this 'witness strategy').
"""
from __future__ import annotations

import sys
import time
from collections import deque
from fiber_rse_check import (
    edges_for_k, live_edges, is_terminal, phi, Q,
    maker_capture, maker_score, breaker_moves, maker_moves,
    State, post_capture_E, post_capture_V, raw_rse,
)


def find_violations(k: int):
    from fiber_rse_check import enumerate_pre_maker_states
    edges = edges_for_k(k)
    visited, order = enumerate_pre_maker_states(k, 5_000_000)
    violations = set()
    for s in order:
        if is_terminal(s, edges):
            continue
        live = live_edges(s, edges)
        if not any(phi(s, ei, edges) > 0 for ei in live):
            continue
        ok, _ = raw_rse(s, edges, k)
        if not ok:
            violations.add(s)
    return violations, edges


def maker_strategy_max_gain(state: State, edges):
    """Returns one Maker move (action, edge_idx, after_state) by ordinary-capture
    max-gain rule. Ties broken by edge index."""
    best = None
    best_gain = None
    Q0 = Q(state, edges)
    for ei in live_edges(state, edges):
        after = maker_capture(state, ei, edges)
        gain = Q(after, edges) - Q0
        if best_gain is None or gain > best_gain:
            best_gain = gain
            best = ("capture", ei, after)
    return best


def maker_strategy_dominant(state: State, edges):
    """Plays an f satisfying Dom(sigma,f), preferring f with maximum (G-max(E,V)).
    If no f satisfies Dom, falls back to max-gain capture."""
    Q0 = Q(state, edges)
    best = None
    best_slack = None
    for ei in live_edges(state, edges):
        after = maker_capture(state, ei, edges)
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
    return maker_strategy_max_gain(state, edges)


def maker_strategy_lookahead(state: State, edges, k: int):
    """Lookahead-1: among all Maker moves (capture or score), pick the one
    maximizing min over Breaker replies of Q. Tiebreak by edge index."""
    best = None
    best_min = None
    for action, ei, after_m in maker_moves(state, edges):
        worst = None
        for b_act, b_target, after_b in breaker_moves(after_m, edges, k):
            v = Q(after_b, edges)
            if worst is None or v < worst:
                worst = v
        if worst is None:  # no Breaker move => Maker wins this branch outright
            worst = Q(after_m, edges)
        if best_min is None or worst > best_min:
            best_min = worst
            best = (action, ei, after_m)
    return best


STRATEGIES = {
    "max_gain": maker_strategy_max_gain,
    "dominant": maker_strategy_dominant,
    "lookahead": maker_strategy_lookahead,
}


def reach_under_strategy(k: int, strategy_name: str, violations: set, edges, verbose: bool = False):
    """BFS over states reached under (Maker = strategy, Breaker = any). Return:
      - set of reachable pre-Maker states
      - list of reached violation states (if any)
      - a sample play sequence reaching the first violation (for diagnostic).
    """
    initial = State(C=frozenset(), D_V=frozenset(), D_E=frozenset(), K=frozenset(), S=0)
    visited = {initial}
    parent = {initial: None}  # for reconstruction
    parent_move = {initial: None}
    queue = deque([initial])
    reached_violations = []
    strategy = STRATEGIES[strategy_name]
    while queue:
        s = queue.popleft()
        if is_terminal(s, edges):
            continue
        live = live_edges(s, edges)
        if not any(phi(s, ei, edges) > 0 for ei in live):
            continue
        m_move = strategy(s, edges) if strategy_name != "lookahead" else strategy(s, edges, k)
        if m_move is None:
            continue
        action, m_ei, after_m = m_move
        for b_act, b_target, after_b in breaker_moves(after_m, edges, k):
            if after_b not in visited:
                visited.add(after_b)
                parent[after_b] = s
                parent_move[after_b] = (("M", action, m_ei), ("B", b_act, b_target))
                if after_b in violations:
                    reached_violations.append(after_b)
                queue.append(after_b)
    # reconstruct path to first violation if any
    path = []
    if reached_violations:
        s = reached_violations[0]
        while s is not None:
            path.append(s)
            s = parent.get(s)
        path.reverse()
    return visited, reached_violations, path, parent_move


def render_path(path, parent_move, edges):
    print("Play sequence:")
    for i, s in enumerate(path):
        live = live_edges(s, edges)
        live_info = [(ei, edges[ei], phi(s, ei, edges)) for ei in live]
        print(f"  Round {i}: C={sorted(s.C)} D_V={sorted(s.D_V)} D_E={sorted(s.D_E)} K={sorted(s.K)} S={s.S} capt_edges={sorted(s.captured_edges)} Q={Q(s, edges)} live={live_info}")
        if i + 1 < len(path):
            mv = parent_move.get(path[i + 1])
            if mv:
                print(f"    -> Maker: {mv[0]}, Breaker: {mv[1]}")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=4)
    args = ap.parse_args()
    k = args.k

    print(f"=== T2 reachability check for k={k} fiber ===\n")
    print(f"Step 1: identifying all raw-RSE violation states...")
    violations, edges = find_violations(k)
    print(f"  {len(violations)} violation states identified.\n")

    for strat_name in ["max_gain", "dominant", "lookahead"]:
        print(f"--- Strategy: {strat_name} ---")
        t0 = time.time()
        visited, reached, path, parent_move = reach_under_strategy(k, strat_name, violations, edges)
        dt = time.time() - t0
        print(f"  Reachable pre-Maker states under this strategy + adversarial Breaker: {len(visited)}")
        print(f"  Violation states reached: {len(reached)}  (in {dt:.2f}s)")
        if reached:
            print(f"  -> Strategy '{strat_name}' is NOT a witness for RSE on T2-states.")
            print(f"  Sample play reaching first violation:")
            render_path(path, parent_move, edges)
        else:
            print(f"  -> Strategy '{strat_name}' IS a witness for RSE on its reachable subspace.")
            print(f"     This proves Certified-RSE(strategy) on the fiber.")
        print()


if __name__ == "__main__":
    main()
