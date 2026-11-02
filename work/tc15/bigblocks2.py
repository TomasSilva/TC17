# Stage 1 of the candidate-lattice enumeration, orderly version (canonical augmentation, McKay).
# Memoryless (no "seen" set) and parallel: the search tree is cut at --depth blocks, the seeds are
# grouped into chunks and the chunks are processed by a pool of workers; each chunk is written
# atomically to its own gzipped file, so a killed run is resumed by re-running the same command.
#
# States: sets of "big" blocks (sizes 4..bmax) on n points, pairwise meeting in <= 1 point, with
#   w(x) = sum_{B ∋ x} (|B| - 2) <= wmax  and, for at least one class c = (d1, d2),
#   deficit sum_x max(0, wmin - w(x)) <= 3 (Wtot_c - W),  W = sum_B C(|B|-1, 2),
#   Wtot_c = C(n,2) - d1 d2 - d1 - d2, and the unjoined-pair condition [Abe 2014, Cor. 1.2(2)]:
#   two disjoint blocks B, B' need (|B|-1) + (|B'|-1) <= d1 or = d2.
# All these are hereditary (sub-states of a valid state are valid), so the orderly generation is
# sound: every isomorphism class of valid states is produced exactly once, as parent-minus-canonical-
# last-block chains.  Blocks are added in non-increasing size order; the canonical last block is the
# block of minimal size with the largest canonical label; a child P + T is accepted iff T lies in
# the Aut(P + T)-orbit of that block.  Output lines: {"blocks", "w", "W", "c": [classes for which the
# state is output-feasible, i.e. also 3 (Wtot_c - W) <= sum_x (wmax - w(x))]}.
import sys, os, json, time, itertools, gzip, argparse
from math import comb
import pynauty
from multiprocessing import Pool

ap = argparse.ArgumentParser()
ap.add_argument('n', type=int); ap.add_argument('wmin', type=int); ap.add_argument('wmax', type=int)
ap.add_argument('bmax', type=int)
ap.add_argument('classes', help='comma-separated d1:d2, e.g. 7:9,8:8')
ap.add_argument('tag')
ap.add_argument('--nojoin', action='store_true', help='disable the unjoined-pair condition')
ap.add_argument('--depth', type=int, default=3, help='seed depth (number of blocks)')
ap.add_argument('--workers', type=int, default=8)
ap.add_argument('--chunks', type=int, default=400)
ap.add_argument('--first', type=int, default=0, help='restrict the first (largest) block to this size')
ap.add_argument('--outdir', default='')
args = ap.parse_args()
n, wmin, wmax, bmax = args.n, args.wmin, args.wmax, args.bmax
CLASSES = []
for s in args.classes.split(','):
    d1, d2 = (int(a) for a in s.split(':'))
    Wtot = comb(n, 2) - d1 * d2 - d1 - d2
    forb = set()
    if not args.nojoin:
        for a in range(3, bmax + 1):
            for b in range(3, bmax + 1):
                if (a - 1) + (b - 1) > d1 and (a - 1) + (b - 1) != d2:
                    forb.add((a, b))
    CLASSES.append((d1, d2, Wtot, forb))
NC = len(CLASSES)
OUTDIR = args.outdir or '/Users/agent/Projects/TC17/work/tc15/bb_%s' % args.tag
os.makedirs(OUTDIR, exist_ok=True)


def graph(blocks):
    """Points coloured 0; block vertices in the order of `blocks` (sorted by decreasing size),
    one colour class per size."""
    nb = len(blocks)
    adj = {n + k: list(B) for k, B in enumerate(blocks)}
    cols = [set(range(n))]
    k = 0
    while k < nb:
        j = k
        while j < nb and len(blocks[j]) == len(blocks[k]):
            j += 1
        cols.append(set(range(n + k, n + j))); k = j
    return pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=cols)


def accept(nb, tpos):
    """Canonicity test for the child state nb (sorted) whose added block is nb[tpos].
    Returns the automorphism generators of nb if accepted, else None."""
    g = graph(nb)
    lab = pynauty.canon_label(g)
    k = len(nb); smin = len(nb[-1])
    kmin = k
    while kmin > 0 and len(nb[kmin - 1]) == smin:
        kmin -= 1
    pos = [0] * (n + k)
    for i, v in enumerate(lab):
        pos[v] = i
    vstar = max(range(n + kmin, n + k), key=lambda v: pos[v])
    gens, _, _, orbits, _ = pynauty.autgrp(g)
    if orbits[vstar] != orbits[n + tpos]:
        return None
    return gens


def orbit_reps(cands, gens):
    if not gens or not cands:
        return cands
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
    return [T for i, T in enumerate(cands) if find(i) == i]


def all_cands(blocks, w, smax):
    """All blocks of size 4..smax meeting every block of `blocks` in <= 1 point, with w-room."""
    unc = [((1 << n) - 1) & ~(1 << u) for u in range(n)]
    for B in blocks:
        for a, b in itertools.combinations(B, 2):
            unc[a] &= ~(1 << b); unc[b] &= ~(1 << a)
    out = []
    for size in range(4, smax + 1):
        room = 0
        for u in range(n):
            if w[u] + size - 2 <= wmax:
                room |= 1 << u

        def rec(cl, mask, k):
            if k == size:
                out.append(tuple(cl)); return
            m = mask
            while m:
                v = (m & -m).bit_length() - 1; m &= m - 1
                rec(cl + [v], mask & unc[v] & ~((2 << v) - 1), k + 1)
        rec([], room, 0)
    return out


def out_flags(w, W, valid):
    lo = sum(max(0, wmin - v) for v in w); hi = sum(wmax - v for v in w)
    return [c for c in valid if 0 <= CLASSES[c][2] - W and lo <= 3 * (CLASSES[c][2] - W) <= hi]


def child_flags(blocks, T, nw, nW, valid):
    """Classes (subset of `valid`) for which the child is valid, and those for which it is output-feasible."""
    s = len(T); Ts = set(T)
    lo = sum(max(0, wmin - v) for v in nw)
    hi = sum(wmax - v for v in nw)
    nvalid, nout = [], []
    for c in valid:
        d1, d2, Wtot, forb = CLASSES[c]
        n3 = Wtot - nW
        if n3 < 0 or lo > 3 * n3:
            continue
        if forb and any((len(B), s) in forb and not (Ts & set(B)) for B in blocks):
            continue
        nvalid.append(c)
        if 3 * n3 <= hi:
            nout.append(c)
    return nvalid, nout


class Search:
    def __init__(self, out, maxdepth=None):
        self.out = out; self.maxdepth = maxdepth; self.seeds = []
        self.count = 0; self.states = 0; self.ccount = [0] * NC

    def emit(self, blocks, w, W, cout):
        self.states += 1
        if cout:
            self.count += 1
            for c in cout:
                self.ccount[c] += 1
            if self.out is not None:
                self.out.write(json.dumps({'blocks': [list(B) for B in blocks], 'w': list(w), 'W': W, 'c': cout}) + '\n')

    def expand(self, blocks, w, W, cands, gens, valid, depth):
        for T in orbit_reps(cands, gens):
            s = len(T)
            if depth == 0 and args.first and s != args.first:
                continue
            nw = list(w)
            for u in T:
                nw[u] += s - 2
            nW = W + comb(s - 1, 2)
            nvalid, nout = child_flags(blocks, T, nw, nW, valid)
            if not nvalid:
                continue
            nb = tuple(sorted(blocks + (T,), key=lambda B: (-len(B), B)))
            g2 = accept(nb, nb.index(T))
            if g2 is None:
                continue
            self.emit(nb, nw, nW, nout)
            if self.maxdepth is not None and depth + 1 >= self.maxdepth:
                self.seeds.append((nb, nvalid))
                continue
            Ts = set(T)
            ncands = [U for U in cands if len(U) <= s and len(Ts.intersection(U)) <= 1
                      and all(nw[u] + len(U) - 2 <= wmax for u in U)]
            self.expand(nb, nw, nW, ncands, g2, nvalid, depth + 1)


def root_state():
    w = [0] * n
    valid = list(range(NC))
    gens = pynauty.autgrp(graph(()))[0]
    cands = all_cands((), w, args.first or bmax)
    return w, cands, gens, valid


def run_seed(S, blocks, valid):
    w = [0] * n; W = 0
    for B in blocks:
        for u in B:
            w[u] += len(B) - 2
        W += comb(len(B) - 1, 2)
    gens = pynauty.autgrp(graph(blocks))[0]
    cands = all_cands(blocks, w, len(blocks[-1]))
    S.expand(blocks, w, W, cands, gens, valid, len(blocks))


def worker(job):
    ci, seeds = job
    final = os.path.join(OUTDIR, 'bb_%s_%04d.jsonl.gz' % (args.tag, ci))
    if os.path.exists(final):
        return ci, None
    tmp = final + '.tmp'
    t0 = time.time()
    with gzip.open(tmp, 'wt', compresslevel=4) as out:
        S = Search(out)
        for blocks, valid in seeds:
            run_seed(S, blocks, valid)
    os.rename(tmp, final)
    return ci, (S.count, S.states, S.ccount, time.time() - t0)


def main():
    t0 = time.time()
    print('classes:', [(d1, d2, Wtot, sorted(forb)) for d1, d2, Wtot, forb in CLASSES], flush=True)
    w, cands, gens, valid = root_state()
    master_path = os.path.join(OUTDIR, 'bb_%s_master.jsonl.gz' % args.tag)
    if os.path.exists(master_path + '.seeds.json'):
        seeds = [(tuple(tuple(B) for B in b), v) for b, v in json.load(open(master_path + '.seeds.json'))]
        print('resuming: %d seeds' % len(seeds), flush=True)
    else:
        with gzip.open(master_path + '.tmp', 'wt') as out:
            S = Search(out, maxdepth=args.depth)
            S.emit((), w, 0, out_flags(w, 0, valid))
            S.expand((), w, 0, cands, gens, valid, 0)
        os.rename(master_path + '.tmp', master_path)
        seeds = S.seeds
        json.dump([([list(B) for B in b], v) for b, v in seeds], open(master_path + '.seeds.json', 'w'))
        print('master: %d states with <= %d blocks (%d output), %d seeds (%.0fs)' % (S.states, args.depth, S.count, len(seeds), time.time() - t0), flush=True)
    nch = min(args.chunks, len(seeds)) or 1
    jobs = [(ci, seeds[ci::nch]) for ci in range(nch)]
    total = states = 0; cc = [0] * NC; done = 0
    with Pool(args.workers) as pool:
        for ci, res in pool.imap_unordered(worker, jobs, chunksize=1):
            done += 1
            if res is not None:
                total += res[0]; states += res[1]
                for c in range(NC):
                    cc[c] += res[2][c]
                print('chunk %d: %d output (%d states) in %.0fs; done %d/%d, total %d (%.0fs)' % (ci, res[0], res[1], res[3], done, nch, total, time.time() - t0), flush=True)
            else:
                print('chunk %d: already done' % ci, flush=True)
    print('FINAL %s: worker output %d states (%d output), per class %s; master separately (%.0fs)' % (args.tag, states, total, cc, time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
