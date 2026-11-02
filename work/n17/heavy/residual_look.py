import sys, itertools, collections
from g6blocks import decode
from leafclass import analyse
d = 17
cnt = collections.Counter()
for line in sys.stdin:
    B = decode(line, d)
    s, W, k8, ph, c4 = analyse(B)
    if ph >= 5 or c4: continue
    # residual: describe 8-line structure: 3-chains? phi=3 4-sets (nf(6,7) cores)?
    cov = set()
    for b in B:
        for q in itertools.combinations(b, 2): cov.add(q)
    pts = [tuple(b) for b in B] + [q for q in itertools.combinations(range(d), 2) if q not in cov]
    e8 = [i for i in range(d) if s[i] == 8]
    def fS(S):
        Ss = set(S); return sum(1 for P in pts if set(P) <= Ss)
    ch3 = any(fS(T) == 0 for T in itertools.combinations(e8, 3))
    # nf(6,7) core: 4-set with sum(s-7) - f = 3
    nf = False
    for S in itertools.combinations(range(d), 4):
        if sum(s[i] - 7 for i in S) - fS(S) == 3: nf = True; break
    prof = collections.Counter(len(b) for b in B)
    cnt[(W, k8, ch3, nf, tuple(sorted(collections.Counter(s).items())))] += 1
for k, v in sorted(cnt.items()): print(v, 'W=%d k8=%d 3chain=%s nfcore=%s lines(s:count)=%s' % (k[0], k[1], k[2], k[3], k[4]))
