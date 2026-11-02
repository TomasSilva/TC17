"""Children (14-16 lines) of the lattice-level step: independent screening with Anghel-Stan's exact code,
compared with our verdicts (fast filters, then Macaulay2 for the deferred ones).
usage: children_check.py base   (run/<base>_ch.jsonl or the special sets dim2_b4849, d2c_dim2)"""
import sys, json, glob, collections, time
AS = '/Users/agent/Projects/TC17/third_party/anghel_stan_anc/anc'
sys.path.insert(0, AS)
from realize import Matroid
from exact import realization_space, Degenerate
R = '/Users/agent/Projects/TC17/work/n17/run/'
base = sys.argv[1]
chf = R + base + '_ch.jsonl'
if base == 'dim2_b4849': ffs = [R + 'dim2_b4849_ch_ff.out']; comps = glob.glob(R + 'dim2_b4849_ch_comp_*.jsonl')
elif base == 'd2c_dim2': ffs = [R + 'd2c_dim2_ch_ff.out']; comps = glob.glob(R + 'd2c2_comp_*.jsonl')
else: ffs = sorted(glob.glob(R + base + '_ff_[0-9].out')); comps = glob.glob(R + base + '_chcomp_*.jsonl')
key = lambda bl: json.dumps(sorted(sorted(b) for b in bl if len(b) >= 3))
ff = {}
for f in ffs:
    for l in open(f):
        q = l.split(None, 1)
        if len(q) == 2 and q[0].isdigit(): ff[int(q[0])] = q[1].strip()
m2 = {}
for f in comps:
    for l in open(f):
        r = json.loads(l); m2[key(r['blocks'])] = r['status']
c = collections.Counter(); bad = []; undecided_nonreal = []
t0 = time.time()
for i, l in enumerate(open(chf)):
    r = json.loads(l); n = r.get('n') or (1 + max(x for b in r['blocks'] for x in b))
    try:
        st = realization_space(Matroid(n, [frozenset(b) for b in r['blocks'] if len(b) >= 3]))['status']
    except Degenerate:
        st = 'empty-degenerate'
    except Exception as e:
        st = 'error:' + type(e).__name__
    a = 'REAL' if st in ('points', 'family') else ('EMPTY' if st.startswith('empty') else st)
    v = ff.get(i)
    if v is None: fin = 'NO-FF-VERDICT'
    elif v.split('|')[-1].strip().startswith('DEFER'): fin = m2.get(key(r['blocks']), 'NO-M2-RECORD')
    else: fin = 'NONREAL'
    c[(a, fin)] += 1
    if (a, fin) in (('REAL', 'NONREAL'), ('EMPTY', 'REAL')) or fin.startswith('NO-') or a.startswith('error'):
        bad.append((i, r.get('idx'), st, v, fin))
    if a == 'cost>1' and fin == 'NONREAL' and not v.split('|')[-1].strip().startswith('DEFER'):
        undecided_nonreal.append(dict(idx=r.get('idx'), blocks=r['blocks'], n=n))
print(base, 'children', sum(c.values()), dict(sorted(c.items())), 'discrepancies', len(bad), bad[:5], '%.0fs' % (time.time() - t0), flush=True)
json.dump(bad, open('disc_%s.json' % base, 'w'))
with open('undecided_nonreal_%s.jsonl' % base, 'w') as f:
    for u in undecided_nonreal: f.write(json.dumps(u) + '\n')
