# Statistics of the weak-realisability test by number of big blocks and by number of triples needed.
import sys, json, collections, glob
n = int(sys.argv[1]); IN = sys.argv[2]; Wtot = int(sys.argv[3])
from math import comb
verdict = {}
for f in glob.glob(IN.replace('.jsonl', '_weak_*.out')):
    for l in open(f):
        if l.startswith('CONF'):
            p = l.split(); verdict[int(p[1])] = (p[2], int(p[3]) if p[2] == 'REAL' else 0, p[4] if p[2] == 'REAL' else '')
recs = [json.loads(l) for l in open(IN)]
by_nb = collections.defaultdict(lambda: [0, 0]); by_n3 = collections.defaultdict(lambda: [0, 0]); dims = collections.Counter()
for i, r in enumerate(recs):
    if i not in verdict:
        continue
    nb = len(r['blocks']); n3 = Wtot - r['W']
    real = verdict[i][0] == 'REAL'
    by_nb[nb][0] += 1; by_nb[nb][1] += real
    by_n3[n3][0] += 1; by_n3[n3][1] += real
    if real:
        dims[verdict[i][2]] += 1
tot = sum(v[0] for v in by_nb.values()); surv = sum(v[1] for v in by_nb.values())
print('configurations tested: %d, weakly realisable: %d (%.2f%%)' % (tot, surv, 100.0 * surv / max(tot, 1)))
print('by #big blocks: ' + ', '.join('%d: %d/%d' % (k, v[1], v[0]) for k, v in sorted(by_nb.items())))
print('by #triples needed: ' + ', '.join('%d: %d/%d' % (k, v[1], v[0]) for k, v in sorted(by_n3.items())))
print('dimension of the realisation space of survivors (chart dims):', sorted(dims.items(), key=lambda x: -x[1])[:12])
