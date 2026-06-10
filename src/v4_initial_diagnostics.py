import sys, json
sys.path.insert(0,'/home/user/workspace/erdos872')
from multi_fiber_rse import build_edges, MultiState, Q, breaker_moves
from k4_avoidance_v4 import initial_state, strategy_v4, make_strategy_v4_safety, worst_round_delta

for cfg in [[5],[7],[5,4],[4,4],[4,3,2]]:
    edges,_=build_edges([list(range(1,k+1)) for k in cfg])
    s=initial_state()
    greedy=strategy_v4(s,edges)
    strat=make_strategy_v4_safety(tuple(edges))
    ok, synth = strat.solve(s)
    move=synth if synth else greedy
    action, ei, after, d, reply=move
    print(json.dumps({
        'cfg':cfg,'n_edges':len(edges),'Q0':Q(s,edges),'safety_solve_initial':ok,
        'chosen':(action,ei,str(edges[ei])),'worst_delta':d,'worst_reply':str(reply),
        'Q_after_maker':Q(after,edges)
    }))
