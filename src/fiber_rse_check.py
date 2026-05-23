"""
Finite-state enumeration of the single-fiber slot game on K_k.

Fiber model: fix one large prime b. The "fiber over b" has
  - 1 + k slot vertices: {b, p_1 b, p_2 b, ..., p_k b}
  - C(k,2) rank-3 hyperedges: e_{i,j} = {b, p_i b, p_j b}, weight 1 each.

This is the local picture surrounding a single large prime in G(n, delta).
The K_4-fiber refutation of Proposition A.2 lives in the k=4 case.

State = (C, D_V, D_E, K, S) restricted to this fiber.
We encode the slot vertices 0..k where index 0 = b (the "hub") and 1..k = p_i b.

Reachability: we enumerate all states reachable from the initial state (no
captures, no deletions, no scored edges) by ALTERNATING Maker-then-Breaker
plies. Maker has three options per ply:
  (M1) ordinary capture of a live edge
  (M2) alternate-scoring of a live edge
Breaker then has three reply options:
  (B1) delete one uncaptured undeleted vertex
  (B2) delete one live edge without scoring
  (B3) scored-edge reply on one live edge

We do FULL ROUNDS so that pre-Maker states are exactly the states between
rounds. A state with no positive-weight live edge is terminal.

For each reachable pre-Maker state with at least one positive-weight live edge,
we check the Certified-RSE predicate:
  exists live edge f with G_sigma(f) >= max(E_sigma(f), V_sigma(f))
where G_sigma(f) is the EXACT Q-change of ordinary capture of f (no Breaker
move yet), E_sigma(f) is the max post-capture edge potential of any other
live edge, and V_sigma(f) is the max post-capture vertex-star sum.

This script reports:
  - total reachable pre-Maker states
  - states violating Certified-RSE (Maker-disaster states)
  - for each violating state, a minimal witness Breaker strategy demonstrating
    that no f satisfies the certificate

We also run the more permissive check: does ANY live edge admit a
"raw safe-edge" property (i.e., satisfies Buddhdev's RSE directly,
allowing all three Maker actions and ranging over all Breaker actions)?
This is the bigger question. Even if Certified-RSE fails, raw RSE could hold.

Usage:
  python fiber_rse_check.py --k 3
  python fiber_rse_check.py --k 4
  python fiber_rse_check.py --k 5 --max-states 2000000
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from dataclasses import dataclass
from typing import Iterable, NamedTuple


class State(NamedTuple):
    # All sets encoded as frozensets of small ints.
    C: frozenset       # captured vertices (subset of {0,1,...,k})
    D_V: frozenset     # deleted vertices  (subset of {0,1,...,k}), disjoint from C
    D_E: frozenset     # unscored deleted edges (subset of edge index set)
    K: frozenset       # scored edges (subset of edge index set), disjoint from D_E
    S: int             # total scored weight (== |captured edges via ordinary| + |K|)
    # captured edges via ordinary capture are tracked implicitly: an edge is "consumed"
    # if it has been captured (its vertices were added to C and S incremented). We
    # encode that by including the edge index in K? No - the spec distinguishes:
    # ordinary capture: vertices to C, S += 1, edge removed from live set.
    # scored edge: edge to K, S += 1, no change to C.
    # We need to track BOTH consumed-by-capture and consumed-by-score, since both
    # remove the edge from "live". Use one more field:
    captured_edges: frozenset = frozenset()  # edges consumed by ordinary capture


def edges_for_k(k: int) -> list[tuple[int, int, int]]:
    """Edge e_{i,j} for 1 <= i < j <= k is the triple (0, i, j) (b, p_i b, p_j b)."""
    es = []
    for i in range(1, k + 1):
        for j in range(i + 1, k + 1):
            es.append((0, i, j))
    return es


def is_live(state: State, e_idx: int, edges: list[tuple[int, int, int]]) -> bool:
    if e_idx in state.D_E or e_idx in state.K or e_idx in state.captured_edges:
        return False
    e = edges[e_idx]
    if any(v in state.D_V for v in e):
        return False
    return True


def live_edges(state: State, edges: list[tuple[int, int, int]]) -> list[int]:
    return [i for i in range(len(edges)) if is_live(state, i, edges)]


def phi(state: State, e_idx: int, edges: list[tuple[int, int, int]]) -> int:
    """2^|e cap C| * w(e). w(e)=1 always."""
    e = edges[e_idx]
    return 1 << sum(1 for v in e if v in state.C)


def Q(state: State, edges: list[tuple[int, int, int]]) -> int:
    val = 8 * state.S
    for i in range(len(edges)):
        if is_live(state, i, edges):
            val += phi(state, i, edges)
    return val


def maker_capture(state: State, e_idx: int, edges: list[tuple[int, int, int]]) -> State:
    e = edges[e_idx]
    return State(
        C=state.C | set(e),
        D_V=state.D_V,
        D_E=state.D_E,
        K=state.K,
        S=state.S + 1,
        captured_edges=state.captured_edges | {e_idx},
    )


def maker_score(state: State, e_idx: int) -> State:
    return State(
        C=state.C,
        D_V=state.D_V,
        D_E=state.D_E,
        K=state.K | {e_idx},
        S=state.S + 1,
        captured_edges=state.captured_edges,
    )


def breaker_delete_vertex(state: State, v: int) -> State:
    return State(
        C=state.C,
        D_V=state.D_V | {v},
        D_E=state.D_E,
        K=state.K,
        S=state.S,
        captured_edges=state.captured_edges,
    )


def breaker_delete_edge(state: State, e_idx: int) -> State:
    return State(
        C=state.C,
        D_V=state.D_V,
        D_E=state.D_E | {e_idx},
        K=state.K,
        S=state.S,
        captured_edges=state.captured_edges,
    )


def breaker_score_edge(state: State, e_idx: int) -> State:
    return State(
        C=state.C,
        D_V=state.D_V,
        D_E=state.D_E,
        K=state.K | {e_idx},
        S=state.S + 1,
        captured_edges=state.captured_edges,
    )


def maker_moves(state: State, edges) -> list[tuple[str, int, State]]:
    moves = []
    for e in live_edges(state, edges):
        moves.append(("capture", e, maker_capture(state, e, edges)))
        moves.append(("score", e, maker_score(state, e)))
    return moves


def breaker_moves(state: State, edges, k: int) -> list[tuple[str, int, State]]:
    moves = []
    live = live_edges(state, edges)
    if not live:
        return moves  # no Breaker move legal if no live edge? actually vertex delete is
        # still legal if there exists an uncaptured undeleted vertex in some live edge.
        # We follow Buddhdev's spec: Breaker may always play if some live edge exists.
        # If no live edge exists, the game is over.
    # vertex deletions (Buddhdev: delete an uncaptured vertex; we require the vertex to
    # be in at least one live edge, else the move is wasted but legal. Actually a
    # vertex deletion of a non-live-incident vertex is legal but useless. To bound the
    # state space we require the vertex to be in some live edge - this never gives
    # Breaker more power.)
    all_verts = set()
    for ei in live:
        all_verts.update(edges[ei])
    for v in sorted(all_verts):
        if v not in state.C and v not in state.D_V:
            moves.append(("del_v", v, breaker_delete_vertex(state, v)))
    # unscored edge deletions
    for ei in live:
        moves.append(("del_e", ei, breaker_delete_edge(state, ei)))
    # scored-edge replies
    for ei in live:
        moves.append(("score_e", ei, breaker_score_edge(state, ei)))
    return moves


def is_terminal(state: State, edges) -> bool:
    return not any(is_live(state, i, edges) for i in range(len(edges)))


def post_capture_E(state_after: State, edges) -> int:
    """E_sigma(f): max post-capture Phi(e) over edges live in state_after."""
    best = 0
    for ei in range(len(edges)):
        if is_live(state_after, ei, edges):
            best = max(best, phi(state_after, ei, edges))
    return best


def post_capture_V(state_after: State, edges) -> int:
    """V_sigma(f): max over uncaptured undeleted v of sum of phi of incident live edges."""
    best = 0
    # candidate vertices: any vertex in some live edge, not in C, not in D_V.
    cand = set()
    for ei in range(len(edges)):
        if is_live(state_after, ei, edges):
            for v in edges[ei]:
                if v not in state_after.C and v not in state_after.D_V:
                    cand.add(v)
    for v in cand:
        s = 0
        for ei in range(len(edges)):
            if is_live(state_after, ei, edges) and v in edges[ei]:
                s += phi(state_after, ei, edges)
        best = max(best, s)
    return best


def G_capture(state: State, e_idx: int, edges) -> int:
    after = maker_capture(state, e_idx, edges)
    return Q(after, edges) - Q(state, edges)


def G_score(state: State, e_idx: int, edges) -> int:
    after = maker_score(state, e_idx)
    return Q(after, edges) - Q(state, edges)


def certified_rse(state: State, edges) -> tuple[bool, int | None]:
    """Return (holds, witness_edge_or_None). Holds iff exists live edge f with
    G_capture(f) >= max(E_sigma(f), V_sigma(f))."""
    for ei in live_edges(state, edges):
        after = maker_capture(state, ei, edges)
        G = Q(after, edges) - Q(state, edges)
        E = post_capture_E(after, edges)
        V = post_capture_V(after, edges)
        if G >= E and G >= V:
            return True, ei
    return False, None


def raw_rse(state: State, edges, k: int) -> tuple[bool, dict]:
    """Buddhdev's actual RSE: exists Maker move (capture OR score) such that for
    every legal Breaker reply, Q does not decrease. Returns (holds, witness)."""
    Q0 = Q(state, edges)
    for action, ei, after_maker in maker_moves(state, edges):
        all_ok = True
        worst_breaker = None
        worst_loss = 0
        for b_action, b_target, after_b in breaker_moves(after_maker, edges, k):
            Q1 = Q(after_b, edges)
            if Q1 < Q0:
                all_ok = False
                loss = Q0 - Q1
                if loss > worst_loss:
                    worst_loss = loss
                    worst_breaker = (b_action, b_target)
                break
        if all_ok:
            return True, {"maker": (action, ei)}
    # No witness found - return one example violation.
    # Find the move minimizing the worst Breaker loss, for diagnostic.
    best_action = None
    best_worst_loss = None
    best_breaker = None
    for action, ei, after_maker in maker_moves(state, edges):
        worst_loss = 0
        worst_breaker = None
        for b_action, b_target, after_b in breaker_moves(after_maker, edges, k):
            Q1 = Q(after_b, edges)
            if Q0 - Q1 > worst_loss:
                worst_loss = Q0 - Q1
                worst_breaker = (b_action, b_target)
        if best_worst_loss is None or worst_loss < best_worst_loss:
            best_worst_loss = worst_loss
            best_action = (action, ei)
            best_breaker = worst_breaker
    return False, {"best_maker": best_action, "best_worst_breaker": best_breaker, "loss": best_worst_loss}


def enumerate_pre_maker_states(k: int, max_states: int) -> tuple[set[State], list[State]]:
    """Enumerate all pre-Maker states reachable from the initial empty state via
    any sequence of full Maker-Breaker rounds. Return (set_of_all_states, ordered_list)."""
    edges = edges_for_k(k)
    initial = State(C=frozenset(), D_V=frozenset(), D_E=frozenset(), K=frozenset(), S=0)
    visited = {initial}
    frontier = [initial]
    order = [initial]
    while frontier:
        if len(visited) > max_states:
            print(f"[warning] hit max_states={max_states}; truncating", file=sys.stderr)
            break
        state = frontier.pop()
        if is_terminal(state, edges):
            continue
        # All ways to play one full round
        for m_action, m_ei, after_m in maker_moves(state, edges):
            for b_action, b_target, after_b in breaker_moves(after_m, edges, k):
                if after_b not in visited:
                    visited.add(after_b)
                    frontier.append(after_b)
                    order.append(after_b)
    return visited, order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--max-states", type=int, default=1_000_000)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    k = args.k
    edges = edges_for_k(k)
    print(f"Fiber on k={k} small primes; {len(edges)} hyperedges; 1+{k} vertices.")
    print(f"Edges: {edges}")

    t0 = time.time()
    visited, order = enumerate_pre_maker_states(k, args.max_states)
    t_enum = time.time() - t0
    print(f"Enumerated {len(visited)} reachable pre-Maker states in {t_enum:.2f}s.")

    # Check Certified-RSE and Raw-RSE on each non-terminal state.
    n_nonterminal = 0
    n_certified = 0
    n_raw = 0
    certified_violations = []
    raw_violations = []
    for state in order:
        if is_terminal(state, edges):
            continue
        # also skip if no positive-weight live edge (== terminal in our weighted setting)
        if not any(phi(state, ei, edges) > 0 for ei in live_edges(state, edges)):
            continue
        n_nonterminal += 1
        c_ok, c_witness = certified_rse(state, edges)
        if c_ok:
            n_certified += 1
        else:
            certified_violations.append(state)
        r_ok, r_witness = raw_rse(state, edges, k)
        if r_ok:
            n_raw += 1
        else:
            raw_violations.append((state, r_witness))

    t_check = time.time() - t0 - t_enum
    print(f"Checking complete in {t_check:.2f}s.")
    print(f"Non-terminal pre-Maker states: {n_nonterminal}")
    print(f"Certified-RSE holds: {n_certified} / {n_nonterminal}  ({100*n_certified/max(n_nonterminal,1):.2f}%)")
    print(f"Raw RSE holds:       {n_raw} / {n_nonterminal}  ({100*n_raw/max(n_nonterminal,1):.2f}%)")

    if raw_violations:
        print(f"\n=== {len(raw_violations)} states where RAW RSE FAILS ===")
        for state, witness in raw_violations[:5]:
            print(f"\nState: C={sorted(state.C)} D_V={sorted(state.D_V)} D_E={sorted(state.D_E)} K={sorted(state.K)} S={state.S} captured_edges={sorted(state.captured_edges)}")
            live = live_edges(state, edges)
            print(f"  Live edges: {[(ei, edges[ei], phi(state, ei, edges)) for ei in live]}")
            print(f"  Q(state) = {Q(state, edges)}")
            print(f"  Best Maker move: {witness['best_maker']}, Breaker response: {witness['best_worst_breaker']}, worst loss: {witness['loss']}")
    else:
        print("\nNo raw-RSE violations: RSE holds on all reachable single-fiber states.")

    if certified_violations and not raw_violations:
        print(f"\n=== {len(certified_violations)} states where CERTIFIED-RSE FAILS but RAW RSE HOLDS ===")
        for state in certified_violations[:5]:
            live = live_edges(state, edges)
            print(f"\nState: C={sorted(state.C)} D_V={sorted(state.D_V)} D_E={sorted(state.D_E)} K={sorted(state.K)} S={state.S} captured_edges={sorted(state.captured_edges)}")
            print(f"  Live edges: {[(ei, edges[ei], phi(state, ei, edges)) for ei in live]}")
            print(f"  Q(state) = {Q(state, edges)}")

    if args.out:
        out = {
            "k": k,
            "n_states": len(visited),
            "n_nonterminal": n_nonterminal,
            "certified_holds": n_certified,
            "raw_holds": n_raw,
            "certified_violations": len(certified_violations),
            "raw_violations": len(raw_violations),
            "enum_seconds": t_enum,
            "check_seconds": t_check,
        }
        with open(args.out, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\nWrote summary to {args.out}")


if __name__ == "__main__":
    main()
