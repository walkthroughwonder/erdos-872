"""
Constructs a concrete arithmetic K5 q-fiber for Buddhdev Appendix A.1.
This verifies only the arithmetic legality and residual incidence. It does not
prove that Buddhdev's under-specified safe-edge selector must choose these ten
activation pairs in the full activation graph.
"""
from itertools import combinations

# Miller-Rabin with deterministic bases sufficient well beyond this range in practice.
def is_probable_prime(n:int)->bool:
    if n < 2: return False
    small=[2,3,5,7,11,13,17,19,23,29,31,37]
    for p in small:
        if n%p==0: return n==p
    d=n-1; s=0
    while d%2==0:
        s+=1; d//=2
    # These bases are deterministic for n < 2^128 according to common bounds with first 12 primes for our use.
    for a in small:
        if a>=n: continue
        x=pow(a,d,n)
        if x==1 or x==n-1: continue
        for _ in range(s-1):
            x=pow(x,2,n)
            if x==n-1: break
        else:
            return False
    return True

def nextprime(m:int)->int:
    if m <= 2: return 2
    x=m+1 if m%2==0 else m
    while not is_probable_prime(x):
        x += 2
    return x

n = 10**20
Y = int(n ** (1/8))
P = [101, 103, 107, 109, 113]
assert all(p <= Y for p in P)
prods = [a*c for a,c in combinations(P,2)]
lo = n // (2*min(prods)) + 1       # q > n/(2*ac) for the smallest ac
hi = n // max(prods)               # q <= n/(ac) for the largest ac
q = int(nextprime(lo))
assert q <= hi, (q, hi)
assert q > Y
print('n', n, 'delta', '1/8', 'Y_floor', Y)
print('small_primes', P)
print('product_range', min(prods), max(prods), 'common_q_interval', (lo, hi), 'q', q)

plays=[]
for a,c in combinations(P,2):
    L = n//(2*a*c)+1
    U = n//(a*c)
    b0 = int(nextprime(L))
    if b0 == q:
        b0 = int(nextprime(b0 + 1))
    assert b0 <= U and b0 > Y and b0 != q
    assert n//2 < a*c*b0 <= n
    assert n//2 < a*c*q <= n
    plays.append((a,c,b0,a*c*b0,a*c*q))
print('activation_targets and residual_q_targets:')
for row in plays:
    print(row)

used_primes=set(P+[q]+[b for _,_,b,_,_ in plays])
short=[]
r=nextprime(n//2+1000)
while len(short)<len(plays):
    if r not in used_primes:
        short.append(int(r)); used_primes.add(int(r))
    r=nextprime(r + 1)
print('harmless_shortener_primes', short)

played=[]
for (a,c,b0,t0,tq), s in zip(plays, short):
    assert all(t0 % x != 0 and x % t0 != 0 for x in played), ('P illegal', t0)
    played.append(t0)
    assert all(s % x != 0 and x % s != 0 for x in played), ('S illegal', s)
    for _,_,_,_,tq2 in plays:
        assert tq2 % s != 0 and s % tq2 != 0
    played.append(s)

for a,c,b0,t0,tq in plays:
    assert all(tq % x != 0 and x % tq != 0 for x in played), ('residual killed', tq)

edges={(a,c): frozenset([('q',q), ('side',a,q), ('side',c,q)]) for a,c,_,_,_ in plays}
expected=set(combinations(P,2))
assert set(edges)==expected and len(edges)==10
print('verified: all 10 q-targets remain live and form the complete graph K5 on side slots p*q')
