# Exact Terao check (characteristic 0) for abstract rank-3 lattices given by blocks on n elements.
# For each lattice (elements = lines, blocks = multiple points):
#   1. realisation space: dual points P_i (normals of the lines) with frame (1,0,0),(0,1,0),(0,0,1),(1,1,1),
#      remaining points determined/parametrised greedily, collinearity equations for blocks, and the
#      minimal primes not containing any forbidden collinearity (= components of the realisation space);
#   2. on each component, Yoshinaga's criterion on H0 = {z = 0}: A is free iff the Ziegler multirestriction
#      (points (-b : a) with multiplicity |block| - 1, double points multiplicity 1) has no derivation of
#      degree d1 - 1, i.e. the matrix of the conditions (a x + b y)^mu | a f + b g (vanishing of all
#      derivatives of order < mu at (-b, a)) has full rank 2 d1.
#   Output per component: dim, FREE / NONFREE, or for positive dimension whether the non-free locus is
#   contained in the degeneration locus (otherwise: MIXED = Terao counterexample).
import sys, json, itertools, subprocess, time, os

n, d1 = int(sys.argv[1]), int(sys.argv[2])
IN = sys.argv[3]; part = int(sys.argv[4]); nparts = int(sys.argv[5])
OUT = IN.replace('.jsonl', '_tc_%d.out' % part)
M2 = '/opt/homebrew/bin/M2'
k = d1 - 1


def setup(blocks):
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
    coords = {frame[0]: ('1', '0', '0'), frame[1]: ('0', '1', '0'), frame[2]: ('0', '0', '1'), frame[3]: ('1', '1', '1')}
    lines = []      # M2 statements
    nvar = 0
    order = list(frame)
    todo = [e for e in range(n) if e not in coords]
    while todo:
        best = None
        for e in todo:
            det_lines = []
            for B in blocks:
                if e in B:
                    D = [x for x in B if x in coords]
                    if len(D) >= 2:
                        det_lines.append((D[0], D[1]))
            score = len(det_lines)
            if best is None or score > best[1]:
                best = (e, score, det_lines)
        e, score, det_lines = best
        todo.remove(e); order.append(e)
        if score >= 2:
            (a1, b1), (a2, b2) = det_lines[0], det_lines[1]
            lines.append('P%d = cr(cr(P%d, P%d), cr(P%d, P%d));' % (e, a1, b1, a2, b2))
            coords[e] = ('sym',)
        elif score == 1:
            a1, b1 = det_lines[0]
            lines.append('P%d = P%d + u_%d * P%d;' % (e, a1, nvar, b1)); nvar += 1
            coords[e] = ('sym',)
        else:
            lines.append('P%d = matrix{{u_%d, u_%d, 1_R}};' % (e, nvar, nvar + 1)); nvar += 2
            coords[e] = ('sym',)
    eqs = []
    for B in blocks:
        Bs = sorted(B, key=lambda x: order.index(x))
        for c in Bs[2:]:
            eqs.append('det(P%d || P%d || P%d)' % (Bs[0], Bs[1], c))
    bad = []
    for t in itertools.combinations(range(n), 3):
        if not collinear(*t):
            bad.append('det(P%d || P%d || P%d)' % t)
    # Ziegler restriction on H0 = frame[2] (normal (0,0,1)): other lines e give points (-b : a), b, a = coords
    h0 = frame[2]
    mult = {}
    for e in range(n):
        if e == h0:
            continue
        B = block_of(e, h0)
        key = tuple(sorted(B)) if B else (e,)
        mult[key] = (len(B) - 1) if B else 1
    pts = []   # (representative element, multiplicity)
    for key, mu in mult.items():
        e = next(x for x in key if x != h0)
        pts.append((e, mu))
    return frame, nvar, lines, eqs, bad, pts


def m2_script(items):
    out = ['needsPackage "PrimaryDecomposition";', 'cr = (p, q) -> matrix{{p_(0,1)*q_(0,2)-p_(0,2)*q_(0,1), p_(0,2)*q_(0,0)-p_(0,0)*q_(0,2), p_(0,0)*q_(0,1)-p_(0,1)*q_(0,0)}};']
    for idx, blocks in items:
        frame, nvar, lines, eqs, bad, pts = setup(blocks)
        s = []
        s.append('R = QQ[%s];' % (','.join('u_%d' % i for i in range(nvar)) if nvar else 'u_0'))
        s.append('P%d = matrix{{1_R,0,0}}; P%d = matrix{{0_R,1,0}}; P%d = matrix{{0_R,0,1}}; P%d = matrix{{1_R,1,1}};' % frame)
        s += lines
        if nvar == 0:
            eqs = eqs + ['u_0']          # pin the dummy variable: the realisation space is then 0-dimensional
        s.append('I = ideal(%s);' % (','.join(eqs) if eqs else '0_R'))
        s.append('if I == ideal(1_R) then print("LATTICE %d NONREAL") else (' % idx)
        s.append('bad = {%s};' % ','.join(bad))
        s.append('bad = select(bad, f -> f != 0); zerobad = %d - #bad;' % len(bad))
        s.append('cs = minimalPrimes I;')
        s.append('good = if zerobad > 0 then {} else select(cs, c -> all(bad, f -> f % c != 0));')
        s.append('print("LATTICE %d components " | toString(#cs) | " good " | toString(#good) | " dims " | toString(apply(good, dim)) | " zerobad " | toString zerobad);' % idx)
        s.append('if #good > 0 then (')
        s.append('S = R[x,y]; kk = %d; mons = flatten entries basis(kk, S);' % k)
        s.append('ptsM = {%s};' % ','.join('{P%d_(0,0), P%d_(0,1), %d}' % (e, e, mu) for e, mu in pts))
        s.append('''rows = flatten for pt in ptsM list (
   a := pt#0; b := pt#1; mu := pt#2;
   flatten for i from 0 to mu - 1 list for j from 0 to mu - 1 - i list (
      flatten for slot from 0 to 1 list for m in mons list (
         h := (if slot == 0 then a else b) * m;
         dh := diff(x^i * y^j, h);
         sub(dh, {x => -b, y => a}) )));
M = matrix pack(2 * #mons, flatten rows);
full = 2 * #mons;
for c in good do (
   if dim c == 0 then (
      F := toField(R / c);
      rk := rank sub(M, F);
      print("  COMP dim 0 degree " | toString(degree c) | " rank " | toString rk | "/" | toString full | (if rk == full then " FREE" else " NONFREE"));
   ) else (
      A := R / c;
      rk := rank sub(M, frac A);
      if rk < full then print("  COMP dim " | toString(dim c) | " generic rank " | toString rk | "/" | toString full | " NONFREE (all)")
      else (
         an := ann coker transpose sub(M, A);
         Z := minimalPrimes(c + lift(an, R));
         okZ := all(Z, q -> any(bad, f -> f % q == 0));
         print("  COMP dim " | toString(dim c) | " generic FREE; non-free locus inside degeneracy locus: " | toString okZ | (if okZ then "" else "  !!! MIXED"));
      ););
);););''')
        out.append('\n'.join(s))
    return '\n'.join(out) + '\nprint("DONE");\n'


def run():
    recs = [json.loads(l) for l in open(IN)]
    mine = [(i, r['blocks']) for i, r in enumerate(recs) if i % nparts == part]
    out = open(OUT, 'w')
    t0 = time.time()
    B = 20
    for start in range(0, len(mine), B):
        batch = mine[start:start + B]
        path = IN.replace('.jsonl', '_tc_%d_%d.m2' % (part, start))
        open(path, 'w').write(m2_script(batch))
        res = subprocess.run([M2, '--script', path], capture_output=True, text=True)
        out.write(res.stdout)
        if 'DONE' not in res.stdout:
            out.write('ERROR in batch %d: %s\n' % (start, res.stderr[-2000:]))
        out.flush()
        os.remove(path)
        print('part %d: %d/%d lattices (%.0fs)' % (part, min(start + B, len(mine)), len(mine), time.time() - t0), flush=True)
    out.write('ALLDONE\n'); out.close()


if __name__ == '__main__':
    run()
