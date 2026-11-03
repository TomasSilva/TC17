# Summarise the Macaulay2 output of exact_tc_lattice.py: per realisable lattice, its profile
# (multiplicities), points per line, component dimensions/degrees and freeness verdicts.
import sys, json, collections
n = int(sys.argv[1]); lattices = sys.argv[2]; tcout = sys.argv[3]
recs = [json.loads(l) for l in open(lattices)]
res = {}
cur = None
for line in open(tcout):
    if line.startswith('LATTICE'):
        p = line.split()
        cur = int(p[1])
        res[cur] = {'line': line.strip(), 'comps': []}
    elif line.startswith('  COMP') and cur is not None:
        res[cur]['comps'].append(line.strip())
real = {i: r for i, r in res.items() if r['comps']}
print('lattices:', len(res), ' realisable:', len(real), ' mixed:', sum(1 for r in real.values() if any('MIXED' in c for c in r['comps'])))
kinds = collections.Counter()
for i, r in sorted(real.items()):
    rec = recs[i]
    prof = dict(sorted(collections.Counter(len(B) for B in rec['blocks']).items()))
    s = sorted(collections.Counter(rec['s']).items())
    verdicts = [c.split()[-1] if 'MIXED' not in c else 'MIXED' for c in r['comps']]
    verdicts = ['FREE(dim>0)' if 'generic FREE' in c else v for c, v in zip(r['comps'], verdicts)]
    kinds[tuple(sorted(set(verdicts)))] += 1
    print('idx %d: profile %s, points/line %s, comps: %s' % (i, prof, s, ' | '.join(c.replace('  COMP ', '') for c in r['comps'])))
print('verdict kinds:', dict(kinds))
