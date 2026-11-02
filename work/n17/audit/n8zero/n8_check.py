"""No 8-point line: independent screening (Anghel-Stan's exact code) of the 23 + 11,201 lattices,
compared with our verdicts (fast filters; Macaulay2 for the deferred ones)."""
import sys, json, glob, collections
AS = '/Users/agent/Projects/TC17/third_party/anghel_stan_anc/anc'
sys.path.insert(0, AS)
from realize import Matroid
from exact import realization_space, Degenerate
N = '/Users/agent/Projects/TC17/work/n17/n8zero/'
key = lambda bl: json.dumps(sorted(sorted(b) for b in bl if len(b) >= 3))
sets = [('k4444', N + 'k4444.jsonl', N + 'k4444_ff.out'), ('43333', N + 'p5b_43333.jsonl', N + 'p5b_43333_ff.out'),
        ('44332', N + 'p5b_44332.jsonl', N + 'p5b_44332_ff.out'), ('a', N + 'p5b_a.jsonl', N + 'p5b_a_ff.out')]
m2 = {}
for f in glob.glob(N + 'p5b_*_comp*.jsonl'):
    for l in open(f):
        r = json.loads(l); m2[key(r['blocks'])] = r['status']
tc = {}   # k4444 deferred: exact_tc_lattice output, LATTICE i ... good g
dfr = [json.loads(l) for l in open(N + 'k4444_ff_defer.jsonl')]
for l in open(N + 'k4444_ff_defer_tc_0.out'):
    if l.startswith('LATTICE'):
        p = l.split(); i = int(p[1]); g = int(p[p.index('good') + 1])
        tc[key(dfr[i]['blocks'])] = 'REAL' if g > 0 else 'NONREAL'
for name, lf, ff in sets:
    ver = {}
    for l in open(ff):
        q = l.split(None, 1)
        if len(q) == 2 and q[0].isdigit(): ver[int(q[0])] = q[1].strip()
    c = collections.Counter(); bad = []
    for i, l in enumerate(open(lf)):
        r = json.loads(l); bl = [b for b in r['blocks'] if len(b) >= 3]
        try: st = realization_space(Matroid(17, [frozenset(b) for b in bl]))['status']
        except Degenerate: st = 'empty-degenerate'
        except Exception as e: st = 'error:' + type(e).__name__
        a = 'REAL' if st in ('points', 'family') else ('EMPTY' if st.startswith('empty') else st)
        v = ver.get(i)
        if v is None: fin = 'NO-VERDICT'
        elif v.split('|')[-1].strip().startswith('DEFER'): fin = m2.get(key(bl), tc.get(key(bl), 'NO-M2'))
        else: fin = 'NONREAL'
        c[(a, fin)] += 1
        if (a, fin) in (('REAL', 'NONREAL'), ('EMPTY', 'REAL')) or fin in ('NO-VERDICT', 'NO-M2') or fin == 'REAL':
            bad.append((i, st, v, fin))
    print(name, dict(sorted(c.items())), 'flags', len(bad), bad[:5])
