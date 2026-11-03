#!/usr/bin/env python
"""Overnight rerun of the computer-assisted proof of Terao's conjecture for 17 lines (TC_N17.md section 8),
from scratch, in work/n17/campaign/, with independent checks at every step (2-3 Nov 2026).

Stages (in order; each writes done/<stage>.json and is skipped on a restart; a file STOP in this directory
stops the campaign between stages; a failed stage is recorded in done/<stage>.FAILED and the stages that
depend on it are skipped):
  prep          tools, compiled enumerators, copies of the scripts, SHA-256 of the code of record
  cover         covering lemma: level 1 (2,471 assignments), Farkas certificates, propagation check, glpsol,
                validation of the model on the 299 lattices with phi_max = 1
  n8zero        no 8-point line: K_{4,4,4,4} (23 lattices), the eleven 5-point vectors (pencil5c), screening
                of the 11,224 lattices (fast filters, Macaulay2), independent screening (Anghel-Stan)
  cores         the 13-line core classes b48 (3-7 points), b48w (3-8 points: the class the manuscript
                leaves open), b49, b50, b51: heavyaug_p + lsgen3 + labelg; invariants re-derived; the 28
                known cores and the phi-max cores of the 16 lattices must be in b48
  indep_cores   second enumerator (bigblocks + fill_triples, no unjoined-pair cut) and comparison
  filters       exact fast filters on every core (10 parts per class)
  as_cores      Anghel-Stan's exact realisation code on every core
  m2            Macaulay2 components of every deferred core; comparison with Anghel-Stan; Macaulay2 on the
                cores only our filter rejected and Anghel-Stan left undecided
  route_timeouts the cores/children on which Macaulay2 timed out (two 14-line children of b51, as in October
                2026) are routed through the lattice-level step; their children screened with Anghel-Stan
  ext_b48, ext_b48w, ext_b49, ext_b50, ext_b51   the extension pipeline (runclass.py) of each class
  as_children   Anghel-Stan's code on every child lattice of the lattice-level step, comparison
  indep_rigid   independent numeric rigid search on every rigid component, comparison
  final         collection of every 17-line lattice found (accepted and rejected), comparison with the 16,
                exact realisation space and freeness (exact_tc_lattice), syzygy degrees over the field of
                definition (freecheck, Macaulay2), Anghel-Stan re-certification, window and 4-chain check
  report        REPORT.md
usage: campaign.py [stage ...]   (default: every stage, in order)"""
import os, sys, json, time, subprocess, glob, shutil, itertools, collections, hashlib, re, traceback
ROOT = '/Users/agent/Projects/TC17'
PY = ROOT + '/.venv/bin/python'
C = ROOT + '/work/n17/campaign'
N17 = ROOT + '/work/n17'
FF = ROOT + '/work/tc15/recheck_resultant/full_recheck.py'
EXACT = ROOT + '/work/tc15/exact_tc_lattice.py'
M2COMPB = N17 + '/comp/m2compb.py'
NCPU = int(os.environ.get('NCPU', '10'))
NICE = ['nice', '-n', '5']
os.makedirs(C + '/done', exist_ok=True)
LOGF = open(C + '/campaign.log', 'a')
RESULTS = {}

def log(*a):
    line = time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + ' '.join(str(x) for x in a)
    print(line, file=LOGF, flush=True); print(line, flush=True)

def short(cmd):
    if isinstance(cmd, str): return cmd[:220]
    return ' '.join(os.path.basename(x) if x.startswith('/') else x for x in cmd)[:220]

def sh(cmd, cwd=None, out=None, err=None, shell=False, check=True):
    """run one command (list, or a string with shell=True); stdout / stderr to files when given"""
    t0 = time.time()
    fo = open(out, 'w') if out else None
    fe = open(err, 'w') if err else None
    p = subprocess.run(cmd if shell else NICE + cmd, cwd=cwd, shell=shell, stdout=fo, stderr=fe)
    for f in (fo, fe):
        if f: f.close()
    log('  ran (%.0fs, rc %d): %s' % (time.time() - t0, p.returncode, short(cmd)))
    if check and p.returncode != 0:
        raise RuntimeError('command failed (rc %d): %s' % (p.returncode, short(cmd)))
    return p.returncode

def par(jobs, maxjobs=None, label=''):
    """jobs: list of dict(cmd=list or str, cwd, out, err, shell); at most maxjobs at a time; returns the rcs"""
    maxjobs = maxjobs or NCPU
    running, rcs, todo, t0 = {}, {}, list(enumerate(jobs)), time.time()
    while todo or running:
        for j, (p, fo, fe) in list(running.items()):
            if p.poll() is not None:
                rcs[j] = p.returncode
                for f in (fo, fe):
                    if f: f.close()
                if p.returncode != 0: log('  JOB FAILED (rc %d): %s' % (p.returncode, short(jobs[j]['cmd'])))
                del running[j]
        while todo and len(running) < maxjobs:
            j, jb = todo.pop(0)
            fo = open(jb['out'], 'w') if jb.get('out') else None
            fe = open(jb['err'], 'w') if jb.get('err') else None
            shell = jb.get('shell', False)
            cmd = jb['cmd'] if shell else NICE + jb['cmd']
            running[j] = (subprocess.Popen(cmd, cwd=jb.get('cwd'), shell=shell, stdout=fo, stderr=fe), fo, fe)
        time.sleep(1)
    nbad = sum(1 for r in rcs.values() if r)
    log('  %s: %d jobs done in %.0fs, failures %d' % (label or 'jobs', len(jobs), time.time() - t0, nbad))
    if nbad: raise RuntimeError('%d of %d jobs failed (%s)' % (nbad, len(jobs), label))
    return [rcs[j] for j in range(len(jobs))]

def expect(stage, name, got, exp=None):
    ok = (exp is None) or (got == exp)
    RESULTS.setdefault(stage, {})[name] = dict(got=got, expected=exp, ok=ok)
    log('  [%s] %s: got %s, expected %s %s' % (stage, name, got, 'n/a' if exp is None else exp, 'OK' if ok else '*** MISMATCH ***'))
    return ok

def record(stage, name, value):
    RESULTS.setdefault(stage, {})[name] = value
    log('  [%s] %s: %s' % (stage, name, json.dumps(value)[:400]))

def mark(stage, t0):
    info = RESULTS.get(stage, {})
    info['_finished'] = time.strftime('%Y-%m-%d %H:%M:%S'); info['_seconds'] = round(time.time() - t0)
    json.dump(info, open(C + '/done/%s.json' % stage, 'w'), indent=1)
    log('DONE stage %s (%.0f s)' % (stage, time.time() - t0))

def done(stage): return os.path.exists(C + '/done/%s.json' % stage)
def failed(stage): return os.path.exists(C + '/done/%s.FAILED' % stage)
def stop_check():
    if os.path.exists(C + '/STOP'):
        log('STOP file present: stopping before the next stage'); sys.exit(0)
def count_lines(path):
    n = 0
    with open(path) as f:
        for _ in f: n += 1
    return n
def patch(path, old, new):
    txt = open(path).read()
    assert old in txt, (path, old)
    open(path, 'w').write(txt.replace(old, new))
def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()
def jl(path):
    with open(path) as f:
        for l in f:
            l = l.strip()
            if l:
                try: yield json.loads(l)
                except Exception: pass

# ----------------------------------------------------------------------------------------------- prep
CODE = [N17 + '/heavy/heavyaug_p.c', N17 + '/heavy/lsgen3.c', N17 + '/heavy/g6blocks.py', FF,
        ROOT + '/work/tc15/recheck_resultant/fast_real_fix.py', ROOT + '/work/tc15/fast_real.py',
        ROOT + '/work/tc15/fast_real2.py', EXACT, N17 + '/comp/m2comp2.py', M2COMPB, N17 + '/comp/extend.py',
        N17 + '/comp/famext.py', N17 + '/comp/famrun.py', N17 + '/comp/famspecial2.py', N17 + '/comp/planemodel.py',
        N17 + '/comp/dim2gen.py', N17 + '/comp/phicap.py', N17 + '/run/runclass.py', N17 + '/validate/canon.py',
        N17 + '/cover/ilp/gamma_ilp.py', N17 + '/cover/ilp/level1.py', N17 + '/cover/ilp/level2.py',
        N17 + '/cover/ilp/farkas.py', N17 + '/cover/ilp/propcheck.py', N17 + '/cover/ilp/validate.py',
        N17 + '/n8zero/k4444.py', N17 + '/n8zero/pencil5c.py', N17 + '/audit/cores/bigblocks.py',
        N17 + '/audit/cores/fill_triples.py', N17 + '/audit/indep/indep_rigid.py', N17 + '/audit/asscreen/as_screen.py',
        ROOT + '/third_party/anghel_stan_anc/anc/exact.py', ROOT + '/third_party/anghel_stan_anc/anc/realize.py',
        ROOT + '/third_party/anghel_stan_anc/anc/arr.py', ROOT + '/third_party/anghel_stan_anc/anc/g6util.py']

def st_prep():
    for d in ['cover', 'n8zero', 'cores', 'indep', 'as', 'comp', 'ext', 'indep_rigid', 'final', 'bin']:
        os.makedirs(C + '/' + d, exist_ok=True)
    info = {}
    info['git_head'] = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    info['M2'] = subprocess.run(['M2', '--version'], capture_output=True, text=True).stdout.strip().split('\n')[0]
    info['python'] = subprocess.run([PY, '-c', 'import sys, flint, pynauty; print(sys.version.split()[0], "python-flint", flint.__version__, "pynauty", pynauty.__version__)'], capture_output=True, text=True).stdout.strip()
    info['labelg'] = shutil.which('labelg'); info['glpsol'] = shutil.which('glpsol')
    info['ncpu'] = NCPU
    sh(['cc', '-O3', '-march=native', '-DWORDSIZE=64', '-I/opt/homebrew/include', '-o', C + '/bin/heavyaug_p', N17 + '/heavy/heavyaug_p.c', '-L/opt/homebrew/lib', '-lnautyL1'])
    sh(['cc', '-O3', '-march=native', '-o', C + '/bin/lsgen3', N17 + '/heavy/lsgen3.c'])
    for f in glob.glob(N17 + '/cover/ilp/*.py'): shutil.copy(f, C + '/cover/')
    for f in ['k4444.py', 'pencil5c.py']: shutil.copy(N17 + '/n8zero/' + f, C + '/n8zero/')
    patch(C + '/n8zero/k4444.py', "'../validate'", "'%s/validate'" % N17)
    for f in ['bigblocks.py', 'fill_triples.py', 'compare.py']:
        shutil.copy(N17 + '/audit/cores/' + f, C + '/indep/')
        if f != 'compare.py': patch(C + '/indep/' + f, N17 + '/audit/cores', C + '/indep')
    shutil.copy(N17 + '/audit/asscreen/as_screen.py', C + '/as/')
    shutil.copy(N17 + '/audit/indep/indep_rigid.py', C + '/indep_rigid/')
    info['sha256'] = {os.path.relpath(f, ROOT): sha(f) for f in CODE}
    anc = ROOT + '/third_party/anghel_stan_anc/anc'
    info['AS_heavyaug_identical'] = sha(N17 + '/heavy/heavyaug_orig.c') == sha(anc + '/heavyaug.c') if os.path.exists(anc + '/heavyaug.c') else None
    info['AS_lsgen3_identical'] = sha(N17 + '/heavy/lsgen3.c') == sha(anc + '/lsgen3.c') if os.path.exists(anc + '/lsgen3.c') else None
    RESULTS['prep'] = info
    r = subprocess.run([PY, '-c', 'import sys; sys.path.insert(0, "%s"); import exact, realize; print("ok")' % anc], capture_output=True, text=True)
    expect('prep', 'Anghel-Stan code imports', r.stdout.strip(), 'ok')

# ----------------------------------------------------------------------------------------------- cover
def st_cover():
    D = C + '/cover'
    sh([PY, 'level1.py'], cwd=D, out=D + '/level1.out', err=D + '/level1.err')
    tot = [l for l in open(D + '/level1.out') if l.startswith('total')]
    expect('cover', 'level1 surviving delta-assignments', int(tot[-1].split()[1]) if tot else None, 2471)
    par([dict(cmd=[PY, 'farkas.py', str(p), str(NCPU), '4'], cwd=D, out=D + '/farkas_%d.out' % p, err=D + '/farkas_%d.err' % p) for p in range(NCPU)], label='farkas')
    cert = bad = 0
    for p in range(NCPU):
        for l in open(D + '/farkas_%d.out' % p):
            if l.startswith('part'):
                q = l.split(); cert += int(q[3]); bad += int(q[6])
    expect('cover', 'Farkas certificates verified exactly', cert, 2471)
    expect('cover', 'Farkas certificates missing', bad, 0)
    par([dict(cmd=[PY, 'propcheck.py', str(p), str(NCPU)], cwd=D, out=D + '/prop_%d.out' % p, err=D + '/prop_%d.err' % p) for p in range(NCPU)], label='propcheck')
    inf = opn = 0
    for p in range(NCPU):
        for l in open(D + '/prop_%d.out' % p):
            if l.startswith('part'):
                q = l.split(); inf += int(q[3]); opn += int(q[5])
    expect('cover', 'propagation check: infeasible', inf, 2435)
    expect('cover', 'propagation check: open (settled by Farkas)', opn, 36)
    par([dict(cmd=[PY, 'level2.py', str(p), str(NCPU), '300'], cwd=D, out=D + '/l2_%d.out' % p, err=D + '/l2_%d.err' % p) for p in range(NCPU)], label='level2 (glpsol)')
    cnt = collections.Counter()
    for p in range(NCPU):
        for l in open(D + '/l2_%d.out' % p):
            w = l.split()
            for key in ('INFEASIBLE', 'FEASIBLE', 'UNDECIDED'):
                if key in w: cnt[key] += 1
    record('cover', 'level2 glpsol verdicts', dict(cnt))
    expect('cover', 'level2 feasible or undecided', cnt['FEASIBLE'] + cnt['UNDECIDED'], 0)
    sh([PY, 'validate.py', N17 + '/cover/phi1_all.g6', '299'], cwd=D, out=D + '/validate.out', err=D + '/validate.err')
    v = [l for l in open(D + '/validate.out') if l.startswith('checked')]
    record('cover', 'validate.py (model evaluated on the 299 lattices with phi_max = 1)', v[-1].strip() if v else None)
    expect('cover', 'model violations on real lattices', int(v[-1].split()[-1]) if v else None, 0)

# ----------------------------------------------------------------------------------------------- screening helper
def final_verdict(v):
    return v.split('|')[-1].strip().split()[0] if v.strip() else 'MISSING'

def screen(D, pref, n, infile, m2timeout=300, batch=25):
    """fast filters (NCPU parts) then Macaulay2 on the deferred lattices; returns (stats, m2 records by idx)"""
    src = [r['idx'] for r in jl(infile)]
    par([dict(cmd=[PY, FF, str(n), infile, str(p), str(NCPU), D + '/%s_ff_%d' % (pref, p)], out=D + '/%s_ff_%d.log' % (pref, p), err=D + '/%s_ff_%d.err' % (pref, p)) for p in range(NCPU)], label=pref + ' fast filters')
    stats = collections.Counter(); nver = 0
    dfr = D + '/%s_defer.jsonl' % pref
    with open(dfr, 'w') as out:
        for p in range(NCPU):
            for r in jl(D + '/%s_ff_%d_defer.jsonl' % (pref, p)):
                r['idx'] = src[r['idx']]; out.write(json.dumps(r) + '\n')
            for l in open(D + '/%s_ff_%d.out' % (pref, p)):
                q = l.split(None, 1)
                if len(q) == 2 and q[0].isdigit(): stats[final_verdict(q[1])] += 1; nver += 1
    ndef = count_lines(dfr)
    recs = {}
    if ndef:
        for p in range(NCPU):
            f = D + '/%s_comp_%d.jsonl' % (pref, p)
            if os.path.exists(f): os.remove(f)
        par([dict(cmd=[PY, M2COMPB, str(n), dfr, str(p), str(NCPU), str(m2timeout), D + '/%s_comp_%d.jsonl' % (pref, p), str(batch)], out=D + '/%s_comp_%d.log' % (pref, p), err=D + '/%s_comp_%d.err' % (pref, p)) for p in range(NCPU)], label=pref + ' Macaulay2')
        for p in range(NCPU):
            for r in jl(D + '/%s_comp_%d.jsonl' % (pref, p)): recs[str(r['idx'])] = r
    return dict(lattices=len(src), verdict_lines=nver, filter_stats=dict(stats), deferred=ndef,
                m2_status=dict(collections.Counter(r['status'] for r in recs.values())), m2_records=len(recs)), recs

def as_jsonl(D, pref, n, infile):
    par([dict(cmd=[PY, C + '/as_jsonl.py', str(n), infile, str(p), str(NCPU), D + '/%s_as_%d.status' % (pref, p)], out=D + '/%s_as_%d.log' % (pref, p), err=D + '/%s_as_%d.err' % (pref, p)) for p in range(NCPU)], label=pref + ' Anghel-Stan screening')

def compare_as(stage, label, n, infile, ffglob, m2glob, asglob, outpath):
    sh([PY, C + '/compare_as.py', str(n), infile, ffglob, m2glob, asglob, outpath], out=outpath + '.out', err=outpath + '.err')
    res = json.load(open(outpath))
    record(stage, label + ': ours vs Anghel-Stan', res['table'])
    expect(stage, label + ': disagreements with Anghel-Stan', res['disagreements'], 0)
    expect(stage, label + ': lattices without a verdict of ours', res['missing_ours'], 0)
    return res

# ----------------------------------------------------------------------------------------------- n8zero
VEC5 = ['55411', '55321', '55222', '54421', '54331', '54322', '53332', '44431', '44422', '44332', '43333']
EXP5 = {'53332': 0, '44431': 122, '44422': 232, '44332': 3124, '43333': 7723}
EXPH = {'53332': 2303, '44431': 87, '44422': 863, '44332': 49565, '43333': 192133}

def st_n8zero():
    D = C + '/n8zero'
    sh([PY, 'k4444.py'], cwd=D, out=D + '/k4444.jsonl', err=D + '/k4444.log')
    expect('n8zero', 'K4444 triangle decompositions (lattices with a 4-point line)', count_lines(D + '/k4444.jsonl'), 23)
    par([dict(cmd=[PY, 'pencil5c.py', v], cwd=D, out=D + '/p5c_%s.jsonl' % v, err=D + '/p5c_%s.log' % v) for v in VEC5], label='pencil5c (eleven vectors)')
    for v in VEC5:
        txt = open(D + '/p5c_%s.log' % v).read()
        hs = re.search(r'heavy sets (\d+)', txt)
        expect('n8zero', '5-point vector %s: heavy configurations' % v, int(hs.group(1)) if hs else None, EXPH.get(v))
        expect('n8zero', '5-point vector %s: lattices' % v, count_lines(D + '/p5c_%s.jsonl' % v), EXP5.get(v, 0))
    k = 0
    with open(D + '/n8_all.jsonl', 'w') as out:
        for name, f in [('k4444', 'k4444.jsonl')] + [(v, 'p5c_%s.jsonl' % v) for v in VEC5]:
            for r in jl(D + '/' + f):
                out.write(json.dumps(dict(idx='%s:%s' % (name, r['idx']), blocks=r['blocks'])) + '\n'); k += 1
    expect('n8zero', 'lattices without an 8-point line to screen', k, 11224)
    sh([PY, C + '/invariants.py', '17', D + '/n8_all.jsonl', '80', '4', '7', '6', '--cut', '--w4'], out=D + '/invariants.json', err=D + '/invariants.err')
    inv = json.load(open(D + '/invariants.json'))
    record('n8zero', 'invariants (b2 = 80, m <= 6, 4-7 points, W5, isomorphism classes)', inv)
    expect('n8zero', 'invariant violations', sum(inv['violations'].values()), 0)
    expect('n8zero', 'distinct lattices (pynauty)', inv['distinct'], k)
    st, recs = screen(D, 'n8', 17, D + '/n8_all.jsonl', m2timeout=900)
    record('n8zero', 'screening', st)
    expect('n8zero', 'verdict lines', st['verdict_lines'], k)
    expect('n8zero', 'realisable lattices (Macaulay2)', st['m2_status'].get('REAL', 0), 0)
    expect('n8zero', 'Macaulay2 timeouts/errors', sum(v for s, v in st['m2_status'].items() if s not in ('REAL', 'NONREAL')), 0)
    expect('n8zero', 'Macaulay2 records', st['m2_records'], st['deferred'])
    as_jsonl(D, 'n8', 17, D + '/n8_all.jsonl')
    compare_as('n8zero', 'no-8-point-line lattices', 17, D + '/n8_all.jsonl', D + '/n8_ff_*.out', D + '/n8_comp_*.jsonl', D + '/n8_as_*.status', D + '/n8_compare.json')

# ----------------------------------------------------------------------------------------------- cores
CLASSES = [('b48', 5, 30, 21164, 213339), ('b48w', 4, 30, None, None), ('b49', 4, 29, 154172, 1820363),
           ('b50', 4, 28, 738023, 12276119), ('b51', 4, 27, 2916332, 65691853)]
EXPHEAVY = {'b48': 258, 'b49': 274}

def st_cores():
    D = C + '/cores'
    for cls, lo, X, nexp, rawexp in CLASSES:
        heavy = D + '/%s_heavy.g6' % cls
        sh([C + '/bin/heavyaug_p', '13', '6', str(lo), '9', str(X), '0', '100', '0', '1', '0', '1000', '2'], out=heavy, err=heavy + '.err')
        H = [h for h in open(heavy).read().split('\n') if h]
        expect('cores', '%s heavy configurations' % cls, len(H), EXPHEAVY.get(cls))
        parts = [open(D + '/%s_heavy_%d.g6' % (cls, p), 'w') for p in range(NCPU)]
        for i, h in enumerate(H): parts[i % NCPU].write(h + '\n')
        for f in parts: f.close()
        par([dict(cmd='%s/bin/lsgen3 13 6 4 %d 9 %d 0 0 complete < %s/%s_heavy_%d.g6 > %s/%s_raw_%d.g6 2> %s/%s_raw_%d.err' % (C, lo, X, D, cls, p, D, cls, p, D, cls, p), shell=True) for p in range(NCPU)], label=cls + ' lsgen3')
        raw = sum(count_lines(D + '/%s_raw_%d.g6' % (cls, p)) for p in range(NCPU))
        expect('cores', '%s raw completions' % cls, raw, rawexp)
        par([dict(cmd='LC_ALL=C labelg -q -f%s < %s/%s_raw_%d.g6 | LC_ALL=C sort -u -S 512M > %s/%s_can_%d.g6' % ('a' * 13, D, cls, p, D, cls, p), shell=True) for p in range(NCPU)], label=cls + ' labelg')
        sh('LC_ALL=C sort -m -u %s/%s_can_*.g6 > %s/%s_classes.g6' % (D, cls, D, cls), shell=True)
        ncl = count_lines(D + '/%s_classes.g6' % cls)
        expect('cores', '%s lattices up to isomorphism' % cls, ncl, nexp)
        for p in range(NCPU):
            os.remove(D + '/%s_raw_%d.g6' % (cls, p)); os.remove(D + '/%s_can_%d.g6' % (cls, p))
        sh([PY, '-c', '''
import sys, json
sys.path.insert(0, "%s/heavy")
from g6blocks import decode
cls = sys.argv[1]
for k, line in enumerate(open(sys.argv[2])):
    B = [b for b in decode(line, 13) if len(b) >= 3]
    print(json.dumps({"idx": "%%s:%%d" %% (cls, k), "blocks": B}))''' % N17, cls, D + '/%s_classes.g6' % cls], out=D + '/%s.jsonl' % cls)
        expect('cores', '%s jsonl records' % cls, count_lines(D + '/%s.jsonl' % cls), ncl)
        sh([PY, C + '/invariants.py', '13', D + '/%s.jsonl' % cls, str(78 - X), '3', '7' if lo == 5 else '8', '6', '--cut'], out=D + '/%s_invariants.json' % cls, err=D + '/%s_invariants.err' % cls)
        inv = json.load(open(D + '/%s_invariants.json' % cls))
        record('cores', '%s invariants' % cls, inv)
        expect('cores', '%s invariant violations' % cls, sum(inv['violations'].values()), 0)
        expect('cores', '%s distinct certificates (pynauty) = class size' % cls, inv['distinct'], ncl)
    sh([PY, C + '/chains.py', 'cores', D + '/b48_classes.g6', D + '/b48w_classes.g6'], out=D + '/chains_cores.json', err=D + '/chains_cores.err')
    ch = json.load(open(D + '/chains_cores.json'))
    record('cores', 'positive controls', ch)
    expect('cores', 'known cores (work/n17/validate/cores13.jsonl) present in b48', ch['cores13_in_b48'], ch['cores13'])
    expect('cores', 'phi-max cores of the 16 lattices present in b48', ch['chain_cores_in_b48'], ch['chain_cores'])
    expect('cores', 'b48 is a subset of b48w', ch['b48_subset_of_b48w'], True)
    record('cores', 'b48w lattices with an 8-point line', ch['b48w_minus_b48'])

# ----------------------------------------------------------------------------------------------- indep_cores
def st_indep_cores():
    D = C + '/indep'
    for tag, lo, X in [('a48', 5, 30), ('a48w', 4, 30), ('a49', 4, 29), ('a50', 4, 28), ('a51', 4, 27)]:
        sh([PY, 'bigblocks.py', '13', str(lo), '9', '6', str(X), tag], cwd=D, out=D + '/bigblocks_%s.log' % tag, err=D + '/bigblocks_%s.err' % tag)
        par([dict(cmd=[PY, 'fill_triples.py', '13', str(lo), '9', '6', str(X), tag, str(p), str(NCPU)], cwd=D, out=D + '/fill_%s_%d.log' % (tag, p), err=D + '/fill_%s_%d.err' % (tag, p)) for p in range(NCPU)], label=tag + ' fill_triples')
        cls = 'b' + tag[1:]
        sh([PY, 'compare.py', C + '/cores/%s_classes.g6' % cls, tag], cwd=D, out=D + '/compare_%s.out' % tag, err=D + '/compare_%s.err' % tag)
        line = [l for l in open(D + '/compare_%s.out' % tag) if 'distinct' in l]
        record('indep_cores', cls + ' comparison', line[-1].strip() if line else None)
        m = re.search(r'only heavyaug (\d+), only ours (\d+) \(of which with an unjoined heavy pair t > 8: (\d+)\)', line[-1]) if line else None
        if m:
            expect('indep_cores', cls + ': lattices found only by heavyaug+lsgen3', int(m.group(1)), 0)
            expect('indep_cores', cls + ': lattices found only by the second enumerator and not explained by the cut', int(m.group(2)) - int(m.group(3)), 0)
            expect('indep_cores', cls + ': lattices removed by the unjoined-pair cut', int(m.group(2)), {'b51': 7, 'b48': 0, 'b49': 0, 'b50': 0}.get(cls))
        else:
            expect('indep_cores', cls + ': comparison parsed', False, True)

# ----------------------------------------------------------------------------------------------- filters
EXPDEF = {'b48': 195, 'b49': 2950, 'b50': 26093, 'b51': 157533}

def st_filters():
    D = C + '/cores'
    for cls, lo, X, nexp, rawexp in CLASSES:
        inp = D + '/%s.jsonl' % cls
        par([dict(cmd=[PY, FF, '13', inp, str(p), str(NCPU), D + '/%s_ff_%d' % (cls, p)], out=D + '/%s_ff_%d.log' % (cls, p), err=D + '/%s_ff_%d.err' % (cls, p)) for p in range(NCPU)], label=cls + ' fast filters')
        stats = collections.Counter(); nver = 0; ndef = 0
        with open(D + '/%s_defer.jsonl' % cls, 'w') as out:
            for p in range(NCPU):
                for r in jl(D + '/%s_ff_%d_defer.jsonl' % (cls, p)):
                    r['idx'] = '%s:%d' % (cls, r['idx']); out.write(json.dumps(r) + '\n'); ndef += 1
                for l in open(D + '/%s_ff_%d.out' % (cls, p)):
                    q = l.split(None, 1)
                    if len(q) == 2 and q[0].isdigit(): stats[final_verdict(q[1])] += 1; nver += 1
        record('filters', cls + ' verdicts', dict(stats))
        expect('filters', cls + ' verdict lines = class size', nver, count_lines(inp))
        expect('filters', cls + ' deferred to Macaulay2', ndef, EXPDEF.get(cls))

# ----------------------------------------------------------------------------------------------- as_cores
def st_as_cores():
    D = C + '/as'
    for cls, lo, X, nexp, rawexp in CLASSES:
        par([dict(cmd=[PY, D + '/as_screen.py', C + '/cores/%s_classes.g6' % cls, '13', D + '/%s_p%d' % (cls, p), str(p), str(NCPU)], out=D + '/%s_p%d.log' % (cls, p), err=D + '/%s_p%d.err' % (cls, p)) for p in range(NCPU)], label=cls + ' Anghel-Stan screening')
        st = collections.Counter()
        for p in range(NCPU):
            for l in open(D + '/%s_p%d.status' % (cls, p)):
                q = l.split()
                if len(q) >= 2 and q[0].isdigit(): st[q[1]] += 1
        record('as_cores', cls + ' Anghel-Stan statuses', dict(st))
        expect('as_cores', cls + ' Anghel-Stan verdict lines = class size', sum(st.values()), count_lines(C + '/cores/%s.jsonl' % cls))

# ----------------------------------------------------------------------------------------------- m2
EXPREAL = {'b48': 85, 'b49': 1147, 'b50': 9162, 'b51': 58871}
EXPDIM = {'b48': (80, 5, 0), 'b49': (1050, 83, 14), 'b50': (7985, 1091, 86), 'b51': (49118, 9001, 752)}

def st_m2():
    D = C + '/comp'
    allf = D + '/defer_all.jsonl'
    with open(allf, 'w') as out:
        for cls, lo, X, nexp, rawexp in CLASSES:
            for l in open(C + '/cores/%s_defer.jsonl' % cls): out.write(l)
    ntot = count_lines(allf)
    record('m2', 'deferred cores (all classes)', ntot)
    par([dict(cmd=[PY, M2COMPB, '13', allf, str(p), str(NCPU), '300', D + '/comp_%d.jsonl' % p, '25'], out=D + '/comp_%d.log' % p, err=D + '/comp_%d.err' % p) for p in range(NCPU)], label='Macaulay2 components of the deferred cores')
    recs = {}
    for p in range(NCPU):
        for r in jl(D + '/comp_%d.jsonl' % p): recs[str(r['idx'])] = r
    expect('m2', 'Macaulay2 records = deferred cores', len(recs), ntot)
    for cls, lo, X, nexp, rawexp in CLASSES:
        mine = [r for k, r in recs.items() if k.split(':')[0] == cls]
        st = collections.Counter(r['status'] for r in mine)
        record('m2', cls + ' statuses', dict(st))
        expect('m2', cls + ' realisable cores', st.get('REAL', 0), EXPREAL.get(cls))
        expect('m2', cls + ' Macaulay2 timeouts/errors', sum(v for s, v in st.items() if s not in ('REAL', 'NONREAL')), 0)
        n0 = n1 = n2 = 0
        for r in mine:
            if r['status'] != 'REAL': continue
            dims = [c['dim'] for c in r.get('comps', [])]
            if 0 in dims: n0 += 1
            if 1 in dims: n1 += 1
            if any(d >= 2 for d in dims): n2 += 1
        expect('m2', cls + ' cores with rigid / curve / surface components', (n0, n1, n2), EXPDIM.get(cls))
        with open(D + '/comp_%s.jsonl' % cls, 'w') as out:
            for r in mine: out.write(json.dumps(r) + '\n')
        if done('as_cores'):
            compare_as('m2', cls, 13, C + '/cores/%s.jsonl' % cls, C + '/cores/%s_ff_*.out' % cls, D + '/comp_%s.jsonl' % cls, C + '/as/%s_p*.status' % cls, D + '/compare_as_%s.json' % cls)
    if not done('as_cores'):
        record('m2', 'comparison with Anghel-Stan', 'skipped: stage as_cores not done'); return
    # Macaulay2 on the cores that only our filters rejected and that Anghel-Stan's code leaves undecided
    with open(D + '/costgt1.jsonl', 'w') as out:
        k = 0
        for cls, lo, X, nexp, rawexp in CLASSES:
            res = json.load(open(D + '/compare_as_%s.json' % cls))
            src = {r['idx']: r['blocks'] for r in jl(C + '/cores/%s.jsonl' % cls)}
            for idx in res['undecided_filter_only']:
                out.write(json.dumps(dict(idx=idx, blocks=src[idx])) + '\n'); k += 1
    record('m2', 'cores rejected by our filters only and undecided by Anghel-Stan (sent to Macaulay2)', k)
    if k:
        par([dict(cmd=[PY, M2COMPB, '13', D + '/costgt1.jsonl', str(p), str(NCPU), '600', D + '/costgt1_comp_%d.jsonl' % p, '10'], out=D + '/costgt1_comp_%d.log' % p, err=D + '/costgt1_comp_%d.err' % p) for p in range(NCPU)], label='Macaulay2 on the filter-only cores')
        st = collections.Counter()
        for p in range(NCPU):
            for r in jl(D + '/costgt1_comp_%d.jsonl' % p): st[r['status']] += 1
        record('m2', 'filter-only cores: Macaulay2 statuses', dict(st))
        expect('m2', 'filter-only cores confirmed non-realisable by Macaulay2', st.get('NONREAL', 0), k)

# ----------------------------------------------------------------------------------------------- extension
def st_ext(cls):
    D = C + '/ext'
    stage = 'ext_' + cls
    comp = C + '/comp/comp_%s.jsonl' % cls
    sh([PY, N17 + '/run/runclass.py', cls, str(NCPU), comp], cwd=D, out=D + '/runclass_%s.log' % cls, err=D + '/runclass_%s.err' % cls)
    txt = open(D + '/runclass_%s.log' % cls).read()
    record(stage, 'runclass log', txt.strip().split('\n'))
    expect(stage, 'worker failures', txt.count('WORKER FAILED'), 0)
    expect(stage, 'components missing a completion record', txt.count('MISSING'), 0)
    expect(stage, 'dim2gen failures', txt.count('DIM2GEN FAILED'), 0)
    expect(stage, 'pipeline finished', 'done; lattice files' in txt, True)
    acc = rej = 0; why = collections.Counter(); comps_done = 0
    for f in glob.glob(D + '/%s_n*_ext_*.jsonl' % cls):
        for r in jl(f):
            if 'L' in r: acc += 1
            if 'L_rejected' in r: rej += 1; why[r['why']] += 1
            if r.get('done') and not r.get('slice'): comps_done += 1
    fam = collections.Counter()
    for f in glob.glob(D + '/%s_n*_fam_*.jsonl' % cls):
        for r in jl(f):
            if 'status' in r and 'comp' in r:
                fam[r['status']] += 1
                acc += len(r.get('generic_L', [])) + len(r.get('special_L', []))
                for x in r.get('rejected', []): rej += 1; why[x['why']] += 1
    record(stage, 'rigid components finished', comps_done)
    record(stage, 'family component statuses', dict(fam))
    record(stage, '17-line lattice records accepted by the window test', acc)
    expect(stage, '17-line lattices rejected by the window test', rej, 0)
    record(stage, 'rejection reasons', dict(why))
    oth = sum(count_lines(f) for f in glob.glob(D + '/%s_other*.jsonl' % cls))
    # the run of October 2026 had exactly two Macaulay2 timeouts, both 14-line children of b51 (MANIFEST.md);
    # they are routed through the lattice-level step by the stage route_timeouts
    expect(stage, 'Macaulay2 timeouts/errors among cores and children', oth, {'b51': 2}.get(cls, 0))
    chs = {}
    for f in sorted(glob.glob(D + '/%s_n*_ch.jsonl' % cls)): chs[os.path.basename(f)] = count_lines(f)
    record(stage, 'children generated at the lattice level', chs)

# ----------------------------------------------------------------------------------------------- as_children
def st_as_children():
    D = C + '/as'
    tot = 0
    for ch in sorted(glob.glob(C + '/ext/*_ch.jsonl')):
        base = os.path.basename(ch)[:-len('_ch.jsonl')]
        n = None
        for r in jl(ch): n = r['n']; break
        if n is None: continue
        tot += count_lines(ch)
        as_jsonl(D, base, n, ch)
        res = compare_as('as_children', base + ' (%d lines)' % n, n, ch, C + '/ext/%s_ff_*.out' % base, C + '/ext/%s_chcomp_*.jsonl' % base, D + '/%s_as_*.status' % base, D + '/compare_%s.json' % base)
        und = res['undecided_filter_only']
        if und:
            src = {str(r['idx']): r['blocks'] for r in jl(ch)}
            uf = D + '/%s_und.jsonl' % base
            with open(uf, 'w') as out:
                for idx in und: out.write(json.dumps(dict(idx=idx, blocks=src[idx])) + '\n')
            par([dict(cmd=[PY, M2COMPB, str(n), uf, str(p), str(NCPU), '600', D + '/%s_und_comp_%d.jsonl' % (base, p), '10'], out=D + '/%s_und_comp_%d.log' % (base, p), err=D + '/%s_und_comp_%d.err' % (base, p)) for p in range(min(NCPU, len(und)))], label=base + ' Macaulay2 on filter-only children')
            st = collections.Counter()
            for p in range(min(NCPU, len(und))):
                for r in jl(D + '/%s_und_comp_%d.jsonl' % (base, p)): st[r['status']] += 1
            expect('as_children', base + ': filter-only children confirmed non-realisable by Macaulay2', st.get('NONREAL', 0), len(und))
    record('as_children', 'children screened', tot)

# ----------------------------------------------------------------------------------------------- indep_rigid
def st_indep_rigid():
    D = C + '/indep_rigid'
    ins = sorted(glob.glob(C + '/ext/*_r0.jsonl'))
    parts = [open(D + '/in_%d.jsonl' % p, 'w') for p in range(NCPU)]
    k = 0
    for f in ins:
        for l in open(f):
            parts[k % NCPU].write(l); k += 1
    for f in parts: f.close()
    record('indep_rigid', 'records with a rigid component', k)
    par([dict(cmd=[PY, D + '/indep_rigid.py', D + '/in_%d.jsonl' % p, D + '/out_%d.jsonl' % p], out=D + '/out_%d.log' % p, err=D + '/out_%d.err' % p) for p in range(NCPU)], label='independent numeric rigid search')
    sh([PY, C + '/compare_indep.py', C + '/ext', D, D + '/compare.json'], out=D + '/compare.out', err=D + '/compare.err')
    res = json.load(open(D + '/compare.json'))
    record('indep_rigid', 'comparison', res)
    expect('indep_rigid', 'rigid components compared', res['compared'], res['exact_components'])
    expect('indep_rigid', 'components whose lattice sets differ', res['differing'], 0)
    expect('indep_rigid', 'numeric realisation not reproducing the core lattice', res['lattice_mismatch'], 0)
    expect('indep_rigid', 'numeric errors', res['errors'], 0)
    record('indep_rigid', 'ambiguous incidences (recomputed in 50 digits)', res['ambiguous'])

# ----------------------------------------------------------------------------------------------- final
def st_final():
    D = C + '/final'
    sh([PY, C + '/collect.py', D, C + '/ext'], out=D + '/collect.out', err=D + '/collect.err')
    col = json.load(open(D + '/collect.json'))
    record('final', 'collection', {k: v for k, v in col.items() if k != 'per_lattice'})
    expect('final', 'distinct 17-line lattices accepted by the window test', col['distinct'], 16)
    expect('final', 'of which among the 16 of work/n17/run/checked_L.jsonl', col['known'], 16)
    expect('final', 'new lattices', col['new'], 0)
    expect('final', 'lattices rejected by the window test (distinct)', col['rejected_distinct'], 0)
    expect('final', 'the 16 known lattices all found', col['known_missing'], 0)
    record('final', 'lattices found per class', col['per_class'])
    nL = col['distinct']
    if nL == 0: return
    todo = D + '/todo_L.jsonl'
    sh([PY, C + '/chains.py', 'window', todo], out=D + '/window.json', err=D + '/window.err')
    w = json.load(open(D + '/window.json'))
    record('final', 'window and 4-chain check of the lattices found', w)
    expect('final', 'lattices found that are window lattices with phi_max = 4 and a 4-chain', w['window_with_4chain'], nL)
    P = min(NCPU, nL)
    par([dict(cmd=[PY, EXACT, '17', '8', todo, str(p), str(P)], cwd=D, out=D + '/exact_%d.log' % p, err=D + '/exact_%d.err' % p) for p in range(P)], label='exact_tc_lattice on the lattices found')
    verdicts = {}
    for p in range(P):
        cur = None
        for l in open(D + '/todo_L_tc_%d.out' % p):
            if l.startswith('LATTICE'):
                cur = int(l.split()[1]); verdicts[cur] = [l.strip()]
            elif l.strip().startswith('COMP') and cur is not None: verdicts[cur].append(l.strip())
            elif l.startswith('ERROR'): verdicts.setdefault('ERROR', []).append(l.strip())
    record('final', 'exact_tc_lattice verdicts', verdicts)
    nonfree = sum(1 for k, v in verdicts.items() if k != 'ERROR' and len(v) >= 2 and all('NONFREE' in c for c in v[1:]))
    expect('final', 'lattices with every component NONFREE (exact_tc_lattice)', nonfree, nL)
    expect('final', 'lattices with a FREE or MIXED component', sum(1 for k, v in verdicts.items() if k != 'ERROR' and any((' FREE' in c and 'NONFREE' not in c) or 'MIXED' in c for c in v[1:])), 0)
    expect('final', 'exact_tc_lattice errors', len(verdicts.get('ERROR', [])), 0)
    par([dict(cmd=[PY, M2COMPB, '17', todo, str(p), str(P), '1800', D + '/L_comp_%d.jsonl' % p, '1'], out=D + '/L_comp_%d.log' % p, err=D + '/L_comp_%d.err' % p) for p in range(P)], label='Macaulay2 components of the lattices found')
    with open(D + '/L_comp.jsonl', 'w') as out:
        for p in range(P):
            for l in open(D + '/L_comp_%d.jsonl' % p): out.write(l)
    par([dict(cmd=[PY, C + '/freecheck.py', D + '/L_comp.jsonl', str(p), str(P), D + '/freecheck_%d.jsonl' % p], out=D + '/freecheck_%d.log' % p, err=D + '/freecheck_%d.err' % p) for p in range(P)], label='syzygy degrees over the field of definition')
    fc = {}
    for p in range(P):
        for r in jl(D + '/freecheck_%d.jsonl' % p): fc[str(r['idx'])] = r
    record('final', 'freecheck (Macaulay2: realisation over K, lattice reproduced, minimal syzygy degrees)', {k: dict(lattice_ok=v.get('lattice_ok'), degrees=v.get('degrees'), field=v.get('field'), free=v.get('free'), error=v.get('error')) for k, v in fc.items()})
    expect('final', 'freecheck: realisations reproduce their lattice', sum(1 for v in fc.values() if v.get('lattice_ok')), nL)
    expect('final', 'freecheck: non-free with minimal syzygy degrees (7, 10, 10)', sum(1 for v in fc.values() if v.get('lattice_ok') and v.get('free') is False and sorted(v.get('degrees') or []) == [7, 10, 10]), nL)
    expect('final', 'freecheck: free realisations', sum(1 for v in fc.values() if v.get('free')), 0)
    sh([PY, C + '/as_recertify.py', todo, D + '/as_recertify.jsonl'], out=D + '/as_recertify.out', err=D + '/as_recertify.err')
    asr = {str(r['idx']): r for r in jl(D + '/as_recertify.jsonl')}
    record('final', 'Anghel-Stan re-certification', {k: dict(status=v['status'], comps=v.get('comps')) for k, v in asr.items()})
    expect('final', 'Anghel-Stan: lattices realisable with every component certified nonfree', sum(1 for v in asr.values() if v['status'] in ('points', 'family-point') and v.get('comps') and all(c[1] == 'nonfree' for c in v['comps'])), nL)

# ----------------------------------------------------------------------------------------------- report
def st_report():
    sh([PY, C + '/report.py'], out=C + '/report.log', err=C + '/report.err')
    record('report', 'written', C + '/REPORT.md')

# ----------------------------------------------------------------------------------------------- route_timeouts
def st_route_timeouts():
    """Cores or children on which Macaulay2 timed out or failed (recorded by runclass.py in *_other*.jsonl) are
    routed through the lattice-level step, exactly as in the run of October 2026 (MANIFEST.md:
    runclass.py b51to2 2 --n=14 b51_to2_forced.jsonl); their children are screened with Anghel-Stan's code too."""
    D = C + '/ext'; stage = 'route_timeouts'
    sys.path.insert(0, N17 + '/validate')
    from canon import canon_many
    todo = {}
    for f in sorted(glob.glob(D + '/*_other*.jsonl')):
        base = os.path.basename(f)[:-len('.jsonl')]
        cls, rest = base.split('_other', 1)
        if 'to2' in cls: continue
        n = int(rest[2:]) if rest.startswith('_n') else 13
        for r in jl(f):
            if r.get('status') in ('REAL', 'NONREAL'): continue
            todo.setdefault((cls, n), []).append(r)
    record(stage, 'Macaulay2 timeouts/errors to route', {'%s n=%d' % k: len(v) for k, v in todo.items()})
    expect(stage, 'timeouts/errors outside b51 at 14 lines', sum(len(v) for k, v in todo.items() if k != ('b51', 14)), 0)
    orig = [json.loads(l) for l in open(N17 + '/run/b51_to2_forced.jsonl')]
    ours = todo.get(('b51', 14), [])
    same = bool(ours) and set(canon_many(14, [r['blocks'] for r in orig])) == set(canon_many(14, [r['blocks'] for r in ours]))
    expect(stage, 'the b51 timeouts are the same two 14-line lattices as in October 2026', same, True)
    tot_children = 0
    for (cls, n), recs in sorted(todo.items()):
        tag = '%sto2' % cls if n == 14 else '%sto2n%d' % (cls, n)
        forced = D + '/%s_forced.jsonl' % tag
        with open(forced, 'w') as out:
            for r in recs:
                out.write(json.dumps(dict(idx=r['idx'], blocks=r['blocks'], status='REAL', comps=[dict(dim=2, degree=0, gens='forced lattice-level step (Macaulay2 %s)' % r.get('status'))])) + '\n')
        sh([PY, N17 + '/run/runclass.py', tag, str(min(NCPU, len(recs))), '--n=%d' % n, forced], cwd=D, out=D + '/runclass_%s.log' % tag, err=D + '/runclass_%s.err' % tag)
        txt = open(D + '/runclass_%s.log' % tag).read()
        record(stage, tag + ' runclass log', txt.strip().split('\n'))
        expect(stage, tag + ' worker failures', txt.count('WORKER FAILED'), 0)
        expect(stage, tag + ' components missing a completion record', txt.count('MISSING'), 0)
        expect(stage, tag + ' dim2gen failures', txt.count('DIM2GEN FAILED'), 0)
        expect(stage, tag + ' pipeline finished', 'done; lattice files' in txt, True)
        acc = rej = 0; why = collections.Counter()
        for f in glob.glob(D + '/%s_n*_ext_*.jsonl' % tag):
            for r in jl(f):
                if 'L' in r: acc += 1
                if 'L_rejected' in r: rej += 1; why[r['why']] += 1
        for f in glob.glob(D + '/%s_n*_fam_*.jsonl' % tag):
            for r in jl(f):
                if 'status' in r and 'comp' in r:
                    acc += len(r.get('generic_L', [])) + len(r.get('special_L', []))
                    for x in r.get('rejected', []): rej += 1; why[x['why']] += 1
        record(stage, tag + ' 17-line lattice records accepted by the window test', acc)
        expect(stage, tag + ' 17-line lattices rejected by the window test', rej, 0)
        record(stage, tag + ' rejection reasons', dict(why))
        oth = sum(count_lines(f) for f in glob.glob(D + '/%s_other*.jsonl' % tag))
        expect(stage, tag + ' Macaulay2 timeouts/errors among the routed children', oth, 0)
        chs = {}
        for f in sorted(glob.glob(D + '/%s_n*_ch.jsonl' % tag)): chs[os.path.basename(f)] = count_lines(f)
        record(stage, tag + ' children generated at the lattice level', chs)
        for ch in sorted(glob.glob(D + '/%s_n*_ch.jsonl' % tag)):
            base = os.path.basename(ch)[:-len('_ch.jsonl')]
            m = None
            for r in jl(ch): m = r['n']; break
            if m is None: continue
            tot_children += count_lines(ch)
            as_jsonl(C + '/as', base, m, ch)
            res = compare_as(stage, base + ' (%d lines)' % m, m, ch, D + '/%s_ff_*.out' % base, D + '/%s_chcomp_*.jsonl' % base, C + '/as/%s_as_*.status' % base, C + '/as/compare_%s.json' % base)
            und = res['undecided_filter_only']
            if und:
                src = {str(r['idx']): r['blocks'] for r in jl(ch)}
                uf = C + '/as/%s_und.jsonl' % base
                with open(uf, 'w') as out:
                    for idx in und: out.write(json.dumps(dict(idx=idx, blocks=src[idx])) + '\n')
                k = min(NCPU, len(und))
                par([dict(cmd=[PY, M2COMPB, str(m), uf, str(q), str(k), '600', C + '/as/%s_und_comp_%d.jsonl' % (base, q), '10'], out=C + '/as/%s_und_comp_%d.log' % (base, q), err=C + '/as/%s_und_comp_%d.err' % (base, q)) for q in range(k)], label=base + ' Macaulay2 on filter-only children')
                st = collections.Counter()
                for q in range(k):
                    for r in jl(C + '/as/%s_und_comp_%d.jsonl' % (base, q)): st[r['status']] += 1
                expect(stage, base + ': filter-only children confirmed non-realisable by Macaulay2', st.get('NONREAL', 0), len(und))
    record(stage, 'children of the routed records screened by Anghel-Stan', tot_children)

STAGES = [('prep', st_prep, []), ('cover', st_cover, ['prep']), ('n8zero', st_n8zero, ['prep']), ('cores', st_cores, ['prep']),
          ('indep_cores', st_indep_cores, ['cores']), ('filters', st_filters, ['cores']), ('as_cores', st_as_cores, ['cores']),
          ('m2', st_m2, ['filters'])] + \
         [('ext_' + c, (lambda c=c: st_ext(c)), ['m2']) for c in ['b48', 'b48w', 'b49', 'b50', 'b51']] + \
         [('route_timeouts', st_route_timeouts, ['ext_b51']),
          ('as_children', st_as_children, ['ext_b48']), ('indep_rigid', st_indep_rigid, ['ext_b48']),
          ('final', st_final, ['ext_b48']), ('report', st_report, [])]

if __name__ == '__main__':
    wanted = sys.argv[1:] or [s for s, _, _ in STAGES]
    log('===== campaign start: stages %s (NCPU %d)' % (' '.join(wanted), NCPU))
    skipped = set()
    for name, fn, deps in STAGES:
        if name not in wanted: continue
        if done(name): log('stage %s already done, skipping' % name); continue
        stop_check()
        bad = [d for d in deps if not done(d)]
        if bad:
            log('stage %s SKIPPED: dependencies not done: %s' % (name, bad)); skipped.add(name); continue
        if failed(name): os.remove(C + '/done/%s.FAILED' % name)
        log('===== stage %s start' % name); t0 = time.time()
        try:
            fn(); mark(name, t0)
        except SystemExit: raise
        except Exception as e:
            log('***** stage %s FAILED after %.0f s: %r' % (name, time.time() - t0, e))
            log(traceback.format_exc())
            RESULTS.setdefault(name, {})['_error'] = repr(e)
            json.dump(RESULTS.get(name, {}), open(C + '/done/%s.FAILED' % name, 'w'), indent=1)
            if name == 'report': pass
    log('===== campaign end')
