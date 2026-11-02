"""SUPERSEDED by pencil5c.py, which deduplicates the heavy configurations up to isomorphisms fixing H0
(audit F1, work/n17/audit/AUDIT.md); the lattice sets of the two are identical.
n8 = 0, a 5-point line H0 (line 16), no 4-point line: exact enumeration with per-line quotas.
For a line X in the pencil with k other lines, with h heavy off-H0 points and s points:
   doubles on X  db = k - 2(s - 1) + 14 - 2k ... = k + 16 - 2(s-1) - ... (derived below) ,
   triples on X  tr = (s - 1) - h - db.
(From Sum_{off}(m-1) = 16 - k and #off = s - 1.)  Every line other than H0 has s in {5,6,7} with
Sum (7 - s) = 13 - W.  Step 1: heavy sets (level-wise isomorph rejection), Step 2: line lengths,
Step 3: exact cover with quotas."""
import itertools, sys, json, collections, time
sys.path.insert(0, '../validate')
from canon import canon_many
k = tuple(int(c) for c in sys.argv[1]); assert len(k) == 5 and sum(k) == 16
H0 = 16
pen = [i for i, ki in enumerate(k) for _ in range(ki)]
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
base = [sorted([i for i in L if pen[i] == p] + [H0]) for p in range(5)]
base = [b for b in base if len(b) >= 3]
level = {'': []}; uniq = {canon_many(17, [base])[0]: []}
while level:
    nxt = {}
    for key, hs in level.items():
        used = set(p for S in hs for p in itertools.combinations(S, 2))
        w = sum(wt(S) for S in hs)
        exts = [hs + [S] for S in heavy_cands if w + wt(S) <= Wmax_off and not any(p in used for p in itertools.combinations(S, 2))]
        if not exts: continue
        for c, e in zip(canon_many(17, [base + [list(S) for S in e] for e in exts]), exts):
            if c not in uniq and c not in nxt: nxt[c] = e
    uniq.update(nxt); level = nxt
print(''.join(map(str, k)), 'W0', W0, 'heavy sets', len(uniq), file=sys.stderr, flush=True)
tri_all = list(transversals(3))
out = []
stats = collections.Counter()
t0 = time.time()
for hs in uniq.values():
    W = W0 + sum(wt(S) for S in hs)
    if W < 11: continue
    t5 = t5_0 + sum(1 for S in hs if len(S) == 5); t6 = t6_0 + sum(1 for S in hs if len(S) == 6)
    t2_off = 3 * W - 32 - t5 - 3 * t6 - b0
    if t2_off < 0: continue
    deficit = 13 - W
    hcount = [0] * 16; hexc = [0] * 16
    covered = set()
    for S in hs:
        for p in itertools.combinations(S, 2): covered.add(p)
        for x in S: hcount[x] += 1; hexc[x] += len(S) - 3
    # line lengths: distribute the deficit (each line 7, or 6 (-1), or 5 (-2))
    lens_options = []
    def dist(i, rem, cur):
        if i == 16:
            if rem == 0: lens_options.append(list(cur))
            return
        for d in (0, 1, 2):
            if d <= rem: cur.append(7 - d); dist(i + 1, rem - d, cur); cur.pop()
    dist(0, deficit, [])
    for lens in lens_options:
        # quotas: #off = s - 1 ; Sum_{off}(m - 1) = 16 - k ; heavy contribute (m-1) = 3 + (m-4)...
        db = [0] * 16; tr = [0] * 16; ok = True
        for x in L:
            noff = lens[x] - 1
            ki = k[pen[x]]
            # off points: h heavy, tr triples, db doubles; 2 tr + db + sum_heavy(m-1) = 16 - ki ; h + tr + db = noff
            # sum_heavy(m-1) = 2h + hexc
            # => tr + (tr + db) = 16 - ki - 2h - hexc ; tr + db = noff - h  => tr = 16 - ki - 2h - hexc - noff + h
            t = 16 - ki - hcount[x] - hexc[x] - noff
            d = noff - hcount[x] - t
            if t < 0 or d < 0: ok = False; break
            tr[x] = t; db[x] = d
        if not ok: continue
        if sum(db) != 2 * t2_off or sum(tr) % 3: continue
        stats['quota systems'] += 1
        # exact cover of the remaining pairs with quotas
        rem = [p for p in cross if p not in covered]
        cov = set(covered)
        tr_left = list(tr); db_left = list(db)
        chosen = []
        sols = []
        def rec():
            best = None; bo = None
            for p in rem:
                if p in cov: continue
                a, b = p
                opts = []
                if tr_left[a] > 0 and tr_left[b] > 0:
                    for z in L:
                        if tr_left[z] <= 0 or pen[z] == pen[a] or pen[z] == pen[b]: continue
                        if (min(a, z), max(a, z)) in cov or (min(b, z), max(b, z)) in cov: continue
                        opts.append(tuple(sorted((a, b, z))))
                dbl = db_left[a] > 0 and db_left[b] > 0
                nopt = len(opts) + (1 if dbl else 0)
                if nopt == 0: return
                if best is None or nopt < bo[0]:
                    best, bo = p, (nopt, opts, dbl)
                    if nopt == 1: break
            if best is None:
                sols.append(list(chosen)); return
            p = best
            for T in bo[1]:
                for q in itertools.combinations(T, 2): cov.add(q)
                for x in T: tr_left[x] -= 1
                chosen.append(T); rec(); chosen.pop()
                for x in T: tr_left[x] += 1
                for q in itertools.combinations(T, 2): cov.discard(q)
            if bo[2]:
                cov.add(p); db_left[p[0]] -= 1; db_left[p[1]] -= 1
                rec()
                db_left[p[0]] += 1; db_left[p[1]] += 1; cov.discard(p)
        rec()
        stats['solutions'] += len(sols)
        for sol in sols:
            out.append(base + [list(S) for S in hs] + [list(T) for T in sol])
print(''.join(map(str, k)), dict(stats), 'raw lattices', len(out), '%.0fs' % (time.time() - t0), file=sys.stderr, flush=True)
if out:
    u2 = {}
    for c, b in zip(canon_many(17, out), out): u2.setdefault(c, b)
    print(''.join(map(str, k)), 'distinct lattices', len(u2), file=sys.stderr, flush=True)
    for i, b in enumerate(u2.values()):
        print(json.dumps(dict(idx='%s_%d' % (''.join(map(str, k)), i), blocks=b)))
