"""
v4 one-step Q-safe residual slot strategy for Erdős 872 experiments.

This file deliberately checks the chosen Maker move, not raw_rse existence.
For every reachable pre-Maker state under v4 against all Shortener replies,
strategy_v4 chooses the legal Maker move maximizing the worst full-round
scaled-potential delta

    min_{Shortener reply} Q(after Maker + reply) - Q(before Maker).

If any legal move has nonnegative worst delta, the chosen move is safe in the
sense required by Buddhdev Proposition A.3.  If none exists, the state is
reported as a v4 counterexample.

The code keeps multi_fiber_rse.MultiState for compatibility.  The field
captured_edges is code-internal bookkeeping for Maker-captured/scored edges;
in Buddhdev's manuscript those edges are simply removed from liveness via the
scored/claimed edge set K and the score S.  The potential calculation matches
Q = 8S + sum_{e live} 2^{|e cap C|} w(e) for unit weights.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import sys
import time
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Iterable

sys.path.insert(0, "/home/user/workspace/erdos872")
from multi_fiber_rse import (  # noqa: E402
    MultiState,
    build_edges,
    is_live,
    live_edges,
    phi,
    Q,
    m_capture,
    m_score,
    b_del_v,
    b_del_e,
    b_score_e,
    breaker_moves,
    maker_moves,
    is_terminal,
)


def initial_state() -> MultiState:
    return MultiState(
        C=frozenset(), D_V=frozenset(), D_E=frozenset(),
        K=frozenset(), S=0, captured_edges=frozenset()
    )


def build_buddhdev_k4_edges() -> tuple[list[tuple], list[int]]:
    """Exact Proposition A.2 local fiber: q plus 13q,17q,19q,23q."""
    return build_edges([[13, 17, 19, 23]])


def describe_edges(edges):
    return [tuple(e) for e in edges]


def worst_round_delta(state: MultiState, edges, move) -> tuple[int, tuple | None, MultiState]:
    """Return min Shortener full-round delta for a fixed Maker move."""
    q0 = Q(state, edges)
    _act, _ei, after_m = move
    replies = breaker_moves(after_m, edges)
    if not replies:
        return Q(after_m, edges) - q0, None, after_m
    best_delta = None
    best_reply = None
    best_state = None
    for b_act, b_tg, after_b in replies:
        d = Q(after_b, edges) - q0
        if best_delta is None or d < best_delta:
            best_delta = d
            best_reply = (b_act, b_tg)
            best_state = after_b
    return best_delta, best_reply, best_state


def strategy_v4(state: MultiState, edges):
    """Choose the legal move with maximal worst-case full-round Q delta."""
    best = None
    best_key = None
    for move in maker_moves(state, edges):
        d, reply, _after = worst_round_delta(state, edges, move)
        # deterministic tie-breaks: prefer nonnegative, capture over score, higher maker-immediate Q,
        # then lower edge index.  The primary criterion is worst-case delta.
        action, ei, after_m = move
        action_pref = 1 if action == "capture" else 0
        key = (d, action_pref, Q(after_m, edges), -ei)
        if best_key is None or key > best_key:
            best_key = key
            best = (action, ei, after_m, d, reply)
    return best


def make_strategy_v4_safety(edges):
    """Return a synthesized finite safety strategy for these edges.

    A state is declared winning if either it is terminal, or Maker has a legal
    move with nonnegative immediate worst-case round delta and every Shortener
    reply reaches a winning state.  Since every move adds to C, D_V, D_E, K, or
    captured_edges, the game graph is acyclic under the tuple-size rank.

    This is still a local slot-game strategy: it inspects only the current
    finite slot state and live incidence table.  It is stronger than the greedy
    one-step strategy above because it refuses safe-looking captures that enter
    Buddhdev's K4 two-Phi=8 trap.
    """

    @lru_cache(maxsize=None)
    def solve(state: MultiState):
        if is_terminal(state, edges) or not live_edges(state, edges):
            return True, None
        candidates = []
        for move in maker_moves(state, edges):
            d, reply, _ = worst_round_delta(state, edges, move)
            if d < 0:
                continue
            action, ei, after_m = move
            replies = breaker_moves(after_m, edges)
            next_states = [after_m] if not replies else [after_b for _ba, _bt, after_b in replies]
            ok = True
            for ns in next_states:
                child_ok, _child = solve(ns)
                if not child_ok:
                    ok = False
                    break
            if ok:
                # Prefer larger immediate safety margin, then capture over score,
                # then larger maker-immediate Q.
                candidates.append((d, 1 if action == "capture" else 0, Q(after_m, edges), -ei, move, reply))
        if not candidates:
            return False, None
        candidates.sort(reverse=True)
        d, _ap, _qm, _nei, move, reply = candidates[0]
        action, ei, after_m = move
        return True, (action, ei, after_m, d, reply)

    def strat(state: MultiState, _edges=None):
        ok, move = solve(state)
        if ok and move is not None:
            return move
        # Diagnostic fallback: choose the one-step best move so verification can
        # report the first obstruction.
        return strategy_v4(state, edges)

    strat.solve = solve
    return strat


def dominant_capture_exists(state: MultiState, edges) -> tuple[bool, tuple | None]:
    """Check GPT-5.5 dominant-capture certificate G >= max(E,V)."""
    q0 = Q(state, edges)
    for ei in live_edges(state, edges):
        after = m_capture(state, ei, edges)
        G = Q(after, edges) - q0
        E = max((phi(after, ej, edges) for ej in live_edges(after, edges)), default=0)
        vloss = collections.defaultdict(int)
        for ej in live_edges(after, edges):
            for v in edges[ej]:
                if v not in after.C and v not in after.D_V:
                    vloss[v] += phi(after, ej, edges)
        V = max(vloss.values(), default=0)
        if G >= max(E, V):
            return True, ("capture", ei, G, E, V)
    return False, None


@dataclass
class CheckResult:
    name: str
    n_edges: int
    n_vertices: int
    states_seen: int
    pre_maker_checked: int
    terminal_states: int
    min_chosen_delta: int | None
    max_chosen_delta: int | None
    delta_hist: dict
    no_nonnegative_states: int
    first_bad_state: str | None
    first_bad_move: str | None
    first_bad_reply: str | None
    min_terminal_score: int | None
    max_terminal_score: int | None
    M_over_8: float
    S_fin_ge_M_over_8: bool | None
    exhausted: bool
    cap_hit: bool
    seconds: float


def state_summary(state: MultiState, edges) -> str:
    live = [(i, edges[i], phi(state, i, edges)) for i in live_edges(state, edges)]
    return (
        f"C={sorted(state.C)} D_V={sorted(state.D_V)} D_E={sorted(state.D_E)} "
        f"K={sorted(state.K)} captured_edges={sorted(state.captured_edges)} S={state.S} "
        f"Q={Q(state, edges)} live={live}"
    )


def verify_edges(name: str, edges, max_states: int = 10_000_000, synthesized: bool = True) -> CheckResult:
    t0 = time.time()
    init = initial_state()
    visited = {init}
    queue = collections.deque([init])
    checked = 0
    terminal_scores = []
    min_delta = None
    max_delta = None
    hist = collections.Counter()
    bad_count = 0
    first_bad_state = first_bad_move = first_bad_reply = None
    cap_hit = False

    synth_strategy = make_strategy_v4_safety(tuple(edges)) if synthesized else None

    while queue:
        if len(visited) > max_states:
            cap_hit = True
            break
        s = queue.popleft()
        if is_terminal(s, edges):
            terminal_scores.append(s.S)
            continue
        if not live_edges(s, edges):
            terminal_scores.append(s.S)
            continue
        move = synth_strategy(s) if synthesized else strategy_v4(s, edges)
        if move is None:
            terminal_scores.append(s.S)
            continue
        action, ei, after_m, d, reply = move
        checked += 1
        min_delta = d if min_delta is None else min(min_delta, d)
        max_delta = d if max_delta is None else max(max_delta, d)
        hist[d] += 1
        if d < 0:
            bad_count += 1
            if first_bad_state is None:
                first_bad_state = state_summary(s, edges)
                first_bad_move = repr((action, ei, edges[ei], "worst_delta", d))
                first_bad_reply = repr(reply)
        replies = breaker_moves(after_m, edges)
        next_states = [after_m] if not replies else [after_b for _ba, _bt, after_b in replies]
        for ns in next_states:
            if ns not in visited:
                visited.add(ns)
                queue.append(ns)

    verts = set(v for e in edges for v in e)
    M = len(edges)
    minS = min(terminal_scores) if terminal_scores else None
    maxS = max(terminal_scores) if terminal_scores else None
    return CheckResult(
        name=name,
        n_edges=len(edges),
        n_vertices=len(verts),
        states_seen=len(visited),
        pre_maker_checked=checked,
        terminal_states=len(terminal_scores),
        min_chosen_delta=min_delta,
        max_chosen_delta=max_delta,
        delta_hist=dict(sorted(hist.items())),
        no_nonnegative_states=bad_count,
        first_bad_state=first_bad_state,
        first_bad_move=first_bad_move,
        first_bad_reply=first_bad_reply,
        min_terminal_score=minS,
        max_terminal_score=maxS,
        M_over_8=M / 8.0,
        S_fin_ge_M_over_8=(minS >= M / 8.0) if minS is not None else None,
        exhausted=(not cap_hit and not queue),
        cap_hit=cap_hit,
        seconds=time.time() - t0,
    )


def verify_config(sizes: list[int], max_states: int = 10_000_000, synthesized: bool = True) -> CheckResult:
    fibers = [list(range(1, k + 1)) for k in sizes]
    edges, _ = build_edges(fibers)
    return verify_edges(str(sizes), edges, max_states=max_states, synthesized=synthesized)


def run_required(max_states: int = 10_000_000, synthesized: bool = True):
    required = [[5], [7], [5, 4], [4, 2], [4, 3], [4, 4], [3, 3, 3], [4, 3, 2]]
    results = []
    for cfg in required:
        print(f"=== v4 verify config {cfg} ===", flush=True)
        res = verify_config(cfg, max_states=max_states, synthesized=synthesized)
        results.append(asdict(res))
        print(json.dumps(asdict(res), indent=2, default=str), flush=True)
    print("=== v4 verify Buddhdev Proposition A.2 K4 fiber {13,17,19,23} over common q ===", flush=True)
    edges, _ = build_buddhdev_k4_edges()
    res = verify_edges("Buddhdev_K4_q_13_17_19_23", edges, max_states=max_states, synthesized=synthesized)
    results.append(asdict(res))
    print(json.dumps(asdict(res), indent=2, default=str), flush=True)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default=None, help="comma list like 5,4; omit to run required")
    ap.add_argument("--buddhdev-k4", action="store_true")
    ap.add_argument("--max-states", type=int, default=10_000_000)
    ap.add_argument("--json-out", type=str, default="/home/user/workspace/erdos872/v4_verification_results.json")
    ap.add_argument("--greedy", action="store_true", help="use one-step max-min strategy instead of synthesized safety strategy")
    args = ap.parse_args()
    if args.buddhdev_k4:
        edges, _ = build_buddhdev_k4_edges()
        results = [asdict(verify_edges("Buddhdev_K4_q_13_17_19_23", edges, args.max_states, synthesized=not args.greedy))]
    elif args.config:
        sizes = [int(x) for x in args.config.split(",") if x.strip()]
        results = [asdict(verify_config(sizes, args.max_states, synthesized=not args.greedy))]
    else:
        results = run_required(args.max_states, synthesized=not args.greedy)
    with open(args.json_out, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"saved {args.json_out}")


if __name__ == "__main__":
    main()
