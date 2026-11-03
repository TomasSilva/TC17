"""Compare our verdicts (fast filters, then Macaulay2 on the deferred lattices) with those of Anghel-Stan's
exact code on one lattice list.  Lattices are matched by line number; Macaulay2 records by the 'idx' field.
usage: compare_as.py n lattices.jsonl 'ff_out_glob' 'm2_glob' 'as_status_glob' out.json
AS statuses: points / family = realisable; empty* = not realisable; cost>1 = undecided (then, if our filters
alone rejected the lattice, it is listed in undecided_filter_only for a Macaulay2 confirmation)."""
import sys, json, glob, collections
n, latf, ffg, m2g, asg, outp = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
idx_of = []
for l in open(latf):
    if l.strip(): idx_of.append(str(json.loads(l)['idx']))
ours = {}
for f in glob.glob(ffg):
    for l in open(f):
        q = l.split(None, 1)
        if len(q) == 2 and q[0].isdigit(): ours[int(q[0])] = q[1].strip()
m2 = {}
for f in glob.glob(m2g):
    for l in open(f):
        try: r = json.loads(l)
        except Exception: continue
        if 'idx' in r and 'status' in r: m2[str(r['idx'])] = r['status']
asv = {}
for f in glob.glob(asg):
    for l in open(f):
        q = l.split()
        if len(q) >= 2 and q[0].isdigit(): asv[int(q[0])] = q[1]
table = collections.Counter(); bad = []; und = []; missing_ours = 0
for k in range(len(idx_of)):
    o = ours.get(k); a = asv.get(k, 'MISSING')
    if o is None:
        fin = 'MISSING'; missing_ours += 1; filter_only = False
    elif o.split('|')[-1].strip().startswith('DEFER'):
        fin = m2.get(idx_of[k], 'NO-M2-RECORD'); filter_only = False
    else:
        fin = 'NONREAL'; filter_only = True
    ar = 'REAL' if a in ('points', 'family') else ('EMPTY' if a.startswith('empty') else a)
    table[(ar, fin)] += 1
    if (ar, fin) in (('REAL', 'NONREAL'), ('EMPTY', 'REAL')) or ar.startswith('error') or fin in ('NO-M2-RECORD', 'MISSING') or a == 'MISSING':
        bad.append((k, idx_of[k], a, o, fin))
    if ar not in ('REAL', 'EMPTY') and filter_only: und.append(idx_of[k])
res = dict(n=len(idx_of), table={'AS %s / ours %s' % k: v for k, v in sorted(table.items())}, disagreements=len(bad), bad=bad[:100],
           missing_ours=missing_ours, undecided_filter_only=und)
json.dump(res, open(outp, 'w'))
print(json.dumps({k: v for k, v in res.items() if k not in ('bad', 'undecided_filter_only')}), 'undecided_filter_only:', len(und))
