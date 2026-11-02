"""Exact extension of a 1-dimensional family C of realisations of a 13-line core B.

All objects (line normals, points, candidate lines) are polynomial vectors in Q[T, Y] on the plane model
F(T, Y) = 0 of C (planemodel.py; for C = A^1 there is no Y and no F).  A polynomial g vanishes on C iff
Res_Y(F, g) = 0 (F irreducible); a fast filter evaluates at a random point x0 of C over F_p first
(g(x0) != 0 proves g != 0 on C).  The search is the exact search of extend.py run at the generic point
of C.  Every test "point R on candidate line N" that is not identically true can change the search only
at the zeros of g = N.R on C, i.e. at the roots T of Res_Y(F, g).  A zero matters only if:
  (a) N is a generic candidate at its node (excess in range): every such root;
  (b) N is too poor generically (excess below range): roots phi at which the points R with phi | Res
      bring enough excess (sum of m_R - 1 over them) to reach the range;
  (c) N too rich: never.
The returned special T-factors (irreducible over Q), together with the zeros of the scaling factors,
contain every point of C at which an extension exists that does not exist generically.  At each of them
the exact rigid search (extend.py) is run on the actual points of C (computed by Macaulay2)."""
import sys, json, itertools, collections, random, re
import flint
from extend import window_ok
from phicap import phi_reaches, CAP
P_ = None
class Curve:
    def __init__(self, pm, seed=1):
        self.ctx = flint.fmpq_mpoly_ctx.get(('T', 'Y'))
        self.T, self.Y = self.ctx.gens()
        self.kind = pm['kind']
        rnd = random.Random(seed)
        if self.kind == 'A1':
            self.F = None
        else:
            self.F = self.parse(pm['F'])
        # random point mod p
        while True:
            p = rnd.randrange(2 ** 28, 2 ** 29) | 1
            if not flint.fmpz(p).is_prime(): continue
            t0 = rnd.randrange(p)
            if self.F is None:
                self.p, self.x0 = p, (t0, 0); break
            fy = self.F.subs({'T': flint.fmpq(t0)}) if False else None
            # univariate in Y mod p
            coeffs = collections.defaultdict(int)
            for (et, ey), c in zip(self.F.monoms(), self.F.coeffs()):
                coeffs[ey] = (coeffs[ey] + int(c.p) * pow(int(c.q), -1, p) * pow(t0, et, p)) % p
            deg = max(coeffs) if coeffs else 0
            poly = flint.nmod_poly([coeffs.get(i, 0) for i in range(deg + 1)], p)
            if poly.degree() < 1: continue
            rts = [r for r, m in poly.roots() if m == 1]
            if rts:
                self.p, self.x0 = p, (t0, int(rts[0])); break
    def parse(self, s):
        s = s.replace('TT', 'T').replace('YY', 'Y').replace('^', '**')
        v = eval(s, {'T': self.T, 'Y': self.Y})
        if not isinstance(v, flint.fmpq_mpoly):
            v = self.ctx.from_dict({(0, 0): flint.fmpq(v) if not isinstance(v, flint.fmpq) else v})
        return v
    def ev(self, g):
        p = self.p; t0, y0 = self.x0
        acc = 0
        for (et, ey), c in zip(g.monoms(), g.coeffs()):
            acc = (acc + int(c.p) * pow(int(c.q) % p, -1, p) * pow(t0, et, p) * pow(y0, ey, p)) % p
        return acc
    def res(self, g):
        """univariate (in T) polynomial whose roots contain the T-coordinates of the zeros of g on C"""
        if self.F is None: return g
        return self.F.resultant(g, 'Y')
    def iszero(self, g):
        if g.is_zero(): return True
        if self.ev(g) != 0: return False
        return self.res(g).is_zero()
def realise_sym(C, rec, pm):
    """Exact line normals on C.  Vectors are kept as (N, D): the true vector is N / D (N a polynomial
    vector, D a polynomial), because the statements P_e = P_a + u_i P_b are not projectively invariant;
    only the final normals are used projectively (N, with the zeros of D added to the special points)."""
    ctx = C.ctx
    one = ctx.from_dict({(0, 0): 1}); zero = ctx.from_dict({})
    nv = max(rec['nvar'], 1)
    if pm['kind'] == 'A1':
        cs = [one]; ds = [C.T]
    else:
        cs = [C.parse(pm['U'][str(i)][0] if str(i) in pm['U'] else pm['U'][i][0]) for i in range(nv)]
        ds = [C.parse(pm['U'][str(i)][1] if str(i) in pm['U'] else pm['U'][i][1]) for i in range(nv)]
    P = {}
    fr = rec['frame']
    P[fr[0]] = ((one, zero, zero), one); P[fr[1]] = ((zero, one, zero), one)
    P[fr[2]] = ((zero, zero, one), one); P[fr[3]] = ((one, one, one), one)
    def cr(x, y):
        return (x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0])
    def simplify(N, D):
        g = D
        for c in N:
            if not c.is_zero(): g = g.gcd(c)
        if not g.is_constant():
            N = tuple(c / g if not c.is_zero() else c for c in N); D = D / g
        return (N, D)
    dens = []
    for st in rec['lines']:
        m = re.match(r'P(\d+) = cr\(cr\(P(\d+), P(\d+)\), cr\(P(\d+), P(\d+)\)\);', st)
        if m:
            e, a, b, c, d = map(int, m.groups())
            N = cr(cr(P[a][0], P[b][0]), cr(P[c][0], P[d][0])); D = P[a][1] * P[b][1] * P[c][1] * P[d][1]
            P[e] = simplify(N, D); continue
        m = re.match(r'P(\d+) = P(\d+) \+ u_(\d+) \* P(\d+);', st)
        if m:
            e, a, i, b = map(int, m.groups())
            (Na, Da), (Nb, Db) = P[a], P[b]
            N = tuple(Na[j] * cs[i] * Db + ds[i] * Da * Nb[j] for j in range(3)); D = Da * cs[i] * Db
            P[e] = simplify(N, D); continue
        m = re.match(r'P(\d+) = matrix\{\{u_(\d+), u_(\d+), 1_R\}\};', st)
        if m:
            e, i, j = map(int, m.groups())
            P[e] = simplify((ds[i] * cs[j], ds[j] * cs[i], cs[i] * cs[j]), cs[i] * cs[j]); continue
        raise ValueError(st)
    out = []
    for e in range(len(P)):
        N, D = P[e]
        dens.append(D)
        out.append(reduce_vec(N))
    return out, cs + dens
REMOVED = []
def reduce_vec(v):
    nz = [c for c in v if not c.is_zero()]
    if not nz: return v
    g = nz[0]
    for c in nz[1:]: g = g.gcd(c)
    if g.is_constant(): return v
    REMOVED.append(g)
    return tuple(c / g if not c.is_zero() else c for c in v)
def cross(x, y):
    return reduce_vec((x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0]))
def cross_raw(x, y):
    return (x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0])
def same_on_C(C, x, y):
    return all(C.iszero(c) for c in cross_raw(x, y))
def dot(x, y): return x[0] * y[0] + x[1] * y[1] + x[2] * y[2]
def keyp(C, v):
    p = C.p
    m = [C.ev(c) for c in v]
    for c in m:
        if c:
            inv = pow(c, -1, p); return tuple(x * inv % p for x in m)
    return None
def points_sym(C, lines):
    n = len(lines); pts = []; seen = set()
    for a in range(n):
        for b in range(a + 1, n):
            if (a, b) in seen: continue
            Q = cross(lines[a], lines[b])
            Ls = frozenset(x for x in range(n) if x in (a, b) or C.iszero(dot(lines[x], Q)))
            for x, y in itertools.combinations(sorted(Ls), 2): seen.add((x, y))
            pts.append((Q, Ls))
    return pts
def gsearch(C, lines, pts, budget, depth, found, special, stats, phicap=None):
    """generic search on C; special: set of univariate T-polynomials (relevant special factors)"""
    n = len(lines)
    stats['nodes'] += 1
    if stats['nodes'] > 1 and phi_reaches([L for Q, L in pts], n, phicap):
        stats['phipruned'] += 1; return
    if depth == 0:
        if budget == 0: found.append([sorted(L) for Q, L in pts])
        return
    s = collections.Counter()
    for Q, L in pts:
        for x in L: s[x] += 1
    cmax = min(8, budget - 2 * (depth - 1)); cmin = max(2, budget - 8 * (depth - 1))
    if cmax < cmin: return
    Elo, Ehi = n - cmax, n - cmin
    cand = {}
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if pts[i][1] & pts[j][1]: continue
            Nr = cross_raw(pts[i][0], pts[j][0])
            if all(C.iszero(c) for c in Nr): continue
            N = reduce_vec(Nr)
            k = keyp(C, N)
            if k is None:  # vanishes at x0 mod p: keep it under its own key
                k = ('deg', i, j)
            if k in cand:
                if any(same_on_C(C, N, M) for M, _, _ in cand[k]): continue
                cand[k].append((N, i, j))
            else:
                cand[k] = [(N, i, j)]
    for k, (N, i, j) in [(k, x) for k, xs in cand.items() for x in xs]:
        if any(same_on_C(C, N, X) for X in lines): continue
        on = []; off = []
        for t, (Q, L) in enumerate(pts):
            g = dot(N, Q)
            if C.iszero(g): on.append(t)
            else: off.append((t, g))
        covered = set(); okd = True
        for t in on:
            L = pts[t][1]
            if covered & L: okd = False; break
            covered |= L
        if not okd: continue
        E = sum(len(pts[t][1]) - 1 for t in on)
        if ALLSPECIAL:
            for t, g in off:
                rr = C.res(g)
                if not rr.is_zero(): special[str(rr)] = rr
        if E > Ehi: continue
        stats['tests'] += len(off)
        if E >= Elo:
            # (a): extra incidences that keep N admissible (an incidence pushing the excess above Ehi
            # only removes this branch at that point, it cannot create an extension there)
            for t, g in off:
                if pts[t][1] & covered: continue
                if E + len(pts[t][1]) - 1 > Ehi: continue
                rr = C.res(g); special[str(rr)] = rr
            # generic child?
            c = len(on) + n - len(covered)
            if any(len(pts[t][1]) > 5 for t in on): continue
            if any(s[x] + 1 > 8 for x in range(n) if x not in covered): continue
            newpts = []
            onset = set(on)
            for t, (Q, L) in enumerate(pts):
                newpts.append((Q, L | {n}) if t in onset else (Q, L))
            for x in range(n):
                if x not in covered:
                    newpts.append((cross(N, lines[x]), frozenset((x, n))))
            gsearch(C, lines + [N], newpts, budget - c, depth - 1, found, special, stats, phicap)
        else:
            need = Elo - E
            # (b): group the zeros of the R's by irreducible factor
            cand_R = [(t, g) for t, g in off if not (pts[t][1] & covered) and len(pts[t][1]) <= 5]
            if sum(len(pts[t][1]) - 1 for t, g in cand_R) < need: continue
            fac = collections.defaultdict(int)
            for t, g in cand_R:
                key = frozenset((id(pts[i][0]), id(pts[j][0]), id(pts[t][0])))
                ent = FACTOR_CACHE.get(key)
                fl = ent[1] if ent is not None else None
                if fl is None:
                    r = C.res(g)
                    stats['res'] += 1
                    fl = [] if (r.is_zero() or r.is_constant()) else [str(f) for f, mult in r.factor()[1]]
                    for f, mult in ([] if (r.is_zero() or r.is_constant()) else r.factor()[1]):
                        special_cache[str(f)] = f
                    FACTOR_CACHE[key] = ((pts[i][0], pts[j][0], pts[t][0]), fl)   # keeps the objects alive: ids stay unique
                else:
                    stats['cached'] += 1
                for fs in fl:
                    fac[fs] += len(pts[t][1]) - 1
            for fs, ex in fac.items():
                if ex >= need: special[fs] = special_cache[fs]
special_cache = {}
ALLSPECIAL = False
FACTOR_CACHE = {}
if __name__ == '__main__':
    import time
    from planemodel import plane_model
    IN, OUT = sys.argv[1], sys.argv[2]
    part, nparts = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, 1)
    with open(OUT, 'w') as out:
        for li, line in enumerate(open(IN)):
            if li % nparts != part: continue
            rec = json.loads(line)
            for ci, comp in enumerate(rec.get('comps', [])):
                if comp['dim'] != 1: continue
                t0 = time.time()
                pm = plane_model(rec['nvar'], comp['gens'], tag='%d_%d' % (li, ci))
                res = dict(idx=rec['idx'], comp=ci, pm=pm)
                if pm['kind'] not in ('A1', 'plane'):
                    res['status'] = 'NOMODEL'; out.write(json.dumps(res) + '\n'); out.flush(); continue
                C = Curve(pm)
                REMOVED.clear(); special_cache.clear()
                lines, cs = realise_sym(C, rec, pm)
                pts = points_sym(C, lines)
                blocks_ok = sorted(sorted(L) for Q, L in pts if len(L) >= 3) == sorted(sorted(b) for b in rec['blocks'])
                b2 = sum(len(L) - 1 for Q, L in pts)
                found = []; special = {}; stats = collections.Counter()
                gsearch(C, lines, pts, 80 - b2, 4, found, special, stats)
                # scaling denominators and removed gcds
                for c in cs + REMOVED:
                    if not c.is_constant():
                        r = C.res(c)
                        if not r.is_zero() and not r.is_constant(): special[str(r)] = r
                # factor specials into irreducible univariate factors in T
                facs = {}
                for r in special.values():
                    if r.is_constant(): continue
                    for f, mult in r.factor()[1]:
                        if f.degrees()[1] == 0 and not f.is_constant(): facs[str(f)] = f
                res.update(status='OK', lattice_ok=blocks_ok, generic_L=found, nodes=stats['nodes'], tests=stats['tests'],
                           resultants=stats['res'], special=[str(f) for f in facs.values()], time=round(time.time() - t0, 1))
                out.write(json.dumps(res) + '\n'); out.flush()
