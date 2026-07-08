#!/usr/bin/env python3
"""
Tighter multi-step activation safety search for the concrete K5 q-fiber witness.

This is a drop-in sharpening of multi_step_activation_safety.py.  It keeps the
same activation-game bookkeeping and the same B_{a,c} edge weights, namely

    B_{a,c} = { prime b : n/(2ac) < b <= n/(ac) }.

Exact prime counts are attempted only when a local primecount executable is
available.  If not, the script falls back to Dusart 2010 explicit bounds

    pi(x) > x / (log x - 1)       for x >= 5393,
    pi(x) < x / (log x - 1.1)     for x >= 60184,

which are much tighter than the older Rosser-Schoenfeld bounds used in the
baseline checker.  All interval endpoints in this instance are far above the
thresholds.  The optional exact path is intentionally disabled when no exact
prime-counting backend exists, rather than trying sympy.primepi at 10^20 scale.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import heapq
import math
import shutil
import subprocess
import time
from typing import Iterable

N = 10**20
Y = int(N ** (1 / 8))
K5 = (101, 103, 107, 109, 113)
Q_WITNESS = 4806305873305829
TIME_BUDGET_SECONDS = 570.0
MAX_EXPANSIONS = 200000
MAX_CHILDREN_PER_STATE = 120


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
INCIDENT = {p: [] for p in P_Y}
for i, (a, c) in enumerate(EDGES):
    INCIDENT[a].append(i)
    INCIDENT[c].append(i)


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


def pi_lower_dusart(x: int) -> float:
    if x < 5393:
        raise ValueError(f"Dusart lower threshold violated: {x}")
    lx = math.log(x)
    return x / (lx - 1.0)


def pi_upper_dusart(x: int) -> float:
    if x < 60184:
        raise ValueError(f"Dusart upper threshold violated: {x}")
    lx = math.log(x)
    return x / (lx - 1.1)


PRIMECOUNT_EXE = shutil.which("primecount")
PI_CACHE: dict[int, int] = {}


def primepi_exact(x: int) -> int | None:
    """Return exact pi(x) if a local primecount executable exists."""
    if PRIMECOUNT_EXE is None:
        return None
    if x not in PI_CACHE:
        cp = subprocess.run([PRIMECOUNT_EXE, str(x)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        PI_CACHE[x] = int(cp.stdout.strip().split()[0])
    return PI_CACHE[x]


def interval_endpoints(a: int, c: int, n: int = N) -> tuple[int, int]:
    # Existing checker bookkeeping: n/(2ac) < b <= n/(ac).
    lo = n // (2 * a * c)
    hi = n // (a * c)
    return lo, hi


EXACT_AVAILABLE = PRIMECOUNT_EXE is not None


def interval_bounds(a: int, c: int) -> tuple[float, float, int | None]:
    lo, hi = interval_endpoints(a, c)
    if EXACT_AVAILABLE:
        pi_hi = primepi_exact(hi)
        pi_lo = primepi_exact(lo)
        assert pi_hi is not None and pi_lo is not None
        exact = pi_hi - pi_lo
        return float(exact), float(exact), exact
    lower = pi_lower_dusart(hi) - pi_upper_dusart(lo)
    upper = pi_upper_dusart(hi) - pi_lower_dusart(lo)
    if lower < 0:
        lower = 0.0
    return lower, upper, None


LOWER_W: tuple[float, ...]
UPPER_W: tuple[float, ...]
EXACT_W: tuple[int | None, ...]
_tmp_lower: list[float] = []
_tmp_upper: list[float] = []
_tmp_exact: list[int | None] = []
for a, c in EDGES:
    lo, hi, exact = interval_bounds(a, c)
    _tmp_lower.append(lo)
    _tmp_upper.append(hi)
    _tmp_exact.append(exact)
LOWER_W = tuple(_tmp_lower)
UPPER_W = tuple(_tmp_upper)
MID_W = tuple((lo + hi) / 2.0 for lo, hi in zip(LOWER_W, UPPER_W))
EXACT_W = tuple(_tmp_exact)


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


def is_live(state: State, ei: int) -> bool:
    if ei in state.claimed or ei in state.deleted_edges:
        return False
    a, c = EDGES[ei]
    return a not in state.deleted_vertices and c not in state.deleted_vertices


def live_edges(state: State) -> list[int]:
    return [ei for ei in range(len(EDGES)) if is_live(state, ei)]


def coeff_for_unclaimed(state: State, ei: int) -> float:
    a, c = EDGES[ei]
    n_cap = int(a in state.captured) + int(c in state.captured)
    return (1.0 / 8.0, 1.0 / 4.0, 1.0 / 2.0)[n_cap]


def phi_bound(state: State, ei: int, weights: tuple[float, ...]) -> float:
    if ei in state.deleted_edges or ei in state.claimed:
        return weights[ei] if ei in state.claimed else 0.0
    if not is_live(state, ei):
        return 0.0
    return coeff_for_unclaimed(state, ei) * weights[ei]


def maker_gain_bound(state: State, ei: int, weights: tuple[float, ...]) -> float:
    a, c = EDGES[ei]
    if not is_live(state, ei):
        return float("-inf")
    before_captured = state.captured
    after_captured = before_captured | {a, c}
    newly_captured = {v for v in (a, c) if v not in before_captured}
    gain = (1.0 - coeff_for_unclaimed(state, ei)) * weights[ei]
    touched = set()
    for v in newly_captured:
        touched.update(INCIDENT[v])
    for ej in touched:
        if ej == ei or not is_live(state, ej):
            continue
        x, y = EDGES[ej]
        old_n = int(x in before_captured) + int(y in before_captured)
        new_n = int(x in after_captured) + int(y in after_captured)
        old_coeff = (1.0 / 8.0, 1.0 / 4.0, 1.0 / 2.0)[old_n]
        new_coeff = (1.0 / 8.0, 1.0 / 4.0, 1.0 / 2.0)[new_n]
        gain += (new_coeff - old_coeff) * weights[ej]
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
    for v in P_Y:
        if v in after.captured or v in after.deleted_vertices:
            continue
        loss = 0.0
        for ei in INCIDENT[v]:
            if is_live(after, ei):
                loss += phi_bound(after, ei, weights)
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
    return MoveSafety(ei, EDGES[ei], gain_lo, gain_hi, gain_mid, loss_lo, loss_hi, loss_mid, reply_lo, reply_hi, reply_mid)


def safe_moves(state: State, certified: bool = True) -> list[MoveSafety]:
    out = []
    for ei in live_edges(state):
        ms = move_safety(state, ei)
        if ms.certified_safe if certified else ms.mid_safe:
            out.append(ms)
    return out


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
    return (-k5_claimed_after, -captures_new_k5, -captures_new, smallest_new, -ms.safe_margin, -k5_edge, product)


def describe_move(ms: MoveSafety) -> str:
    tag = "K5" if ms.edge_index in K5_EDGE_INDICES else "--"
    return (
        f"{ms.edge} {tag} "
        f"gain_lo={ms.maker_gain_lower:.6e} "
        f"gain_hi={ms.maker_gain_upper:.6e} "
        f"loss_lo={ms.max_breaker_loss_lower:.6e} "
        f"loss_hi={ms.max_breaker_loss_upper:.6e} "
        f"margin={ms.safe_margin:.6e} "
        f"worst_hi={ms.worst_breaker_upper}"
    )


def best_diagnostic(state: State) -> MoveSafety | None:
    best = None
    for ei in live_edges(state):
        ms = move_safety(state, ei)
        if best is None or ms.safe_margin > best.safe_margin:
            best = ms
    return best


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


def priority_search(time_budget: float, max_expansions: int = MAX_EXPANSIONS) -> tuple[list[MoveSafety], State, str, int, int, int]:
    t0 = time.time()
    initial = State(frozenset(), frozenset(), frozenset(), frozenset())
    heap: list[tuple[tuple, int, State, list[MoveSafety], int]] = []
    counter = 0
    seen: set[tuple[frozenset[int], frozenset[int]]] = {(initial.captured, initial.claimed)}

    def state_priority(state: State, depth: int, safe_all_at: int) -> tuple:
        return (
            len(K5_EDGE_INDICES - state.claimed),
            len([p for p in K5 if p not in state.captured]),
            len(P_Y) - len(state.captured),
            -depth,
            safe_all_at if safe_all_at >= 0 else 10**9,
        )

    heapq.heappush(heap, (state_priority(initial, 0, -1), counter, initial, [], -1))
    expansions = 0
    while heap and time.time() - t0 < time_budget and expansions < max_expansions:
        _, _, state, path, safe_all_at = heapq.heappop(heap)
        expansions += 1
        if K5_EDGE_INDICES <= state.claimed:
            return path, state, "POS", safe_all_at, expansions, len(seen)
        now_safe_all = safe_all_at
        if now_safe_all < 0 and all_k5_edges_certified_safe_now(state):
            now_safe_all = len(path)
        moves = sorted(safe_moves(state, certified=True), key=lambda m: rank_move(state, m))[:MAX_CHILDREN_PER_STATE]
        for ms in moves:
            new_state = after_maker(state, ms.edge_index)
            key = (new_state.captured, new_state.claimed)
            if key in seen:
                continue
            seen.add(key)
            counter += 1
            new_path = path + [ms]
            heapq.heappush(heap, (state_priority(new_state, len(new_path), now_safe_all), counter, new_state, new_path, now_safe_all))
    if heap:
        _, _, state, path, safe_all_at = heap[0]
        return path, state, "NEG_NO_POS_WITHIN_BUDGET", safe_all_at, expansions, len(seen)
    return [], initial, "NEG_FRONTIER_EXHAUSTED", -1, expansions, len(seen)


def initial_diagnostics() -> None:
    initial = State(frozenset(), frozenset(), frozenset(), frozenset())
    moves = [move_safety(initial, ei) for ei in live_edges(initial)]
    print("Initial-state diagnostics:")
    print(f"  live_edges={len(moves)}")
    print(f"  certified_safe_moves={sum(1 for m in moves if m.certified_safe)}")
    print(f"  certified_unsafe_moves={sum(1 for m in moves if m.certified_unsafe)}")
    print(f"  indeterminate_moves={sum(1 for m in moves if not m.certified_safe and not m.certified_unsafe)}")
    print(f"  mid_estimate_safe_moves={sum(1 for m in moves if m.mid_safe)}")
    print("  top certified safe initial moves:")
    for ms in sorted([m for m in moves if m.certified_safe], key=lambda m: rank_move(initial, m))[:20]:
        print(f"    {describe_move(ms)}")
    print("  top margin initial moves, certified or not:")
    for ms in sorted(moves, key=lambda m: -m.safe_margin)[:12]:
        print(f"    {describe_move(ms)}")
    print("  K5 initial moves:")
    for ei in sorted(K5_EDGE_INDICES, key=lambda i: EDGES[i]):
        print(f"    {describe_move(move_safety(initial, ei))}")


def print_weight_summary() -> None:
    widths = []
    rel_widths = []
    for lo, hi in zip(LOWER_W, UPPER_W):
        widths.append(hi - lo)
        rel_widths.append((hi - lo) / ((hi + lo) / 2.0))
    print("Weight-count backend:")
    print(f"  exact_primecount_available={EXACT_AVAILABLE}")
    print(f"  backend={'exact primecount' if EXACT_AVAILABLE else 'Dusart 2010 explicit pi bounds'}")
    print("  interval_model=B_ac primes with n/(2ac) < b <= n/(ac)")
    print(f"  distinct_pair_intervals={len(EDGES)}")
    print(f"  exact_edge_counts={sum(1 for x in EXACT_W if x is not None)}")
    print(f"  min_lower_weight={min(LOWER_W):.6e}")
    print(f"  max_upper_weight={max(UPPER_W):.6e}")
    print(f"  max_absolute_bound_width={max(widths):.6e}")
    print(f"  max_relative_bound_width={max(rel_widths):.6e}")
    sample_edges = [(3, 5), (3, 7), (101, 103), (109, 113), (311, 313)]
    print("  sample_intervals:")
    for e in sample_edges:
        ei = EDGE_TO_INDEX[e]
        lo, hi = interval_endpoints(*e)
        exact = EXACT_W[ei]
        extra = f" exact={exact}" if exact is not None else ""
        print(f"    {e}: lo_exclusive={lo} hi_inclusive={hi} lower={LOWER_W[ei]:.6e} upper={UPPER_W[ei]:.6e}{extra}")


def main() -> int:
    print("=== Multi-step activation safety search with exact-or-Dusart bounds ===")
    print(f"n={N}")
    print("delta=1/8")
    print(f"Y_floor={Y}")
    print(f"|P_Y|={len(P_Y)} odd primes")
    print(f"P_Y first/last={P_Y[:8]} ... {P_Y[-8:]}")
    print(f"pair_graph_edges={len(EDGES)}")
    print(f"K5={K5}")
    print(f"q={Q_WITNESS}")
    print(f"q_membership_all_10={verify_q_membership()}")
    print()
    print_weight_summary()
    print()
    initial_diagnostics()
    print()

    t0 = time.time()
    greedy_path, greedy_state, greedy_status, greedy_safe_all_at = greedy_certified_path(20.0)
    print("Greedy certified Maker-only path:")
    print(f"  status={greedy_status}")
    print(f"  steps={len(greedy_path)}")
    print(f"  captured_vertices={len(greedy_state.captured)}")
    print(f"  claimed_edges={len(greedy_state.claimed)}")
    print(f"  claimed_k5_edges={len(greedy_state.claimed & K5_EDGE_INDICES)} / 10")
    print(f"  all_k5_certified_safe_at_step={greedy_safe_all_at}")
    print("  sequence:")
    for i, ms in enumerate(greedy_path[:60], 1):
        mark = "*" if ms.edge_index in K5_EDGE_INDICES else " "
        print(f"    {i:03d}{mark} {describe_move(ms)}")
    if len(greedy_path) > 60:
        print(f"    ... truncated {len(greedy_path) - 60} further moves")
    print()

    remaining = max(0.0, TIME_BUDGET_SECONDS - (time.time() - t0))
    path, state, status, safe_all_at, expansions, seen = priority_search(remaining)
    elapsed = time.time() - t0
    print("Best-first certified Maker-only search:")
    print(f"  status={status}")
    print(f"  wall_clock_seconds={elapsed:.2f}")
    print(f"  expansions={expansions}")
    print(f"  seen_states={seen}")
    print(f"  steps={len(path)}")
    print(f"  captured_vertices={len(state.captured)}")
    print(f"  claimed_edges={len(state.claimed)}")
    print(f"  claimed_k5_edges={len(state.claimed & K5_EDGE_INDICES)} / 10")
    print(f"  all_k5_certified_safe_at_step={safe_all_at}")
    print("  sequence:")
    for i, ms in enumerate(path[:120], 1):
        mark = "*" if ms.edge_index in K5_EDGE_INDICES else " "
        print(f"    {i:03d}{mark} {describe_move(ms)}")
    if len(path) > 120:
        print(f"    ... truncated {len(path) - 120} further moves")
    diag = best_diagnostic(state)
    if diag:
        print(f"  best_current_diagnostic={describe_move(diag)}")
    if status == "POS":
        print("POS: found a certified safe Maker-only activation sequence ending with all ten K5 pair edges claimed.")
    else:
        print("NEG: no POS sequence found within the configured budget and pruning limits.")
    print()
    print("Honesty notes:")
    print("  Exact prime counts were used only if a local primecount backend was present.")
    print("  Otherwise the result is a certified Dusart-bound search, not exact counting.")
    print("  This is still a Maker-only ordering search, not an adversarial strategy-tree proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
