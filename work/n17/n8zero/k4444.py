"""n8 = 0 with a 4-point line: H0 = line 16 with four 5-fold points (k = (4,4,4,4)), the 16 other lines
in pencils A = 0..3, B = 4..7, C = 8..11, D = 12..15; every pair of lines from different pencils meets in
a triple point with lines from three different pencils (t2 = 0, W = 12: no other heavy points).
Enumerate the triangle decompositions of K_{4,4,4,4} (exact cover of the 96 cross edges), with the
neighbourhood of line 0 fixed (WLOG), dedup by nauty, write 17-line lattices."""
import itertools, sys, json, subprocess
part = lambda x: x // 4
lines = range(16)
edges = [(a, b) for a in lines for b in lines if a < b and part(a) != part(b)]
eid = {e: i for i, e in enumerate(edges)}
tris = [t for t in itertools.combinations(lines, 3) if len({part(x) for x in t}) == 3]
tri_edges = [[eid[(t[0], t[1])], eid[(t[0], t[2])], eid[(t[1], t[2])]] for t in tris]
by_edge = [[] for _ in edges]
for ti, es in enumerate(tri_edges):
    for e in es: by_edge[e].append(ti)
# WLOG for line 0 (pencil A): its six triangles are {0,4,8},{0,5,9} (ABC), {0,6,12},{0,7,13} (ABD), {0,10,14},{0,11,15} (ACD)
fixed = [(0, 4, 8), (0, 5, 9), (0, 6, 12), (0, 7, 13), (0, 10, 14), (0, 11, 15)]
covered = [False] * len(edges)
chosen = [tris.index(t) for t in fixed]
for ti in chosen:
    for e in tri_edges[ti]:
        assert not covered[e]; covered[e] = True
sols = []
def rec():
    # choose the uncovered edge with fewest options
    best = None; bopts = None
    for e in range(len(edges)):
        if covered[e]: continue
        opts = [ti for ti in by_edge[e] if not any(covered[x] for x in tri_edges[ti])]
        if not opts: return
        if best is None or len(opts) < len(bopts):
            best, bopts = e, opts
            if len(opts) == 1: break
    if best is None:
        sols.append(list(chosen)); return
    for ti in bopts:
        for x in tri_edges[ti]: covered[x] = True
        chosen.append(ti)
        rec()
        chosen.pop()
        for x in tri_edges[ti]: covered[x] = False
rec()
print('solutions with fixed neighbourhood of line 0:', len(sols), file=sys.stderr)
sys.path.insert(0, '../validate')
from canon import canon_many
lats = []
for s in sols:
    blocks = [list(tris[ti]) for ti in s] + [[0, 1, 2, 3, 16], [4, 5, 6, 7, 16], [8, 9, 10, 11, 16], [12, 13, 14, 15, 16]]
    lats.append(blocks)
cs = canon_many(17, lats)
uniq = {}
for c, b in zip(cs, lats): uniq.setdefault(c, b)
print('distinct lattices:', len(uniq), file=sys.stderr)
for k, b in enumerate(uniq.values()):
    print(json.dumps(dict(idx=k, blocks=b)))
