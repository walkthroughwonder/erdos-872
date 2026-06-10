import sys, json
sys.path.insert(0,'/home/user/workspace/erdos872')
from multi_fiber_rse import build_edges, Q
from k4_avoidance_v4 import initial_state, strategy_v4
for cfg in [[5],[7],[5,4],[4,4],[4,3,2]]:
    edges,_=build_edges([list(range(1,k+1)) for k in cfg])
    s=initial_state()
    action,ei,after,d,reply=strategy_v4(s,edges)
    print(json.dumps({'cfg':cfg,'n_edges':len(edges),'Q0':Q(s,edges),'chosen':(action,ei,str(edges[ei])),'worst_delta':d,'worst_reply':str(reply),'Q_after_maker':Q(after,edges)}))
