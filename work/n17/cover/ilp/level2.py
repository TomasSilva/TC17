"""Level 2: for each level-1 survivor (fixed deltas), the 0/1 problem in e (double points) and tau (full
triple points) of gamma_ilp.build, solved with glpsol.  Prints FEASIBLE / INFEASIBLE / UNDECIDED per case."""
import sys, subprocess, os
from gamma_ilp import vectors, write_lp
from level1 import survivors
part, nparts = int(sys.argv[1]), int(sys.argv[2])
tlim = int(sys.argv[3]) if len(sys.argv) > 3 else 120
cases = []
for k in vectors():
    for Delta, chosen in survivors(k):
        cases.append((k, Delta, chosen))
os.makedirs('l2', exist_ok=True)
for idx, (k, Delta, chosen) in enumerate(cases):
    if idx % nparts != part: continue
    deltas = [d for tup in chosen for d in tup]
    def extra(k_, g, y, e, t, Dl, deltas=deltas):
        return [('%s' % y(X, deltas[X]), '=', 1) for X in range(16)]
    path = 'l2/c%d.lp' % idx
    write_lp(k, path, extra)
    r = subprocess.run(['glpsol', '--lp', path, '--tmlim', str(tlim), '-o', path + '.sol'], capture_output=True, text=True)
    out = r.stdout
    if 'PROBLEM HAS NO PRIMAL FEASIBLE SOLUTION' in out or 'PROBLEM HAS NO INTEGER FEASIBLE SOLUTION' in out or 'LP HAS NO PRIMAL FEASIBLE SOLUTION' in out:
        st = 'INFEASIBLE'
    elif 'INTEGER OPTIMAL SOLUTION FOUND' in out or 'OPTIMAL SOLUTION FOUND' in out and 'INTEGER' in out:
        st = 'FEASIBLE'
    elif 'TIME LIMIT EXCEEDED' in out:
        st = 'UNDECIDED'
    else:
        st = 'OTHER'
    print(idx, ''.join(map(str, k)), Delta, chosen, st, flush=True)
    if st == 'INFEASIBLE':
        os.remove(path); os.remove(path + '.sol')
