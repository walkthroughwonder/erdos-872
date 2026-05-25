"""Independent verifier for construct_k5_arithmetic_witness.py output."""
from itertools import combinations
n=10**20
P=[101,103,107,109,113]
q=4806305873305829
plays=[
(101,103,4806305873305877,50000000000001038431,50000000000000539087),
(101,107,4626630887387813,50000000000000095091,51941747572816094003),
(101,109,4541738577527497,50000000000000214473,52912621359223871461),
(101,113,4380969070358401,50000000000000430613,54854368932039426377),
(103,107,4536793394428837,50000000000000212577,52970297029703541409),
(103,109,4453549478934817,50000000000001190459,53960396039604542183),
(103,113,4295901709768891,50000000000000122349,55940594059406543731),
(107,109,4287061647946543,50000000000000531009,56055945400365883627),
(107,113,4135307253328939,50000000000000201449,58113044314140778439),
(109,113,4059430056020147,50000000000000150599,59199269441507895793),
]
short=[50000000000000001043,50000000000000001053,50000000000000001067,50000000000000001089,50000000000000001101,50000000000000001139,50000000000000001157,50000000000000001167,50000000000000001187,50000000000000001191]

def comp(a,b): return a%b==0 or b%a==0
# arithmetic identities and interval membership
for a,c,b,t0,tq in plays:
    assert t0==a*c*b
    assert tq==a*c*q
    assert n//2 < t0 <= n and n//2 < tq <= n
    assert q > n/(2*a*c) and q <= n/(a*c)
    assert b > n/(2*a*c) and b <= n/(a*c)
# play legality
played=[]
for row,s in zip(plays,short):
    t0=row[3]
    assert not any(comp(t0,x) for x in played)
    played.append(t0)
    assert not any(comp(s,x) for x in played)
    played.append(s)
# residual q targets survived
for row in plays:
    tq=row[4]
    assert not any(comp(tq,x) for x in played)
# exact K5 pair set
assert {(a,c) for a,c,_,_,_ in plays} == set(combinations(P,2))
# slot-incidence degrees in q fiber: q in 10 edges, each side p*q in 4 edges
slot_degree={('q',q):0}
for p in P: slot_degree[('side',p*q)]=0
for a,c,_,_,_ in plays:
    slot_degree[('q',q)]+=1
    slot_degree[('side',a*q)]+=1
    slot_degree[('side',c*q)]+=1
assert slot_degree[('q',q)]==10
assert all(slot_degree[('side',p*q)]==4 for p in P)
print('independent verification passed: legal play, survived q targets, K5 slot incidence')
