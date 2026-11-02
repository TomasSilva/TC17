"""Pass-2 scheduler: keep MAXJOBS2 extaudit workers busy on the unsettled family components (counting
workers already running), 1800 s family limit, 200 plane-model trials."""
import os, subprocess, time, glob
D = os.path.dirname(os.path.abspath(__file__))
PY = '/Users/agent/Projects/TC17/.venv/bin/python'
env = dict(os.environ, EXTAUDIT_TRIES='200')
def finished(f):
    o = os.path.join(D, 'out2', os.path.basename(f).replace('.jsonl', '_family.jsonl'))
    if not os.path.exists(o): return False
    last = ''
    for last in open(o): pass
    return 'ALLDONE' in last
def running_files():
    out = subprocess.run(['ps', '-eo', 'args'], capture_output=True, text=True).stdout
    fs = set()
    for l in out.split('\n'):
        if 'MacOS/Python' in l and 'extaudit.py' in l and 'p2_' in l:
            for tok in l.split():
                if 'in2/p2_' in tok: fs.add(os.path.basename(tok))
    return fs
busy = running_files()
todo = [f for f in sorted(glob.glob(os.path.join(D, 'in2/p2_*.jsonl'))) if not finished(f) and os.path.basename(f) not in busy]
log = open(os.path.join(D, 'sched_p2.log'), 'a')
def maxjobs():
    try: return int(open(os.path.join(D, 'MAXJOBS2')).read().strip())
    except Exception: return 10
def nrunning():
    return len(running_files())
print(time.strftime('%d %H:%M:%S'), 'start, to do', len(todo), file=log, flush=True)
procs = []
while todo or any(p.poll() is None for p in procs) or nrunning():
    while todo and nrunning() < maxjobs():
        f = todo.pop(0); b = os.path.basename(f).replace('.jsonl', '')
        o = os.path.join(D, 'out2', b + '_family.jsonl')
        procs.append(subprocess.Popen(['nice', '-n', '3', PY, os.path.join(D, 'extaudit.py'), f, o, 'family', '1800'],
                                      cwd=D, env=env, stdout=subprocess.DEVNULL, stderr=open(o + '.err', 'a')))
        print(time.strftime('%d %H:%M:%S'), 'start', b, file=log, flush=True)
        time.sleep(2)
    time.sleep(5)
print(time.strftime('%d %H:%M:%S'), 'ALL DONE', file=log, flush=True)
