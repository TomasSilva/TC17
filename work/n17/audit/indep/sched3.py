"""Run indep_rigid.py on each rigid input file, at most K at a time (K re-read from MAXJOBS)."""
import sys, os, subprocess, time, glob
D = os.path.dirname(os.path.abspath(__file__))
PY = '/Users/agent/Projects/TC17/.venv/bin/python'
ins = sorted(glob.glob('/Users/agent/Projects/TC17/work/n17/audit/ext/in/rig_*.jsonl'))
log = open(os.path.join(D, 'sched3.log'), 'a')
def maxjobs():
    try: return int(open(os.path.join(D, 'MAXJOBS')).read().strip())
    except Exception: return 2
def finished(p):
    if not os.path.exists(p): return False
    last = ''
    for last in open(p): pass
    return 'ALLDONE' in last
todo = [(i, os.path.join(D, 'out', os.path.basename(i))) for i in ins]
todo = [t for t in todo if not finished(t[1])]
running = {}
print(time.strftime('%d %H:%M:%S'), 'start', len(todo), file=log, flush=True)
while todo or running:
    for j, p in list(running.items()):
        if p.poll() is not None:
            print(time.strftime('%d %H:%M:%S'), 'end', j, p.returncode, file=log, flush=True); del running[j]
    while todo and len(running) < maxjobs():
        i, o = todo.pop(0)
        running[i] = subprocess.Popen(['nice', '-n', '3', PY, os.path.join(D, 'indep_rigid.py'), i, o], stdout=subprocess.DEVNULL, stderr=open(o + '.err', 'a'))
        print(time.strftime('%d %H:%M:%S'), 'start', i, file=log, flush=True)
    time.sleep(3)
print(time.strftime('%d %H:%M:%S'), 'ALL DONE', file=log, flush=True)
