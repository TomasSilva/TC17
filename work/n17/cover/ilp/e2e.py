import sys, itertools, subprocess
sys.path.insert(0, '../../heavy')
from g6blocks import decode
from gamma_ilp import write_lp
d = 17
res = {}
cnt = 0
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
        onH = sorted([P for P in pts if H0 in P], key=lambda P: (-len(P), tuple(sorted(8 - s[x] for x in P if x != H0))))
        k = tuple(len(P) - 1 for P in onH)
        if 1 not in k: continue
        lines = []
        for P in onH: lines += sorted((x for x in P if x != H0), key=lambda x: 8 - s[x])
        deltas = [8 - s[x] for x in lines]
        best = -99
        for T in itertools.combinations([x for x in range(d) if x != H0], 3):
            S = frozenset(T) | {H0}
            f = sum(1 for P in pts if P <= S)
            best = max(best, sum(s[x] - 7 for x in S) - f)
        thr = 4 - best
        def extra(k_, g, y, e, t, Dl): return [('%s' % y(X, deltas[X]), '=', 1) for X in range(16)]
        write_lp(k, 'e2e.lp', extra, thr)
        r = subprocess.run(['glpsol', '--lp', 'e2e.lp', '--tmlim', '60', '-o', 'e2e.sol'], capture_output=True, text=True)
        st = 'INF' if 'NO PRIMAL FEASIBLE' in r.stdout or 'NO INTEGER FEASIBLE' in r.stdout else ('FEAS' if 'INTEGER OPTIMAL' in r.stdout else 'OTHER')
        res[(thr, st)] = res.get((thr, st), 0) + 1
        cnt += 1
        if cnt >= int(sys.argv[2]): print(res); sys.exit()
print(res)
