"""Independent screening of the 13-line cores with the exact code of Anghel-Stan (arXiv:2610.25868,
ancillary files: exact.realization_space, constructions with at most one parameter over Z[t]).
usage: as_screen.py core.g6 d out_prefix part nparts
writes out_prefix.status: one line per core 'k status cost' (k = line number in core.g6)."""
import sys, time, collections
AS = '/Users/agent/Projects/TC17/third_party/anghel_stan_anc/anc'
sys.path.insert(0, AS)
from g6util import blocks_checked
from realize import Matroid
from exact import realization_space, Degenerate
path, d, pref, part, nparts = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
st = collections.Counter(); t0 = time.time()
with open(path) as f, open(pref + '.status', 'w') as out:
    for k, s in enumerate(f):
        if k % nparts != part: continue
        s = s.strip()
        try:
            M = Matroid(d, blocks_checked(s, d))
            R = realization_space(M)
            status, cost = R['status'], R['cost']
        except Degenerate:
            status, cost = 'empty-degenerate', None
        except Exception as ex:
            status, cost = 'error:' + type(ex).__name__, None
        st[status] += 1
        out.write('%d %s %s\n' % (k, status, cost))
        if sum(st.values()) % 100000 == 0:
            print(dict(st), '%.0fs' % (time.time() - t0), flush=True)
    out.write('ALLDONE\n')
print('FINAL', dict(st), '%.0fs' % (time.time() - t0), flush=True)
