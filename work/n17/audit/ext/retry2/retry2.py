"""(retry2: the 93 unsettled components covered by the lattice-level step; uses the cores left free) Retry the family method with fresh random plane models (one attempt = one extaudit run, 400 s limit)
until each component is settled (status OK), at most 10 attempts, 10 attempts in parallel."""
import glob, os, subprocess, json, time
PY = '/Users/agent/Projects/TC17/.venv/bin/python'
EXT = '/Users/agent/Projects/TC17/work/n17/audit/ext/extaudit.py'
recs = sorted(glob.glob('rec_*.jsonl'))
def status(o):
    if not os.path.exists(o): return None
    for l in open(o):
        r = json.loads(l)
        if r.get('kind') == 'family': return r['status']
    return None
def settled(r):
    return any(status(o) == 'OK' for o in glob.glob(r.replace('rec_', 'att_').replace('.jsonl', '_*.jsonl')))
attempt = {r: 0 for r in recs}; running = {}
def slots():
    # free cores: 10 minus every extaudit worker on the machine (own ones included)
    out = subprocess.run(['ps', '-eo', 'args'], capture_output=True, text=True).stdout
    alln = sum(1 for l in out.split('\n') if 'MacOS/Python' in l and 'extaudit.py' in l)
    return max(0, 10 - alln)
log = open('retry.log', 'a')
while True:
    for r, p in list(running.items()):
        if p.poll() is not None:
            del running[r]
            print(time.strftime('%H:%M:%S'), os.path.basename(r), 'attempt', attempt[r], '->', status(r.replace('rec_', 'att_').replace('.jsonl', '_%d.jsonl' % attempt[r])), file=log, flush=True)
    todo = [r for r in recs if r not in running and not settled(r) and attempt[r] < 6]
    if not todo and not running: break
    for r in todo:
        if slots() <= 0: break
        attempt[r] += 1
        o = r.replace('rec_', 'att_').replace('.jsonl', '_%d.jsonl' % attempt[r])
        time.sleep(2)
        running[r] = subprocess.Popen(['nice', '-n', '3', PY, EXT, r, o, 'family', '400'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)
print(time.strftime('%H:%M:%S'), 'DONE', {os.path.basename(r): (settled(r), attempt[r]) for r in recs}, file=log, flush=True)
