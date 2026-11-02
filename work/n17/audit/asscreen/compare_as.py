"""Compare the independent screening of Anghel-Stan's code (as<b>_p*.status) with our verdicts on every
core: fast-filter verdict files (cores*/c<b>_p*.out) and Macaulay2 records (comp/*comp_*.jsonl)."""
import sys, json, glob, collections
W = '/Users/agent/Projects/TC17/work/n17/'
CFG = {'48': (W + 'cores/c48_p%d.out', 10), '49': (W + 'cores/c49_p%d.out', 10),
       '50': (W + 'cores50/c50_p%d.out', 6), '51': (W + 'cores50/c51_p%d.out', 6)}
m2 = {}
for f in glob.glob(W + 'comp/dall_comp_*.jsonl') + glob.glob(W + 'comp/dallb_comp_*.jsonl') + glob.glob(W + 'comp/d51_comp_*.jsonl') + glob.glob(W + 'comp/d51b_comp_*.jsonl'):
    for l in open(f):
        r = json.loads(l); m2[r['idx']] = r['status']
for b in sys.argv[1:]:
    pat, np_ = CFG[b]
    ours = {}
    for p in range(np_):
        for l in open(pat % p):
            q = l.split(None, 1)
            if len(q) == 2 and q[0].isdigit(): ours[int(q[0])] = q[1].strip()
    asv = {}
    for f in glob.glob('as%s_p*.status' % b):
        for l in open(f):
            q = l.split()
            if len(q) >= 2 and q[0].isdigit(): asv[int(q[0])] = q[1]
    c = collections.Counter(); bad = []
    for k in sorted(set(ours) | set(asv)):
        o = ours.get(k); a = asv.get(k, 'MISSING')
        if o is None: fin = 'MISSING'
        elif o.split('|')[-1].strip().startswith('DEFER'): fin = m2.get('b%s:%d' % (b, k), 'NO-M2-RECORD')
        else: fin = 'NONREAL'
        ar = 'REAL' if a in ('points', 'family') else ('EMPTY' if a.startswith('empty') else a)
        c[(ar, fin)] += 1
        if (ar, fin) in (('REAL', 'NONREAL'), ('EMPTY', 'REAL')) or 'MISSING' in (ar, fin) or fin == 'NO-M2-RECORD' or ar.startswith('error'):
            bad.append((k, a, o, fin))
    print('b%s: cores %d' % (b, len(set(ours) | set(asv))), dict(sorted(c.items())))
    print('   discrepancies:', len(bad), bad[:10])
    json.dump(bad, open('discrepancies_b%s.json' % b, 'w'))
