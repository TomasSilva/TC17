"""n8 = 0 with a 5-point line H0 (line 16) and no 4-point line.  H0 has points with k = (k_1..k_5) other
lines (pencils); every pair of lines from different pencils meets in exactly one off-H0 point, whose lines
come from distinct pencils.  Constraints: all lines <= 7 points (n8 = 0), >= 5 points (no 4-point line),
m <= 6, W = W(H0) + W_off in [11, 13], t2 = 3W - 32 - t5 - 3t6 (double points), sum_{H != H0}(7 - s_H) = 13 - W.
Step 1: heavy off-H0 points (m >= 4) with W_off <= 13 - W(H0), enumerated with pairwise-intersection <= 1,
up to symmetry (nauty).  Step 2: exact cover of the remaining cross pairs by triple points and double points.
Output: distinct 17-line lattices (blocks of size >= 3)."""
import itertools, sys, json, collections
sys.path.insert(0, '../validate')
from canon import canon_many
k = tuple(int(c) for c in sys.argv[1])
assert len(k) == 5 and sum(k) == 16
H0 = 16
pen = []
for i, ki in enumerate(k): pen += [i] * ki
L = range(16)
W0 = sum((x - 1) * (x - 2) // 2 for x in k)
t5_0 = sum(1 for x in k if x == 4); t6_0 = sum(1 for x in k if x == 5); b0 = sum(1 for x in k if x == 1)
cross = [(a, b) for a in L for b in L if a < b and pen[a] != pen[b]]
def transversals(size):
    for S in itertools.combinations(L, size):
        if len({pen[x] for x in S}) == size: yield S
heavy_cands = [S for m in (4, 5, 6) for S in transversals(m)]
wt = lambda S: (len(S) - 2) * (len(S) - 3) // 2
Wmax_off = 13 - W0
# Step 1: sets of heavy points (pairwise share <= 1 line), W_off <= Wmax_off, generated level by level
# with one representative per isomorphism class (nauty canonical form of H0 + pencils + heavy points).
base = [sorted([i for i in L if pen[i] == p] + [H0]) for p in range(5)]
base = [b for b in base if len(b) >= 3]
level = {'': []}
uniq = {}
cs0 = canon_many(17, [base])
uniq[cs0[0]] = []
while level:
    nxt = {}
    for key, hs in level.items():
        used = set(p for S in hs for p in itertools.combinations(S, 2))
        w = sum(wt(S) for S in hs)
        exts = []
        for S in heavy_cands:
            if w + wt(S) > Wmax_off: continue
            if any(p in used for p in itertools.combinations(S, 2)): continue
            exts.append(hs + [S])
        if not exts: continue
        cs = canon_many(17, [base + [list(S) for S in e] for e in exts])
        for c, e in zip(cs, exts):
            if c not in uniq and c not in nxt: nxt[c] = e
    for c, e in nxt.items(): uniq[c] = e
    level = nxt
print(''.join(map(str, k)), 'W0', W0, 'distinct heavy sets', len(uniq), file=sys.stderr)
# Step 2
out_lats = []
tri_all = list(transversals(3))
for hs in uniq.values():
    Woff = sum(wt(S) for S in hs)
    W = W0 + Woff
    if W < 11: continue
    t5 = t5_0 + sum(1 for S in hs if len(S) == 5); t6 = t6_0 + sum(1 for S in hs if len(S) == 6)
    t2 = 3 * W - 32 - t5 - 3 * t6
    t2_off = t2 - b0
    if t2_off < 0: continue
    deficit = 13 - W          # sum over the 16 lines of (7 - s)
    covered = set()
    noff = [0] * 16          # off-H0 points on each line
    for S in hs:
        for p in itertools.combinations(S, 2): covered.add(p)
        for x in S: noff[x] += 1
    rem = [p for p in cross if p not in covered]
    # each line X: off points total = s_X - 1 in [4, 6]; we track noff and cap at 6
    tri_ok = [T for T in tri_all if not any(p in covered for p in itertools.combinations(T, 2))]
    by_pair = collections.defaultdict(list)
    for T in tri_ok:
        for p in itertools.combinations(T, 2): by_pair[p].append(T)
    cov = set(covered)
    nd = [0]
    sols = []
    chosen = []
    def feasible_lines():
        return all(x <= 6 for x in noff)
    def rec():
        # pick uncovered pair with fewest options
        best = None; bo = None
        for p in rem:
            if p in cov: continue
            opts = [T for T in by_pair[p] if not any(q in cov for q in itertools.combinations(T, 2)) and all(noff[x] < 6 for x in T)]
            nopt = len(opts) + (1 if (nd[0] < t2_off and noff[p[0]] < 6 and noff[p[1]] < 6) else 0)
            if nopt == 0: return
            if best is None or nopt < bo[0]:
                best, bo = p, (nopt, opts)
                if nopt == 1: break
        if best is None:
            if nd[0] != t2_off: return
            s = [1 + noff[x] for x in L]
            if any(v < 5 or v > 7 for v in s): return
            if sum(7 - v for v in s) != deficit: return
            sols.append(list(chosen)); return
        p = best
        for T in bo[1]:
            for q in itertools.combinations(T, 2): cov.add(q)
            for x in T: noff[x] += 1
            chosen.append(T); rec(); chosen.pop()
            for x in T: noff[x] -= 1
            for q in itertools.combinations(T, 2): cov.discard(q)
        if nd[0] < t2_off and noff[p[0]] < 6 and noff[p[1]] < 6:
            cov.add(p); noff[p[0]] += 1; noff[p[1]] += 1; nd[0] += 1
            rec()
            nd[0] -= 1; noff[p[0]] -= 1; noff[p[1]] -= 1; cov.discard(p)
    rec()
    for sol in sols:
        out_lats.append(base + [list(S) for S in hs] + [list(T) for T in sol])
print(''.join(map(str, k)), 'raw lattices', len(out_lats), file=sys.stderr)
if out_lats:
    cs = canon_many(17, out_lats)
    u2 = {}
    for c, b in zip(cs, out_lats): u2.setdefault(c, b)
    print(''.join(map(str, k)), 'distinct lattices', len(u2), file=sys.stderr)
    for i, b in enumerate(u2.values()):
        print(json.dumps(dict(idx='%s_%d' % (''.join(map(str, k)), i), blocks=b)))
