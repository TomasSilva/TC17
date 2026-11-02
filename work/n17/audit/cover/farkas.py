"""Rigorous infeasibility certificates for the level-2 problems: the LP relaxation (0 <= x <= 1) of
  sum_j c_ij x_j >= b_i  (all rows)
is infeasible iff there are multipliers y >= 0 with  sum_j max(0, sum_i y_i c_ij) < sum_i y_i b_i.
We get y from the duals of the phase-1 LP (glpsol simplex, floating point) and then VERIFY the
inequality exactly with Fractions (any y >= 0 satisfying it is a valid certificate)."""
import sys, subprocess, os, re
from fractions import Fraction
from propcheck import prepare
from gamma_ilp import vectors
from level1 import survivors
def certify(k, deltas, thr=4, tag='f'):
    C, V = prepare(k, deltas, thr)
    vid = {v: j for j, v in enumerate(V)}
    lp = tag + '.lp'
    with open(lp, 'w') as f:
        f.write('Minimize\n obj: ' + ' + '.join('s%d' % i for i in range(len(C))) + '\nSubject To\n')
        for i, (terms, rhs) in enumerate(C):
            t = ' '.join(('+ %d x%d' % (c, vid[v])) if c > 0 else ('- %d x%d' % (-c, vid[v])) for c, v in terms)
            f.write(' r%d: %s + s%d >= %d\n' % (i, t if t else '0 x0', i, rhs))
        f.write('Bounds\n')
        for j in range(len(V)): f.write(' 0 <= x%d <= 1\n' % j)
        f.write('End\n')
    out = tag + '.out'
    r = subprocess.run(['glpsol', '--lp', lp, '--nomip', '-w', out], capture_output=True, text=True)
    lines = open(out).read().split('\n')
    # plain text solution format: header lines starting with 'c', then 's bas ROWS COLS pst dst obj',
    # then 'i ROW st prim dual' lines and 'j COL st prim dual' lines
    y = {}
    obj = None
    for ln in lines:
        p = ln.split()
        if not p: continue
        if p[0] == 's': obj = float(p[-1])
        if p[0] == 'i':
            y[int(p[1]) - 1] = Fraction(p[4])
    if obj is None or obj <= 1e-9: return False, obj
    # verify exactly
    yy = [max(Fraction(0), y.get(i, Fraction(0))) for i in range(len(C))]
    agg = {}
    rhs = Fraction(0)
    for i, (terms, b) in enumerate(C):
        if yy[i] == 0: continue
        rhs += yy[i] * b
        for c, v in terms: agg[v] = agg.get(v, Fraction(0)) + yy[i] * c
    mx = sum(max(Fraction(0), a) for a in agg.values())
    return mx < rhs, (float(rhs - mx), obj)
if __name__ == '__main__':
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    thr = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    idx = 0; ok = bad = 0
    for k in vectors():
        for Delta, chosen in survivors(k, thr):
            if idx % nparts == part:
                deltas = [d for tup in chosen for d in tup]
                cert, info = certify(k, deltas, thr, 'f%d' % part)
                if cert: ok += 1
                else:
                    bad += 1; print('NOCERT', idx, k, chosen, info, flush=True)
            idx += 1
    print('part', part, 'certified', ok, 'not certified', bad, flush=True)
