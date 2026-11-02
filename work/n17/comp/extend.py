"""Geometric extension of a rigid realisation of a 13-line core B to 17-line window lattices.

Input: jsonl from m2comp.py (lattice blocks, parametrisation statements, components with shape-lemma
representation u_i = g_i(T), f(T) = 0).  For every 0-dimensional component, the realisation of B over
K = Q[T]/(f) is rebuilt exactly; every element carries its exact value (fmpq_poly mod f) and its image
mod a prime p at a simple root r of f (a ring homomorphism on the p-integral elements we use: no division
is ever performed).  A value is zero iff it is zero mod p AND exactly zero; nonzero mod p is a proof of
nonzero, and zero mod p is confirmed exactly.  So all incidences are exact.

Search: add 4 lines, each through >= 2 multiple points of the current arrangement (complete by Lemma 5:
c_i + i <= 12 for every deletion order), with sum of point counts = 80 - b2(B), every line ending with
4..8 points and every point with multiplicity <= 6.  Output: every 17-line lattice L found (canonical
block list) with the component index; window conditions on L are checked at the end.
usage: extend.py comp.jsonl part nparts out.jsonl"""
import sys, json, itertools, random, collections
import flint
from phicap import phi_reaches, CAP
P_ = (1 << 61) - 1
def parse_list(s):
    s = s.strip().strip('{}')
    return [flint.fmpq(*map(int, x.split('/'))) if '/' in x else flint.fmpq(int(x)) for x in s.split(',')] if s else []
def modp(q, p):
    return (int(q.p) % p) * pow(int(q.q) % p, -1, p) % p
class Field:
    def __init__(self, fco):
        self.f = flint.fmpq_poly(fco)
        self.d = self.f.degree()
        # choose a prime with a simple root of f, all coefficients p-integral
        rnd = random.Random(12345)
        while True:
            p = rnd.randrange(2 ** 29, 2 ** 30) | 1
            if not flint.fmpz(p).is_prime(): continue
            if any(int(c.q) % p == 0 for c in self.f.coeffs()): continue
            fp = flint.nmod_poly([modp(c, p) for c in self.f.coeffs()], p)
            if fp.degree() != self.d: continue
            roots = [r for r, m in fp.roots() if m == 1]
            if roots:
                self.p = p; self.r = int(roots[0]); break
    def elt(self, poly):   # fmpq_poly -> (exact, modp)
        poly = poly % self.f
        return (poly, self.ev(poly))
    def ev(self, poly):
        p, r = self.p, self.r
        acc = 0
        for c in reversed(poly.coeffs()):
            acc = (acc * r + modp(c, p)) % p
        return acc
    def const(self, q):
        return (flint.fmpq_poly([q]), modp(flint.fmpq(q), self.p))
    def add(self, a, b): return ((a[0] + b[0]), (a[1] + b[1]) % self.p)
    def sub(self, a, b): return ((a[0] - b[0]), (a[1] - b[1]) % self.p)
    def mul(self, a, b): return ((a[0] * b[0]) % self.f, (a[1] * b[1]) % self.p)
    def iszero(self, a):
        if a[1] != 0: return False
        return (a[0] % self.f) == 0
def cross(F, x, y):
    return (F.sub(F.mul(x[1], y[2]), F.mul(x[2], y[1])),
            F.sub(F.mul(x[2], y[0]), F.mul(x[0], y[2])),
            F.sub(F.mul(x[0], y[1]), F.mul(x[1], y[0])))
def dot(F, x, y):
    return F.add(F.add(F.mul(x[0], y[0]), F.mul(x[1], y[1])), F.mul(x[2], y[2]))
def dotp(F, x, y):
    p = F.p
    return (x[0][1] * y[0][1] + x[1][1] * y[1][1] + x[2][1] * y[2][1]) % p
def iszerovec(F, v): return all(F.iszero(c) for c in v)
def keyp(F, v):
    """normalised mod-p key of a projective vector"""
    p = F.p
    m = [c[1] for c in v]
    for c in m:
        if c:
            inv = pow(c, -1, p); return tuple(x * inv % p for x in m)
    return None
def realise(F, rec, comp):
    gs = [flint.fmpq_poly(parse_list(g)) for g in comp['g']]
    u = [F.elt(g) for g in gs]
    one, zero = F.const(1), F.const(0)
    P = {}
    fr = rec['frame']
    P[fr[0]] = (one, zero, zero); P[fr[1]] = (zero, one, zero); P[fr[2]] = (zero, zero, one); P[fr[3]] = (one, one, one)
    import re
    for st in rec['lines']:
        m = re.match(r'P(\d+) = cr\(cr\(P(\d+), P(\d+)\), cr\(P(\d+), P(\d+)\)\);', st)
        if m:
            e, a, b, c, d = map(int, m.groups())
            P[e] = cross(F, cross(F, P[a], P[b]), cross(F, P[c], P[d])); continue
        m = re.match(r'P(\d+) = P(\d+) \+ u_(\d+) \* P(\d+);', st)
        if m:
            e, a, i, b = map(int, m.groups())
            P[e] = tuple(F.add(P[a][j], F.mul(u[i], P[b][j])) for j in range(3)); continue
        m = re.match(r'P(\d+) = matrix\{\{u_(\d+), u_(\d+), 1_R\}\};', st)
        if m:
            e, i, j = map(int, m.groups())
            P[e] = (u[i], u[j], one); continue
        raise ValueError(st)
    return [P[e] for e in range(len(P))]
def points_of(F, lines):
    """multiple points: dict key -> (coords, frozenset of lines)"""
    n = len(lines)
    pts = []
    seen = set()
    for a in range(n):
        for b in range(a + 1, n):
            if (a, b) in seen: continue
            Q = cross(F, lines[a], lines[b])
            Ls = frozenset(x for x in range(n) if (x in (a, b)) or (dotp(F, lines[x], Q) == 0 and F.iszero(dot(F, lines[x], Q))))
            for x, y in itertools.combinations(sorted(Ls), 2): seen.add((x, y))
            pts.append((Q, Ls))
    return pts
def lattice_blocks(pts):
    return sorted(sorted(L) for Q, L in pts if len(L) >= 3)
NODES = collections.Counter()
COLLISIONS = [0]
def search(F, lines, pts, budget, depth, found, added, visited, phicap=None, avecs=None):
    """visited: dict {frozenset of mod-p keys of the added lines: {key: exact line}}.  A key match is
    accepted as a repetition only after the lines are compared exactly (audit F3, 23 Oct 2026)."""
    if not isinstance(visited, dict): raise TypeError('visited must be a dict (exact memoisation)')
    if avecs is None: avecs = []
    n = len(lines)
    NODES[n - 13] += 1
    if added and phi_reaches([L for Q, L in pts], n, phicap): return
    if depth == 0:
        if budget == 0: found.append((tuple(added), [list(sorted(L)) for Q, L in pts]))
        return
    s = collections.Counter()
    for Q, L in pts:
        for x in L: s[x] += 1
    cmax = min(8, budget - 2 * (depth - 1)); cmin = max(2, budget - 8 * (depth - 1))
    if cmax < cmin: return
    cand = {}
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if pts[i][1] & pts[j][1]: continue
            N = cross(F, pts[i][0], pts[j][0])
            k = keyp(F, N)
            if k is None:
                if iszerovec(F, N): continue
                k = ('deg', i, j)
            if k in cand:
                if any(iszerovec(F, cross(F, N, M)) for M in cand[k]): continue
                cand[k].append(N)
            else:
                cand[k] = [N]
    lkeys = set(keyp(F, X) for X in lines)
    for k, N, coll in [(k, N, len(Ns) > 1) for k, Ns in cand.items() for N in Ns]:
        if k in lkeys:
            if any(iszerovec(F, cross(F, N, X)) for X in lines): continue
        T = [t for t, (Q, L) in enumerate(pts) if dotp(F, N, Q) == 0 and F.iszero(dot(F, N, Q))]
        if len(T) < 2: continue
        covered = set()
        okd = True
        for t in T:
            L = pts[t][1]
            if covered & L: okd = False; break
            covered |= L
            if len(L) > 5: okd = False; break
        if not okd: continue
        c = len(T) + n - len(covered)
        if not (cmin <= c <= cmax): continue
        if any(s[x] + 1 > 8 for x in range(n) if x not in covered): continue
        if coll:
            COLLISIONS[0] += 1          # distinct lines with equal mod-p key: explore without memoisation
            kk = (k, id(N))
        else:
            kk = k
            st = frozenset(added + [k])
            if len(st) == len(added) + 1:
                cur = dict(zip(added, avecs)); cur[k] = N
                prev = visited.get(st)
                if prev is not None:
                    if all(iszerovec(F, cross(F, prev[x], cur[x])) for x in st): continue
                    COLLISIONS[0] += 1      # equal mod-p keys of different line sets: explore
                else:
                    visited[st] = cur
            else:
                COLLISIONS[0] += 1          # two added lines with the same key: explore without memoisation
        newpts = []
        Tset = set(T)
        for t, (Q, L) in enumerate(pts):
            newpts.append((Q, L | {n}) if t in Tset else (Q, L))
        for x in range(n):
            if x not in covered:
                newpts.append((cross(F, N, lines[x]), frozenset((x, n))))
        search(F, lines + [N], newpts, budget - c, depth - 1, found, added + [kk], visited, phicap, avecs + [N])
def window_ok(blocks17):
    pts = [frozenset(b) for b in blocks17]
    s = collections.Counter()
    for P in pts:
        for x in P: s[x] += 1
    if any(not (4 <= s[x] <= 8) for x in range(17)): return False, 'linelen'
    if any(len(P) > 6 for P in pts): return False, 'mult'
    if sum(len(P) - 1 for P in pts) != 80: return False, 'b2'
    for x in range(17):
        if s[x] == 8 and not any(len(P) == 2 and x in P for P in pts): return False, '8-line without double point'
    nd = 0
    big = [P for P in pts if len(P) >= 3]
    for P, Q in itertools.combinations(big, 2):
        if not (P & Q):
            sg = len(P) + len(Q) - 2
            if sg > 8: return False, 'W5'
            if sg == 8: nd += 1
    if nd > 4: return False, 'Dpairs'
    return True, ''
if __name__ == '__main__':
    IN, part, nparts, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    stats = collections.Counter()
    with open(OUT, 'w') as out:
        for li, line in enumerate(open(IN)):
            if li % nparts != part: continue
            rec = json.loads(line)
            if rec.get('status') != 'REAL': continue
            nl = len(rec['lines']) + 4
            b2 = sum(len(b) - 1 for b in rec['blocks']) + (nl * (nl - 1) // 2 - sum(len(b) * (len(b) - 1) // 2 for b in rec['blocks']))
            for ci, comp in enumerate(rec['comps']):
                slice_ = False
                if comp['dim'] != 0:
                    stats['family'] += 1; out.write(json.dumps(dict(idx=rec['idx'], comp=ci, family=True, dim=comp['dim'])) + '\n')
                    if 'slice_g' not in comp: continue
                    comp = dict(comp, f=comp['slice_f'], g=comp['slice_g']); slice_ = True
                if 'g' not in comp: stats['noshape'] += 1; out.write(json.dumps(dict(idx=rec['idx'], comp=ci, noshape=True)) + '\n'); continue
                F = Field(parse_list(comp['f']))
                lines = realise(F, rec, comp)
                pts = points_of(F, lines)
                # sanity: realised lattice equals B
                if lattice_blocks(pts) != sorted(sorted(b) for b in rec['blocks']):
                    stats['lattice-mismatch'] += 1; out.write(json.dumps(dict(idx=rec['idx'], comp=ci, mismatch=True)) + '\n'); continue
                found = []
                NODES.clear()
                search(F, lines, pts, 80 - b2, 17 - len(lines), found, [], {}, CAP.get(str(rec['idx']).split(':')[0]))
                if slice_: out.write(json.dumps(dict(idx=rec['idx'], comp=ci, slice_nodes=dict(NODES))) + '\n')
                Ls = {}
                for keys, blocks in found:
                    key = tuple(sorted(tuple(b) for b in blocks))
                    Ls[key] = blocks
                nwin = 0
                for key, blocks in Ls.items():
                    ok, why = window_ok(blocks)
                    if ok:
                        nwin += 1
                        out.write(json.dumps(dict(idx=rec['idx'], comp=ci, slice=slice_, L=[b for b in blocks if len(b) >= 3])) + '\n')
                    else:
                        stats['reject ' + why] += 1
                        out.write(json.dumps(dict(idx=rec['idx'], comp=ci, slice=slice_, L_rejected=[b for b in blocks if len(b) >= 3], why=why)) + '\n')
                # one record per component, written when it is finished (audit F4)
                out.write(json.dumps(dict(idx=rec['idx'], comp=ci, slice=slice_, done=True, found=len(Ls), window=nwin, nodes=sum(NODES.values()))) + '\n')
                stats['slices' if slice_ else 'comps'] += 1; stats['ext found'] += len(Ls); stats['window L'] += nwin
                if slice_ and Ls: stats['slices with extensions'] += 1
                out.flush()
    stats['key collisions'] = COLLISIONS[0]
    print(dict(stats))
