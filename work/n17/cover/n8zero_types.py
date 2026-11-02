import sys, itertools, collections
sys.path.insert(0, '../heavy')
from g6blocks import decode
d = 17
c = collections.Counter()
for line in sys.stdin:
    try:
        B = decode(line, d)
    except IndexError:
        continue
    cov = set(); pts = [frozenset(b) for b in B]
    for b in B:
        for q in itertools.combinations(sorted(b), 2): cov.add(q)
    pts += [frozenset(q) for q in itertools.combinations(range(d), 2) if q not in cov]
    s = collections.Counter()
    for P in pts:
        for x in P: s[x] += 1
    if max(s.values()) == 8: continue
    W = sum((len(P)-2)*(len(P)-3)//2 for P in pts)
    c[(W, tuple(sorted(collections.Counter(s.values()).items())))] += 1
for k, v in sorted(c.items()): print(v, k)
