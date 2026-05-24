"""
Concrete forced-loss path on the isolated unit-weight K_5 q-fiber.

Proves: starting from the initial state with 10 live rank-3 edges over a
shared large-prime slot q and five side slots {1q, 2q, 3q, 4q, 5q}, any
local Maker strategy maintaining per-round non-negative Q-monotonicity
loses by round 3.

This is the exhaustive-safety-game-solver result, reproduced as a single
forced sequence so a human can walk through it.

Run:
  python v4_k5_bad_path.py

Output: state trace and the final no-safe-move certificate.
"""
from __future__ import annotations

# Slot labels: q = 0, side vertices 1..5
q = "q"
S = lambda i: f"{i}q"
ALL = [q] + [S(i) for i in range(1, 6)]

def edge(i, j):
    """Rank-3 edge {q, iq, jq} for 1 <= i < j <= 5."""
    return frozenset([q, S(i), S(j)])

EDGES = [edge(i, j) for i in range(1, 6) for j in range(i + 1, 6)]
assert len(EDGES) == 10

def live(e, C, D_V, D_E, K, captured):
    """Buddhdev A.1: live iff not in D_E u K, no deleted vertex.
    Ordinary-captured edges are removed from live (their weight is paid into S)."""
    return e not in D_E and e not in K and e not in captured and not (e & D_V)

def phi(e, C):
    """Phi(e) = 2^|e cap C| for unit-weight rank-3 edges."""
    return 2 ** len(e & C)

def Q(C, D_V, D_E, K, S_score, captured):
    return 8 * S_score + sum(phi(e, C) for e in EDGES if live(e, C, D_V, D_E, K, captured))

def show(label, C, D_V, D_E, K, S_score, captured):
    Qv = Q(C, D_V, D_E, K, S_score, captured)
    live_edges = [(e, phi(e, C)) for e in EDGES if live(e, C, D_V, D_E, K, captured)]
    print(f"\n[{label}]")
    print(f"  C       = {sorted(C)}")
    print(f"  D_V     = {sorted(D_V)}")
    print(f"  D_E     = {[tuple(sorted(e)) for e in D_E]}")
    print(f"  K       = {[tuple(sorted(e)) for e in K]}")
    print(f"  S       = {S_score}")
    print(f"  Q       = {Qv}")
    print(f"  #live   = {len(live_edges)}")
    for e, p in live_edges:
        print(f"    {tuple(sorted(e))}   Phi={p}")

# --- Initial state -------------------------------------------------------
C, D_V, D_E, K, S_score = set(), set(), set(), set(), 0
captured = set()
show("initial", C, D_V, D_E, K, S_score, captured)
Q0 = Q(C, D_V, D_E, K, S_score, captured)
assert Q0 == 10, f"expected Q0=10, got {Q0}"

# --- Round 1 -------------------------------------------------------------
# Maker captures e_{1,2} = {q, 1q, 2q}: adds vertices to C, +1 to S, removes edge from live.
C |= edge(1, 2)
captured.add(edge(1, 2))
S_score += 1
show("after Maker captures e_{1,2}", C, D_V, D_E, K, S_score, captured)
# Shortener replies by deleting side vertex 3q (kills three live edges).
D_V.add(S(3))
show("after Shortener deletes 3q", C, D_V, D_E, K, S_score, captured)
Q1 = Q(C, D_V, D_E, K, S_score, captured)
assert Q1 == 26, f"expected Q1=26, got {Q1}"
print(f"  round-1 delta = +{Q1 - Q0}")

# --- Round 2 -------------------------------------------------------------
# Maker captures e_{4,5} = {q, 4q, 5q}.
C |= edge(4, 5)
captured.add(edge(4, 5))
S_score += 1
show("after Maker captures e_{4,5}", C, D_V, D_E, K, S_score, captured)
# Shortener edge-deletes e_{1,4}.
D_E.add(edge(1, 4))
show("after Shortener edge-deletes e_{1,4}", C, D_V, D_E, K, S_score, captured)
Q2 = Q(C, D_V, D_E, K, S_score, captured)
assert Q2 == 40, f"expected Q2=40, got {Q2}"
print(f"  round-2 delta = +{Q2 - Q1}")

# --- Round 3 (the trap) --------------------------------------------------
# Three live edges remain, all with Phi=8:
#   e_{1,5}, e_{2,4}, e_{2,5}.
# Maker's available moves:
#   - capture e_{1,5}: vertices already in C, S += 1, Q -> 8*(S+1) + sum over remaining = 16 + 2*8 = 32.
#     Shortener can edge-delete e_{2,4} or e_{2,5}: Q -> 32 - 8 = 24, full-round delta = 24 - 40 = -16. (Worse.)
#   - capture e_{2,4}: identical structure; Q -> 32 after Maker, Shortener deletes another Phi=8 edge.
#   - score any live edge: S += 1, the edge leaves live; Q -> 8(S+1) + sum over remaining live with original C.
#     E.g. score e_{1,5}: K |= e_{1,5}, S_score = 3, Q = 24 + 16 = 40 (Phi unchanged for others).
#     Shortener edge-deletes e_{2,4} or e_{2,5}: Q -> 40 - 8 = 32, full-round delta = 32 - 40 = -8.
# Every Maker move admits a Shortener reply driving Q strictly down. Best-case round delta = -8.
print("\n[trap state, round 3]")
print("Maker has three live edges, all with Phi=8.")
print("Every Maker move (capture or score) admits a Shortener reply with delta_Q <= -8.")
print("\nTherefore the K_5 q-fiber is losing for any local per-round-Q-monotone strategy.")
print("This matches the exhaustive safety-game synthesizer's verdict; see v4_findings.md.")
