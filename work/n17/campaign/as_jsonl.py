"""Anghel-Stan's exact realisation code (arXiv:2610.25868, ancillary files) on a jsonl list of lattices.
usage: as_jsonl.py n lattices.jsonl part nparts out.status   -> one line 'k status cost' per lattice (k = line number)"""
import sys, json, time, collections
AS = '/Users/agent/Projects/TC17/third_party/anghel_stan_anc/anc'
sys.path.insert(0, AS)
from realize import Matroid
from exact import realization_space, Degenerate
n, path, part, nparts, outp = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
st = collections.Counter(); t0 = time.time()
with open(path) as f, open(outp, 'w') as out:
    for k, line in enumerate(f):
        if k % nparts != part or not line.strip(): continue
        r = json.loads(line)
        try:
            M = Matroid(n, [frozenset(b) for b in r['blocks'] if len(b) >= 3])
            R = realization_space(M)
            status, cost = R['status'], R['cost']
        except Degenerate:
            status, cost = 'empty-degenerate', None
        except Exception as ex:
            status, cost = 'error:' + type(ex).__name__, None
        st[status] += 1
        out.write('%d %s %s\n' % (k, status, cost))
    out.write('ALLDONE\n')
print('FINAL', dict(st), '%.0fs' % (time.time() - t0), flush=True)
