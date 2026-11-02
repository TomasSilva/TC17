"""Lattice-level step for cores whose realisation space has a component of dimension >= 2.
Every window lattice L over such a core B is reached by first adding one line N (through >= 2 multiple
points of B, Lemma 5).  We enumerate the lattices B + N combinatorially: N is given by the set T of
multiple points of B it passes through (pairwise without common line, multiplicity <= 5), its point count
c = |T| + n - sum_T m must fit the budget, and no line may exceed 8 points.  Children with a 4-set of
phi >= cap (class threshold) are dropped (they are reached from a lower class).  The children (n + 1
lines) are deduplicated up to isomorphism and written as jsonl for the fast filters / m2compb / extend /
famrun / dim2gen pipeline.
usage: dim2gen.py records.jsonl out.jsonl"""
import sys, json, itertools, collections
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/validate')
from canon import canon_many
from phicap import phi_reaches, CAP
def pts_of(n, blocks):
    cov = set(); pts = []
    for b in blocks:
        b = frozenset(b); pts.append(b)
        for q in itertools.combinations(sorted(b), 2): cov.add(q)
    for q in itertools.combinations(range(n), 2):
        if q not in cov: pts.append(frozenset(q))
    return pts
def children(n, blocks, cls):
    pts = pts_of(n, blocks)
    b2 = sum(len(P) - 1 for P in pts)
    budget = 80 - b2; depth = 17 - n
    cmax = min(8, budget - 2 * (depth - 1)); cmin = max(2, budget - 8 * (depth - 1))
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
    out = []
    for T in res:
        Tset = set(T)
        newpts = [P | {n} if P in Tset else P for P in pts]
        covered = set().union(*T)
        newpts += [frozenset((x, n)) for x in range(n) if x not in covered]
        if phi_reaches(newpts, n + 1, CAP.get(cls)): continue
        out.append(sorted(sorted(P) for P in newpts if len(P) >= 3))
    return out
if __name__ == '__main__':
    IN, OUT = sys.argv[1], sys.argv[2]
    allc = []
    for l in open(IN):
        r = json.loads(l)
        n = len(r['lines']) + 4 if 'lines' in r else 1 + max(x for b in r['blocks'] for x in b)
        cls = str(r['idx']).split(':')[0]
        for ch in children(n, r['blocks'], cls):
            allc.append((r['idx'], n + 1, ch))
    by_n = collections.defaultdict(list)
    for p, n1, ch in allc: by_n[n1].append((p, ch))
    with open(OUT, 'w') as f:
        for n1, items in by_n.items():
            cs = canon_many(n1, [ch for p, ch in items])
            seen = {}
            for (p, ch), c in zip(items, cs):
                if c in seen: continue
                seen[c] = 1
                cls = str(p).split(':')[0]
                f.write(json.dumps(dict(idx='%s:%s/%d' % (cls, str(p).split(':', 1)[-1], len(seen)), blocks=ch, n=n1, parent=p)) + '\n')
            print('n=%d children %d distinct %d' % (n1, len(items), len(seen)), file=sys.stderr)
