"""Points of C over the special T-factors found by famext.py, as 0-dimensional pseudo-components in the
format of m2comp.py (f, g: shape lemma), so that extend.py can run the exact rigid search at them."""
import sys, json, subprocess, os
M2 = '/opt/homebrew/bin/M2'
def points_over(rec, comp, pm, factors, tag, nlines=13):
    nv = max(rec['nvar'], 1)
    # T as a linear form in u
    if pm['kind'] == 'A1': tform = 'u_0'
    else:
        a = [int(x) for x in pm['a'].strip('{}').split(',')]
        tform = '+'.join('(%d)*u_%d' % (c, i) for i, c in enumerate(a))
    import exact_tc_lattice as ex
    ex.n = nlines
    frame, nvar, lines, eqs, bad, pts = ex.setup(rec['blocks'])
    s = ['needsPackage "PrimaryDecomposition";',
         'cr = (p, q) -> matrix{{p_(0,1)*q_(0,2)-p_(0,2)*q_(0,1), p_(0,2)*q_(0,0)-p_(0,0)*q_(0,2), p_(0,0)*q_(0,1)-p_(0,1)*q_(0,0)}};',
         'R = QQ[%s];' % ','.join('u_%d' % i for i in range(nv))]
    s.append('P%d = matrix{{1_R,0,0}}; P%d = matrix{{0_R,1,0}}; P%d = matrix{{0_R,0,1}}; P%d = matrix{{1_R,1,1}};' % frame)
    s += lines
    s.append('bad = select({%s}, f -> f != 0);' % ','.join(bad))
    s.append('IC = ideal(%s);' % (comp['gens'].strip('{}') if pm['kind'] != 'A1' else '0_R'))
    s.append('tf = %s; Tsym = getSymbol "T"; RT = QQ[Tsym];' % tform)
    s.append('seen = new MutableHashTable;')
    for f in factors:
        s.append('phi = sub(%s, {(gens RT)#0 => tf});' % f.replace('**', '^'))
        s.append('''for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));''')
    s.append('print("DONE");')
    path = '/tmp/claude-502/fs_%s_%d.m2' % (tag, os.getpid())
    open(path, 'w').write('\n'.join(s))
    r = subprocess.run([M2, '--script', path], capture_output=True, text=True, timeout=1800)
    os.remove(path)
    out = []
    ok = 'DONE' in r.stdout
    for ln in r.stdout.split('\n'):
        if ln.startswith('PT '):
            parts = ln[3:].split(' ; ')
            out.append(dict(dim=0, degree=None, f=parts[0], g=parts[1:], special=True))
        elif ln.startswith('PT-NOSHAPE'):
            out.append(dict(dim=0, noshape=True, special=True))
    return ok, out, (r.stderr[-300:] if not ok else '')
