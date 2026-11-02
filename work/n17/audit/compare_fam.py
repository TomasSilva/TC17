"""Family components: original runs vs the audit rerun (ext/out/fam_*_family.jsonl)."""
import json, glob, sys, collections
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/validate')
from canon import canon_many
R = '/Users/agent/Projects/TC17/work/n17/run/'
def cset(lists):
    lists = [L for L in lists]
    return set(canon_many(17, lists)) if lists else set()
orig = collections.defaultdict(lambda: dict(status=set(), L=[]))
files = [f for f in glob.glob(R + '*_fam_*.jsonl') + glob.glob(R + 'famall_b4849_v*_*.jsonl') + glob.glob(R + '*_fam[0-9]_*.jsonl') + glob.glob(R + 'famrun_b4849_*.jsonl') + glob.glob(R + 'fam_redo.jsonl') + glob.glob(R + 'famrun_redo.jsonl') + glob.glob(R + 'd2c_famrun_*.jsonl') + glob.glob(R + 'b50_fam2_*.jsonl') + glob.glob(R + 'b50_fam3_*.jsonl') + glob.glob(R + 'b50_n14_fam2_*.jsonl')]
for f in set(files):
    for l in open(f):
        try: r = json.loads(l)
        except Exception: continue
        if 'comp' not in r or 'idx' not in r: continue
        k = (str(r['idx']), r['comp'])
        orig[k]['status'].add(r.get('status'))
        orig[k]['L'] += r.get('generic_L', []) + r.get('special_L', [])
re_ = {}
rej = []; st = collections.Counter(); par = collections.Counter(); sdeg = 0; spts = 0; snosh = 0
for f in glob.glob('ext/out/fam_*_family.jsonl'):
    for l in open(f):
        r = json.loads(l)
        if r.get('kind') != 'family': continue
        k = (str(r['idx']), r['comp'])
        st[r['status']] += 1; par[str(r.get('param_ok'))] += 1
        sdeg += r.get('special_degenerate', 0); spts += r.get('special_points', 0); snosh += r.get('special_noshape', 0)
        acc = [x['L'] for x in r.get('generic', []) + r.get('special', []) if x['ok']]
        for x in r.get('generic', []) + r.get('special', []):
            if not x['ok']: rej.append((k, x['why'], x['L']))
        re_[k] = dict(status=r['status'], L=acc)
print('rerun family components:', dict(st), '; parametrisation consistent:', dict(par))
print('special points', spts, 'of which B degenerates', sdeg, 'no shape lemma', snosh, '; rejected by the window test:', len(rej), dict(collections.Counter(w for _, w, _ in rej)))
both = set(orig) & set(re_)
print('components in the original outputs', len(orig), 'in the rerun', len(re_), 'in both', len(both), 'rerun only', len(set(re_) - set(orig)), 'original only', len(set(orig) - set(re_)))
trans = collections.Counter((tuple(sorted(str(s) for s in orig[k]['status'])), re_[k]['status']) for k in both)
print('status (original -> rerun):', dict(trans))
diff = []
for k in both:
    if re_[k]['status'] != 'OK' or 'OK' not in orig[k]['status']: continue
    a, b = cset(orig[k]['L']), cset(re_[k]['L'])
    if a != b: diff.append((k, len(a), len(b), len(a - b), len(b - a)))
print('components OK in both with different accepted lattices:', len(diff), diff[:10])
allL = cset([L for v in re_.values() for L in v['L']])
final = set(json.loads(l)['canon'] for l in open(R + 'checked_L.jsonl'))
print('distinct accepted lattices from families (rerun):', len(allL), 'outside the final 16:', len(allL - final))
json.dump(rej, open('family_rejected.json', 'w'))
json.dump([list(k) for k in re_ if re_[k]['status'] != 'OK'], open('family_not_ok.json', 'w'))
