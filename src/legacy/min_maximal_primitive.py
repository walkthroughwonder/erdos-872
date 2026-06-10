"""Find the smallest maximal primitive subset of {2,...,n}.
A set M is primitive if no element divides another.
M is maximal primitive in {2,...,n} if no element of {2,...,n}\M can be added while keeping it primitive.
i.e. for every x in {2,...,n}\M, there exists m in M with m | x or x | m.
Find min |M| over all maximal primitive M in {2,...,n}.
"""
import sys
from itertools import combinations

def is_primitive(S):
    L = sorted(S)
    for i, a in enumerate(L):
        for b in L[i+1:]:
            if b % a == 0:
                return False
    return True

def is_maximal_primitive(M, n):
    if not is_primitive(M):
        return False
    Mset = set(M)
    for x in range(2, n+1):
        if x in Mset: continue
        ok = False
        for m in M:
            if x % m == 0 or m % x == 0:
                ok = True; break
        if not ok:
            return False
    return True

def min_maximal_primitive(n):
    # try k=1,2,... until we find a maximal primitive subset of size k
    elements = list(range(2, n+1))
    for k in range(1, n):
        for combo in combinations(elements, k):
            if is_maximal_primitive(combo, n):
                return k, combo
    return None

if __name__ == "__main__":
    for n in range(4, 21):
        k, ex = min_maximal_primitive(n)
        print(f"n={n}: min |M|={k}, example={ex}")
