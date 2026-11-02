"""One runner for both retry sets (retry/: the 17 components not covered by the lattice-level step,
retry/2: the 93 covered ones).  A component is settled when one of its attempts ends with status OK.
At most MAXATT attempts each; at most 10 extaudit workers on the whole machine (running ones counted)."""
import glob, os, subprocess, json, time
PY = '/Users/agent/Projects/TC17/.venv/bin/python'
EXT = '/Users/agent/Projects/TC17/work/n17/audit/ext/extaudit.py'
D = '/Users/agent/Projects/TC17/work/n17/audit/ext/'
SETS = [(D + 'retry', 10), (D + 'retry2', 6)]
def status(o):
    if not os.path.exists(o): return None
    for l in open(o):
        try: r = json.loads(l)
        except Exception: continue
        if r.get('kind') == 'family': return r['status']
    return None
def atts(d, r): return sorted(glob.glob(os.path.join(d, os.path.basename(r).replace('rec_', 'att_').replace('.jsonl', '_*.jsonl'))))
def busy():
    out = subprocess.run(['ps', '-eo', 'args'], capture_output=True, text=True).stdout
    names = set(); n = 0
    for l in out.split('\n'):
        if 'MacOS/Python' in l and 'extaudit.py' in l:
            n += 1
            for t in l.split():
                if os.path.basename(t).startswith('rec_'): names.add(os.path.basename(t))
    return n, names
log = open(D + 'retry_all.log', 'a')
while True:
    n, names = busy()
    todo = []
    for d, mx in SETS:
        for r in sorted(glob.glob(os.path.join(d, 'rec_*.jsonl'))):
            a = atts(d, r)
            if any(status(o) == 'OK' for o in a) or os.path.basename(r) in names: continue
            if len(a) < mx: todo.append((d, r, len(a) + 1))
    if not todo and n == 0: break
    for d, r, k in todo:
        if busy()[0] >= 10: break
        o = os.path.join(d, os.path.basename(r).replace('rec_', 'att_').replace('.jsonl', '_%d.jsonl' % k))
        subprocess.Popen(['nice', '-n', '3', PY, EXT, os.path.basename(r), os.path.basename(o), 'family', '400'], cwd=d,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(time.strftime('%H:%M:%S'), 'start', os.path.basename(o), file=log, flush=True)
        time.sleep(2)
    time.sleep(10)
summary = {}
for d, mx in SETS:
    for r in sorted(glob.glob(os.path.join(d, 'rec_*.jsonl'))):
        a = atts(d, r); summary[os.path.basename(r)] = (any(status(o) == 'OK' for o in a), len(a))
print(time.strftime('%H:%M:%S'), 'DONE settled %d of %d' % (sum(v[0] for v in summary.values()), len(summary)), json.dumps(summary), file=log, flush=True)
