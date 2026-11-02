"""Run exact_tc_lattice's Macaulay2 script one lattice at a time with a timeout.
usage: m2single.py n d1 lattices.jsonl out_file timeout idx1 idx2 ...   (idx = line numbers in the jsonl)"""
import sys, json, subprocess, os, time
n, d1, IN, OUT, TO = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
idxs = [int(x) for x in sys.argv[6:]]
sys.argv = ['x', n, d1, IN, '0', '1']
sys.path.insert(0, '/Users/agent/Projects/TC17/work/tc15')
import exact_tc_lattice as ex
recs = [json.loads(l) for l in open(IN)]
with open(OUT, 'a') as out:
    for i in idxs:
        path = OUT + '.%d.m2' % i
        open(path, 'w').write(ex.m2_script([(i, recs[i]['blocks'])]))
        t0 = time.time()
        try:
            r = subprocess.run([ex.M2, '--script', path], capture_output=True, text=True, timeout=TO)
            txt = r.stdout if 'DONE' in r.stdout else r.stdout + 'ERROR %d\n' % i
        except subprocess.TimeoutExpired:
            txt = 'LATTICE %d TIMEOUT %ds\n' % (i, TO)
        out.write(txt); out.flush()
        os.remove(path)
        print(i, '%.0fs' % (time.time() - t0), txt.strip().split('\n')[0][:80], flush=True)
