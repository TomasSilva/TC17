"""Independent exact check of level-2 infeasibility: integer bound propagation with probing (sound:
it only derives consequences of the constraints for 0/1 variables).  Reads the constraints from
gamma_ilp.build with the deltas fixed."""
import sys, re, itertools
from gamma_ilp import build, vectors
from level1 import survivors
TOK = re.compile(r'([+-]?)\s*(\d*)\s*([yet]_[\d_]+)')
def parse(l):
    terms = []
    for m in TOK.finditer(l):
        sign = -1 if m.group(1) == '-' else 1
        c = int(m.group(2)) if m.group(2) else 1
        terms.append((sign * c, m.group(3)))
    return terms
def prepare(k, deltas, thr=4):
    binv, cons = build(k, None, thr)
    fixed = {}
    for X in range(16):
        for d in range(5): fixed['y_%d_%d' % (X, d)] = 1 if deltas[X] == d else 0
    C = []
    for l, op, r in cons:
        terms = parse(l)
        const = sum(c * fixed[v] for c, v in terms if v in fixed)
        rest = [(c, v) for c, v in terms if v not in fixed]
        rr = r - const
        if op in ('<=', '='): C.append(([(-c, v) for c, v in rest], -rr))   # -sum >= -r
        if op in ('>=', '='): C.append((rest, rr))
    vars_ = sorted({v for t, _ in C for _, v in t})
    return C, vars_
def propagate(C, lo, hi):
    """C: list of (terms, rhs) meaning sum c*x >= rhs.  Returns False if infeasible."""
    changed = True
    while changed:
        changed = False
        for terms, rhs in C:
            mx = 0
            for c, v in terms: mx += c * (hi[v] if c > 0 else lo[v])
            if mx < rhs: return False
            for c, v in terms:
                if lo[v] == hi[v]: continue
                # if setting v to its 'bad' value makes max < rhs, fix it
                if c > 0 and mx - c < rhs: lo[v] = 1; changed = True; mx = mx  # v must be 1
                elif c < 0 and mx + c < rhs: hi[v] = 0; changed = True
    return True
def infeasible(C, vars_, probe=True):
    lo = {v: 0 for v in vars_}; hi = {v: 1 for v in vars_}
    if not propagate(C, lo, hi): return True
    if not probe: return False
    again = True
    while again:
        again = False
        for v in vars_:
            if lo[v] != hi[v]:
                l0, h0 = dict(lo), dict(hi); h0[v] = 0
                ok0 = propagate(C, l0, h0)
                l1, h1 = dict(lo), dict(hi); l1[v] = 1
                ok1 = propagate(C, l1, h1)
                if not ok0 and not ok1: return True
                if not ok0: lo[v] = 1; again = True
                elif not ok1: hi[v] = 0; again = True
                if again:
                    if not propagate(C, lo, hi): return True
                    break
    return False
if __name__ == '__main__':
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    idx = 0; n_inf = n_open = 0
    for k in vectors():
        for Delta, chosen in survivors(k, 4):
            if idx % nparts == part:
                deltas = [d for tup in chosen for d in tup]
                C, V = prepare(k, deltas)
                if infeasible(C, V): n_inf += 1
                else:
                    n_open += 1; print('OPEN', idx, k, chosen, flush=True)
            idx += 1
    print('part', part, 'infeasible', n_inf, 'open', n_open)
