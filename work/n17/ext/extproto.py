"""Prototype: combinatorial extensions of a 13-line core B to 17-line window lattices L = B + 4 lines,
with sum of deletion counts = 80 - b2(B).  Counts extensions (with duplicates)."""
import sys, json, itertools, collections, time
def points_of(n, blocks):
    cov = set()
    pts = []
    for b in blocks:
        b = frozenset(b); pts.append(b)
        for q in itertools.combinations(sorted(b), 2): cov.add(q)
    for q in itertools.combinations(range(n), 2):
        if q not in cov: pts.append(frozenset(q))
    return pts
def b2(pts): return sum(len(P) - 1 for P in pts)
def extend(n, pts, depth, budget, out, cap):
    if depth == 0:
        if budget == 0: out.append(pts)
        return
    if len(out) >= cap: return
    s = collections.Counter()
    for P in pts:
        for x in P: s[x] += 1
    cand = [P for P in pts if len(P) <= 5]
    # T: pairwise disjoint, sum(m-1) >= n - 8 ; c = |T| + n - sum m
    need_lo = max(1, budget - 8 * (depth - 1))
    need_hi = min(8, budget - 1 * (depth - 1))
    res = []
    def rec(i, T, used, exc):
        c = len(T) + n - sum(len(P) for P in T)
        if T and need_lo <= c <= need_hi:
            res.append((tuple(T), c))
        for j in range(i, len(cand)):
            P = cand[j]
            if P & used: continue
            # adding P lowers c by (m-1)
            if len(T) + 1 + n - sum(len(Q) for Q in T) - len(P) < need_lo: continue
            rec(j + 1, T + [P], used | P, exc + len(P) - 1)
    rec(0, [], frozenset(), 0)
    for T, c in res:
        h = n
        newpts = []
        Tset = set(T)
        covered = set()
        for P in pts:
            if P in Tset: newpts.append(P | {h}); covered |= P
            else: newpts.append(P)
        for x in range(n):
            if x not in covered: newpts.append(frozenset((x, h)))
        # line-length check: every old line gets +1 point unless covered by T
        s2 = collections.Counter()
        for P in newpts:
            for x in P: s2[x] += 1
        if max(s2[x] for x in range(n + 1)) > 8: continue
        extend(n + 1, newpts, depth - 1, budget - c, out, cap)
        if len(out) >= cap: return
def window_ok(pts, d=17):
    s = collections.Counter()
    for P in pts:
        for x in P: s[x] += 1
    if any(not (4 <= s[x] <= 8) for x in range(d)): return False
    if any(len(P) > 6 for P in pts): return False
    if b2(pts) != 80: return False
    # 8-lines have a double point
    for x in range(d):
        if s[x] == 8 and not any(len(P) == 2 and x in P for P in pts): return False
    # (W5): unjoined multiple points sigma <= 8 (only points with m>=2: all points)
    big = [P for P in pts if len(P) >= 5]
    for P, Q in itertools.combinations(big, 2):
        if not (P & Q) and len(P) + len(Q) - 2 > 8: return False
    return True
if __name__ == '__main__':
    f = sys.argv[1]; nmax = int(sys.argv[2]); cap = int(sys.argv[3])
    for k, line in enumerate(open(f)):
        if k >= nmax: break
        rec = json.loads(line)
        pts = points_of(13, rec['blocks'])
        t0 = time.time()
        out = []
        extend(13, pts, 4, 80 - b2(pts), out, cap)
        ok = [P for P in out if window_ok(P)]
        print(rec.get('idx'), 'b2', b2(pts), 'raw ext', len(out), 'window', len(ok), '%.1fs' % (time.time() - t0), flush=True)
