# Stage 2: for each big-block configuration, enumerate all ways to add triples so that every point has
# w(x) in [wmin, wmax] and the total W equals Wtot (exactly n3 = Wtot - W_B triples).  Each solution is a
# candidate lattice; solutions are deduplicated up to isomorphism by certificate.
# Search: pairs are decided in a fixed order (point x ascending, partner y ascending): either (x, y) stays
# a double point, or it is covered by a new triple {x, y, z} with z > y.  Each triple set is found once.
import sys, json, time, itertools, hashlib
from math import comb
import pynauty

n, wmin, wmax, bmax, Wtot = (int(a) for a in sys.argv[1:6])
tag = sys.argv[6]
part = int(sys.argv[7]) if len(sys.argv) > 7 else 0
nparts = int(sys.argv[8]) if len(sys.argv) > 8 else 1
IN = '/Users/agent/Projects/TC17/work/tc15/bigblocks_%s.jsonl' % tag
OUT = '/Users/agent/Projects/TC17/work/tc15/lattices_%s_%d.jsonl' % (tag, part)


def cert(blocks):
    nb = len(blocks)
    adj = {n + k: list(B) for k, B in enumerate(blocks)}
    g = pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=[set(range(n)), set(range(n, n + nb))])
    return hashlib.sha1(pynauty.certificate(g)).digest()


def fill(big, w0, n3):
    """Exact-cover style search with bitmasks: always decide the undecided uncovered pair with the
    fewest options (triples through it, plus 'stays a double point' while slack remains); slack =
    (uncovered pairs) - 3 n3 is the number of pairs that will remain uncovered.  Isomorph rejection at
    nodes: options up to the automorphism group of the structure decided so far (nauty), computed while
    the group stays nontrivial along the path."""
    big = [tuple(B) for B in big]
    full = (1 << n) - 1
    unc = [full & ~(1 << a) for a in range(n)]
    for B in big:
        for a, b in itertools.combinations(B, 2):
            unc[a] &= ~(1 << b); unc[b] &= ~(1 << a)
    w = list(w0)
    npairs = sum(bin(unc[a]).count('1') for a in range(n)) // 2
    slack0 = npairs - 3 * n3
    if slack0 < 0:
        return []
    tri, dbl, sols = [], [], []
    bits = lambda m: [i for i in range(n) if m >> i & 1]
    seen_partial = set()

    def partial_key():
        blocks = big + tri + dbl
        nb = len(blocks)
        adj = {n + k: list(B) for k, B in enumerate(blocks)}
        cols = [set(range(n)), set(range(n, n + len(big))), set(range(n + len(big), n + len(big) + len(tri))),
                set(range(n + len(big) + len(tri), n + nb))]
        cols = [c for c in cols if c]
        g = pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=cols)
        return hashlib.sha1(pynauty.certificate(g)).digest()

    def node_gens(a, b):
        blocks = big + tri + dbl
        nb = len(blocks)
        adj = {n + k: list(B) for k, B in enumerate(blocks)}
        cols = [{a, b}, set(range(n)) - {a, b}, set(range(n, n + len(big))),
                set(range(n + len(big), n + len(big) + len(tri))), set(range(n + len(big) + len(tri), n + nb))]
        cols = [c for c in cols if c]
        g = pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=cols)
        return pynauty.autgrp(g)[0]

    def rec(ntri, slack, use_aut):
        if ntri == n3:
            if all(wmin <= v <= wmax for v in w):
                sols.append(list(tri))
            return
        need = 3 * (n3 - ntri)
        deficit = 0; room = 0
        for v in range(n):
            if w[v] < wmin:
                deficit += wmin - w[v]
            if w[v] < wmax:
                room |= 1 << v
        if deficit > need:
            return
        cap = 0
        for v in range(n):
            if w[v] < wmax:
                av = bin(unc[v] & room).count('1') // 2
                if w[v] + av < wmin:
                    return
                cap += min(wmax - w[v], av)
            elif w[v] < wmin:
                return
        if cap < need:
            return
        if tri or dbl:
            pk = partial_key()
            if pk in seen_partial:
                return
            seen_partial.add(pk)
        # choose the undecided pair with the fewest options
        best = None
        leave = 1 if slack > 0 else 0
        for a in range(n):
            ua = unc[a] >> (a + 1) << (a + 1)
            if not ua:
                continue
            if w[a] >= wmax:
                if leave == 0:
                    return
                b = bits(ua)[0]
                best = (1, a, b, 0); break
            while ua:
                b = (ua & -ua).bit_length() - 1; ua &= ua - 1
                if w[b] >= wmax:
                    if leave == 0:
                        return
                    best = (1, a, b, 0); break
                om = unc[a] & unc[b] & room
                cnt = bin(om).count('1') + leave
                if cnt == 0:
                    return
                if best is None or cnt < best[0]:
                    best = (cnt, a, b, om)
                    if cnt == 1:
                        break
            if best is not None and best[0] == 1:
                break
        if best is None:
            return
        _, a, b, om = best
        opts = bits(om)
        child_aut = use_aut
        if use_aut and len(opts) > 1:
            gens = node_gens(a, b)
            if not gens:
                child_aut = False
            else:
                parent = {z: z for z in opts}

                def find(z):
                    while parent[z] != z:
                        parent[z] = parent[parent[z]]; z = parent[z]
                    return z
                for gg in gens:
                    for z in opts:
                        gz = gg[z]
                        if gz in parent:
                            ra, rb = find(z), find(gz)
                            if ra != rb:
                                parent[ra] = rb
                opts = [z for z in opts if find(z) == z]
        for z in opts:
            T = (a, b, z)
            for u in T:
                w[u] += 1
            for u, v in ((a, b), (a, z), (b, z)):
                unc[u] &= ~(1 << v); unc[v] &= ~(1 << u)
            tri.append(tuple(sorted(T)))
            rec(ntri + 1, slack, child_aut)
            tri.pop()
            for u, v in ((a, b), (a, z), (b, z)):
                unc[u] |= 1 << v; unc[v] |= 1 << u
            for u in T:
                w[u] -= 1
        if slack > 0:
            unc[a] &= ~(1 << b); unc[b] &= ~(1 << a)
            dbl.append((a, b))
            rec(ntri, slack - 1, child_aut)
            dbl.pop()
            unc[a] |= 1 << b; unc[b] |= 1 << a
    rec(0, slack0, True)
    return sols


def autsize_and_gens(blocks):
    nb = len(blocks)
    adj = {n + k: list(B) for k, B in enumerate(blocks)}
    g = pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=[set(range(n)), set(range(n, n + nb))])
    gens, s1, s2, _, _ = pynauty.autgrp(g)
    return s1 * 10 ** s2, gens


def fill_bfs(big, w0, n3):
    """Isomorph-free search: add one triple at a time, one representative per orbit of Aut(current
    structure); partial structures deduplicated by certificate.  Returns one triple set per class."""
    from collections import deque
    big = [tuple(B) for B in big]
    start = ()
    seen = {cert(big)}
    queue = deque([(start, tuple(w0))])
    sols = []
    while queue:
        tri, w = queue.popleft()
        blocks = big + list(tri)
        ntri = len(tri)
        if ntri == n3:
            if all(wmin <= v <= wmax for v in w):
                sols.append(list(tri))
            continue
        cov = set()
        for B in blocks:
            cov.update(itertools.combinations(B, 2))
        unc = [(a, b) for a in range(n) for b in range(a + 1, n) if (a, b) not in cov]
        if 3 * (n3 - ntri) > len(unc):
            continue
        if sum(max(0, wmin - v) for v in w) > 3 * (n3 - ntri):
            continue
        rem = [0] * n
        for a, b in unc:
            if w[a] < wmax and w[b] < wmax:
                rem[a] += 1; rem[b] += 1
        if any(w[v] + rem[v] // 2 < wmin for v in range(n)):
            continue
        cands = [T for T in itertools.combinations(range(n), 3)
                 if all(w[u] < wmax for u in T) and not any(p in cov for p in itertools.combinations(T, 2))]
        if not cands:
            continue
        _, gens = autsize_and_gens(blocks)
        if gens:
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
            reps = [T for i, T in enumerate(cands) if find(i) == i]
        else:
            reps = cands
        for T in reps:
            nw = list(w)
            for u in T:
                nw[u] += 1
            ntri2 = tuple(sorted(tri + (T,)))
            c = cert(big + list(ntri2))
            if c not in seen:
                seen.add(c); queue.append((ntri2, tuple(nw)))
    return sols


def run():
    """Stream the configurations of this part (never holding them all in memory); solutions are
    written as they are found and deduplicated by certificate within each configuration."""
    t0 = time.time()
    out = open(OUT, 'w')
    total_raw = total_distinct = nconf = 0
    with open(IN) as fh:
        for i, line in enumerate(fh):
            if i % nparts != part:
                continue
            c = json.loads(line); nconf += 1
            big = [tuple(B) for B in c['blocks']]
            n3 = Wtot - c['W']
            t1 = time.time()
            sols = fill(big, c['w'], n3)
            if time.time() - t1 > 60:
                print('  slow config %d: %d big blocks, n3=%d, %d solutions, %.0fs' % (i, len(big), n3, len(sols), time.time() - t1), flush=True)
            total_raw += len(sols)
            seen = set()
            for T in sols:
                blocks = sorted(big + [tuple(t) for t in T])
                k = cert(blocks)
                if k in seen:
                    continue
                seen.add(k); total_distinct += 1
                w = list(c['w'])
                for t in T:
                    for u in t:
                        w[u] += 1
                out.write(json.dumps({'blocks': [list(B) for B in blocks], 's': [n - 1 - v for v in w]}) + '\n')
            if nconf % 20000 == 0:
                print('%d configs, raw solutions %d, distinct lattices %d (%.0fs)' % (nconf, total_raw, total_distinct, time.time() - t0), flush=True)
                out.flush()
    out.close()
    print('FINAL %s part %d: %d configs, %d raw solutions, %d distinct lattices (%.0fs)' % (tag, part, nconf, total_raw, total_distinct, time.time() - t0), flush=True)


if __name__ == '__main__':
    run()
