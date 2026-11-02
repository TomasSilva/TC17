"""Empirical check of Corollary (external lines of a nearly free arrangement) and of the rich-line bound on
the 16 realisable window lattices, over F_p: Bourbaki point P0 from the degree-7 Jacobian syzygy (Macaulay2),
then the weight sigma of every line through two multiple points that is not a line of the arrangement."""
import json, re, subprocess, itertools, collections, sys
from fractions import Fraction
p = int(sys.argv[1]) if len(sys.argv) > 1 else 10009
def pq(s):
    s = s.strip(); a = Fraction(s) if s else Fraction(0); return a.numerator * pow(a.denominator, -1, p) % p
def plist(s):
    s = s.strip().strip('{}'); return [pq(x) for x in s.split(',')] if s else []
def cross(a, b): return [(a[1]*b[2]-a[2]*b[1]) % p, (a[2]*b[0]-a[0]*b[2]) % p, (a[0]*b[1]-a[1]*b[0]) % p]
def norm(v):
    for c in v:
        if c: inv = pow(c, -1, p); return tuple(x * inv % p for x in v)
    return None
def dot(a, b): return (a[0]*b[0]+a[1]*b[1]+a[2]*b[2]) % p
out = []
for l in open('L16_comp.jsonl'):
    rec = json.loads(l); comp = rec['comps'][0]
    f = plist(comp['f']); gs = [plist(g) for g in comp['g']]
    roots = [x for x in range(p) if sum(c * pow(x, j, p) for j, c in enumerate(f)) % p == 0]
    if not roots: out.append((rec['idx'], 'no root mod p')); continue
    r = roots[0]; u = [sum(c * pow(r, j, p) for j, c in enumerate(g)) % p for g in gs]
    P = {}; fr = rec['frame']
    P[fr[0]] = [1, 0, 0]; P[fr[1]] = [0, 1, 0]; P[fr[2]] = [0, 0, 1]; P[fr[3]] = [1, 1, 1]
    for st in rec['lines']:
        m = re.match(r'P(\d+) = cr\(cr\(P(\d+), P(\d+)\), cr\(P(\d+), P(\d+)\)\);', st)
        if m: e, a, b, c, d = map(int, m.groups()); P[e] = cross(cross(P[a], P[b]), cross(P[c], P[d])); continue
        m = re.match(r'P(\d+) = P(\d+) \+ u_(\d+) \* P(\d+);', st)
        if m: e, a, i, b = map(int, m.groups()); P[e] = [(P[a][j] + u[i] * P[b][j]) % p for j in range(3)]; continue
        m = re.match(r'P(\d+) = matrix\{\{u_(\d+), u_(\d+), 1_R\}\};', st)
        if m: e, i, j = map(int, m.groups()); P[e] = [u[i], u[j], 1]; continue
        raise ValueError(st)
    lines = [norm(P[e]) for e in range(17)]
    pts = {}
    for a, b in itertools.combinations(range(17), 2):
        Q = norm(cross(lines[a], lines[b]))
        pts.setdefault(Q, set()).update((a, b))
    for Q in pts: pts[Q] = frozenset(x for x in range(17) if dot(lines[x], Q) == 0)
    blocks = sorted(sorted(L) for L in pts.values() if len(L) >= 3)
    if blocks != sorted(sorted(b) for b in rec['blocks']): out.append((rec['idx'], 'lattice differs mod p')); continue
    # Macaulay2: degree-7 syzygy and its zero
    forms = ['((%d)*x+(%d)*y+(%d)*z)' % tuple(L) for L in lines]
    m2 = 'R = ZZ/%d[x,y,z]; Q = %s; S = syz matrix{{diff(x,Q), diff(y,Q), diff(z,Q)}}; G = mingens image S;\n' % (p, '*'.join(forms))
    m2 += 'ds = apply(degrees source G, d -> first d - 16); print toString ds;\n'
    m2 += 'j7 = position(ds, d -> d == 7); th = flatten entries G_{j7};\n'
    m2 += 'I = saturate(ideal th, ideal(x,y,z)); print toString(degree I);\n'
    m2 += 'pt = first decompose I; L = flatten entries gens gb pt;\n'
    m2 += 'print toString apply(L, f -> {coefficient(x, f), coefficient(y, f), coefficient(z, f)});\n'
    open('/tmp/claude-502/extl.m2', 'w').write(m2)
    r2 = subprocess.run(['M2', '--script', '/tmp/claude-502/extl.m2'], capture_output=True, text=True)
    lines_out = r2.stdout.strip().split('\n')
    try:
        vecs = [[int(x) % p for x in v.split(',')] for v in lines_out[2].replace(' ', '').strip('{}').split('},{')]
        P0 = norm(cross(vecs[0], vecs[1]))
    except Exception as e:
        out.append((rec['idx'], 'M2 parse', r2.stdout[-300:], r2.stderr[-300:])); continue
    if any(dot(L, P0) == 0 for L in lines): onA = 'P0 on a line of A'
    else: onA = 'P0 on no line of A'
    # external lines through two multiple points
    plist_ = list(pts.items())
    ext = {}
    for (Q1, L1), (Q2, L2) in itertools.combinations(plist_, 2):
        if L1 & L2: continue
        ell = norm(cross(Q1, Q2))
        if ell in ext: continue
        sig = sum(len(L) - 1 for Q, L in plist_ if dot(ell, Q) == 0)
        ext[ell] = (sig, dot(ell, P0) == 0)
    bad = [(s, th) for s, th in ext.values() if (not th and not (s <= 7 or s == 9)) or (th and not (s <= 6 or s == 10))]
    rich = sorted(s for s, th in ext.values() if s >= 8)
    hist = collections.Counter((s, th) for s, th in ext.values() if s >= 6)
    out.append((rec['idx'], 'syz degrees ' + lines_out[0], 'deg(B)=' + lines_out[1], onA, 'external lines %d' % len(ext),
                'violations %d' % len(bad), 'rich (sigma>=8): %s' % rich, dict(sorted(hist.items()))))
for o in out: print(o)
