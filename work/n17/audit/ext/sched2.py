"""Run extaudit.py on each job (input file + kind), at most K at a time (K re-read from MAXJOBS)."""
import sys, os, subprocess, time
D = os.path.dirname(os.path.abspath(__file__))
PY = '/Users/agent/Projects/TC17/.venv/bin/python'
jobs = [l.split() for l in open(sys.argv[1]) if l.strip()]
extra = sys.argv[2:]
log = open(os.path.join(D, 'sched2.log'), 'a')
def maxjobs():
    try: return int(open(os.path.join(D, 'MAXJOBS')).read().strip())
    except Exception: return 2
def finished(outp):
    if not os.path.exists(outp): return False
    with open(outp) as f:
        for l in f: pass
    return '"ALLDONE"' in l if 'l' in dir() else False
todo = []
for inp, kind in jobs:
    outp = os.path.join(D, 'out', os.path.basename(inp).replace('.jsonl', '_' + kind + '.jsonl'))
    if not finished(outp): todo.append((inp, kind, outp))
running = {}
print(time.strftime('%d %H:%M:%S'), 'start: %d jobs, %d to do' % (len(jobs), len(todo)), file=log, flush=True)
while todo or running:
    for j, p in list(running.items()):
        if p.poll() is not None:
            print(time.strftime('%d %H:%M:%S'), 'end', j, 'rc', p.returncode, file=log, flush=True)
            del running[j]
    while todo and len(running) < maxjobs():
        inp, kind, outp = todo.pop(0)
        cmd = ['nice', '-n', '3', PY, os.path.join(D, 'extaudit.py'), os.path.join(D, inp), outp, kind] + extra
        running[inp] = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=open(outp + '.err', 'a'))
        print(time.strftime('%d %H:%M:%S'), 'start', inp, kind, file=log, flush=True)
    time.sleep(3)
print(time.strftime('%d %H:%M:%S'), 'ALL DONE', file=log, flush=True)
