# Exact, fast realisability pre-filter for abstract rank-3 lattices (blocks on n elements), using
# python-flint.  Frame-fixed parametrisation as in exact_tc_lattice.py (dual points = lines).
#   0 unknowns: all incidence equations are rational numbers -> exact decision.
#   1 unknown u: I = (g), g = gcd of the equations in Z[u]; bad (forbidden-collinearity) factors are
#               removed from g by repeated gcds; NONREAL iff what remains is constant.
#   2 unknowns u, v: G(u) = gcd of the v-resultants of pairs of equations; every solution has u a
#               root of G, so G constant => NONREAL.  Otherwise, or with >= 3 unknowns, DEFER to M2.
# Any bad determinant that vanishes identically => NONREAL.  Realisable lattices are DEFERred too
# (their freeness is decided by Macaulay2).  Output: one line per lattice: NONREAL / DEFER <reason>.
import sys, json, itertools, time
import flint

n = int(sys.argv[1]); IN = sys.argv[2]; part = int(sys.argv[3]); nparts = int(sys.argv[4])
OUT = IN.replace('.jsonl', '_fast_%d.out' % part)
DEFER = IN.replace('.jsonl', '_defer_%d.jsonl' % part)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def det3(a, b, c):
    return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])


def setup(blocks, ctx, gens):
    """Returns (nvar, points dict, eqs, bad) with symbolic coordinates in ctx (fmpz_mpoly)."""
    blocks = [tuple(B) for B in blocks]
    inblock = {}
    for B in blocks:
        for p in itertools.combinations(sorted(B), 2):
            inblock[p] = B

    def block_of(a, b):
        return inblock.get((min(a, b), max(a, b)))

    def collinear(a, b, c):
        B = block_of(a, b)
        return B is not None and c in B
    frame = next(f for f in itertools.combinations(range(n), 4)
                 if not any(collinear(*t) for t in itertools.combinations(f, 3)))
    one, zero = ctx.from_dict({(0,) * ctx.nvars(): 1}), ctx.from_dict({})
    P = {frame[0]: (one, zero, zero), frame[1]: (zero, one, zero), frame[2]: (zero, zero, one), frame[3]: (one, one, one)}
    nvar = 0
    order = list(frame)
    todo = [e for e in range(n) if e not in P]
    while todo:
        best = None
        for e in todo:
            det_lines = []
            for B in blocks:
                if e in B:
                    D = [x for x in B if x in P]
                    if len(D) >= 2:
                        det_lines.append((D[0], D[1]))
            if best is None or len(det_lines) > best[1]:
                best = (e, len(det_lines), det_lines)
        e, score, det_lines = best
        todo.remove(e); order.append(e)
        if score >= 2:
            (a1, b1), (a2, b2) = det_lines[0], det_lines[1]
            P[e] = cross(cross(P[a1], P[b1]), cross(P[a2], P[b2]))
        elif score == 1:
            if nvar >= len(gens):
                return None
            a1, b1 = det_lines[0]
            g = gens[nvar]; nvar += 1
            P[e] = tuple(P[a1][i] + g * P[b1][i] for i in range(3))
        else:
            if nvar + 1 >= len(gens):
                return None
            P[e] = (gens[nvar], gens[nvar + 1], one); nvar += 2
    eqs = []
    for B in blocks:
        Bs = sorted(B, key=lambda x: order.index(x))
        for c in Bs[2:]:
            eqs.append(det3(P[Bs[0]], P[Bs[1]], P[c]))
    bad = []
    for t in itertools.combinations(range(n), 3):
        if not collinear(*t):
            bad.append(det3(P[t[0]], P[t[1]], P[t[2]]))
    return nvar, P, eqs, bad


def univariate(f, var):
    """fmpz_mpoly in one effective variable -> fmpz_poly."""
    d = f.to_dict()
    deg = max((k[var] for k in d), default=-1)
    coeffs = [0] * (deg + 1)
    for k, c in d.items():
        coeffs[k[var]] += int(c)
    return flint.fmpz_poly(coeffs)


def strip_bad(g, bads):
    """Remove from g in Z[u] all factors shared with any bad polynomial."""
    for d in bads:
        if d == 0:
            continue
        while True:
            h = g.gcd(d)
            if h.degree() <= 0:
                break
            g = g // h
    return g


def classify(blocks, ctx3, gens3):
    r = setup(blocks, ctx3, gens3)
    if r is None:
        return 'DEFER nvar>=3'
    nvar, P, eqs, bad = r
    if any(b == 0 for b in bad):
        return 'NONREAL zerobad'
    eqs = [f for f in eqs if f != 0]
    if nvar == 0:
        return 'NONREAL const' if eqs else 'DEFER real0'
    if nvar == 1:
        if not eqs:
            return 'DEFER dim1'
        g = univariate(eqs[0], 0)
        for f in eqs[1:]:
            g = g.gcd(univariate(f, 0))
            if g.degree() == 0:
                return 'NONREAL gcd1'
        g = strip_bad(g, [univariate(b, 0) for b in bad])
        return 'NONREAL allbad1' if g.degree() == 0 else 'DEFER real1'
    if nvar == 2:
        if len(eqs) < 2:
            return 'DEFER dim2'
        G = None
        for i in range(min(len(eqs), 6)):
            for j in range(i + 1, min(len(eqs), 8)):
                R = eqs[i].resultant(eqs[j], 'u1')
                if R == 0:
                    continue
                Ru = univariate(R, 0)
                G = Ru if G is None else G.gcd(Ru)
                if G.degree() == 0:
                    return 'NONREAL res'
        if G is None:
            return 'DEFER commonfactor'
        return 'DEFER res-nonconst'
    return 'DEFER nvar>=3'


def run():
    ctx3 = flint.fmpz_mpoly_ctx.get(('u0', 'u1', 'u2'))
    gens3 = ctx3.gens()
    t0 = time.time()
    out = open(OUT, 'w'); defer = open(DEFER, 'w')
    stats = {}
    with open(IN) as f:
        for i, line in enumerate(f):
            if i % nparts != part:
                continue
            rec = json.loads(line)
            res = classify(rec['blocks'], ctx3, gens3)
            stats[res] = stats.get(res, 0) + 1
            out.write('%d %s\n' % (i, res))
            if res.startswith('DEFER'):
                rec['idx'] = i; defer.write(json.dumps(rec) + '\n')
            if (i // nparts) % 20000 == 0:
                print(i, stats, '(%.0fs)' % (time.time() - t0), flush=True)
    out.write('ALLDONE\n'); out.close(); defer.close()
    print('FINAL part %d %s (%.0fs)' % (part, stats, time.time() - t0), flush=True)


if __name__ == '__main__':
    run()
