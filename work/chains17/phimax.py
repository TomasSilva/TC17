"""For lattices (blocks on 17 lines), compute max over sets S of 8-point lines, |S| <= 9, of
phi(S) = |S| - f(S), f(S) = #points all of whose lines lie in S.  (7-point lines cannot raise phi.)
Prediction for nearly free (7,10) window arrangements: phi <= 4 for |S| <= 9."""
import sys, json, itertools
def analyse(n, blocks):
    allL = list(range(n))
    pts = [tuple(B) for B in blocks]
    cov = set()
    for B in pts:
        for q in itertools.combinations(sorted(B), 2): cov.add(q)
    dbl = [q for q in itertools.combinations(allL, 2) if q not in cov]
    allpts = pts + dbl
    s = {i: 0 for i in allL}
    for P in allpts:
        for i in P: s[i] += 1
    e8 = [i for i in allL if s[i] == 8]
    best = {}
    for k in range(1, min(9, len(e8)) + 1):
        mb = -99; wit = None
        for S in itertools.combinations(e8, k):
            Ss = set(S)
            f = sum(1 for P in allpts if set(P) <= Ss)
            if k - f > mb: mb, wit = k - f, S
        best[k] = (mb, wit)
    return s, e8, best
for fn in sys.argv[1:]:
    for line in open(fn):
        rec = json.loads(line)
        s, e8, best = analyse(17, rec['blocks'])
        tag = (rec.get('source', '') + str(rec.get('deleted', rec.get('sizes', ''))))[:26]
        print('%-26s k8=%2d  max phi by |S|: %s' % (tag, len(e8), ' '.join('%d:%d' % (k, best[k][0]) for k in sorted(best))))
