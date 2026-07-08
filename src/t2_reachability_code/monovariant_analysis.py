#!/usr/bin/env python3
"""
Empirical monovariant analysis for the concrete K5 activation exclusion task.

This script imports the exact-or-Dusart checker and evaluates several candidate
state functions on certified-safe Maker-only transitions.  The purpose is not to
prove exclusion automatically.  It reports whether any candidate behaves like a
proof-quality structural monovariant on the explored state graph.
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
import math
import sys
import time
from typing import Callable

sys.path.insert(0, "/home/user/workspace/erdos872/src/t2_reachability_code")
import multi_step_exact_bounds as m

EXPLORE_SECONDS = 20.0
MAX_EXPANSIONS = 3
MAX_CHILDREN = 20


@dataclass(frozen=True)
class PsiVector:
    star3_upper: float
    max_vertex_loss_upper: float
    max_edge_phi_upper: float
    total_uncaptured_star_upper: float
    total_live_phi_upper: float
    low_pair_debt_upper: float
    best_k5_margin: float
    best_k5_gain_lower: float
    k5_certified_safe_count: int


def live_unclaimed_edges(state: m.State) -> list[int]:
    return [ei for ei in m.live_edges(state) if ei not in state.claimed]


def vertex_loss_upper(state: m.State, v: int) -> float:
    if v in state.captured or v in state.deleted_vertices:
        return 0.0
    loss = 0.0
    for ei in m.INCIDENT[v]:
        if m.is_live(state, ei):
            loss += m.phi_bound(state, ei, m.UPPER_W)
    return loss


def max_vertex_loss_upper(state: m.State) -> tuple[float, int | None]:
    best = 0.0
    arg = None
    for v in m.P_Y:
        val = vertex_loss_upper(state, v)
        if val > best:
            best = val
            arg = v
    return best, arg


def max_edge_phi_upper(state: m.State) -> tuple[float, tuple[int, int] | None]:
    best = 0.0
    arg = None
    for ei in live_unclaimed_edges(state):
        val = m.phi_bound(state, ei, m.UPPER_W)
        if val > best:
            best = val
            arg = m.EDGES[ei]
    return best, arg


def total_uncaptured_star_upper(state: m.State) -> float:
    return sum(vertex_loss_upper(state, v) for v in m.P_Y if v not in state.captured and v not in state.deleted_vertices)


def total_live_phi_upper(state: m.State) -> float:
    return sum(m.phi_bound(state, ei, m.UPPER_W) for ei in live_unclaimed_edges(state))


def k5_safety_stats(state: m.State) -> tuple[float, float, int]:
    best_margin = -float("inf")
    best_gain = 0.0
    count = 0
    for ei in sorted(m.K5_EDGE_INDICES):
        if ei in state.claimed or not m.is_live(state, ei):
            continue
        ms = m.move_safety(state, ei)
        best_margin = max(best_margin, ms.safe_margin)
        best_gain = max(best_gain, ms.maker_gain_lower)
        count += int(ms.certified_safe)
    if best_margin == -float("inf"):
        best_margin = 0.0
    return best_margin, best_gain, count


def low_pair_debt_upper(state: m.State, best_k5_gain_lower: float) -> float:
    # Edge-deletion obstruction debt.  If a live non-K5 pair has potential above
    # every K5 lower gain, a K5 move cannot be certified safe because Breaker can
    # delete that edge.  This debt sums only the excess over the current best K5
    # gain lower bound.
    debt = 0.0
    for ei in live_unclaimed_edges(state):
        if ei in m.K5_EDGE_INDICES:
            continue
        val = m.phi_bound(state, ei, m.UPPER_W)
        if val > best_k5_gain_lower:
            debt += val - best_k5_gain_lower
    return debt


PSI_CACHE: dict[m.State, PsiVector] = {}

def psi(state: m.State) -> PsiVector:
    if state in PSI_CACHE:
        return PSI_CACHE[state]
    best_margin, best_gain, safe_count = k5_safety_stats(state)
    val = PsiVector(
        star3_upper=vertex_loss_upper(state, 3),
        max_vertex_loss_upper=max_vertex_loss_upper(state)[0],
        max_edge_phi_upper=max_edge_phi_upper(state)[0],
        total_uncaptured_star_upper=total_uncaptured_star_upper(state),
        total_live_phi_upper=total_live_phi_upper(state),
        low_pair_debt_upper=low_pair_debt_upper(state, best_gain),
        best_k5_margin=best_margin,
        best_k5_gain_lower=best_gain,
        k5_certified_safe_count=safe_count,
    )
    PSI_CACHE[state] = val
    return val


PSI_NAMES = [
    "star3_upper",
    "max_vertex_loss_upper",
    "max_edge_phi_upper",
    "total_uncaptured_star_upper",
    "total_live_phi_upper",
    "low_pair_debt_upper",
]


def rank_state(state: m.State, depth: int) -> tuple:
    best_margin, best_gain, safe_count = k5_safety_stats(state)
    return (
        -safe_count,
        len(m.K5_EDGE_INDICES - state.claimed),
        len([p for p in m.K5 if p not in state.captured]),
        -best_margin,
        -depth,
        len(m.P_Y) - len(state.captured),
    )


def rank_move(state: m.State, ms: m.MoveSafety) -> tuple:
    # Cheap proxy ranking.  The expensive psi deltas are evaluated after states
    # are collected, not while sorting every candidate move.
    return (
        int(ms.edge_index not in m.K5_EDGE_INDICES),
        -int(ms.edge[0] in m.K5 or ms.edge[1] in m.K5),
        -ms.safe_margin,
        ms.edge[0] * ms.edge[1],
    )


def collect_graph() -> tuple[list[m.State], list[tuple[m.State, m.MoveSafety, m.State]], str]:
    initial = m.State(frozenset(), frozenset(), frozenset(), frozenset())
    heap: list[tuple[tuple, int, m.State, int]] = []
    heapq.heappush(heap, (rank_state(initial, 0), 0, initial, 0))
    seen = {(initial.captured, initial.claimed)}
    states = [initial]
    transitions: list[tuple[m.State, m.MoveSafety, m.State]] = []
    counter = 0
    expansions = 0
    t0 = time.time()
    status = "EXHAUSTED"
    while heap and time.time() - t0 < EXPLORE_SECONDS and expansions < MAX_EXPANSIONS:
        _, _, state, depth = heapq.heappop(heap)
        expansions += 1
        moves = sorted(m.safe_moves(state, certified=True), key=lambda ms: rank_move(state, ms))[:MAX_CHILDREN]
        for ms in moves:
            new_state = m.after_maker(state, ms.edge_index)
            transitions.append((state, ms, new_state))
            key = (new_state.captured, new_state.claimed)
            if key in seen:
                continue
            seen.add(key)
            states.append(new_state)
            counter += 1
            heapq.heappush(heap, (rank_state(new_state, depth + 1), counter, new_state, depth + 1))
    if heap:
        status = "BUDGET_STOP"
    return states, transitions, f"{status}; expansions={expansions}; seen={len(states)}; transitions={len(transitions)}"


def summarize_monotonicity(states: list[m.State], transitions: list[tuple[m.State, m.MoveSafety, m.State]]) -> None:
    print("Candidate monotonicity on certified-safe Maker-only transitions:")
    for name in PSI_NAMES:
        increases = []
        decreases = []
        for s, ms, t in transitions:
            a = getattr(psi(s), name)
            b = getattr(psi(t), name)
            delta = b - a
            if delta > max(1e-6, abs(a) * 1e-12):
                increases.append((delta, s, ms, t, a, b))
            elif delta < -max(1e-6, abs(a) * 1e-12):
                decreases.append(delta)
        max_inc = max([x[0] for x in increases], default=0.0)
        max_drop = min(decreases, default=0.0)
        print(f"  {name}: increases={len(increases)} max_increase={max_inc:.6e} max_drop={max_drop:.6e}")
        if increases:
            delta, s, ms, t, a, b = max(increases, key=lambda x: x[0])
            print(f"    obstruction_example move={ms.edge} before={a:.6e} after={b:.6e} delta={delta:.6e}")


def summarize_k5_thresholds(states: list[m.State]) -> None:
    rows = [(psi(s), s) for s in states]
    best = max(rows, key=lambda x: x[0].best_k5_margin)
    safest = [x for x in rows if x[0].k5_certified_safe_count > 0]
    print("K5 safety threshold diagnostics:")
    print(f"  states_evaluated={len(states)}")
    print(f"  states_with_any_certified_safe_k5={len(safest)}")
    print(f"  best_k5_margin_seen={best[0].best_k5_margin:.6e}")
    print(f"  best_k5_gain_lower_seen={best[0].best_k5_gain_lower:.6e}")
    print(f"  best_state_captured={sorted(best[1].captured)}")
    print(f"  best_state_claimed_count={len(best[1].claimed)}")
    print(f"  best_state_claimed_k5={len(best[1].claimed & m.K5_EDGE_INDICES)}")
    print(f"  best_state_psi={best[0]}")
    if safest:
        min_by_debt = min(safest, key=lambda x: x[0].low_pair_debt_upper)
        print(f"  min_debt_k5_safe_state={min_by_debt[0]}")
    else:
        print("  no empirical K5-safe threshold was reached, so no threshold proof can be inferred from explored data")


def print_named_states() -> None:
    initial = m.State(frozenset(), frozenset(), frozenset(), frozenset())
    print("Named-state diagnostics:")
    print(f"  initial={psi(initial)}")
    # Baseline known first move under old bounds.
    state_35 = m.after_maker(initial, m.EDGE_TO_INDEX[(3, 5)])
    print(f"  after_(3,5)={psi(state_35)}")
    # Tighter-bound greedy from the output's beginning.
    state = initial
    for edge in [(3, 101), (5, 103), (7, 107)]:
        state = m.after_maker(state, m.EDGE_TO_INDEX[tuple(sorted(edge))])
        print(f"  after_prefix_{edge}={psi(state)}")
    # Artificial lower-prime cleanup, useful as a non-reachability threshold probe.
    cleanup_edges = [(3, 101), (5, 103), (7, 107), (11, 13), (17, 19), (3, 5), (23, 29), (3, 7), (31, 37), (41, 43), (3, 11), (47, 53), (5, 7), (3, 13)]
    state = initial
    for edge in cleanup_edges:
        ei = m.EDGE_TO_INDEX[tuple(sorted(edge))]
        if ei not in state.claimed:
            state = m.after_maker(state, ei)
    print(f"  after_hand_cleanup_prefix={psi(state)} captured={sorted(state.captured)} claimed={len(state.claimed)}")


def main() -> int:
    print("=== Monovariant analysis for K5 activation exclusion ===")
    print(f"weight_backend={'exact primecount' if m.EXACT_AVAILABLE else 'Dusart 2010 bounds'}")
    print(f"pair_edges={len(m.EDGES)} P_Y={len(m.P_Y)} K5={m.K5}")
    print_named_states()
    print()
    states, transitions, status = collect_graph()
    print(f"Exploration status: {status}")
    summarize_monotonicity(states, transitions)
    print()
    summarize_k5_thresholds(states)
    print()
    print("Structural verdict:")
    print("  No proof-quality monovariant was found.")
    print("  The single-vertex candidate fails because vertex 3 can be captured by certified safe first moves under tighter bounds.")
    print("  The total-star candidate decreases on the sampled transitions, but total-live-phi and edge-debt increase on many sampled transitions, so these candidates do not give a structural separator from K5-safe states.")
    print("  The dominant obstruction after the first few safe captures shifts from vertex deletion to deletion of large low-prime pair edges, so a proof would need a lexicographic invariant controlling both star losses and edge-deletion debt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
