"""Independent certification of a 17-line lattice from a Macaulay2 component record with a shape lemma
(m2compb.py 17: frame, parametrisation statements, f(T), u_i = g_i(T)): the realisation is rebuilt in
Macaulay2 over the field of definition K = Q[T]/(f) (or Q), the lattice of the realisation is recomputed
from the normals and compared with the record, and the minimal generators of the module of Jacobian
syzygies D_0 (syzygies of (Q_x, Q_y, Q_z), Q the product of the linear forms) are computed over K: the
arrangement is free iff there are two of them; nearly free with exponents (7, 10) iff their degrees are
7, 10, 10.  This uses neither Yoshinaga's criterion nor the code of the proof.
usage: freecheck.py L_comp.jsonl part nparts out.jsonl"""
import sys, json, re, subprocess, os, time
M2 = '/opt/homebrew/bin/M2'
IN, part, nparts, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
def plist(s):
    s = s.strip().strip('{}')
    return [x.strip() for x in s.split(',')] if s else []
def script(rec, comp):
    F = plist(comp['f']); G = [plist(g) for g in comp['g']]
    d = len(F) - 1
    s = []
    if d == 1:
        s.append('K = QQ; TT = -(%s)/(%s);' % (F[0], F[1]))
    else:
        s.append('A = QQ[T]; K = toField(A/ideal(%s)); TT = T_K;' % ' + '.join('(%s)*T^%d' % (c, j) for j, c in enumerate(F)))
    s.append('uu = {%s};' % ', '.join('(' + ' + '.join('(%s)*TT^%d' % (c, j) for j, c in enumerate(g)) + ')' if g else '0_K' for g in G))
    s.append('cr = (p, q) -> matrix{{p_(0,1)*q_(0,2)-p_(0,2)*q_(0,1), p_(0,2)*q_(0,0)-p_(0,0)*q_(0,2), p_(0,0)*q_(0,1)-p_(0,1)*q_(0,0)}};')
    fr = rec['frame']
    s.append('P%d = matrix{{1_K,0,0}}; P%d = matrix{{0_K,1,0}}; P%d = matrix{{0_K,0,1}}; P%d = matrix{{1_K,1,1}};' % tuple(fr))
    for st in rec['lines']:
        s.append(re.sub(r'u_(\d+)', r'(uu#\1)', st))
    s.append('Ls = {%s};' % ', '.join('P%d' % i for i in range(17)))
    s.append('print("ZERO " | toString any(Ls, P -> P == 0));')
    s.append('print("DISTINCT " | toString all(subsets(17, 2), q -> rank(Ls#(q#0) || Ls#(q#1)) == 2));')
    s.append('blocks = {}; covered = new MutableHashTable;')
    s.append('for q in subsets(17, 2) do (if not covered#?q then (i := q#0; j := q#1; B := select(toList(0..16), k -> k == i or k == j or det(Ls#i || Ls#j || Ls#k) == 0); if #B >= 3 then blocks = append(blocks, B); for t in subsets(B, 2) do covered#t = true;));')
    s.append('print("BLOCKS " | toString blocks);')
    s.append('R = K[x,y,z]; X = matrix{{x},{y},{z}};')
    s.append('forms = apply(Ls, P -> (promote(P, R) * X)_(0,0)); Q = product forms;')
    s.append('J = matrix{{diff(x,Q), diff(y,Q), diff(z,Q)}};')
    s.append('S = mingens image syz J;')
    s.append('print("SYZDEG " | toString apply(degrees source S, first));')
    s.append('print("DONE");')
    return '\n'.join(s) + '\n'
with open(OUT, 'w') as out:
    for k, line in enumerate(open(IN)):
        if k % nparts != part or not line.strip(): continue
        rec = json.loads(line)
        res = dict(idx=rec.get('idx'), status=rec.get('status'))
        comps = [c for c in rec.get('comps', []) if c.get('dim') == 0 and 'g' in c]
        if rec.get('status') != 'REAL' or not comps:
            res['error'] = 'no rigid component with a shape lemma'; out.write(json.dumps(res) + '\n'); continue
        comp = comps[0]
        res['field'] = 'Q[T]/(%s)' % comp['f'] if len(plist(comp['f'])) > 2 else 'Q'
        res['components'] = len(rec['comps']); res['degree'] = comp.get('degree')
        path = OUT + '.%d.m2' % part
        open(path, 'w').write(script(rec, comp))
        t0 = time.time()
        try:
            p = subprocess.run([M2, '--script', path], capture_output=True, text=True, timeout=3600)
            o = p.stdout
            if 'DONE' not in o: res['error'] = 'M2: ' + (p.stderr[-600:] + o[-300:])
            else:
                zero = re.search(r'ZERO (\w+)', o).group(1) == 'true'
                dist = re.search(r'DISTINCT (\w+)', o).group(1) == 'true'
                bl = json.loads(re.search(r'BLOCKS (.*)', o).group(1).replace('{', '[').replace('}', ']'))
                want = sorted(sorted(b) for b in rec['blocks'] if len(b) >= 3)
                res['lattice_ok'] = (not zero) and dist and sorted(sorted(b) for b in bl) == want
                res['degrees'] = [d - 16 for d in json.loads(re.search(r'SYZDEG (.*)', o).group(1).replace('{', '[').replace('}', ']'))]
                res['free'] = len(res['degrees']) == 2
        except subprocess.TimeoutExpired:
            res['error'] = 'M2 timeout'
        except Exception as e:
            res['error'] = repr(e)[:300]
        res['time'] = round(time.time() - t0, 1)
        if os.path.exists(path): os.remove(path)
        out.write(json.dumps(res) + '\n'); out.flush()
