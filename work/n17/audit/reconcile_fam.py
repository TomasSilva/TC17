"""Final reconciliation of the family components (pass 1 + pass 2 of the audit rerun)."""
import json, glob, gzip, collections, sys
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/validate')
from canon import canon_many
R = '/Users/agent/Projects/TC17/work/n17/run/'
A = '/Users/agent/Projects/TC17/work/n17/results/'
# all family components of all realisable records
comps = set(); rec_of = {}
for f in ['core_components_b48_b49_b50.jsonl.gz', 'core_components_b51.jsonl.gz', 'children_components.jsonl.gz']:
    for l in gzip.open(A + f, 'rt'):
        r = json.loads(l)
        if r.get('status') != 'REAL': continue
        for ci, c in enumerate(r['comps']):
            if c['dim'] == 1: comps.add((str(r['idx']), ci)); rec_of[(str(r['idx']), ci)] = r
res = collections.defaultdict(list)
for pat in ('ext/out/fam_*_family.jsonl', 'ext/out2/p2_*_family.jsonl'):
    for f in glob.glob(pat):
        for l in open(f):
            r = json.loads(l)
            if r.get('kind') == 'family': res[(str(r['idx']), r['comp'])].append(r)
settled = {k for k, v in res.items() if any(x['status'] == 'OK' for x in v)}
unsettled = comps - settled
print('family components', len(comps), '; with a rerun record', len(set(res) & comps), '; settled by the family method', len(settled & comps), '; unsettled', len(unsettled))
# consistency where several OK records exist
def acc(x): return [y['L'] for y in x.get('generic', []) + x.get('special', []) if y['ok']]
rej = [(k, y['why']) for k, v in res.items() for x in v for y in x.get('generic', []) + x.get('special', []) if not y['ok']]
incons = 0
for k, v in res.items():
    oks = [x for x in v if x['status'] == 'OK']
    if len(oks) > 1:
        sets = [frozenset(canon_many(17, acc(x))) if acc(x) else frozenset() for x in oks]
        incons += len(set(sets)) > 1
print('components settled twice with different results:', incons, '; window rejections in families:', len(rej))
# lattice-level coverage: parents of children in the original runs
parents = set()
for f in glob.glob(R + '*_ch.jsonl'):
    if 'd2t' in f or 'b51s20' in f: continue
    for l in open(f):
        r = json.loads(l); parents.add(str(r.get('parent')))
# dim2_b4849 / d2c children carry the parent as in their records
cov = {k for k in unsettled if k[0] in parents}
st_un = collections.Counter(res[k][-1]['status'] if res.get(k) else 'no record' for k in unsettled)
print('unsettled by status', dict(st_un), '; covered by the lattice-level step of the original runs', len(cov), '; not covered', len(unsettled - cov))
for k in sorted(unsettled - cov)[:20]: print('   NOT COVERED', k, [x['status'] for x in res.get(k, [])])
# cross-validation: components routed to the lattice level originally AND settled by the family method now
routed_settled = [k for k in settled & comps if k[0] in parents]
print('routed to the lattice level originally and settled now by the family method:', len(routed_settled))
# lattices found from the descendants of a record (rerun outputs of children components)
desc = collections.defaultdict(list)
for pat in ('ext/out/*.jsonl', 'ext/out2/*.jsonl'):
    for f in glob.glob(pat):
        for l in open(f):
            r = json.loads(l)
            if 'idx' not in r: continue
            for grp in ('found', 'generic', 'special'):
                for y in r.get(grp, []):
                    if y['ok']: desc[str(r['idx'])].append(y['L'])
fam_only = 0; lat_only = 0; both_nonempty = 0
for k in routed_settled:
    f = set(canon_many(17, [L for x in res[k] if x['status'] == 'OK' for L in acc(x)])) if any(acc(x) for x in res[k] if x['status'] == 'OK') else set()
    pref = k[0] + '/'
    dl = [L for idx, Ls in desc.items() if idx.startswith(pref) or idx.startswith(k[0].split(':')[0] + ':' + k[0].split(':', 1)[-1] + '/') for L in Ls]
    d = set(canon_many(17, dl)) if dl else set()
    if f - d: fam_only += 1
    if f or d: both_nonempty += 1
print('   of these: family lattices not found through the lattice level:', fam_only, '; with any lattice on either side:', both_nonempty)
allacc = [L for v in res.values() for x in v if x['status'] == 'OK' for L in acc(x)]
final = set(json.loads(l)['canon'] for l in open(R + 'checked_L.jsonl'))
fa = set(canon_many(17, allacc)) if allacc else set()
print('distinct lattices accepted from families:', len(fa), '; outside the final 16:', len(fa - final))
json.dump(sorted(map(list, unsettled - cov)), open('fam_not_covered.json', 'w'))
