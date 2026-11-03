"""Collect every 17-line lattice produced by the extension runs of the campaign: accepted by the window test
(rigid: 'L'; families: 'generic_L', 'special_L') and rejected ('L_rejected'; families: 'rejected'), reduce to
canonical forms (labelg), compare with the 16 lattices of work/n17/run/checked_L.jsonl.
usage: collect.py outdir extdir   -> outdir/todo_L.jsonl (distinct accepted), outdir/rejected.jsonl, outdir/collect.json"""
import sys, json, glob, os, collections
N17 = '/Users/agent/Projects/TC17/work/n17'
sys.path.insert(0, N17 + '/validate')
from canon import canon_many
outdir, extdir = sys.argv[1], sys.argv[2]
def jl(f):
    for l in open(f):
        try: yield json.loads(l)
        except Exception: pass
def cls_of(f): return os.path.basename(f).split('_')[0]
acc, rej = [], []
for f in sorted(glob.glob(extdir + '/*_ext_*.jsonl')):
    c = cls_of(f)
    for r in jl(f):
        src = (c, str(r.get('idx')), r.get('comp'), 'slice' if r.get('slice') else 'rigid')
        if 'L' in r: acc.append((src, r['L']))
        if 'L_rejected' in r: rej.append((src, r['why'], r['L_rejected']))
for f in sorted(glob.glob(extdir + '/*_L17.jsonl')):   # realisable 17-line children of the lattice-level step at 16 lines
    c = cls_of(f)
    for r in jl(f):
        if 'L' in r: acc.append(((c, str(r.get('idx')), None, 'child17'), r['L']))
for f in sorted(glob.glob(extdir + '/*_fam_*.jsonl')):
    c = cls_of(f)
    for r in jl(f):
        if 'status' not in r or 'comp' not in r: continue
        src = (c, str(r.get('idx')), r.get('comp'), 'family')
        for L in r.get('generic_L', []): acc.append((src + ('generic',), L))
        for L in r.get('special_L', []): acc.append((src + ('special',), L))
        for x in r.get('rejected', []): rej.append((src, x['why'], x['L']))
def canons(items):
    out = []
    for k in range(0, len(items), 20000):
        out += canon_many(17, [bl for bl in items[k:k + 20000]])
    return out
known = {}
for i, r in enumerate(jl(N17 + '/run/checked_L.jsonl')):
    known[r['canon']] = dict(index=i, known=r.get('known') or 'new (21 Oct 2026)', verdict=r.get('verdict'))
distinct, src_of = {}, collections.defaultdict(set)
for (src, L), c in zip(acc, canons([L for _, L in acc])):
    distinct.setdefault(c, L); src_of[c].add(src)
rdistinct, rsrc = {}, collections.defaultdict(set)
for (src, why, L), c in zip(rej, canons([L for _, _, L in rej])):
    rdistinct.setdefault(c, L); rsrc[c].add(src + (why,))
per_class = collections.defaultdict(set)
for c, ss in src_of.items():
    for s in ss: per_class[s[0]].add(c)
with open(outdir + '/todo_L.jsonl', 'w') as out:
    for k, (c, L) in enumerate(sorted(distinct.items(), key=lambda kv: (known.get(kv[0], {}).get('index', 99), kv[0]))):
        out.write(json.dumps(dict(idx=k, canon=c, blocks=L, known=known.get(c, {}).get('known', 'NEW'), known_index=known.get(c, {}).get('index'),
                                  classes=sorted({s[0] for s in src_of[c]}), records=len(src_of[c]))) + '\n')
with open(outdir + '/rejected.jsonl', 'w') as out:
    for c, L in rdistinct.items():
        out.write(json.dumps(dict(canon=c, blocks=L, sources=[list(s) for s in sorted(rsrc[c])][:20], records=len(rsrc[c]))) + '\n')
res = dict(accepted_records=len(acc), rejected_records=len(rej), distinct=len(distinct), known=sum(1 for c in distinct if c in known),
           new=sum(1 for c in distinct if c not in known), known_missing=sum(1 for c in known if c not in distinct),
           rejected_distinct=len(rdistinct), per_class={c: len(v) for c, v in sorted(per_class.items())},
           per_lattice={c: dict(known=known.get(c, {}).get('known', 'NEW'), records=len(src_of[c]), classes=sorted({s[0] for s in src_of[c]})) for c in distinct})
json.dump(res, open(outdir + '/collect.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'per_lattice'}))
