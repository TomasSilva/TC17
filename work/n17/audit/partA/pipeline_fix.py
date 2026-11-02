# AUDIT COPY (22 Oct 2026): pipeline.py with the corrected filters of recheck_resultant/fast_real_fix.py.
# Streaming stages 2-4 for one or more big-block chunk files (output of bigblocks2.py):
#   skeleton -> triple filling (fill_triples.fill, exact cover, isomorph-free)
#            -> fast realisability filter (fast_real.classify, python-flint)
#            -> number-field pass (fast_real2.classify2)
#            -> lattices still undecided are written out for Macaulay2 (exact_tc_lattice.py).
# Nothing but the deferred lattices and per-chunk statistics is stored.  Resumable per chunk: the
# progress file records how many skeletons of the chunk are done; a restart skips them and appends.
#   python pipeline.py n wmin wmax bmax tag CLASSES chunk.jsonl.gz [chunk2 ...] [--workers k] [--outdir D]
# CLASSES: comma-separated c:d1:d2 where c is the class index used in the chunk's "c" field.
import sys, os, json, time, gzip, argparse, hashlib, itertools
from math import comb
from multiprocessing import Pool

ap = argparse.ArgumentParser()
ap.add_argument('n', type=int); ap.add_argument('wmin', type=int); ap.add_argument('wmax', type=int)
ap.add_argument('bmax', type=int); ap.add_argument('tag'); ap.add_argument('classes')
ap.add_argument('chunks', nargs='+')
ap.add_argument('--workers', type=int, default=1)
ap.add_argument('--outdir', default='')
ap.add_argument('--limit', type=int, default=0, help='process only the first k skeletons of each chunk (testing)')
args = ap.parse_args()
n, wmin, wmax, bmax = args.n, args.wmin, args.wmax, args.bmax
CLASSES = {}
for s in args.classes.split(','):
    c, d1, d2 = (int(a) for a in s.split(':'))
    CLASSES[c] = (d1, d2, comb(n, 2) - d1 * d2 - d1 - d2)
OUTDIR = args.outdir or '/Users/agent/Projects/TC17/work/tc15/pipe_%s' % args.tag
os.makedirs(OUTDIR, exist_ok=True)

HERE = '/Users/agent/Projects/TC17/work/tc15'
import importlib.util


def load(name, argv):
    saved = sys.argv; sys.argv = argv
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    sys.argv = saved
    return mod


ft = load('fill_triples', ['x', str(n), str(wmin), str(wmax), str(bmax), '0', 'none', '0', '1'])
# audit 22 Oct 2026: the corrected filters (fast_real_fix.py) instead of fast_real / fast_real2
_saved = sys.argv; sys.argv = ['x', str(n)]
sys.path.insert(0, '/Users/agent/Projects/TC17/work/tc15/recheck_resultant')
import fast_real_fix as fx
sys.argv = _saved
import pynauty, flint


def cert(blocks):
    nb = len(blocks)
    adj = {n + k: list(B) for k, B in enumerate(blocks)}
    g = pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=[set(range(n)), set(range(n, n + nb))])
    return hashlib.sha1(pynauty.certificate(g)).digest()


def process_chunk(path):
    base = os.path.basename(path).replace('.jsonl.gz', '')
    prog_path = os.path.join(OUTDIR, 'prog_%s.json' % base)
    done_path = os.path.join(OUTDIR, 'done_%s.json' % base)
    if os.path.exists(done_path):
        return base, None
    prog = json.load(open(prog_path)) if os.path.exists(prog_path) else {'done': 0, 'stats': {}, 'lattices': 0, 'raw': 0, 'skeletons': 0, 'time': 0.0}
    skip = prog['done']
    stats = prog['stats']
    defer_files = {c: open(os.path.join(OUTDIR, 'defer_%s_c%d.jsonl' % (base, c)), 'a') for c in CLASSES}
    ctx3 = flint.fmpz_mpoly_ctx.get(('u0', 'u1', 'u2')); gens3 = ctx3.gens()
    t0 = time.time(); tprev = prog['time']
    i = -1
    with gzip.open(path, 'rt') as fh:
        for i, line in enumerate(fh):
            if i < skip:
                continue
            if args.limit and i >= args.limit:
                i -= 1
                break
            rec = json.loads(line)
            big = [tuple(B) for B in rec['blocks']]
            t1 = time.time(); l1 = prog['lattices']
            for c in rec.get('c', [0]):
                if c not in CLASSES:
                    continue
                d1, d2, Wtot = CLASSES[c]
                n3 = Wtot - rec['W']
                sols = ft.fill(big, rec['w'], n3)
                prog['raw'] += len(sols)
                seen = set()
                for T in sols:
                    blocks = sorted(big + [tuple(t) for t in T])
                    k = cert(blocks)
                    if k in seen:
                        continue
                    seen.add(k); prog['lattices'] += 1
                    res = fx.classify_fixed(blocks, ctx3, gens3)
                    if res.startswith('DEFER'):
                        try:
                            res2 = fx.classify2_fixed(blocks, res[6:], ctx3, gens3)
                        except Exception as e:
                            res2 = 'DEFER error %s' % type(e).__name__
                        res = res2
                    key = '%d|%s' % (c, res.split(' deg')[0])
                    stats[key] = stats.get(key, 0) + 1
                    if res.startswith('DEFER'):
                        w = list(rec['w'])
                        for t in T:
                            for u in t:
                                w[u] += 1
                        defer_files[c].write(json.dumps({'blocks': [list(B) for B in blocks], 's': [n - 1 - v for v in w],
                                                         'c': c, 'reason': res, 'src': [base, i]}) + '\n')
            prog['skeletons'] += 1
            if time.time() - t1 > 10:
                print('slow skeleton %s:%d: %d blocks, W=%d, classes %s, %d lattices, %.0fs' % (base, i, len(big), rec['W'], rec.get('c'), prog['lattices'] - l1, time.time() - t1), flush=True)
            if (i + 1) % 200 == 0:
                for f in defer_files.values():
                    f.flush()
                prog['done'] = i + 1; prog['time'] = tprev + time.time() - t0
                json.dump(prog, open(prog_path + '.tmp', 'w')); os.rename(prog_path + '.tmp', prog_path)
    for f in defer_files.values():
        f.close()
    prog['done'] = i + 1; prog['time'] = tprev + time.time() - t0
    json.dump(prog, open(done_path + '.tmp', 'w')); os.rename(done_path + '.tmp', done_path)
    if os.path.exists(prog_path):
        os.remove(prog_path)
    return base, prog


def main():
    t0 = time.time()
    todo = [p for p in args.chunks if not os.path.exists(os.path.join(OUTDIR, 'done_%s.json' % os.path.basename(p).replace('.jsonl.gz', '')))]
    print('%d chunks, %d to do; classes %s' % (len(args.chunks), len(todo), CLASSES), flush=True)
    tot = {'skeletons': 0, 'lattices': 0, 'stats': {}}
    with Pool(args.workers) as pool:
        for k, (base, prog) in enumerate(pool.imap_unordered(process_chunk, todo, chunksize=1)):
            if prog is None:
                continue
            tot['skeletons'] += prog['skeletons']; tot['lattices'] += prog['lattices']
            for key, v in prog['stats'].items():
                tot['stats'][key] = tot['stats'].get(key, 0) + v
            print('%s: %d skeletons, %d lattices, %.0fs; cumulative %d skeletons, %d lattices (%d/%d chunks, %.0fs)' % (
                base, prog['skeletons'], prog['lattices'], prog['time'], tot['skeletons'], tot['lattices'], k + 1, len(todo), time.time() - t0), flush=True)
    print('FINAL %s: %s (%.0fs)' % (args.tag, json.dumps(tot), time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
