# Experiment: triple filling with exact realisability pruning of partial structures.
# At a node (big blocks + triples so far + decided doubles), the partial structure must be weakly
# realisable: all its blocks collinear, no point on the line of a block it does not belong to, and
# the decided double points not collinear with any third point... (the last is a condition on a pair
# of polynomials and is skipped).  Tested with the python-flint fast path when the frame-fixed
# parametrisation needs <= 2 unknowns (one-sided: only NONREAL is ever asserted).
import sys, os, json, itertools, time
import flint
sys.argv = [sys.argv[0], '15', '/dev/null', '0', '1']
import importlib.util
spec = importlib.util.spec_from_file_location('fr', '/Users/agent/Projects/TC17/work/tc15/fast_real.py')
fr = importlib.util.module_from_spec(spec); spec.loader.exec_module(fr)
n = 15
ctx3 = flint.fmpz_mpoly_ctx.get(('u0', 'u1', 'u2')); gens3 = ctx3.gens()


def partial_setup(blocks):
    """Like fr.setup but 'bad' = points on block lines they do not belong to (necessary for any completion)."""
    blocks = [tuple(B) for B in blocks]
    inblock = {}
    for B in blocks:
        for p in itertools.combinations(sorted(B), 2):
            inblock[p] = B

    def collinear(a, b, c):
        B = inblock.get((min(a, b), max(a, b)))
        return B is not None and c in B
    frame = next((f for f in itertools.combinations(range(n), 4)
                  if not any(collinear(*t) for t in itertools.combinations(f, 3))), None)
    if frame is None:
        return None
    one, zero = ctx3.from_dict({(0, 0, 0): 1}), ctx3.from_dict({})
    P = {frame[0]: (one, zero, zero), frame[1]: (zero, one, zero), frame[2]: (zero, zero, one), frame[3]: (one, one, one)}
    nvar, order = 0, list(frame)
    todo = [e for e in range(n) if e not in P]
    while todo:
        best = None
        for e in todo:
            det_lines = []
            for B in blocks:
                if e in B:
                    D = [x for x in B if x in P]
                    if len(D) >= 2:
                        det_lines.append((D[0], D[1]))
            if best is None or len(det_lines) > best[1]:
                best = (e, len(det_lines), det_lines)
        e, score, det_lines = best
        todo.remove(e); order.append(e)
        if score >= 2:
            (a1, b1), (a2, b2) = det_lines[0], det_lines[1]
            P[e] = fr.cross(fr.cross(P[a1], P[b1]), fr.cross(P[a2], P[b2]))
        elif score == 1:
            if nvar >= 3:
                return None
            a1, b1 = det_lines[0]
            g = gens3[nvar]; nvar += 1
            P[e] = tuple(P[a1][i] + g * P[b1][i] for i in range(3))
        else:
            if nvar + 1 >= 3:
                return None
            P[e] = (gens3[nvar], gens3[nvar + 1], one); nvar += 2
    eqs, bad = [], []
    for B in blocks:
        Bs = sorted(B, key=lambda x: order.index(x))
        for c in Bs[2:]:
            eqs.append(fr.det3(P[Bs[0]], P[Bs[1]], P[c]))
        for x in range(n):
            if x not in B:
                bad.append(fr.det3(P[Bs[0]], P[Bs[1]], P[x]))
    return nvar, eqs, bad


def partial_nonreal(blocks):
    r = partial_setup(blocks)
    if r is None:
        return False
    nvar, eqs, bad = r
    if any(b == 0 for b in bad):
        return True
    eqs = [f for f in eqs if f != 0]
    if nvar == 0:
        return bool(eqs)
    if nvar == 1:
        if not eqs:
            return False
        g = fr.univariate(eqs[0], 0)
        for f in eqs[1:]:
            g = g.gcd(fr.univariate(f, 0))
            if g.degree() == 0:
                return True
        g = fr.strip_bad(g, [fr.univariate(b, 0) for b in bad])
        return g.degree() == 0
    if nvar == 2:
        if len(eqs) < 2:
            return False
        G = None
        for i in range(min(len(eqs), 6)):
            for j in range(i + 1, min(len(eqs), 8)):
                R = eqs[i].resultant(eqs[j], 'u1')
                if R == 0:
                    continue
                Ru = fr.univariate(R, 0)
                G = Ru if G is None else G.gcd(Ru)
                if G.degree() == 0:
                    return True
        return False
    return False


# --- the triple filler (as in fill_triples.py, bitmask version) with an optional pruning hook ---
def fill(big, w0, n3, wmin, wmax, prune, stats):
    import hashlib, pynauty
    from math import comb
    big = [tuple(B) for B in big]
    full = (1 << n) - 1
    unc = [full & ~(1 << a) for a in range(n)]
    for B in big:
        for a, b in itertools.combinations(B, 2):
            unc[a] &= ~(1 << b); unc[b] &= ~(1 << a)
    w = list(w0)
    npairs = sum(bin(unc[a]).count('1') for a in range(n)) // 2
    slack0 = npairs - 3 * n3
    tri, dbl, sols = [], [], []
    bits = lambda m: [i for i in range(n) if m >> i & 1]
    seen = set()

    def key():
        blocks = big + tri + dbl
        nb = len(blocks)
        adj = {n + k: list(B) for k, B in enumerate(blocks)}
        cols = [set(range(n)), set(range(n, n + len(big))), set(range(n + len(big), n + len(big) + len(tri))), set(range(n + len(big) + len(tri), n + nb))]
        cols = [c for c in cols if c]
        return hashlib.sha1(pynauty.certificate(pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=cols))).digest()

    def rec(ntri, slack):
        stats['nodes'] += 1
        if ntri == n3:
            if all(wmin <= v <= wmax for v in w):
                sols.append(list(tri))
            return
        need = 3 * (n3 - ntri)
        deficit = 0; room = 0
        for v in range(n):
            if w[v] < wmin: deficit += wmin - w[v]
            if w[v] < wmax: room |= 1 << v
        if deficit > need:
            return
        cap = 0
        for v in range(n):
            if w[v] < wmax:
                av = bin(unc[v] & room).count('1') // 2
                if w[v] + av < wmin: return
                cap += min(wmax - w[v], av)
            elif w[v] < wmin:
                return
        if cap < need:
            return
        if tri or dbl:
            k = key()
            if k in seen: return
            seen.add(k)
        if prune and tri:
            stats['checks'] += 1
            if partial_nonreal(big + tri):
                stats['pruned'] += 1; return
        best = None; leave = 1 if slack > 0 else 0
        for a in range(n):
            ua = unc[a] >> (a + 1) << (a + 1)
            if not ua: continue
            if w[a] >= wmax:
                if leave == 0: return
                best = (1, a, bits(ua)[0], 0); break
            while ua:
                b = (ua & -ua).bit_length() - 1; ua &= ua - 1
                if w[b] >= wmax:
                    if leave == 0: return
                    best = (1, a, b, 0); break
                om = unc[a] & unc[b] & room
                cnt = bin(om).count('1') + leave
                if cnt == 0: return
                if best is None or cnt < best[0]:
                    best = (cnt, a, b, om)
                    if cnt == 1: break
            if best is not None and best[0] == 1: break
        if best is None: return
        _, a, b, om = best
        for z in bits(om):
            T = (a, b, z)
            for u in T: w[u] += 1
            for u, v in ((a, b), (a, z), (b, z)):
                unc[u] &= ~(1 << v); unc[v] &= ~(1 << u)
            tri.append(tuple(sorted(T)))
            rec(ntri + 1, slack)
            tri.pop()
            for u, v in ((a, b), (a, z), (b, z)):
                unc[u] |= 1 << v; unc[v] |= 1 << u
            for u in T: w[u] -= 1
        if slack > 0:
            unc[a] &= ~(1 << b); unc[b] &= ~(1 << a)
            dbl.append((a, b))
            rec(ntri, slack - 1)
            dbl.pop()
            unc[a] |= 1 << b; unc[b] |= 1 << a
    rec(0, slack0)
    return sols


if __name__ == '__main__':
    recs = [json.loads(l) for l in open('/Users/agent/Projects/TC17/work/tc15/bigblocks_n15_7_7.jsonl')]
    idxs = [int(a) for a in os.environ.get('IDXS', '').split(',') if a]
    for idx in idxs:
        c = recs[idx]; big = [tuple(B) for B in c['blocks']]; n3 = 42 - c['W']
        for prune in (False, True):
            stats = {'nodes': 0, 'checks': 0, 'pruned': 0}
            t0 = time.time()
            sols = fill(big, c['w'], n3, 7, 10, prune, stats)
            print('config %d (%d big blocks, n3=%d) prune=%s: %d solutions, %s, %.1fs' % (idx, len(big), n3, prune, len(sols), stats, time.time() - t0), flush=True)
