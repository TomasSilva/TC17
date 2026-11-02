"""Exact Terao check (work/tc15/exact_tc_lattice.py, n = 17, d1 = 8) of every lattice in todo_L.jsonl,
one Macaulay2 run per lattice; verdicts appended to checked_L.jsonl.
Verdict: NONREAL, or the list of components with dimension, degree, FREE/NONFREE (dim 0) or generic
freeness and whether the non-free locus lies in the degeneracy locus (dim > 0).  A counterexample is a
lattice with a FREE and a NONFREE component, or a MIXED component."""
import sys, json, subprocess, os, time
sys.argv_s = list(sys.argv); sys.argv = ['x', '17', '8', '/dev/null', '0', '1']
sys.path.insert(0, '/Users/agent/Projects/TC17/work/tc15')
import exact_tc_lattice as ex
sys.argv = sys.argv_s
TO = int(sys.argv[1]) if len(sys.argv) > 1 else 1800
with open('checked_L.jsonl', 'a') as out:
    for l in open('todo_L.jsonl'):
        r = json.loads(l)
        path = 'chk_%d.m2' % os.getpid()
        open(path, 'w').write(ex.m2_script([(r['idx'], [b for b in r['blocks'] if len(b) >= 3])]))
        t0 = time.time()
        try:
            p = subprocess.run([ex.M2, '--script', path], capture_output=True, text=True, timeout=TO)
            o = p.stdout
            v = 'ERROR' if 'DONE' not in o else ' | '.join(x.strip() for x in o.split('\n') if x.strip().startswith(('LATTICE', 'COMP')))
        except subprocess.TimeoutExpired:
            v = 'TIMEOUT'
        os.remove(path)
        comps = [x for x in v.split(' | ') if x.startswith('COMP')]
        free = any(' FREE' in c and 'NONFREE' not in c and 'dim 0' in c for c in comps)
        nonfree = any('NONFREE' in c for c in comps)
        mixed = any('MIXED' in c for c in comps)
        genfree = any('generic FREE' in c for c in comps)
        cex = mixed or (nonfree and (free or genfree))
        rec = dict(canon=r['canon'], known=r.get('known'), verdict=v, counterexample=cex, time=round(time.time() - t0, 1), blocks=r['blocks'])
        out.write(json.dumps(rec) + '\n'); out.flush()
        print(r['idx'], r.get('known'), 'CEX' if cex else 'ok', v[:150], flush=True)
