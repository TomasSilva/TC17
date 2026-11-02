"""Covering lemma, computer-assisted part (see TC_N17.md).  (gamma) = a window lattice with an 8-point line H0
in which every 4-set S of lines has phi(S) <= 0, phi(S) = sum_{H in S}(s_H - 7) - f(S).  Only 4-sets S that
contain H0 are used.  For each multiplicity vector k of H0 (k_i = m_i - 1, sum 16, 8 points, k_i <= 5, at
least one k_i = 1) an ILP whose feasibility is NECESSARY for (gamma):
  the 16 other lines X, grouped by their point P_i on H0 (group sizes k_i); delta_X = 8 - s_X in 0..4;
  e_AB = 1 iff A, B (different groups) meet in a double point;
  tau_ABC = 1 iff A, B, C (pairwise different groups) meet in a point carrying exactly these three lines;
  (gamma): for every 3 lines A,B,C: delta_A + delta_B + delta_C + f({H0,A,B,C}) >= 4;
  line consistency: the double points b' of X off H0 satisfy 2s-18+k <= b' <= floor((5s-21+k)/4), X has at
  least two points of multiplicity >= 3, 8-point lines have a double point;
  global: Delta = sum delta <= 32 - max(11, W(H0)); t2 = b0 + sum e <= 64 - 3 Delta - t5(H0) - 3 t6(H0)."""
import itertools, sys
def vectors():
    out = []
    def rec(prefix, remaining, slots, maxv):
        if slots == 0:
            if remaining == 0: out.append(tuple(prefix))
            return
        for v in range(min(maxv, remaining - (slots - 1)), 0, -1):
            rec(prefix + [v], remaining - v, slots - 1, v)
    rec([], 16, 8, 5)
    return [v for v in out if 1 in v]
def lin(terms):
    """terms: list of (coef, var); returns LP string"""
    s = []
    for c, v in terms:
        if c == 0: continue
        if not s:
            s.append(('%d %s' % (c, v)) if c != 1 else v)
            if c == -1: s[-1] = '- ' + v
        else:
            if c > 0: s.append('+ %s' % v if c == 1 else '+ %d %s' % (c, v))
            else: s.append('- %s' % v if c == -1 else '- %d %s' % (-c, v))
    return ' '.join(s) if s else '0 dummy'
THR = 4
def build(k, extra=None, thr=None):
    thr = THR if thr is None else thr
    g = [i for i, ki in enumerate(k) for _ in range(ki)]
    n = len(g); assert n == 16
    D = range(5)
    y = lambda X, d: 'y_%d_%d' % (X, d)
    e = lambda A, B: 'e_%d_%d' % (min(A, B), max(A, B))
    t = lambda A, B, C: 't_%d_%d_%d' % tuple(sorted((A, B, C)))
    pairs = [(A, B) for A in range(n) for B in range(A + 1, n) if g[A] != g[B]]
    triples = [T for T in itertools.combinations(range(n), 3) if len({g[x] for x in T}) == 3]
    binv, cons = [], []
    for X in range(n):
        binv += [y(X, d) for d in D]
        cons.append((lin([(1, y(X, d)) for d in D]), '=', 1))
    binv += [e(A, B) for A, B in pairs] + [t(*T) for T in triples]
    dl = lambda X: [(d, y(X, d)) for d in D if d]
    tri_by_pair = {}
    for T in triples:
        for P in itertools.combinations(T, 2): tri_by_pair.setdefault(P, []).append(T)
    for A, B in pairs:
        cons.append((lin([(1, e(A, B))] + [(1, t(*T)) for T in tri_by_pair.get((A, B), [])]), '<=', 1))
    for A, B, C in itertools.combinations(range(n), 3):
        terms = dl(A) + dl(B) + dl(C); const = 0
        gs = [g[A], g[B], g[C]]
        if len(set(gs)) == 1:
            if k[gs[0]] == 3: const += 1
        elif len(set(gs)) == 2:
            for (X, Y, Z) in ((A, B, C), (A, C, B), (B, C, A)):
                if g[X] == g[Y]:
                    if k[g[X]] == 2: const += 1
                    if k[g[Z]] == 1: const += 1
                    terms += [(1, e(X, Z)), (1, e(Y, Z))]
        else:
            const += sum(1 for X in (A, B, C) if k[g[X]] == 1)
            terms += [(1, e(A, B)), (1, e(A, C)), (1, e(B, C)), (1, t(A, B, C))]
        cons.append((lin(terms), '>=', thr - const))
    for X in range(n):
        ki = k[g[X]]
        bt = [(1, e(X, Y)) for Y in range(n) if g[Y] != g[X]]
        cons.append((lin(bt + [(-((5 * (8 - d) - 21 + ki) // 4), y(X, d)) for d in D]), '<=', 0))
        cons.append((lin(bt + [(-(2 * (8 - d) - 18 + ki), y(X, d)) for d in D]), '>=', 0))
        cons.append((lin(bt + [(-((8 - d) - 3 + (1 if ki >= 2 else 0)), y(X, d)) for d in D]), '<=', 0))
        if ki != 1:
            cons.append((lin(bt + [(-1, y(X, 0))]), '>=', 0))
    W0 = sum((ki - 1) * (ki - 2) // 2 for ki in k)
    t5 = sum(1 for ki in k if ki == 4); t6 = sum(1 for ki in k if ki == 5)
    b0 = sum(1 for ki in k if ki == 1)
    Dl = [term for X in range(n) for term in dl(X)]
    cons.append((lin(Dl), '<=', 32 - max(11, W0)))
    cons.append((lin([(1, e(A, B)) for A, B in pairs] + [(3 * c, v) for c, v in Dl]), '<=', 64 - t5 - 3 * t6 - b0))
    if extra: cons += extra(k, g, y, e, t, Dl)
    return binv, cons
def write_lp(k, path, extra=None, thr=None):
    binv, cons = build(k, extra, thr)
    with open(path, 'w') as f:
        f.write('Minimize\n obj: %s\nSubject To\n' % binv[0])
        for i, (l, op, r) in enumerate(cons):
            f.write(' c%d: %s %s %d\n' % (i, l, op, r))
        f.write('Binary\n')
        for v in binv: f.write(' %s\n' % v)
        f.write('End\n')
if __name__ == '__main__':
    for k in vectors():
        write_lp(k, 'k_%s.lp' % ''.join(map(str, k)))
        print(''.join(map(str, k)))
