"""Validate the (gamma) model on real lattices: for each lattice and each 8-point line H0, compute the model
variables (delta, e, tau) and evaluate every constraint of build(k, thr) with thr = 4 - phimax_H0 where
phimax_H0 = max phi over 4-sets containing H0.  A violated constraint is a modelling error."""
import sys, itertools, re
sys.path.insert(0, '../../heavy')
from g6blocks import decode
from gamma_ilp import build
d = 17
def check(B):
    cov = {}
    pts = [frozenset(b) for b in B]
    for b in B:
        for q in itertools.combinations(sorted(b), 2): cov[q] = 1
    pts += [frozenset(q) for q in itertools.combinations(range(d), 2) if q not in cov]
    s = [0] * d
    for P in pts:
        for i in P: s[i] += 1
    bad = []
    for H0 in range(d):
        if s[H0] != 8: continue
        onH = [P for P in pts if H0 in P]
        # order points by k descending to match vector order
        onH.sort(key=lambda P: -len(P))
        k = tuple(len(P) - 1 for P in onH)
        if 1 not in k: continue
        lines = []
        for P in onH:
            lines += sorted(x for x in P if x != H0)
        idx = {x: i for i, x in enumerate(lines)}
        val = {}
        for X in lines:
            for dd in range(5): val['y_%d_%d' % (idx[X], dd)] = 1 if 8 - s[X] == dd else 0
        for P in pts:
            if H0 in P: continue
            L = sorted(idx[x] for x in P)
            if len(L) == 2: val['e_%d_%d' % tuple(L)] = 1
            if len(L) == 3: val['t_%d_%d_%d' % tuple(L)] = 1
        # phimax over S containing H0
        best = -99
        for T in itertools.combinations([x for x in range(d) if x != H0], 3):
            S = frozenset(T) | {H0}
            f = sum(1 for P in pts if P <= S)
            best = max(best, sum(s[x] - 7 for x in S) - f)
        thr = 4 - best
        binv, cons = build(k, None, thr)
        for l, op, r in cons:
            tot = 0
            for m in re.finditer(r'([+-]?)\s*(\d*)\s*([yet]_[\d_]+)', l):
                sign = -1 if m.group(1) == '-' else 1
                c = int(m.group(2)) if m.group(2) else 1
                tot += sign * c * val.get(m.group(3), 0)
            ok = (tot <= r) if op == '<=' else (tot >= r) if op == '>=' else (tot == r)
            if not ok: bad.append((k, thr, l[:80], op, r, tot))
    return bad
n = 0; nb = 0
for line in open(sys.argv[1]):
    B = decode(line, d)
    bad = check(B)
    n += 1
    if bad:
        nb += 1
        if nb <= 5: print('VIOLATION', bad[:3])
    if n >= int(sys.argv[2]): break
print('checked', n, 'lattices, with violations:', nb)
