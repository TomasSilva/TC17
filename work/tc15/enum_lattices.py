# Enumerate, up to isomorphism, the rank-3 simple matroids ("linear spaces") on n elements that could
# carry a Terao counterexample with exponents (1, d1, d2):
#   elements = lines of the arrangement, blocks = multiple points (|B| = multiplicity, 3 <= |B| <= bmax),
#   w(x) = sum_{B ∋ x} (|B| - 2) = (n - 1) - s_x  must lie in [wmin, wmax]  (s_x = points on line x),
#   W = sum_B C(|B| - 1, 2) = C(n, 2) - b2  must equal Wtot  (chi splits with the given exponents).
# Search: states = (blocks, processed points, active point).  Children: add one block through the active
# point (one representative per orbit of Aut(state), which fixes the active point by colouring), or declare
# the active point complete and pick the next active point canonically (max w, then first canonical label).
# States are explored once up to isomorphism (pynauty certificate + colour signature).
import sys, json, time, itertools, hashlib
from math import comb
from collections import deque
import pynauty

n, wmin, wmax, bmax, Wtot = (int(a) for a in sys.argv[1:6])
tag = sys.argv[6]
OUT = '/Users/agent/Projects/TC17/work/tc15/lattices_%s.jsonl' % tag
RATIO = 3  # a triple raises w of 3 points by 1 at W-cost 1: the best deficit/cost ratio of any block


def graph(blocks, processed, active):
    nb = len(blocks)
    adj = {n + k: list(B) for k, B in enumerate(blocks)}
    rest = set(range(n)) - set(processed) - ({active} if active is not None else set())
    cols = [set(processed), {active} if active is not None else set(), rest, set(range(n, n + nb))]
    cols = [c for c in cols if c]
    return pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=cols)


def key(blocks, processed, active):
    c = pynauty.certificate(graph(blocks, processed, active))
    return (len(processed), active is not None, len(blocks), hashlib.sha1(c).digest())


def covered(blocks):
    cov = set()
    for B in blocks:
        for a, b in itertools.combinations(B, 2):
            cov.add((a, b)); cov.add((b, a))
    return cov


def next_active(blocks, processed, w):
    unproc = [y for y in range(n) if y not in processed]
    if not unproc:
        return None
    if not blocks:
        return unproc[0]
    lab = pynauty.canon_label(graph(blocks, processed, None))
    pos = {v: i for i, v in enumerate(lab)}
    return max(unproc, key=lambda y: (w[y], -pos[y]))


def tail_orbits(blocks, processed, x, tails):
    """One representative per orbit of Aut(blocks, processed, x) on the candidate tails."""
    if not tails:
        return []
    gens = pynauty.autgrp(graph(blocks, processed, x))[0]
    if not gens:
        return tails
    idx = {T: i for i, T in enumerate(tails)}
    parent = list(range(len(tails)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for g in gens:
        for T in tails:
            gT = tuple(sorted(g[v] for v in T))
            j = idx.get(gT)
            if j is not None:
                a, b = find(idx[T]), find(j)
                if a != b:
                    parent[a] = b
    return [T for i, T in enumerate(tails) if find(i) == i]


def run():
    t0 = time.time()
    seen = set()
    finals = {}
    root = ((), (), 0, tuple([0] * n), 0)        # blocks, processed, active, w, W
    seen.add(key((), (), 0))
    queue = deque([root])
    expanded = 0
    while queue:
        blocks, processed, x, w, W = queue.popleft()
        expanded += 1
        if expanded % 2000 == 0:
            print('expanded %d, queue %d, seen %d, finals %d (%.0fs)' % (expanded, len(queue), len(seen), len(finals), time.time() - t0), flush=True)
        cov = covered(blocks)
        # (a) declare x complete
        if wmin <= w[x] <= wmax:
            nproc = tuple(sorted(processed + (x,)))
            y = next_active(blocks, nproc, w)
            if y is None:
                if W == Wtot:
                    c = pynauty.certificate(graph(blocks, (), None))
                    finals.setdefault(c, {'blocks': [list(B) for B in blocks], 's': [n - 1 - v for v in w]})
            else:
                k = key(blocks, nproc, y)
                if k not in seen:
                    seen.add(k); queue.append((blocks, nproc, y, w, W))
        # (b) add one block {x} u T
        avail = [y for y in range(n) if y not in processed and y != x and (x, y) not in cov]
        tails = []
        for size in range(2, bmax):
            if W + comb(size, 2) > Wtot or w[x] + size - 1 > wmax:
                continue
            for T in itertools.combinations(avail, size):
                if all(w[u] + size - 1 <= wmax for u in T) and all((a, b) not in cov for a, b in itertools.combinations(T, 2)):
                    tails.append(T)
        for T in tail_orbits(blocks, processed, x, tails):
            nb = tuple(sorted(blocks + (tuple(sorted((x,) + T)),)))
            nw = list(w)
            for u in T + (x,):
                nw[u] += len(T) - 1
            nW = W + comb(len(T), 2)
            deficit = sum(max(0, wmin - nw[y]) for y in range(n) if y not in processed and y != x) + max(0, wmin - nw[x])
            if deficit > RATIO * (Wtot - nW):
                continue
            nw = tuple(nw)
            if nW == Wtot:
                if all(wmin <= v <= wmax for v in nw):
                    c = pynauty.certificate(graph(nb, (), None))
                    finals.setdefault(c, {'blocks': [list(B) for B in nb], 's': [n - 1 - v for v in nw]})
                continue
            k = key(nb, processed, x)
            if k not in seen:
                seen.add(k); queue.append((nb, processed, x, nw, nW))
    with open(OUT, 'w') as f:
        for rec in finals.values():
            f.write(json.dumps(rec) + '\n')
    print('FINAL %s: %d lattices, %d states expanded (%.0fs)' % (tag, len(finals), expanded, time.time() - t0), flush=True)


if __name__ == '__main__':
    run()
