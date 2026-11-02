"""Leaf filters from the chain/obstruction theory, on complete 17-line lattices (graph6 from lsgen3).
 - obstructed: some S of 8-lines with |S|<=9 and |S|-f(S) >= 5  -> not a counterexample
 - 4-chain S: core L\\S must be a free (6,6) lattice: necessary: every core line has <= 7 points (Abe),
   unjoined pairs in the core have (m-1)+(m'-1) <= 6 (external lines of a free (6,6) arr. have >= 7 points)
 - phi=3 4-set S: core has a nearly free (6,7) realization: necessary: unjoined pairs sigma <= 7
Report how many leaves survive."""
import sys, itertools, collections
from g6blocks import decode
d = 17
def lattice(blocks):
    cov = set()
    for B in blocks:
        for q in itertools.combinations(B, 2): cov.add(q)
    pts = [frozenset(B) for B in blocks] + [frozenset(q) for q in itertools.combinations(range(d), 2) if q not in cov]
    return pts
def sub(pts, keep):
    """points of the sub-arrangement on lines `keep` (with >= 2 lines)"""
    out = []
    for P in pts:
        Q = P & keep
        if len(Q) >= 2: out.append(Q)
    return out
def core_ok_free(pts, keep):
    sp = sub(pts, keep)
    s = collections.Counter()
    for P in sp:
        for i in P: s[i] += 1
    if any(s[i] > 7 for i in keep): return False
    # unjoined pairs of multiple points (m >= 2 in core) : sigma <= 6
    mult = [P for P in sp if len(P) >= 3]
    for P, Q in itertools.combinations(sp, 2):
        if len(P & Q) == 0 and (len(P) - 1) + (len(Q) - 1) > 6: return False
    return True
def core_ok_nf(pts, keep):
    sp = sub(pts, keep)
    for P, Q in itertools.combinations(sp, 2):
        if len(P & Q) == 0 and (len(P) - 1) + (len(Q) - 1) > 7: return False
    return True
def classify(blocks):
    pts = lattice(blocks)
    s = [0] * d
    for P in pts:
        for i in P: s[i] += 1
    e8 = [i for i in range(d) if s[i] == 8]
    allL = frozenset(range(d))
    def f(S):
        return sum(1 for P in pts if P <= S)
    # obstruction
    for k in range(5, min(9, len(e8)) + 1):
        for S in itertools.combinations(e8, k):
            if k - f(frozenset(S)) >= 5: return 'obstructed'
    chains = [frozenset(S) for S in itertools.combinations(e8, 4) if f(frozenset(S)) == 0]
    if chains:
        for S in chains:
            if not core_ok_free(pts, allL - S): return '4chain-core-not-free'
        return '4chain-survives'
    # phi = 3 four-sets (any lines)
    nf = []
    for S in itertools.combinations(range(d), 4):
        S = frozenset(S)
        if sum(s[i] - 7 for i in S) - f(S) == 3: nf.append(S)
    if nf:
        for S in nf:
            if not core_ok_nf(pts, allL - S): return 'nfcore-fails'
        return 'nfcore-survives'
    return 'R2'
if __name__ == '__main__':
    cnt = collections.Counter()
    for line in sys.stdin:
        cnt[classify(decode(line, d))] += 1
    print(dict(cnt))
