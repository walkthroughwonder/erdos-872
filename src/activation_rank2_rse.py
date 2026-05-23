"""
Activation-stage RSE check.

Setup (Buddhdev Proposition A.6): the activation game is a RANK-2 weighted
graph game with the scaled-potential rule of Proposition A.3. The board is:

  Vertices: small primes P_Y (we model as {1, 2, ..., k}).
  Edges:    one edge e_{a,c} for each pair (a, c) with a < c, both in P_Y.
  Initial weight w_0(e_{a,c}) = |B_{a,c}|, an externally-given positive int.

State:
  - V_avail: set of small primes not yet captured and not yet deleted.
  - E_status[e]: "live" / "claimed" / "deleted".
  - w[e]: current token weight (decreases by off-model Shortener moves, but
    in this finite check we model only on-model moves: Shortener vertex
    deletion (delete a small prime) and Shortener edge deletion (delete a
    pair). Off-model token deletions are bounded by Proposition A.7 and
    don't affect the RSE check since they leave w >= 0.

Coefficient phi_t(e) in the scaled potential:
  unclaimed, both endpoints uncaptured:       (1/8) w
  unclaimed, one endpoint captured:           (1/4) w
  unclaimed, two endpoints captured:          (1/2) w
  claimed:                                    w
  deleted:                                    0

The scaled potential is Q_t = S_t + sum_e phi_t(e), where S_t is the count
of activation targets already played. (Note: this is Buddhdev's Q, NOT the
8*S + sum 2^|C cap e|*w(e) form from the rank-3 game.)

Move semantics:
  Maker (Prolonger) on a live edge e=(a,c) with w(e) > 0:
    "claim" e: e becomes claimed, S_t += 1, w(e) -= 1.
    No alternate-scoring (it's rank 2, only one Maker action type).
  Breaker (Shortener) reply, after Maker's move:
    "del_v" a vertex v (small prime) not yet captured/deleted.
    "del_e" a live edge e' (sets phi to 0; w stays).

A vertex is "captured" once Maker claims an incident edge. The vertex set
is small (just P_Y), so the state space is much smaller than the rank-3 case.

We check RAW RSE on every reachable pre-Maker state with positive-weight
live edge: does there exist a Maker move f such that every Breaker reply
leaves Q non-decreasing.

We expect RSE to hold here because activation is rank 2 and Buddhdev only
needed the rank-3 K_4 fiber to refute the general case.
"""
from __future__ import annotations

import argparse
import itertools
import time
from typing import NamedTuple


class State(NamedTuple):
    C: frozenset           # captured small primes (vertex set V_avail \ C are uncaptured)
    D_V: frozenset         # deleted small primes (not captured, not in C)
    claimed: frozenset     # claimed edges (by edge index)
    D_E: frozenset         # deleted edges (by edge index)
    w: tuple               # current token weight per edge (int tuple, len = |edges|)
    S: int                 # number of activation targets played


def edges_for_k(k: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(k) for j in range(i + 1, k)]


def is_live(state: State, e_idx: int, edges: list[tuple[int, int]]) -> bool:
    if e_idx in state.claimed or e_idx in state.D_E:
        return False
    a, c = edges[e_idx]
    if a in state.D_V or c in state.D_V:
        return False
    if state.w[e_idx] <= 0:
        return False
    return True


def live_edges(state: State, edges) -> list[int]:
    return [i for i in range(len(edges)) if is_live(state, i, edges)]


def phi(state: State, e_idx: int, edges) -> float:
    a, c = edges[e_idx]
    if e_idx in state.D_E:
        return 0.0
    if e_idx in state.claimed:
        return float(state.w[e_idx])
    if state.w[e_idx] <= 0:
        return 0.0
    if a in state.D_V or c in state.D_V:
        return 0.0
    n_cap = int(a in state.C) + int(c in state.C)
    coeff = {0: 0.125, 1: 0.25, 2: 0.5}[n_cap]
    return coeff * state.w[e_idx]


def Q(state: State, edges) -> float:
    val = float(state.S)
    for i in range(len(edges)):
        val += phi(state, i, edges)
    return val


def maker_claim(state: State, e_idx: int, edges) -> State:
    a, c = edges[e_idx]
    new_w = list(state.w)
    new_w[e_idx] = max(0, new_w[e_idx] - 1)  # consume one token
    return State(
        C=state.C | {a, c},
        D_V=state.D_V,
        claimed=state.claimed | {e_idx},
        D_E=state.D_E,
        w=tuple(new_w),
        S=state.S + 1,
    )


def breaker_del_vertex(state: State, v: int) -> State:
    return State(
        C=state.C,
        D_V=state.D_V | {v},
        claimed=state.claimed,
        D_E=state.D_E,
        w=state.w,
        S=state.S,
    )


def breaker_del_edge(state: State, e_idx: int) -> State:
    return State(
        C=state.C,
        D_V=state.D_V,
        claimed=state.claimed,
        D_E=state.D_E | {e_idx},
        w=state.w,
        S=state.S,
    )


def breaker_moves(state: State, edges, k: int) -> list[tuple[str, int, State]]:
    moves = []
    live = live_edges(state, edges)
    if not live:
        return moves
    # vertex deletions: any small prime not in C and not in D_V that's incident to a live edge
    cand_v = set()
    for ei in live:
        a, c = edges[ei]
        if a not in state.C and a not in state.D_V:
            cand_v.add(a)
        if c not in state.C and c not in state.D_V:
            cand_v.add(c)
    for v in sorted(cand_v):
        moves.append(("del_v", v, breaker_del_vertex(state, v)))
    # edge deletions
    for ei in live:
        moves.append(("del_e", ei, breaker_del_edge(state, ei)))
    return moves


def maker_moves(state: State, edges) -> list[tuple[str, int, State]]:
    return [("claim", ei, maker_claim(state, ei, edges)) for ei in live_edges(state, edges)]


def is_terminal(state: State, edges) -> bool:
    return not any(is_live(state, i, edges) for i in range(len(edges)))


def raw_rse(state: State, edges, k: int) -> tuple[bool, dict]:
    Q0 = Q(state, edges)
    for action, ei, after_m in maker_moves(state, edges):
        ok = True
        worst_loss = 0.0
        worst_breaker = None
        for b_act, b_target, after_b in breaker_moves(after_m, edges, k):
            Q1 = Q(after_b, edges)
            loss = Q0 - Q1
            if loss > 1e-12:
                ok = False
                if loss > worst_loss:
                    worst_loss = loss
                    worst_breaker = (b_act, b_target)
                break
        if ok:
            return True, {"maker": (action, ei)}
    # diagnostic: find the move with smallest worst loss
    best_action = None
    best_worst = None
    best_b = None
    for action, ei, after_m in maker_moves(state, edges):
        worst = 0.0
        worst_b = None
        for b_act, b_target, after_b in breaker_moves(after_m, edges, k):
            v = Q0 - Q(after_b, edges)
            if v > worst:
                worst = v
                worst_b = (b_act, b_target)
        if best_worst is None or worst < best_worst:
            best_worst = worst
            best_action = (action, ei)
            best_b = worst_b
    return False, {"best_maker": best_action, "best_worst_breaker": best_b, "loss": best_worst}


def enumerate_states(k: int, w_init: tuple, max_states: int):
    edges = edges_for_k(k)
    initial = State(
        C=frozenset(),
        D_V=frozenset(),
        claimed=frozenset(),
        D_E=frozenset(),
        w=w_init,
        S=0,
    )
    visited = {initial}
    frontier = [initial]
    order = [initial]
    while frontier:
        if len(visited) > max_states:
            print(f"[warning] hit max_states={max_states}; stopping enumeration")
            break
        state = frontier.pop()
        if is_terminal(state, edges):
            continue
        for m_act, m_ei, after_m in maker_moves(state, edges):
            br = breaker_moves(after_m, edges, k)
            if not br:
                # Maker move ends the round; treat as terminal
                if after_m not in visited:
                    visited.add(after_m)
                    frontier.append(after_m)
                    order.append(after_m)
                continue
            for b_act, b_tg, after_b in br:
                if after_b not in visited:
                    visited.add(after_b)
                    frontier.append(after_b)
                    order.append(after_b)
    return visited, order, edges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=4, help="number of small primes")
    ap.add_argument("--w", type=int, default=1, help="initial token weight per edge")
    ap.add_argument("--max-states", type=int, default=2_000_000)
    args = ap.parse_args()
    k = args.k
    edges = edges_for_k(k)
    w_init = tuple([args.w] * len(edges))
    print(f"=== Activation rank-2 RSE check ===")
    print(f"k = {k} small primes, |E| = {len(edges)}, initial weight w = {args.w} per edge.")

    t0 = time.time()
    visited, order, _ = enumerate_states(k, w_init, args.max_states)
    t_enum = time.time() - t0
    print(f"Enumerated {len(visited)} states in {t_enum:.2f}s.")

    n_nonterminal = 0
    n_ok = 0
    violations = []
    for s in order:
        if is_terminal(s, edges):
            continue
        live = live_edges(s, edges)
        if not any(phi(s, ei, edges) > 0 for ei in live):
            continue
        n_nonterminal += 1
        ok, witness = raw_rse(s, edges, k)
        if ok:
            n_ok += 1
        else:
            violations.append((s, witness))

    t_check = time.time() - t0 - t_enum
    print(f"Non-terminal pre-Maker states: {n_nonterminal}")
    print(f"Raw RSE holds: {n_ok} / {n_nonterminal}  ({100*n_ok/max(n_nonterminal,1):.2f}%)")
    print(f"Check time: {t_check:.2f}s.")

    if violations:
        print(f"\n=== {len(violations)} RSE VIOLATIONS ===")
        for s, w in violations[:5]:
            print(f"\nState: C={sorted(s.C)} D_V={sorted(s.D_V)} claimed={sorted(s.claimed)} D_E={sorted(s.D_E)} S={s.S}")
            print(f"  w = {s.w}")
            print(f"  live edges: {[(ei, edges[ei], phi(s, ei, edges)) for ei in live_edges(s, edges)]}")
            print(f"  Q = {Q(s, edges):.3f}")
            print(f"  Best Maker move: {w['best_maker']}; Breaker reply: {w['best_worst_breaker']}; loss: {w['loss']:.3f}")
    else:
        print("\nNo RSE violations. RSE holds on all reachable activation states.")


if __name__ == "__main__":
    main()
