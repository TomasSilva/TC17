"""Independent numeric re-implementation of the rigid extension search (audit, 22 Oct 2026).

For a zero-dimensional component of R(B) (shape lemma u_i = g_i(T), f(T) = 0), one complex root of f is
taken (Galois conjugates give isomorphic arrangements), the 13..16 line normals are computed in 50-digit
arithmetic from the parametrisation statements and then rounded to double precision.  The search adds
lines through two intersection points, one at a time, up to 17 lines, with
  - every point of multiplicity <= 6, every line with <= 8 points (counts only grow),
  - b2 reaching 80 exactly (each added line raises b2 by its number of points),
  - the phi cap of the class (a 4-set S with sum_{H in S}(s_H - 7) - f(S) >= cap is pruned),
written from these definitions, not from extend.py.  Incidences are decided by |N.Q| / (|N| |Q|) < 1e-9
(zero) or > 1e-6 (nonzero); values in between are recomputed in 50 digits and counted.
Output per component: the 17-line lattices found (blocks of size >= 3).
usage: indep_rigid.py records.jsonl out.jsonl"""
import sys, json, itertools, collections, re
import numpy as np, mpmath
mpmath.mp.dps = 50
CAP = {'b48': None, 'b49': 4, 'b50': 3, 'b51': 2}
STATS = collections.Counter()
def q(s):
    s = s.strip()
    if '/' in s:
        a, b = s.split('/'); return mpmath.mpf(int(a)) / int(b)
    return mpmath.mpf(int(s))
def plist(s):
    s = s.strip().strip('{}')
    return [q(x) for x in s.split(',')] if s.strip() else []
def mcross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def realise(rec, comp):
    f = plist(comp['f']); gs = [plist(g) for g in comp['g']]
    roots = mpmath.polyroots(f[::-1], maxsteps=400, extraprec=200)
    r = roots[0]
    u = [sum(c * r ** j for j, c in enumerate(g)) for g in gs]
    one, zero = mpmath.mpc(1), mpmath.mpc(0)
    P = {}
    fr = rec['frame']
    P[fr[0]] = [one, zero, zero]; P[fr[1]] = [zero, one, zero]; P[fr[2]] = [zero, zero, one]; P[fr[3]] = [one, one, one]
    for st in rec['lines']:
        m = re.match(r'P(\d+) = cr\(cr\(P(\d+), P(\d+)\), cr\(P(\d+), P(\d+)\)\);', st)
        if m:
            e, a, b, c, d = map(int, m.groups()); P[e] = mcross(mcross(P[a], P[b]), mcross(P[c], P[d])); continue
        m = re.match(r'P(\d+) = P(\d+) \+ u_(\d+) \* P(\d+);', st)
        if m:
            e, a, i, b = map(int, m.groups()); P[e] = [P[a][j] + u[i] * P[b][j] for j in range(3)]; continue
        m = re.match(r'P(\d+) = matrix\{\{u_(\d+), u_(\d+), 1_R\}\};', st)
        if m:
            e, i, j = map(int, m.groups()); P[e] = [u[i], u[j], one]; continue
        raise ValueError(st)
    out = []
    for e in range(len(P)):
        v = P[e]; nr = mpmath.sqrt(sum(abs(c) ** 2 for c in v))
        out.append(np.array([complex(c / nr) for c in v]))
    return out
def unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v
def inc(N, Q):
    """True iff the point Q lies on the line N (both unit vectors)."""
    x = abs(np.dot(N, Q))
    if x < 1e-9: return True
    if x > 1e-6: return False
    STATS['ambiguous incidence'] += 1
    return x < 1e-7
def points(lines):
    n = len(lines); pts = []; seen = set()
    for a in range(n):
        for b in range(a + 1, n):
            if (a, b) in seen: continue
            Q = unit(np.cross(lines[a], lines[b]))
            Ls = frozenset([a, b] + [x for x in range(n) if x not in (a, b) and inc(lines[x], Q)])
            for x, y in itertools.combinations(sorted(Ls), 2): seen.add((x, y))
            pts.append((Q, Ls))
    return pts
def phi_reaches(pts, n, cap):
    if cap is None: return False
    s = collections.Counter(x for Q, L in pts for x in L)
    for S in itertools.combinations(range(n), 4):
        Sset = set(S)
        w = sum(s[x] - 7 for x in S) - sum(1 for Q, L in pts if L <= Sset)
        if w >= cap: return True
    return False
def key(N):
    i = int(np.argmax(np.abs(N))); v = N / N[i]
    return tuple(np.round(np.concatenate([v.real, v.imag]), 6))
def search(lines, pts, budget, depth, found, added, memo, cap):
    n = len(lines)
    STATS['nodes'] += 1
    if added and phi_reaches(pts, n, cap): return
    if depth == 0:
        if budget == 0: found.append(sorted(sorted(L) for Q, L in pts if len(L) >= 3))
        return
    s = collections.Counter(x for Q, L in pts for x in L)
    cands = {}
    for (Qi, Li), (Qj, Lj) in itertools.combinations(pts, 2):
        if Li & Lj: continue
        N = unit(np.cross(Qi, Qj))
        k = key(N)
        if k in cands: continue
        cands[k] = N
    for k, N in cands.items():
        T = [t for t, (Q, L) in enumerate(pts) if inc(N, Q)]
        Ls = [pts[t][1] for t in T]
        cov = set().union(*Ls)
        if sum(len(L) for L in Ls) != len(cov): continue          # two points of an existing line: N is that line
        if any(len(L) >= 6 for L in Ls): continue                 # multiplicity would exceed 6
        c = len(T) + (n - len(cov))                                  # points on N after adding it
        rest = depth - 1
        if c < 2 or c > 8 or budget - c < 2 * rest or budget - c > 8 * rest: continue
        if any(s[x] >= 8 for x in range(n) if x not in cov): continue   # a new point on a full line
        mk = frozenset(added + [k])
        if mk in memo: continue
        memo.add(mk)
        newpts = [(Q, L | {n}) if t in set(T) else (Q, L) for t, (Q, L) in enumerate(pts)]
        newpts += [(unit(np.cross(N, lines[x])), frozenset((x, n))) for x in range(n) if x not in cov]
        search(lines + [N], newpts, budget - c, depth - 1, found, added + [k], memo, cap)
if __name__ == '__main__':
    IN, OUT = sys.argv[1], sys.argv[2]
    with open(OUT, 'w') as out:
        for line in open(IN):
            rec = json.loads(line)
            if rec.get('status') != 'REAL': continue
            cap = CAP.get(str(rec['idx']).split(':')[0])
            for ci, comp in enumerate(rec['comps']):
                if comp['dim'] != 0 or 'g' not in comp: continue
                STATS.clear()
                try:
                    lines = realise(rec, comp)
                    pts = points(lines)
                    ok = sorted(sorted(L) for Q, L in pts if len(L) >= 3) == sorted(sorted(b) for b in rec['blocks'])
                    found = []
                    if ok:
                        b2 = sum(len(L) - 1 for Q, L in pts)
                        search(lines, pts, 80 - b2, 17 - len(lines), found, [], set(), cap)
                    res = dict(idx=rec['idx'], comp=ci, lattice_ok=ok, found=[json.loads(x) for x in sorted(set(json.dumps(L) for L in found))], stats=dict(STATS))
                except Exception as e:
                    res = dict(idx=rec['idx'], comp=ci, error=repr(e)[:200])
                out.write(json.dumps(res) + '\n'); out.flush()
        out.write(json.dumps(dict(ALLDONE=IN)) + '\n')
