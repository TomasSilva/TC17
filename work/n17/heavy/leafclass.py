"""Classify complete 17-line lattices (graph6 from lsgen3: points first, then blocks of size >= 3):
s_H, k8, W, phi_max over 8-line subsets of size <= 9 (obstruction: phi <= 4), 4-chain existence."""
import sys, itertools, collections
from g6blocks import decode
d = 17
def analyse(blocks):
    cov = set()
    for B in blocks:
        for q in itertools.combinations(B, 2): cov.add(q)
    pts = [tuple(B) for B in blocks] + [q for q in itertools.combinations(range(d), 2) if q not in cov]
    s = [0] * d
    for P in pts:
        for i in P: s[i] += 1
    W = sum((len(b) - 2) * (len(b) - 3) // 2 for b in blocks)
    e8 = [i for i in range(d) if s[i] == 8]
    e8s = set(e8)
    # full points among 8-lines: points all of whose lines are 8-lines
    full = [set(P) for P in pts if set(P) <= e8s]
    phimax = 0; chain4 = False
    for k in range(1, min(9, len(e8)) + 1):
        for S in itertools.combinations(e8, k):
            Ss = set(S)
            f = sum(1 for P in full if P <= Ss)
            ph = k - f
            if ph > phimax: phimax = ph
            if k == 4 and f == 0: chain4 = True
        if phimax >= 5: break
    return s, W, len(e8), phimax, chain4
if __name__ == '__main__':
 cnt = collections.Counter(); byW = collections.defaultdict(collections.Counter)
 for line in sys.stdin:
    B = decode(line, d)
    s, W, k8, ph, c4 = analyse(B)
    cls = 'obstructed(phi>=5)' if ph >= 5 else ('4-chain' if c4 else 'residual')
    cnt[cls] += 1; byW[W][cls] += 1
    cnt['k8=%d' % k8] += 1
 print(dict(cnt))
 for W in sorted(byW): print(W, dict(byW[W]))
