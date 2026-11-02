"""Special points of a 1-dimensional component C of R(B) (B a 13-line core).

A point of C at which some extension of B exists but none exists at the generic point must be a point
where some triple of multiple points of B (pairwise without common line) becomes collinear, or, more
generally, where some incidence test of the search changes value.  At level 1 these tests are exactly the
triple determinants det(Q_i, Q_j, Q_k).  This script (Macaulay2) computes, on C:
  - the triples that are collinear on all of C (generic collinearities),
  - for every other triple, the points of C (minus the degenerate locus) where it becomes collinear,
and prints every such special point (as a 0-dimensional prime, in shape-lemma form), with the list of
triples collinear there.  Deeper levels are handled by the exact search at each special point; the
generic behaviour is the exact search at a random slice (extend.py).  If the generic search has nodes
at level >= 1, the special points for deeper levels must be added (reported as GENERIC_NODES > 0).
usage: famspecial.py comp.jsonl part nparts timeout out.jsonl"""
import sys, json, subprocess, os, time, itertools
IN, part, nparts, TO, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
sys.argv = ['x', '13', '6', IN, '0', '1']
sys.path.insert(0, '/Users/agent/Projects/TC17/work/tc15')
import exact_tc_lattice as ex
def script(rec, comp):
    blocks = rec['blocks']
    frame, nvar, lines, eqs, bad, pts = ex.setup(blocks)
    n = 13
    inb = {}
    P = []
    for b in blocks:
        P.append(tuple(sorted(b)))
        for q in itertools.combinations(sorted(b), 2): inb[q] = 1
    for q in itertools.combinations(range(n), 2):
        if q not in inb: P.append(q)
    triples = [(i, j, k) for i, j, k in itertools.combinations(range(len(P)), 3)
               if not (set(P[i]) & set(P[j])) and not (set(P[i]) & set(P[k])) and not (set(P[j]) & set(P[k]))]
    s = ['needsPackage "PrimaryDecomposition";',
         'cr = (p, q) -> matrix{{p_(0,1)*q_(0,2)-p_(0,2)*q_(0,1), p_(0,2)*q_(0,0)-p_(0,0)*q_(0,2), p_(0,0)*q_(0,1)-p_(0,1)*q_(0,0)}};']
    s.append('R = QQ[%s];' % (','.join('u_%d' % i for i in range(nvar)) if nvar else 'u_0'))
    s.append('P%d = matrix{{1_R,0,0}}; P%d = matrix{{0_R,1,0}}; P%d = matrix{{0_R,0,1}}; P%d = matrix{{1_R,1,1}};' % frame)
    s += lines
    s.append('IC = ideal(%s);' % comp['gens'].strip('{}'))
    s.append('bad = select({%s}, f -> f != 0);' % ','.join(bad))
    s.append('Q = {%s};' % ','.join('cr(P%d, P%d)' % (p[0], p[1]) for p in P))
    s.append('T = {%s};' % ','.join('{%d,%d,%d}' % t for t in triples))
    s.append('gen = {}; spec = new MutableHashTable;')
    s.append('''for t in T do (
  g := det(Q#(t#0) || Q#(t#1) || Q#(t#2));
  if g % IC == 0 then gen = append(gen, t) else (
     for q in minimalPrimes(IC + ideal g) do (
        if dim q == 0 and all(bad, f -> f % q != 0) then (
           key := toString flatten entries gens gb q;
           if not spec#?key then spec#key = {q, {}};
           spec#key = {(spec#key)#0, append((spec#key)#1, t)}))));''')
    s.append('print("GENERIC " | toString gen);')
    s.append('''kk := numgens R;
for key in keys spec do (
  q := (spec#key)#0; ok := false; tries := 0;
  while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "T"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
        f := first fl; d := (degree f)#0;
        nfs := apply(kk, i -> (gens S)#i % ideal G);
        if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
           print("SPECIAL " | toString((spec#key)#1) | " ; " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h)))))))));
  if not ok then print("SPECIAL-NOSHAPE " | toString((spec#key)#1)));''')
    s.append('print("DONE");')
    return '\n'.join(s), len(triples)
with open(OUT, 'a') as out:
    for li, line in enumerate(open(IN)):
        if li % nparts != part: continue
        rec = json.loads(line)
        for ci, comp in enumerate(rec.get('comps', [])):
            if comp['dim'] != 1: continue
            txt, ntr = script(rec, comp)
            path = OUT + '.%d.m2' % part
            open(path, 'w').write(txt)
            t0 = time.time()
            res = dict(idx=rec['idx'], comp=ci, ntriples=ntr)
            try:
                r = subprocess.run([ex.M2, '--script', path], capture_output=True, text=True, timeout=TO)
                o = r.stdout
                if 'DONE' not in o: res['status'] = 'ERROR'; res['err'] = r.stderr[-300:]
                else:
                    res['status'] = 'OK'; res['special'] = []
                    for ln in o.split('\n'):
                        if ln.startswith('GENERIC '): res['generic'] = ln[8:]
                        elif ln.startswith('SPECIAL '):
                            tr, f, *g = ln[8:].split(' ; ')
                            res['special'].append(dict(triples=tr, f=f, g=g))
                        elif ln.startswith('SPECIAL-NOSHAPE'): res.setdefault('noshape', []).append(ln)
            except subprocess.TimeoutExpired:
                res['status'] = 'TIMEOUT'
            res['time'] = round(time.time() - t0, 1)
            out.write(json.dumps(res) + '\n'); out.flush()
            os.remove(path)
