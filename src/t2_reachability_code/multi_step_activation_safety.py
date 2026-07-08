#!/usr/bin/env python3
"""
Multi-step activation safety search for the concrete K5 q-fiber witness.

Instance:
  n = 10^20, delta = 1/8, Y = floor(n^delta) = 316
  P_Y = odd primes <= Y
  K5 primes = {101, 103, 107, 109, 113}
  q = 4806305873305829

Rule checked:
  Proposition A.6 activation graph safety.  A Maker move is certified safe at
  the current state only if, after Maker claims the chosen live edge, every
  modeled Breaker reply leaves Q nondecreasing.  Modeled replies are deletion
  of an uncaptured live small-prime vertex, or deletion of one currently live
  pair edge.

Important limitation:
  The main search is a Maker-only certificate path.  It checks whether there is
  a sequence of safe Maker activations if no particular Breaker deletion is
  committed to the next state.  This attacks the narrow ordering gap, namely
  whether pre-capturing small primes can make the K5 edges safely activatable.
  It is not a proof of an adversarial strategy tree.

Rigorous bounds:
  The same Rosser-Schoenfeld style interval bounds as full_activation_safety.py
  are used.  Safe means lower_bound(Maker gain) >= upper_bound(max Breaker loss).
  Unsafe means upper_bound(Maker gain) < lower_bound(max Breaker loss).
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import heapq
import math
import time
from typing import Iterable


N = 10**20
Y = int(N ** (1 / 8))
K5 = (101, 103, 107, 109, 113)
Q_WITNESS = 4806305873305829
RS_C = 1.25506
TIME_BUDGET_SECONDS = 300.0


def odd_primes_upto(y: int) -> list[int]:
    out: list[int] = []
    for m in range(3, y + 1, 2):
        ok = True
        r = int(m**0.5)
        for p in range(3, r + 1, 2):
            if m % p == 0:
                ok = False
                break
        if ok:
            out.append(m)
    return out


P_Y = tuple(odd_primes_upto(Y))
PRIME_TO_INDEX = {p: i for i, p in enumerate(P_Y)}
EDGES = tuple(combinations(P_Y, 2))
EDGE_TO_INDEX = {e: i for i, e in enumerate(EDGES)}
K5_EDGE_SET = {tuple(sorted(e)) for e in combinations(K5, 2)}
K5_EDGE_INDICES = frozenset(EDGE_TO_INDEX[e] for e in K5_EDGE_SET)


def upper_w(a: int, c: int, n: int = N) -> float:
    x = n / (a * c)
    return RS_C * x / math.log(x)


def lower_w(a: int, c: int, n: int = N) -> float:
    x = n / (a * c)
    return x / math.log(x) - RS_C * (x / 2) / math.log(x / 2)


LOWER_W = tuple(lower_w(a, c) for a, c in EDGES)
UPPER_W = tuple(upper_w(a, c) for a, c in EDGES)
MID_W = tuple((lo + hi) / 2.0 for lo, hi in zip(LOWER_W, UPPER_W))


def deterministic_miller_rabin(n: int) -> bool:
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in [2, 3, 5, 7, 11, 13, 17]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def verify_q_membership() -> bool:
    if not deterministic_miller_rabin(Q_WITNESS):
        return False
    for a, c in combinations(K5, 2):
        if not (N / (2 * a * c) < Q_WITNESS <= N / (a * c)):
            return False
    return True


@dataclass(frozen=True)
class State:
    captured: frozenset[int]
    claimed: frozenset[int]
    deleted_vertices: frozenset[int]
    deleted_edges: frozenset[int]


@dataclass(frozen=True)
class MoveSafety:
    edge_index: int
    edge: tuple[int, int]
    maker_gain_lower: float
    maker_gain_upper: float
    maker_gain_mid: float
    max_breaker_loss_lower: float
    max_breaker_loss_upper: float
    max_breaker_loss_mid: float
    worst_breaker_lower: tuple[str, int | tuple[int, int]] | None
    worst_breaker_upper: tuple[str, int | tuple[int, int]] | None
    worst_breaker_mid: tuple[str, int | tuple[int, int]] | None

    @property
    def certified_safe(self) -> bool:
        return self.maker_gain_lower + 1e-9 >= self.max_breaker_loss_upper

    @property
    def certified_unsafe(self) -> bool:
        return self.maker_gain_upper + 1e-9 < self.max_breaker_loss_lower

    @property
    def mid_safe(self) -> bool:
        return self.maker_gain_mid + 1e-9 >= self.max_breaker_loss_mid

    @property
    def safe_margin(self) -> float:
        return self.maker_gain_lower - self.max_breaker_loss_upper

    @property
    def mid_margin(self) -> float:
        return self.maker_gain_mid - self.max_breaker_loss_mid


def edge_key(edge: tuple[int, int]) -> tuple[int, int]:
    return tuple(sorted(edge))


def edge_index(a: int, c: int) -> int:
    return EDGE_TO_INDEX[edge_key((a, c))]


def is_live(state: State, ei: int) -> bool:
    if ei in state.claimed or ei in state.deleted_edges:
        return False
    a, c = EDGES[ei]
    if a in state.deleted_vertices or c in state.deleted_vertices:
        return False
    return True


def live_edges(state: State) -> list[int]:
    return [ei for ei in range(len(EDGES)) if is_live(state, ei)]


def coeff_for_unclaimed(state: State, ei: int) -> float:
    a, c = EDGES[ei]
    n_cap = int(a in state.captured) + int(c in state.captured)
    return (1.0 / 8.0, 1.0 / 4.0, 1.0 / 2.0)[n_cap]


def phi_bound(state: State, ei: int, weights: tuple[float, ...]) -> float:
    if ei in state.deleted_edges:
        return 0.0
    if ei in state.claimed:
        return weights[ei]
    if not is_live(state, ei):
        return 0.0
    return coeff_for_unclaimed(state, ei) * weights[ei]


def maker_gain_bound(state: State, ei: int, weights: tuple[float, ...]) -> float:
    a, c = EDGES[ei]
    if not is_live(state, ei):
        return float("-inf")
    before_captured = state.captured
    newly_captured = {v for v in (a, c) if v not in before_captured}
    gain = (1.0 - coeff_for_unclaimed(state, ei)) * weights[ei]
    for ej in live_edges(state):
        if ej == ei:
            continue
        x, y = EDGES[ej]
        inc = 0.0
        if x in newly_captured or y in newly_captured:
            old_n = int(x in before_captured) + int(y in before_captured)
            new_n = int(x in (before_captured | newly_captured)) + int(y in (before_captured | newly_captured))
            old_coeff = (1.0 / 8.0, 1.0 / 4.0, 1.0 / 2.0)[old_n]
            new_coeff = (1.0 / 8.0, 1.0 / 4.0, 1.0 / 2.0)[new_n]
            inc = new_coeff - old_coeff
        gain += inc * weights[ej]
    return gain


def after_maker(state: State, ei: int) -> State:
    a, c = EDGES[ei]
    return State(
        captured=state.captured | {a, c},
        claimed=state.claimed | {ei},
        deleted_vertices=state.deleted_vertices,
        deleted_edges=state.deleted_edges,
    )


def max_breaker_loss_bound(after: State, weights: tuple[float, ...]) -> tuple[float, tuple[str, int | tuple[int, int]] | None]:
    best = 0.0
    best_reply: tuple[str, int | tuple[int, int]] | None = None
    live = live_edges(after)
    if not live:
        return 0.0, None

    incident_live: dict[int, list[int]] = {}
    for ei in live:
        a, c = EDGES[ei]
        incident_live.setdefault(a, []).append(ei)
        incident_live.setdefault(c, []).append(ei)

    for v, inc_edges in incident_live.items():
        if v in after.captured or v in after.deleted_vertices:
            continue
        loss = sum(phi_bound(after, ei, weights) for ei in inc_edges)
        if loss > best:
            best = loss
            best_reply = ("del_v", v)

    for ei in live:
        loss = phi_bound(after, ei, weights)
        if loss > best:
            best = loss
            best_reply = ("del_e", EDGES[ei])
    return best, best_reply


def move_safety(state: State, ei: int) -> MoveSafety:
    after = after_maker(state, ei)
    gain_lo = maker_gain_bound(state, ei, LOWER_W)
    gain_hi = maker_gain_bound(state, ei, UPPER_W)
    gain_mid = maker_gain_bound(state, ei, MID_W)
    loss_lo, reply_lo = max_breaker_loss_bound(after, LOWER_W)
    loss_hi, reply_hi = max_breaker_loss_bound(after, UPPER_W)
    loss_mid, reply_mid = max_breaker_loss_bound(after, MID_W)
    return MoveSafety(
        edge_index=ei,
        edge=EDGES[ei],
        maker_gain_lower=gain_lo,
        maker_gain_upper=gain_hi,
        maker_gain_mid=gain_mid,
        max_breaker_loss_lower=loss_lo,
        max_breaker_loss_upper=loss_hi,
        max_breaker_loss_mid=loss_mid,
        worst_breaker_lower=reply_lo,
        worst_breaker_upper=reply_hi,
        worst_breaker_mid=reply_mid,
    )


def safe_moves(state: State, certified: bool = True) -> list[MoveSafety]:
    out = []
    for ei in live_edges(state):
        ms = move_safety(state, ei)
        if ms.certified_safe if certified else ms.mid_safe:
            out.append(ms)
    return out


def best_unsafe_diagnostic(state: State) -> MoveSafety | None:
    best = None
    for ei in live_edges(state):
        ms = move_safety(state, ei)
        if best is None or ms.mid_margin > best.mid_margin:
            best = ms
    return best


def all_k5_edges_certified_safe_now(state: State) -> bool:
    for ei in K5_EDGE_INDICES:
        if ei in state.claimed:
            continue
        if not is_live(state, ei):
            return False
        if not move_safety(state, ei).certified_safe:
            return False
    return True


def rank_move(state: State, ms: MoveSafety) -> tuple:
    a, c = ms.edge
    k5_claimed_after = len((state.claimed | {ms.edge_index}) & K5_EDGE_INDICES)
    captures_new_k5 = int(a in K5 and a not in state.captured) + int(c in K5 and c not in state.captured)
    captures_new = int(a not in state.captured) + int(c not in state.captured)
    smallest_new = min([v for v in (a, c) if v not in state.captured], default=10**9)
    product = a * c
    k5_edge = int(ms.edge_index in K5_EDGE_INDICES)
    return (
        -k5_claimed_after,
        -captures_new_k5,
        -captures_new,
        smallest_new,
        -ms.safe_margin,
        -k5_edge,
        product,
    )


def greedy_certified_path(time_budget: float) -> tuple[list[MoveSafety], State, str, int]:
    t0 = time.time()
    state = State(frozenset(), frozenset(), frozenset(), frozenset())
    path: list[MoveSafety] = []
    safe_all_at = None
    while time.time() - t0 < time_budget:
        if K5_EDGE_INDICES <= state.claimed:
            return path, state, "POS", safe_all_at if safe_all_at is not None else len(path)
        if safe_all_at is None and all_k5_edges_certified_safe_now(state):
            safe_all_at = len(path)
        moves = safe_moves(state, certified=True)
        if not moves:
            return path, state, "STOP_NO_CERTIFIED_SAFE_MOVE", safe_all_at if safe_all_at is not None else -1
        k5_live_safe = [m for m in moves if m.edge_index in K5_EDGE_INDICES]
        if k5_live_safe and safe_all_at is not None:
            choice = sorted(k5_live_safe, key=lambda m: (m.edge[0] * m.edge[1], -m.safe_margin))[0]
        else:
            choice = sorted(moves, key=lambda m: rank_move(state, m))[0]
        path.append(choice)
        state = after_maker(state, choice.edge_index)
    return path, state, "TIMEOUT", safe_all_at if safe_all_at is not None else -1


def priority_search(time_budget: float, max_expansions: int = 20000) -> tuple[list[MoveSafety], State, str, int, int]:
    """Best-first Maker-only search using certified safe moves only."""
    t0 = time.time()
    initial = State(frozenset(), frozenset(), frozenset(), frozenset())
    heap: list[tuple[tuple, int, State, list[MoveSafety], int]] = []
    counter = 0

    def state_priority(state: State, depth: int, safe_all_at: int) -> tuple:
        unclaimed_k5 = len(K5_EDGE_INDICES - state.claimed)
        uncaptured_k5 = len([p for p in K5 if p not in state.captured])
        uncaptured_small = len([p for p in P_Y if p not in state.captured])
        return (unclaimed_k5, uncaptured_k5, uncaptured_small, depth, safe_all_at if safe_all_at >= 0 else 10**9)

    heapq.heappush(heap, (state_priority(initial, 0, -1), counter, initial, [], -1))
    seen: set[tuple[frozenset[int], frozenset[int]]] = {(initial.captured, initial.claimed)}
    expansions = 0
    while heap and time.time() - t0 < time_budget and expansions < max_expansions:
        _, _, state, path, safe_all_at = heapq.heappop(heap)
        expansions += 1
        if K5_EDGE_INDICES <= state.claimed:
            return path, state, "POS", safe_all_at, expansions
        now_safe_all = safe_all_at
        if now_safe_all < 0 and all_k5_edges_certified_safe_now(state):
            now_safe_all = len(path)
        moves = safe_moves(state, certified=True)
        if not moves:
            continue
        moves = sorted(moves, key=lambda m: rank_move(state, m))[:80]
        for ms in moves:
            new_state = after_maker(state, ms.edge_index)
            key = (new_state.captured, new_state.claimed)
            if key in seen:
                continue
            seen.add(key)
            new_path = path + [ms]
            counter += 1
            heapq.heappush(heap, (state_priority(new_state, len(new_path), now_safe_all), counter, new_state, new_path, now_safe_all))
    if heap:
        _, _, state, path, safe_all_at = heap[0]
        return path, state, "NEG_NO_POS_WITHIN_BUDGET", safe_all_at, expansions
    return [], initial, "NEG_FRONTIER_EXHAUSTED", -1, expansions


def describe_move(ms: MoveSafety) -> str:
    tag = "K5" if ms.edge_index in K5_EDGE_INDICES else "--"
    return (
        f"{ms.edge} {tag} "
        f"gain_lo={ms.maker_gain_lower:.6e} "
        f"loss_hi={ms.max_breaker_loss_upper:.6e} "
        f"margin={ms.safe_margin:.6e} "
        f"worst_hi={ms.worst_breaker_upper}"
    )


def print_initial_diagnostics() -> None:
    initial = State(frozenset(), frozenset(), frozenset(), frozenset())
    moves = [move_safety(initial, ei) for ei in live_edges(initial)]
    n_cert_safe = sum(1 for m in moves if m.certified_safe)
    n_cert_unsafe = sum(1 for m in moves if m.certified_unsafe)
    n_mid_safe = sum(1 for m in moves if m.mid_safe)
    print("Initial-state diagnostics:")
    print(f"  live_edges={len(moves)}")
    print(f"  certified_safe_moves={n_cert_safe}")
    print(f"  certified_unsafe_moves={n_cert_unsafe}")
    print(f"  mid_estimate_safe_moves={n_mid_safe}")
    print("  top certified safe initial moves:")
    for ms in sorted([m for m in moves if m.certified_safe], key=lambda m: rank_move(initial, m))[:10]:
        print(f"    {describe_move(ms)}")
    print("  K5 initial moves:")
    for ei in sorted(K5_EDGE_INDICES, key=lambda i: EDGES[i]):
        print(f"    {describe_move(move_safety(initial, ei))}")


def adversarial_reply_warning(path: list[MoveSafety]) -> None:
    """Report the first path move where a legal modeled reply can delete a K5 vertex or edge."""
    state = State(frozenset(), frozenset(), frozenset(), frozenset())
    for step, ms in enumerate(path, 1):
        after = after_maker(state, ms.edge_index)
        live = live_edges(after)
        deletable_vertices = set()
        for ei in live:
            a, c = EDGES[ei]
            if a not in after.captured and a not in after.deleted_vertices:
                deletable_vertices.add(a)
            if c not in after.captured and c not in after.deleted_vertices:
                deletable_vertices.add(c)
        vulnerable_k5_vertices = sorted(set(K5) & deletable_vertices)
        vulnerable_k5_edges = sorted([EDGES[ei] for ei in live if ei in K5_EDGE_INDICES])
        if vulnerable_k5_vertices or vulnerable_k5_edges:
            print("Adversarial continuation warning:")
            print(f"  first_path_step={step}")
            print(f"  maker_move={ms.edge}")
            print(f"  deletable_k5_vertices_after_move={vulnerable_k5_vertices[:10]}")
            print(f"  deletable_live_k5_edges_after_move={vulnerable_k5_edges[:10]}")
            print("  This Maker-only sequence is not an adversarial strategy tree certificate.")
            return
        state = after
    print("Adversarial continuation warning: no vulnerable K5 vertex or edge was detected along the printed path.")


def main() -> int:
    print("=== Multi-step activation safety search for the concrete K5 witness ===")
    print(f"n={N}")
    print("delta=1/8")
    print(f"Y_floor={Y}")
    print(f"|P_Y|={len(P_Y)} odd primes")
    print(f"P_Y first/last={P_Y[:8]} ... {P_Y[-8:]}")
    print(f"pair_graph_edges={len(EDGES)}")
    print(f"K5={K5}")
    print(f"q={Q_WITNESS}")
    print(f"q_membership_all_10={verify_q_membership()}")
    print(f"min_lower_weight_bound={min(LOWER_W):.6e}")
    print(f"max_upper_weight_bound={max(UPPER_W):.6e}")
    print()

    print_initial_diagnostics()
    print()

    t0 = time.time()
    greedy_path, greedy_state, greedy_status, greedy_safe_all_at = greedy_certified_path(30.0)
    print("Greedy certified Maker-only path:")
    print(f"  status={greedy_status}")
    print(f"  steps={len(greedy_path)}")
    print(f"  captured_vertices={len(greedy_state.captured)}")
    print(f"  claimed_edges={len(greedy_state.claimed)}")
    print(f"  claimed_k5_edges={len(greedy_state.claimed & K5_EDGE_INDICES)} / 10")
    print(f"  all_k5_certified_safe_at_step={greedy_safe_all_at}")
    print("  first_25_moves:")
    for i, ms in enumerate(greedy_path[:25], 1):
        print(f"    {i:03d}: {describe_move(ms)}")
    if len(greedy_path) > 25:
        print("  last_20_moves:")
        for i, ms in enumerate(greedy_path[-20:], len(greedy_path) - 19):
            print(f"    {i:03d}: {describe_move(ms)}")
    adversarial_reply_warning(greedy_path)
    print()

    remaining_budget = max(0.0, TIME_BUDGET_SECONDS - (time.time() - t0))
    search_budget = min(remaining_budget, 240.0)
    path, state, status, safe_all_at, expansions = priority_search(search_budget)
    elapsed = time.time() - t0
    print("Best-first certified Maker-only search:")
    print(f"  status={status}")
    print(f"  wall_clock_seconds={elapsed:.2f}")
    print(f"  expansions={expansions}")
    print(f"  steps={len(path)}")
    print(f"  captured_vertices={len(state.captured)}")
    print(f"  claimed_edges={len(state.claimed)}")
    print(f"  claimed_k5_edges={len(state.claimed & K5_EDGE_INDICES)} / 10")
    print(f"  all_k5_certified_safe_at_step={safe_all_at}")
    print("  sequence:")
    for i, ms in enumerate(path, 1):
        mark = "*" if ms.edge_index in K5_EDGE_INDICES else " "
        print(f"    {i:03d}{mark} {describe_move(ms)}")
    if status == "POS":
        print("POS: found a certified safe Maker-only activation sequence ending with all ten K5 pair edges claimed.")
    else:
        diag = best_unsafe_diagnostic(state)
        print("NEG: no POS sequence found within the configured budget and pruning limits.")
        if diag:
            print(f"  best_current_diagnostic={describe_move(diag)}")
    print()
    print("Limitations:")
    print("  This is a bounded heuristic search, not an exhaustive proof of exclusion.")
    print("  A POS path here is a safe ordering certificate for the Maker-only state path, not a full adversarial strategy tree.")
    print("  A NEG result here means no counterexample was found within budget, not that none exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
