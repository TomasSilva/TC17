"""Corrected two-parameter branch of fast_real.py / fast_real2.py (not committed).
Flaw: eqs[i].resultant(eqs[j], 'u1') is 1 when both equations are free of u1, so the gcd G became
constant and the lattice was declared NONREAL although u0 may be a common root of the two
univariate equations.  Fix: an equation free of u1 is itself a univariate condition on u0 and
enters G directly; resultants are only taken for pairs in which both equations involve u1.
Everything else is identical to the original code."""
import sys, json, time, flint
ARGV = list(sys.argv)
NLINES = ARGV[1] if len(ARGV) > 1 and ARGV[1].isdigit() else '15'
sys.argv = ['fast_real.py', NLINES, '/dev/null', '0', '1']
import importlib.util
HERE = '/Users/agent/Projects/TC17/work/tc15/'
spec = importlib.util.spec_from_file_location('fr', HERE + 'fast_real.py')
fr = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(fr)
except SystemExit:
    pass
spec2 = importlib.util.spec_from_file_location('fr2', HERE + 'fast_real2.py')
fr2 = importlib.util.module_from_spec(spec2)
try:
    spec2.loader.exec_module(fr2)
except SystemExit:
    pass


def gcd_of_conditions(eqs, imax, jmax):
    """G(u0): gcd of the u1-free equations (as univariate polynomials) and of the u1-resultants of
    pairs of equations both involving u1, over the same index ranges as the original loops.
    Returns (G, found) where found says whether any condition was collected."""
    G = None
    for i in range(min(len(eqs), imax)):
        fi = eqs[i]
        if fi.degrees()[1] == 0:
            Ru = fr.univariate(fi, 0)
            G = Ru if G is None else G.gcd(Ru)
            if G.degree() == 0:
                return G, True
            continue
        for j in range(i + 1, min(len(eqs), jmax)):
            fj = eqs[j]
            if fj.degrees()[1] == 0:
                Ru = fr.univariate(fj, 0)
            else:
                R = fi.resultant(fj, 'u1')
                if R == 0:
                    continue
                Ru = fr.univariate(R, 0)
            G = Ru if G is None else G.gcd(Ru)
            if G.degree() == 0:
                return G, True
    return G, G is not None


def classify_fixed(blocks, ctx3, gens3):
    r = fr.setup(blocks, ctx3, gens3)
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
        g = fr.univariate(eqs[0], 0)
        for f in eqs[1:]:
            g = g.gcd(fr.univariate(f, 0))
            if g.degree() == 0:
                return 'NONREAL gcd1'
        g = fr.strip_bad(g, [fr.univariate(b, 0) for b in bad])
        return 'NONREAL allbad1' if g.degree() == 0 else 'DEFER real1'
    if nvar == 2:
        if len(eqs) < 2:
            return 'DEFER dim2'
        G, found = gcd_of_conditions(eqs, 6, 8)
        if not found:
            return 'DEFER commonfactor'
        if G.degree() == 0:
            return 'NONREAL res'
        return 'DEFER res-nonconst'
    return 'DEFER nvar>=3'


def classify2_fixed(blocks, reason, ctx3, gens3):
    r = fr.setup(blocks, ctx3, gens3)
    nvar, P, eqs, bad = r
    eqs = [f for f in eqs if f != 0]
    if nvar != 2:
        return 'DEFER ' + reason
    h = eqs[0]
    for f in eqs[1:]:
        h = h.gcd(f)
    if h.total_degree() > 0:
        for fac, mult in h.factor()[1]:
            if fac.total_degree() == 0:
                continue
            if not any((d.gcd(fac) - fac == 0) or (d.gcd(fac) + fac == 0) for d in bad):
                return 'DEFER curve'
        eqs = [f // h for f in eqs]
        eqs = [f for f in eqs if f != 0 and f.total_degree() > 0]
        if not eqs:
            return 'NONREAL curve-all-bad'
    G, found = gcd_of_conditions(eqs, 8, 10)
    if not found:
        return 'DEFER commonfactor2'
    if G.degree() == 0:
        return 'NONREAL res2'
    for phi, mult in G.factor()[1]:
        if phi.degree() <= 0:
            continue
        if fr2.nondegenerate_solutions_over(phi, eqs, bad):
            return 'DEFER real2 deg%d' % phi.degree()
    return 'NONREAL nf'


if __name__ == '__main__':
    # usage: fast_real_fix.py n lattices.jsonl indexfile out.jsonl   (re-classify the listed indices)
    IN, IDX, OUT = ARGV[2], ARGV[3], ARGV[4]
    want = set(int(l.split()[0]) for l in open(IDX) if l.strip())
    ctx3 = flint.fmpz_mpoly_ctx.get(('u0', 'u1', 'u2')); gens3 = ctx3.gens()
    stats = {}
    t0 = time.time()
    n = 0
    with open(IN) as f, open(OUT, 'w') as out:
        for i, line in enumerate(f):
            if i not in want:
                continue
            rec = json.loads(line)
            v1 = classify_fixed(rec['blocks'], ctx3, gens3)
            v = v1
            if v1.startswith('DEFER') and v1 != 'DEFER nvar>=3':
                v = v1 + ' | pass2: ' + classify2_fixed(rec['blocks'], v1[6:], ctx3, gens3)
            stats[v] = stats.get(v, 0) + 1
            out.write(json.dumps(dict(idx=i, verdict=v, blocks=rec['blocks'])) + '\n')
            n += 1
            if n % 20000 == 0:
                print(n, stats, '(%.0fs)' % (time.time() - t0), flush=True)
    print('DONE', n, stats, '(%.0fs)' % (time.time() - t0), flush=True)
