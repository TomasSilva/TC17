"""Unattended extension pipeline for one core class.
usage: runclass.py TAG P comp_files...      (TAG: output prefix, P: parallel workers)
Level n = 13 (cores), then recursively n = 14, 15, 16 for components of dimension >= 2:
  rigid  (dim 0)  -> extend.py        (exact)
  dim 1           -> famrun.py        (exact, special points)
  dim >= 2        -> dim2gen.py (children n + 1) -> fast filters -> retag -> m2compb -> next level
At n + 1 = 17 the children are complete lattices; the realisable ones go to the collection directly.
All outputs: TAG_*.jsonl; final list of lattice files: TAG_Lfiles.txt"""
import sys, json, subprocess, os, glob, time
TAG, P = sys.argv[1], int(sys.argv[2]); files = sys.argv[3:]
N0 = 13
if files and files[0].startswith('--n='): N0 = int(files[0][4:]); files = files[1:]
PY = '/Users/agent/Projects/TC17/.venv/bin/python'
COMP = '/Users/agent/Projects/TC17/work/n17/comp'
FF = '/Users/agent/Projects/TC17/work/tc15/recheck_resultant/full_recheck.py'
def par(cmds):
    """Run the commands in parallel; stderr goes to TAG_workers.err and a non-zero return code is logged
    with its command (audit F4, 23 Oct 2026: failures used to pass unnoticed)."""
    errf = open(TAG + '_workers.err', 'a')
    procs = [(c, subprocess.Popen(c, stdout=subprocess.DEVNULL, stderr=errf)) for c in cmds]
    bad = 0
    for c, p in procs:
        if p.wait() != 0:
            bad += 1
            log('WORKER FAILED (return code %d): %s' % (p.returncode, ' '.join(os.path.basename(x) for x in c[1:])))
    errf.close()
    return bad
def check_done(infile, outfiles, kind, level):
    """Every component of the input must have its record in the outputs: extend.py writes one 'done' record
    per searched component, famrun.py one record per component (audit F4)."""
    want, got = set(), set()
    for l in open(infile):
        r = json.loads(l)
        if r.get('status') != 'REAL': continue
        for ci, c in enumerate(r.get('comps', [])):
            if (kind == 'rigid' and c['dim'] == 0) or (kind == 'family' and c['dim'] >= 1): want.add((str(r['idx']), ci))
    for f in outfiles:
        if not os.path.exists(f): continue
        for l in open(f):
            try: r = json.loads(l)
            except Exception: continue
            if kind == 'rigid' and r.get('done') and not r.get('slice'): got.add((str(r['idx']), r['comp']))
            if kind == 'family' and 'status' in r and 'comp' in r: got.add((str(r['idx']), r['comp']))
    miss = sorted(want - got)
    log('n=%d %s components: %d expected, %d finished%s' % (level, kind, len(want), len(want & got),
        '' if not miss else ', MISSING %d, e.g. %s' % (len(miss), miss[:3])))
    return miss
def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)
def split_by_dim(recs, base):
    f0, f1, f2 = base + '_r0.jsonl', base + '_r1.jsonl', base + '_r2.jsonl'
    n0 = n1 = n2 = 0
    with open(f0, 'w') as a, open(f1, 'w') as b, open(f2, 'w') as c:
        for r in recs:
            if r.get('status') != 'REAL': continue
            dims = [x['dim'] for x in r.get('comps', [])]
            l = json.dumps(r) + '\n'
            if 0 in dims: a.write(l); n0 += 1
            if 1 in dims: b.write(l); n1 += 1
            if any(x >= 2 for x in dims): c.write(l); n2 += 1
    return f0, f1, f2, (n0, n1, n2)
def load(fs):
    out = {}
    for f in fs:
        if not os.path.exists(f): continue
        for l in open(f):
            try: r = json.loads(l)
            except Exception: continue
            out[str(r.get('idx'))] = r
    return list(out.values())
Lfiles = []
recs = load(files)
other = [r for r in recs if r.get('status') not in ('REAL', 'NONREAL')]
log('records', len(recs), 'REAL', sum(1 for r in recs if r.get('status') == 'REAL'), 'other (timeout/error)', len(other))
with open(TAG + '_other.jsonl', 'w') as f:
    for r in other: f.write(json.dumps(r) + '\n')
n = N0
while recs:
    base = '%s_n%d' % (TAG, n)
    f0, f1, f2, cnt = split_by_dim(recs, base)
    log('n=%d rigid %d, dim1 %d, dim>=2 %d' % (n, *cnt))
    if n < 17:
        par([[PY, COMP + '/extend.py', f0, str(p), str(P), '%s_ext_%d.jsonl' % (base, p)] for p in range(P)])
        Lfiles += ['%s_ext_%d.jsonl' % (base, p) for p in range(P)]
        log('n=%d rigid done' % n)
        check_done(f0, ['%s_ext_%d.jsonl' % (base, p) for p in range(P)], 'rigid', n)
        par([[PY, COMP + '/famrun.py', f1, '%s_fam_%d.jsonl' % (base, p), str(p), str(P)] for p in range(P)])
        Lfiles += ['%s_fam_%d.jsonl' % (base, p) for p in range(P)]
        check_done(f1, ['%s_fam_%d.jsonl' % (base, p) for p in range(P)], 'family', n)
        slow = set()
        for p in range(P):
            for l in open('%s_fam_%d.jsonl' % (base, p)):
                r = json.loads(l)
                if r.get('status') in ('SLOW', 'EXC', 'NOMODEL', 'LATTICE-MISMATCH', 'SPECIAL-ERROR'): slow.add(str(r['idx']))
        log('n=%d families done; %d family records sent to the lattice-level step (slow or failed)' % (n, len(slow)))
        if slow:
            with open(f2, 'a') as c2:
                for r in recs:
                    if str(r.get('idx')) in slow: c2.write(json.dumps(r) + '\n')
            cnt = (cnt[0], cnt[1], cnt[2] + len(slow))
    if cnt[2] == 0 or n >= 17:
        break
    ch = base + '_ch.jsonl'
    rc = subprocess.run([PY, COMP + '/dim2gen.py', f2, ch], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
    if rc != 0: log('DIM2GEN FAILED (return code %d)' % rc)
    nch = sum(1 for _ in open(ch))
    log('n=%d -> %d children with %d lines' % (n, nch, n + 1))
    par([[PY, FF, str(n + 1), ch, str(p), str(P), '%s_ff_%d' % (base, p)] for p in range(P)])
    src = [json.loads(l)['idx'] for l in open(ch)]
    dfr = base + '_chdefer.jsonl'
    with open(dfr, 'w') as out:
        for p in range(P):
            for l in open('%s_ff_%d_defer.jsonl' % (base, p)):
                r = json.loads(l); r['idx'] = src[r['idx']]; out.write(json.dumps(r) + '\n')
    nd = sum(1 for _ in open(dfr))
    log('n=%d children deferred by fast filters: %d' % (n, nd))
    par([[PY, COMP + '/m2compb.py', str(n + 1), dfr, str(p), str(P), '300', '%s_chcomp_%d.jsonl' % (base, p), '25'] for p in range(P)])
    recs = load(['%s_chcomp_%d.jsonl' % (base, p) for p in range(P)])
    oth = [r for r in recs if r.get('status') not in ('REAL', 'NONREAL')]
    with open('%s_other_n%d.jsonl' % (TAG, n + 1), 'w') as f:
        for r in oth: f.write(json.dumps(r) + '\n')
    log('n=%d children: REAL %d, NONREAL %d, other (timeout/error) %d' % (n + 1, sum(1 for r in recs if r.get('status') == 'REAL'), sum(1 for r in recs if r.get('status') == 'NONREAL'), len(oth)))
    if n + 1 == 17:
        # complete lattices: the realisable ones are candidate L's
        with open(base + '_L17.jsonl', 'w') as f:
            for r in recs:
                if r.get('status') == 'REAL': f.write(json.dumps(dict(idx=r['idx'], L=[b for b in r['blocks'] if len(b) >= 3])) + '\n')
        Lfiles.append(base + '_L17.jsonl')
        break
    n += 1
open(TAG + '_Lfiles.txt', 'w').write('\n'.join(Lfiles) + '\n')
log('done; lattice files:', len(Lfiles))
