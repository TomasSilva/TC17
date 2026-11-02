# Second exact pass on the lattices deferred by fast_real.py (2 unknowns u, v):
#   * 'res-nonconst': G(u) = gcd of v-resultants is nonconstant.  For every irreducible factor phi of
#     G, work in K = Q[u]/(phi): psi = gcd over K[v] of the equations; strip factors shared with bad
#     determinants; if psi is constant for every phi, there is no non-degenerate solution: NONREAL.
#   * 'commonfactor': all equations share a factor h(u, v).  Each irreducible factor of h is a curve
#     of solutions; it is degenerate iff some bad determinant is divisible by it.  If every factor is
#     degenerate, divide h out and redo the resultant analysis on the quotients.
# Everything else stays DEFER (handled by Macaulay2).
import sys, json, itertools, time
import flint
sys.argv_saved = list(sys.argv)
n = int(sys.argv[1]); IN = sys.argv[2]
OUT = IN.replace('.jsonl', '_pass2.out')
DEFER = IN.replace('.jsonl', '_pass2.jsonl')
sys.argv = [sys.argv[0], str(n), IN, '0', '1']
import importlib.util
spec = importlib.util.spec_from_file_location('fr', '/Users/agent/Projects/TC17/work/tc15/fast_real.py')
fr = importlib.util.module_from_spec(spec); spec.loader.exec_module(fr)


# ---------- arithmetic in K = Q[u]/(phi) and in K[v] ----------
class NF:
    def __init__(self, phi):
        self.phi = flint.fmpq_poly(phi) / flint.fmpq_poly([phi[phi.degree()]])   # monic

    def red(self, a):
        return a % self.phi

    def inv(self, a):
        g, s, t = a.xgcd(self.phi)
        assert g.degree() == 0 and g != 0
        return self.red(s / g)

    def mul(self, a, b):
        return (a * b) % self.phi


def kpoly_trim(A):
    while A and A[-1] == 0:
        A.pop()
    return A


def kpoly_mod(A, B, K):
    A = list(A)
    db = len(B) - 1
    inv_lead = K.inv(B[-1])
    while len(A) - 1 >= db and A:
        c = K.mul(A[-1], inv_lead)
        shift = len(A) - 1 - db
        for i in range(db + 1):
            A[shift + i] = K.red(A[shift + i] - K.mul(c, B[i]))
        kpoly_trim(A)
    return A


def kpoly_gcd(A, B, K):
    A, B = kpoly_trim(list(A)), kpoly_trim(list(B))
    while B:
        A, B = B, kpoly_mod(A, B, K)
    return A


def kpoly_div(A, B, K):
    """Exact quotient A / B (B divides A)."""
    A = list(A); Q = [flint.fmpq_poly([0])] * (len(A) - len(B) + 1)
    db = len(B) - 1
    inv_lead = K.inv(B[-1])
    while len(A) - 1 >= db and A:
        c = K.mul(A[-1], inv_lead)
        shift = len(A) - 1 - db
        Q[shift] = c
        for i in range(db + 1):
            A[shift + i] = K.red(A[shift + i] - K.mul(c, B[i]))
        kpoly_trim(A)
    return kpoly_trim(Q)


def to_Kv(f, K, uvar=0, vvar=1):
    """fmpz_mpoly f(u, v) -> polynomial in v with coefficients in K."""
    d = f.to_dict()
    degv = max((k[vvar] for k in d), default=-1)
    coeffs = []
    for j in range(degv + 1):
        c = {}
        for k, val in d.items():
            if k[vvar] == j:
                c[k[uvar]] = c.get(k[uvar], 0) + int(val)
        poly = flint.fmpq_poly([c.get(i, 0) for i in range(max(c) + 1)]) if c else flint.fmpq_poly([0])
        coeffs.append(K.red(poly))
    return kpoly_trim(coeffs)


def nondegenerate_solutions_over(phi, eqs, bad):
    """True iff the system has a solution (u0, v0) with phi(u0) = 0 and no bad determinant vanishing."""
    K = NF(phi)
    psi = None
    for f in eqs:
        A = to_Kv(f, K)
        if not A:
            continue
        psi = A if psi is None else kpoly_gcd(psi, A, K)
        if len(psi) == 1:
            return False
    if psi is None:
        return True          # every equation vanishes on u0: positive-dimensional -> defer (treated as realisable)
    for d in bad:
        D = to_Kv(d, K)
        if not D:
            return False     # a bad determinant vanishes identically above phi: all solutions degenerate?  no: it vanishes for every v -> every solution degenerate
        while True:
            g = kpoly_gcd(psi, D, K)
            if len(g) <= 1:
                break
            psi = kpoly_div(psi, g, K)
            if len(psi) == 1:
                return False
    return len(psi) > 1


def classify2(blocks, reason, ctx3, gens3):
    r = fr.setup(blocks, ctx3, gens3)
    nvar, P, eqs, bad = r
    eqs = [f for f in eqs if f != 0]
    if nvar != 2:
        return 'DEFER ' + reason
    u, v = gens3[0], gens3[1]
    # common factor handling
    h = eqs[0]
    for f in eqs[1:]:
        h = h.gcd(f)
    if h.total_degree() > 0:
        for fac, mult in h.factor()[1]:
            if fac.total_degree() == 0:
                continue
            if not any((d.gcd(fac) - fac == 0) or (d.gcd(fac) + fac == 0) for d in bad):
                return 'DEFER curve'          # a curve of solutions with no forced degeneracy
        eqs = [f // h for f in eqs]           # exact division
        eqs = [f for f in eqs if f != 0 and f.total_degree() > 0]
        if not eqs:
            return 'NONREAL curve-all-bad'
    G = None
    for i in range(min(len(eqs), 8)):
        for j in range(i + 1, min(len(eqs), 10)):
            R = eqs[i].resultant(eqs[j], 'u1')
            if R == 0:
                continue
            Ru = fr.univariate(R, 0)
            G = Ru if G is None else G.gcd(Ru)
            if G.degree() == 0:
                return 'NONREAL res2'
    if G is None:
        return 'DEFER commonfactor2'
    for phi, mult in G.factor()[1]:
        if phi.degree() <= 0:
            continue
        if nondegenerate_solutions_over(phi, eqs, bad):
            return 'DEFER real2 deg%d' % phi.degree()
    return 'NONREAL nf'


def run():
    ctx3 = flint.fmpz_mpoly_ctx.get(('u0', 'u1', 'u2'))
    gens3 = ctx3.gens()
    t0 = time.time()
    out = open(OUT, 'w'); defer = open(DEFER, 'w')
    stats = {}
    for k, line in enumerate(open(IN)):
        rec = json.loads(line)
        reason = rec.get('reason', '')
        try:
            res = classify2(rec['blocks'], reason, ctx3, gens3)
        except Exception as e:
            res = 'DEFER error %s' % type(e).__name__
        stats[res.split(' deg')[0]] = stats.get(res.split(' deg')[0], 0) + 1
        out.write('%d %s\n' % (rec.get('idx', k), res))
        if res.startswith('DEFER'):
            defer.write(json.dumps(rec) + '\n')
        if k % 20000 == 0:
            print(k, stats, '(%.0fs)' % (time.time() - t0), flush=True)
    out.write('ALLDONE\n'); out.close(); defer.close()
    print('FINAL %s (%.0fs)' % (stats, time.time() - t0), flush=True)


if __name__ == '__main__':
    run()
