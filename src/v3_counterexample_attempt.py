"""
Counterexample to the operational v3 invariant as implemented in k4_avoidance_v3.py.

Configuration: one K_5 large-prime fiber, or [5,4].  The initial state is
reachable.  Because v3's near-trap predicate treats any first ordinary capture
in a K_k (k>=4) as unsafe (post-capture max Phi is 4), v3 plays SAFE_SCORE on
one edge.  Shortener then deletes the shared q vertex.  The full-round scaled
potential drops below its pre-Maker value even though raw RSE at the state is
true (there exists a different safe ordinary capture).
"""
import sys
sys.path.insert(0, '/home/user/workspace/erdos872')
from multi_fiber_rse import build_edges, MultiState, Q, raw_rse, breaker_moves
from k4_avoidance_v3 import strategy_v3, fiber_state


def initial_state():
    return MultiState(C=frozenset(), D_V=frozenset(), D_E=frozenset(),
                      K=frozenset(), S=0, captured_edges=frozenset())


def demonstrate(cfg):
    fibers = [list(range(1, k+1)) for k in cfg]
    edges, _ = build_edges(fibers)
    s0 = initial_state()
    q0 = Q(s0, edges)
    print(f"config={cfg}, edges={len(edges)}, Q0={q0}, raw_rse={raw_rse(s0, edges)}")
    move = strategy_v3(s0, edges)
    action, ei, after_m = move
    print(f"v3_move={action} edge={ei} {edges[ei]}, Q_after_maker={Q(after_m, edges)}")
    print(f"fiber_state_after_maker={fiber_state(after_m, edges, 0)}")
    worst = min(breaker_moves(after_m, edges), key=lambda bm: Q(bm[2], edges))
    b_act, b_tgt, after_b = worst
    q1 = Q(after_b, edges)
    print(f"worst_shortener_reply={b_act} target={b_tgt}, Q_after_round={q1}, delta={q1-q0}")
    assert q1 < q0, "expected v3's chosen move to allow Q decrease"


if __name__ == '__main__':
    demonstrate([5])      # breaks the forum's claimed nonnegative per-round Q change
    demonstrate([5,4])    # one of the Monte Carlo configs: initial state already breaks chosen-v3 safety
    demonstrate([7])      # stronger: delta=-13 < -8*w_max (with unit weights)
