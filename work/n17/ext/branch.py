import sys, json, itertools, collections
def pts_of(n, blocks):
    cov = set(); pts = []
    for b in blocks:
        b = frozenset(b); pts.append(b)
        for q in itertools.combinations(sorted(b), 2): cov.add(q)
    for q in itertools.combinations(range(n), 2):
        if q not in cov: pts.append(frozenset(q))
    return pts
def candidates(n, pts, cmin, cmax):
    s = collections.Counter()
    for P in pts:
        for x in P: s[x] += 1
    cand = [P for P in pts if len(P) <= 5]
    res = []
    def rec(i, T, used, msum):
        c = len(T) + n - msum
        if len(T) >= 2 and cmin <= c <= cmax:
            if all(s[x] + 1 <= 8 for x in range(n) if x not in used):
                res.append(tuple(T))
        for j in range(i, len(cand)):
            P = cand[j]
            if P & used: continue
            if len(T) + 1 + n - msum - len(P) < cmin: continue
            rec(j + 1, T + [P], used | P, msum + len(P))
    rec(0, [], frozenset(), 0)
    return res
if __name__ == '__main__':
  for line in open(sys.argv[1]):
    r = json.loads(line)
    B = r['blocks']; pts = pts_of(13, B)
    b2 = sum(len(P) - 1 for P in pts)
    budget = 80 - b2
    c = candidates(13, pts, max(2, budget - 24), min(8, budget - 6))
    print(r.get('idx'), 'b2', b2, 'points', len(pts), 'level-1 candidate lines', len(c))
