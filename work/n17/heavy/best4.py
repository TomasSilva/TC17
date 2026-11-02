"""For complete 17-line lattices, the best 4-line deletion: max over 4-sets S (each line determined at deletion)
of sum_c(S) = sum s_H - f(S); core b2 = 80 - sum_c.  Also best 5-set (12-line core b2 = 80 - sum_c)."""
import sys, itertools, collections
from g6blocks import decode
d = 17
def stats(B):
    cov = set()
    for b in B:
        for q in itertools.combinations(b, 2): cov.add(q)
    pts = [frozenset(b) for b in B] + [frozenset(q) for q in itertools.combinations(range(d), 2) if q not in cov]
    s = [0] * d
    for P in pts:
        for i in P: s[i] += 1
    order = sorted(range(d), key=lambda i: -s[i])
    best4 = 0
    long = [i for i in range(d) if s[i] >= 7]
    cand = long if len(long) >= 4 else order[:8]
    for S in itertools.combinations(cand, 4):
        Sf = frozenset(S)
        f = sum(1 for P in pts if P <= Sf)
        best4 = max(best4, sum(s[i] for i in S) - f)
    return best4, s
cnt = collections.Counter()
for line in sys.stdin:
    b4, s = stats(decode(line, d))
    cnt[80 - b4] += 1
print('best 13-line core b2 :', sorted(cnt.items()))
