"""Run one pipeline_fix.py process per chunk, at most K at a time; K is re-read from the file MAXJOBS
whenever a slot frees up, so the concurrency can be changed while the campaign runs.
usage: sched.py joblist.txt   (one chunk base name per line, largest first)"""
import sys, os, subprocess, time
D = os.path.dirname(os.path.abspath(__file__))
PY = '/Users/agent/Projects/TC17/.venv/bin/python'
BB = '/Users/agent/Projects/TC17/work/tc15/bb_n17/'
OUT = os.path.join(D, 'out')
jobs = [l.strip() for l in open(sys.argv[1]) if l.strip()]
todo = [j for j in jobs if not os.path.exists(os.path.join(OUT, 'done_%s.json' % j))]
log = open(os.path.join(D, 'sched.log'), 'a')
def maxjobs():
    try: return int(open(os.path.join(D, 'MAXJOBS')).read().strip())
    except Exception: return 4
running = {}
print(time.strftime('%d %H:%M:%S'), 'start: %d jobs, %d to do' % (len(jobs), len(todo)), file=log, flush=True)
while todo or running:
    for j, p in list(running.items()):
        if p.poll() is not None:
            print(time.strftime('%d %H:%M:%S'), 'end', j, 'rc', p.returncode, file=log, flush=True)
            del running[j]
    while todo and len(running) < maxjobs():
        j = todo.pop(0)
        cmd = ['nice', '-n', '5', PY, os.path.join(D, 'pipeline_fix.py'), '17', '9', '10', '6', 'n17fix', '1:8:8',
               BB + j + '.jsonl.gz', '--workers', '1', '--outdir', OUT]
        running[j] = subprocess.Popen(cmd, stdout=open(os.path.join(OUT, j + '.log'), 'a'), stderr=subprocess.STDOUT)
        print(time.strftime('%d %H:%M:%S'), 'start', j, file=log, flush=True)
    time.sleep(5)
print(time.strftime('%d %H:%M:%S'), 'ALL DONE', file=log, flush=True)
