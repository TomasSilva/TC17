import sys, itertools
sys.path.insert(0, '../../heavy')
from g6blocks import decode
from level1 import survivors
d = 17
cache = {}
n = nb = nh = 0
for line in open(sys.argv[1]):
    B = decode(line, d)
    cov = {}
    pts = [frozenset(b) for b in B]
    for b in B:
        for q in itertools.combinations(sorted(b), 2): cov[q] = 1
    pts += [frozenset(q) for q in itertools.combinations(range(d), 2) if q not in cov]
    s = [0] * d
    for P in pts:
        for i in P: s[i] += 1
    for H0 in range(d):
        if s[H0] != 8: continue
        onH = [P for P in pts if H0 in P]
        groups = sorted([(len(P) - 1, tuple(sorted(8 - s[x] for x in P if x != H0))) for P in onH], key=lambda t: (-t[0], t[1]))
        k = tuple(g[0] for g in groups)
        if 1 not in k: continue
        best = -99
        for T in itertools.combinations([x for x in range(d) if x != H0], 3):
            S = frozenset(T) | {H0}
            f = sum(1 for P in pts if P <= S)
            best = max(best, sum(s[x] - 7 for x in S) - f)
        thr = 4 - best
        key = (k, thr)
        if key not in cache: cache[key] = set(ch for D, ch in survivors(k, thr))
        nh += 1
        chosen = tuple(g[1] for g in groups)
        if chosen not in cache[key]:
            nb += 1
            if nb <= 5: print('NOT A SURVIVOR', k, thr, chosen)
    n += 1
    if n >= int(sys.argv[2]): break
print('lattices', n, '8-lines checked', nh, 'failures', nb)
