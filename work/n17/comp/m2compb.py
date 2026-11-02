"""Batched version of m2comp2.py: B lattices per Macaulay2 session (startup amortised); a batch that
exceeds its timeout is redone lattice by lattice with the single-lattice timeout.  Records already present
in the output files (by idx) are skipped, so a run can be restarted.
usage: m2compb.py n lattices.jsonl part nparts timeout out.jsonl [B] [skipfiles...]"""
import sys, json, subprocess, os, time, glob
n, IN, part, nparts, TO, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
B = int(sys.argv[7]) if len(sys.argv) > 7 else 25
skipfiles = sys.argv[8:]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'm2comp2.py')).read()
pre = src[:src.index('recs = [json.loads(l) for l in open(IN)]')]
sys.argv = ['x', n, IN, '0', '1', str(TO), '/dev/null']
_saved = (n, IN, part, nparts, TO, OUT)
exec(pre)          # defines script(idx, blocks) and ex
n, IN, part, nparts, TO, OUT = _saved
done = set()
for f in skipfiles + [OUT]:
    if os.path.exists(f):
        for l in open(f):
            try: done.add(json.loads(l)['idx'])
            except Exception: pass
HEAD = 2
def parse(o, rec, meta):
    res = dict(idx=rec.get('idx'), blocks=rec['blocks'], **meta)
    if 'RESULT NONREAL' in o: res['status'] = 'NONREAL'; return res
    res['status'] = 'REAL'; res['comps'] = []
    for ln in o.split('\n'):
        if ln.startswith('COMP '):
            _, dm, dg, gens = ln.split(' ', 3)
            res['comps'].append(dict(dim=int(dm), degree=int(dg), gens=gens))
        elif ln.startswith('SHAPE ') and res['comps']:
            parts = ln[6:].split(' ; '); res['comps'][-1]['f'] = parts[0]; res['comps'][-1]['g'] = parts[1:]
        elif ln.startswith('SLICE ') and res['comps']:
            parts = ln[6:].split(' ; '); res['comps'][-1]['slice_f'] = parts[0]; res['comps'][-1]['slice_g'] = parts[1:]
        elif ln.startswith('NOSHAPE') and res['comps']: res['comps'][-1]['noshape'] = True
    return res
def run_batch(items, to):
    body = []
    metas = {}
    for i, rec in items:
        txt, meta = script(i, rec['blocks'])
        lines = txt.split('\n')
        metas[i] = meta
        body.append('print("BEGIN %d");' % i)
        body += lines[HEAD:-1]          # drop header and the final print("DONE")
        body.append('print("END %d");' % i)
    head = txt.split('\n')[:HEAD]
    path = OUT + '.%d.b.m2' % part
    open(path, 'w').write('\n'.join(head + body) + '\nprint("ALLDONE");\n')
    try:
        r = subprocess.run([ex.M2, '--script', path], capture_output=True, text=True, timeout=to)
        o = r.stdout; timed = False
    except subprocess.TimeoutExpired as e:
        o = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or ''); timed = True
    os.remove(path)
    outres = {}
    for i, rec in items:
        b = o.find('BEGIN %d\n' % i); e_ = o.find('END %d\n' % i)
        if b >= 0 and e_ > b:
            outres[i] = parse(o[b:e_], rec, metas[i])
    return outres, timed
recs = [json.loads(l) for l in open(IN)]
mine = [(i, r) for i, r in enumerate(recs) if i % nparts == part and r.get('idx', i) not in done]
with open(OUT, 'a') as out:
    for s in range(0, len(mine), B):
        items = mine[s:s + B]
        t0 = time.time()
        res, timed = run_batch(items, max(TO, 60 * len(items)))
        for i, rec in items:
            if i in res:
                r = res[i]; r['time'] = round((time.time() - t0) / len(items), 2)
            else:
                r1, t1 = run_batch([(i, rec)], TO)
                r = r1.get(i, dict(idx=rec.get('idx'), blocks=rec['blocks'], status='TIMEOUT' if t1 else 'ERROR'))
            out.write(json.dumps(r) + '\n')
        out.flush()
