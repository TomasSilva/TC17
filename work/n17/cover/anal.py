import sys, itertools, collections
sys.path.insert(0, '../heavy')
from g6blocks import decode
d = 17
def pts_of(B):
    cov = set()
    for b in B:
        for q in itertools.combinations(b, 2): cov.add(q)
    return [frozenset(b) for b in B] + [frozenset(q) for q in itertools.combinations(range(d), 2) if q not in cov]
stats = collections.Counter()
for line in open(sys.argv[1]):
    B = decode(line, d); P = pts_of(B)
    s = [0]*d
    for p in P:
        for i in p: s[i] += 1
    W = sum((len(p)-2)*(len(p)-3)//2 for p in P)
    t = collections.Counter(len(p) for p in P)
    n8 = sum(1 for x in s if x == 8)
    stypes = tuple(sorted(collections.Counter(s).items()))
    # vectors of 8-lines
    vec8 = []
    for i in range(d):
        if s[i] == 8:
            vec8.append(tuple(sorted((len(p)-1 for p in P if i in p), reverse=True)))
    stats[(W, n8, stypes, t[2])] += 1
for k, v in sorted(stats.items()): print(v, 'W=%d n8=%d lines=%s t2=%d' % k)
