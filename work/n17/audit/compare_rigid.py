"""Rigid components: compare, component by component, the lattices found by
  (1) the original runs (run/*ext*.jsonl, window-accepted lattices only),
  (2) the exact audit rerun (ext/out/*_rigid.jsonl: all lattices found, with window verdicts),
  (3) the independent numeric search (indep/out/rig_*.jsonl: all lattices found, no window test)."""
import json, glob, sys, collections
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/validate')
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/comp')
from canon import canon_many
from extend import window_ok
R = '/Users/agent/Projects/TC17/work/n17/run/'
def canon_map(items):   # items: list of (key, blocks) -> dict key -> set(canon)
    out = collections.defaultdict(set)
    for k in range(0, len(items), 50000):
        part = items[k:k + 50000]
        for (key, bl), c in zip(part, canon_map.cm(part)): out[key].add(c)
    return out
canon_map.cm = lambda part: canon_many(17, [bl for _, bl in part])
orig_items = []
for f in glob.glob(R + '*_ext_*.jsonl') + [R + 'ext_b4849_rigid.jsonl', R + 'd2c_rigid_ext.jsonl'] + glob.glob(R + 'rerun/*_ext.jsonl'):
    for l in open(f):
        r = json.loads(l)
        if 'L' in r and not r.get('slice'): orig_items.append(((str(r['idx']), r['comp']), r['L']))
re_items, re_rej, re_comps, acc_items = [], [], set(), []
for f in glob.glob('ext/out/*_rigid.jsonl'):
    for l in open(f):
        r = json.loads(l)
        if r.get('kind') != 'rigid': continue
        key = (str(r['idx']), r['comp']); re_comps.add((key, r['status']))
        for x in r.get('found', []):
            re_items.append((key, x['L']))
            if x['ok']: acc_items.append((key, x['L']))
            else: re_rej.append((key, x['why'], x['L']))
ind_items, ind_comps = [], {}
for f in glob.glob('indep/out/rig_*.jsonl'):
    for l in open(f):
        r = json.loads(l)
        if 'idx' not in r: continue
        key = (str(r['idx']), r['comp']); ind_comps[key] = (r.get('lattice_ok'), r.get('error'), r.get('stats', {}).get('ambiguous incidence', 0))
        for L in r.get('found', []): ind_items.append((key, L))
O, RR_, I = canon_map(orig_items), canon_map(re_items), canon_map(ind_items)
st = collections.Counter(s for _, s in re_comps)
print('rerun rigid components:', dict(st), '; with lattices found:', len(RR_), '; rejected by the window test:', len(re_rej))
for why, n in collections.Counter(w for _, w, _ in re_rej).items(): print('   rejected:', why, n)
acc = {k: {c for c in v} for k, v in RR_.items()}
# accepted-only sets for the rerun
acc_only = canon_map(acc_items)
d1 = [k for k in set(O) | set(acc_only) if O.get(k, set()) != acc_only.get(k, set())]
print('original vs rerun (accepted), components differing:', len(d1))
for k in d1[:10]: print('   ', k, 'orig', len(O.get(k, ())), 'rerun', len(acc_only.get(k, ())), 'orig-rerun', len(O.get(k, set()) - acc_only.get(k, set())), 'rerun-orig', len(acc_only.get(k, set()) - O.get(k, set())))
common = [k for k in ind_comps]
d2 = [k for k in common if I.get(k, set()) != RR_.get(k, set())]
print('independent numeric vs rerun (all found), components compared:', len(common), 'differing:', len(d2),
      '; numeric lattice-mismatch:', sum(1 for v in ind_comps.values() if v[0] is False), '; errors:', sum(1 for v in ind_comps.values() if v[1]),
      '; ambiguous incidences:', sum(v[2] for v in ind_comps.values()))
for k in d2[:10]: print('   ', k, 'numeric', len(I.get(k, ())), 'exact', len(RR_.get(k, ())))
allc = set().union(*acc_only.values()) if acc_only else set()
final = set(json.loads(l)['canon'] for l in open(R + 'checked_L.jsonl'))
print('distinct accepted lattices in the rerun:', len(allc), '; equal to the final 16:', allc == final, '; outside the 16:', len(allc - final))
json.dump(re_rej, open('rigid_rejected.json', 'w'))
