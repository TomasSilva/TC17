"""Realisation components of rank-3 lattices (no freeness test), one lattice per Macaulay2 run with a
timeout.  Uses the parametrisation of work/tc15/exact_tc_lattice.py (frame + greedy determination).
Output per lattice (jsonl): {"idx", "status": NONREAL|REAL|TIMEOUT|ERROR, "comps": [{"dim","degree","gens"}],
"nvar", "frame", "lines"} where gens are the generators of each good minimal prime (strings in u_i).
usage: m2comp.py n lattices.jsonl part nparts timeout out.jsonl"""
import sys, json, subprocess, os, time
n, IN, part, nparts, TO, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
sys.argv = ['x', n, '6', IN, '0', '1']
sys.path.insert(0, '/Users/agent/Projects/TC17/work/tc15')
import exact_tc_lattice as ex
def script(idx, blocks):
    frame, nvar, lines, eqs, bad, pts = ex.setup(blocks)
    s = ['needsPackage "PrimaryDecomposition";',
         'cr = (p, q) -> matrix{{p_(0,1)*q_(0,2)-p_(0,2)*q_(0,1), p_(0,2)*q_(0,0)-p_(0,0)*q_(0,2), p_(0,0)*q_(0,1)-p_(0,1)*q_(0,0)}};']
    s.append('R = QQ[%s];' % (','.join('u_%d' % i for i in range(nvar)) if nvar else 'u_0'))
    s.append('P%d = matrix{{1_R,0,0}}; P%d = matrix{{0_R,1,0}}; P%d = matrix{{0_R,0,1}}; P%d = matrix{{1_R,1,1}};' % frame)
    s += lines
    if nvar == 0: eqs = eqs + ['u_0']
    s.append('I = ideal(%s);' % (','.join(eqs) if eqs else '0_R'))
    s.append('bad = {%s};' % ','.join(bad))
    s.append('bad = select(bad, f -> f != 0); zerobad = %d - #bad;' % len(bad))
    s.append('if I == ideal(1_R) or zerobad > 0 then print("RESULT NONREAL") else (')
    s.append(' cs = minimalPrimes I;')
    s.append(' good = select(cs, c -> all(bad, f -> f % c != 0));')
    s.append(' if #good == 0 then print("RESULT NONREAL") else (')
    s.append('  print("RESULT REAL " | toString(#good));')
    s.append('  for c in good do (print("COMP " | toString(dim c) | " " | toString(degree c) | " " | toString(flatten entries gens c));')
    s.append('   if dim c == 0 then (')
    s.append('    kk := numgens R; ok := false; tries := 0;')
    s.append('    while not ok and tries < 20 do (tries = tries + 1;')
    s.append('     a := apply(kk, i -> random(-7, 7) + (if i == 0 then 0 else 0));')
    s.append('     S := QQ[gens R | {getSymbol "T"}, MonomialOrder => Lex]; TT := last gens S;')
    s.append('     J := sub(c, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));')
    s.append('     G := flatten entries gens gb J;')
    s.append('     fl := select(G, g -> isSubset(support g, {TT}));')
    s.append('     if #G == kk + 1 and #fl == 1 then (')
    s.append('      f := first fl; d := (degree f)#0;')
    s.append('      nfs := apply(kk, i -> (gens S)#i % ideal G);')
    s.append('      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;')
    s.append('       print("SHAPE " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));')
    s.append('    if not ok then print("NOSHAPE")))')
    s.append(' ));')
    s.append('print("DONE");')
    return '\n'.join(s), dict(nvar=nvar, frame=list(frame), lines=lines)
recs = [json.loads(l) for l in open(IN)]
with open(OUT, 'a') as out:
    for i, rec in enumerate(recs):
        if i % nparts != part: continue
        txt, meta = script(i, rec['blocks'])
        path = OUT + '.%d.m2' % part
        open(path, 'w').write(txt)
        t0 = time.time()
        res = dict(idx=rec.get('idx', i), line=i, blocks=rec['blocks'], **meta)
        try:
            r = subprocess.run([ex.M2, '--script', path], capture_output=True, text=True, timeout=TO)
            o = r.stdout
            if 'DONE' not in o: res['status'] = 'ERROR'; res['err'] = r.stderr[-500:]
            elif 'RESULT NONREAL' in o: res['status'] = 'NONREAL'
            else:
                res['status'] = 'REAL'
                res['comps'] = []
                for ln in o.split('\n'):
                    if ln.startswith('COMP '):
                        _, dm, dg, gens = ln.split(' ', 3)
                        res['comps'].append(dict(dim=int(dm), degree=int(dg), gens=gens))
                    elif ln.startswith('SHAPE ') and res['comps']:
                        parts = ln[6:].split(' ; ')
                        res['comps'][-1]['f'] = parts[0]; res['comps'][-1]['g'] = parts[1:]
                    elif ln.startswith('NOSHAPE') and res['comps']:
                        res['comps'][-1]['noshape'] = True
        except subprocess.TimeoutExpired:
            res['status'] = 'TIMEOUT'
        res['time'] = round(time.time() - t0, 1)
        out.write(json.dumps(res) + '\n'); out.flush()
        os.remove(path)
