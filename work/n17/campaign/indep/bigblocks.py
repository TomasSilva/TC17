# Stage 1 of the candidate-lattice enumeration: all configurations (up to isomorphism) of "big" blocks
# (sizes 4..bmax, pairwise meeting in <= 1 point) on n points that can be completed by triples to a
# lattice with w(x) in [wmin, wmax] for all x and W = Wtot.  Every partial configuration is output.
#   w_B(x) = sum_{B ∋ x} (|B| - 2) <= wmax;  W_B = sum_B C(|B|-1, 2) <= Wtot;
#   deficit bound: sum_x max(0, wmin - w_B(x)) <= 3 (Wtot - W_B)   (triples have the best ratio 3).
import sys, json, time, itertools, hashlib
from math import comb
from collections import deque
import pynauty

n, wmin, wmax, bmax, Wtot = (int(a) for a in sys.argv[1:6])
tag = sys.argv[6]
OUT = '/Users/agent/Projects/TC17/work/n17/campaign/indep/bigblocks_%s.jsonl' % tag


def graph(blocks):
    nb = len(blocks)
    adj = {n + k: list(B) for k, B in enumerate(blocks)}
    cols = [set(range(n))] + ([set(range(n, n + nb))] if nb else [])
    return pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=cols)


def feasible(w, W):
    n3 = Wtot - W
    lo = sum(max(0, wmin - v) for v in w)
    hi = sum(wmax - v for v in w)
    return lo <= 3 * n3 <= hi and lo <= 3 * n3


def run():
    """Depth-first, blocks added in non-increasing size order (each configuration has a unique
    size-sorted sequence, so intermediate states are only its size-prefixes); states deduplicated by
    certificate; orbit pruning of candidate blocks under Aut(state)."""
    t0 = time.time()
    seen = {hashlib.sha1(pynauty.certificate(graph(()))).digest()}
    stack = [((), tuple([0] * n), 0, bmax)]
    out = open(OUT, 'w')
    count = expanded = 0
    while stack:
        blocks, w, W, smax = stack.pop()
        expanded += 1
        if feasible(w, W):
            out.write(json.dumps({'blocks': [list(B) for B in blocks], 'w': list(w), 'W': W}) + '\n')
            count += 1
        cov = set()
        for B in blocks:
            cov.update(itertools.combinations(B, 2))
        cands = []
        for size in range(4, smax + 1):
            if W + comb(size - 1, 2) > Wtot:
                continue
            for T in itertools.combinations(range(n), size):
                if all(w[u] + size - 2 <= wmax for u in T) and not any(p in cov for p in itertools.combinations(T, 2)):
                    cands.append(T)
        if not cands:
            continue
        g = graph(blocks)
        gens = pynauty.autgrp(g)[0]
        idx = {T: i for i, T in enumerate(cands)}
        parent = list(range(len(cands)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]; i = parent[i]
            return i
        for gg in gens:
            for T in cands:
                j = idx.get(tuple(sorted(gg[v] for v in T)))
                if j is not None:
                    a, b = find(idx[T]), find(j)
                    if a != b:
                        parent[a] = b
        for i, T in enumerate(cands):
            if find(i) != i:
                continue
            nb = tuple(sorted(blocks + (T,)))
            nw = list(w)
            for u in T:
                nw[u] += len(T) - 2
            nW = W + comb(len(T) - 1, 2)
            if sum(max(0, wmin - v) for v in nw) > 3 * (Wtot - nW):
                continue
            k = hashlib.sha1(pynauty.certificate(graph(nb))).digest()
            if k not in seen:
                seen.add(k); stack.append((nb, tuple(nw), nW, len(T)))
        if expanded % 20000 == 0:
            print('expanded %d, stack %d, seen %d, output %d (%.0fs)' % (expanded, len(stack), len(seen), count, time.time() - t0), flush=True)
    out.close()
    print('FINAL %s: %d big-block configurations, %d states (%.0fs)' % (tag, count, len(seen), time.time() - t0), flush=True)


if __name__ == '__main__':
    run()
