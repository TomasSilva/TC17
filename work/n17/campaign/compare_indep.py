"""Compare the exact rigid extension (ext/*_ext_*.jsonl: one record per 17-line lattice found, accepted ('L') or
rejected by the window test ('L_rejected'), per component (idx, comp); records of slices of families excluded)
with the independent numeric search (indep_rigid/out_*.jsonl: 'found' = every lattice, no window test).
usage: compare_indep.py extdir indepdir out.json"""
import sys, json, glob, collections
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/validate')
from canon import canon_many
extdir, inddir, outp = sys.argv[1], sys.argv[2], sys.argv[3]
def jl(f):
    for l in open(f):
        try: yield json.loads(l)
        except Exception: pass
def canon_map(items):
    out = collections.defaultdict(set)
    for k in range(0, len(items), 20000):
        part = items[k:k + 20000]
        for (key, bl), c in zip(part, canon_many(17, [bl for _, bl in part])): out[key].add(c)
    return out
ex_items, ex_comps = [], set()
for f in glob.glob(extdir + '/*_ext_*.jsonl'):
    for r in jl(f):
        if r.get('slice'): continue
        key = (str(r['idx']), r['comp'])
        if 'L' in r: ex_items.append((key, r['L']))
        if 'L_rejected' in r: ex_items.append((key, r['L_rejected']))
        if r.get('done'): ex_comps.add(key)
in_items, info = [], {}
for f in glob.glob(inddir + '/out_*.jsonl'):
    for r in jl(f):
        if 'idx' not in r: continue
        key = (str(r['idx']), r['comp'])
        info[key] = (r.get('lattice_ok'), r.get('error'), r.get('stats', {}).get('ambiguous incidence', 0))
        for L in r.get('found', []): in_items.append((key, L))
E, I = canon_map(ex_items), canon_map(in_items)
common = [k for k in info if k in ex_comps]
diff = [k for k in common if I.get(k, set()) != E.get(k, set())]
res = dict(exact_components=len(ex_comps), numeric_components=len(info), compared=len(common), differing=len(diff),
           examples=[dict(key=list(k), numeric=len(I.get(k, ())), exact=len(E.get(k, ()))) for k in diff[:20]],
           lattice_mismatch=sum(1 for v in info.values() if v[0] is False), errors=sum(1 for v in info.values() if v[1]),
           ambiguous=sum(v[2] for v in info.values()), numeric_only_components=len([k for k in info if k not in ex_comps]),
           distinct_lattices_exact=len(set().union(*E.values())) if E else 0, distinct_lattices_numeric=len(set().union(*I.values())) if I else 0)
json.dump(res, open(outp, 'w'), indent=1)
print(json.dumps(res))
