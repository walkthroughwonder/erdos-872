import sys
sys.path.insert(0, '/home/user/workspace/erdos872')
from activation_rank2_rse import edges_for_k, State, raw_rse, maker_claim, Q, live_edges

k=5
edges=edges_for_k(k)
# weights 2 so every claimed pair has one residual token left after securing play
state=State(C=frozenset(), D_V=frozenset(), claimed=frozenset(), D_E=frozenset(), w=tuple([2]*len(edges)), S=0)
print('edges', list(enumerate(edges)))
print('initial Q', Q(state, edges))
seq=list(range(len(edges)))
for step, ei in enumerate(seq,1):
    ok, cert=raw_rse(state, edges, k)
    print('step', step, 'state Q', Q(state,edges), 'C', sorted(state.C), 'claimed', sorted(state.claimed), 'safe_exists', ok, cert, 'chosen', ei, edges[ei])
    # Check chosen is safe
    Q0=Q(state,edges)
    after=maker_claim(state, ei, edges)
    safe=True; worst=10**9; wb=None
    from activation_rank2_rse import breaker_moves
    br=breaker_moves(after, edges, k)
    if not br: worst=Q(after,edges)-Q0
    for act,t,afterb in br:
        delta=Q(afterb,edges)-Q0
        if delta<worst: worst=delta; wb=(act,t)
        if delta < -1e-9: safe=False
    print('  chosen safe?', safe, 'worst_delta', worst, 'worst_breaker', wb, 'afterM Q', Q(after,edges))
    if not safe:
        break
    # simulate off-model harmless Shortener: no graph state change after Maker
    state=after
print('final', state, 'Q', Q(state,edges))
