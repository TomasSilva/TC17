"""Final audit of the extension campaign: every core and child accounted for, every failure routed."""
import json, glob, collections, os
def lines(f):
    for l in open(f):
        try: yield json.loads(l)
        except Exception: pass
# 1. family outputs: statuses per (idx, comp); a record counts as handled if some run gave OK/DIM>=2,
#    or if it was routed through the lattice-level step (slowrecs files or runclass 'sent' routing)
fam_files = [f for f in glob.glob('*.jsonl') if ('_fam' in f or f.startswith('famall_b4849_v')) and 'r1' not in f and 'done' not in f and 'slowrecs' not in f]
fam_files = [f for f in fam_files if not f.startswith(('famrun_b4849_', 'd2c_famrun_', 'famrun_redo', 'fam_b4849', 'famall_b4849.jsonl', 'd2c_fam.jsonl'))]
st = collections.defaultdict(set)
for f in fam_files:
    for r in lines(f):
        if 'status' in r and 'comp' in r: st[(str(r['idx']), r['comp'])].add(r['status'])
bad = {k: v for k, v in st.items() if not (v & {'OK', 'DIM>=2'})}
routed = set()
for f in glob.glob('*_slowrecs.jsonl'):
    for r in lines(f): routed.add(str(r['idx']))
# runclass routes slow families into its own *_r2 files (appended)
for f in glob.glob('*_n1[3-6]_r2.jsonl'):
    for r in lines(f): routed.add(str(r['idx']))
unrouted = {k: v for k, v in bad.items() if k[0] not in routed}
print('family components seen:', len(st), '; never completed:', len(bad), '; of those not routed to the lattice step:', len(unrouted))
for k, v in list(unrouted.items())[:10]: print('   UNROUTED', k, v)
# 2. rigid outputs: noshape / mismatch markers
c = collections.Counter()
for f in glob.glob('*ext*.jsonl') + glob.glob('rerun/*_ext.jsonl'):
    for r in lines(f):
        if r.get('noshape'): c['noshape'] += 1
        if r.get('mismatch'): c['mismatch'] += 1
print('rigid search markers:', dict(c))
# 3. special points without shape in family runs
ns = sum((r.get('special_noshape') or 0) for f in fam_files for r in lines(f))
print('special points without shape:', ns)
# 4. Macaulay2 failures at child levels and in the core runs
oc = collections.Counter()
for f in glob.glob('*chcomp*.jsonl') + glob.glob('../comp/*comp_*.jsonl'):
    for r in lines(f):
        if r.get('status') not in ('REAL', 'NONREAL'): oc[(f.split('/')[-1].split('_chcomp')[0].split('_comp')[0], r.get('status'))] += 1
print('Macaulay2 non-REAL/NONREAL records:', dict(oc))
