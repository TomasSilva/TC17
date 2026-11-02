"""Full re-run of the exact realisability filters with the corrected two-parameter branch.
usage: full_recheck.py n lattices.jsonl part nparts outprefix
Every lattice with index i = part (mod nparts) is classified by the corrected first pass
(classify_fixed) and, if deferred, by the corrected second pass (classify2_fixed); one verdict line
per lattice goes to outprefix.out, the lattices still deferred go to outprefix_defer.jsonl (for
Macaulay2), and the final tallies are printed."""
import sys, json, time, os
ARGV = list(sys.argv)
n, IN, part, nparts, PREF = ARGV[1], ARGV[2], int(ARGV[3]), int(ARGV[4]), ARGV[5]
sys.argv = ['x', n]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flint
import fast_real_fix as fx

ctx3 = flint.fmpz_mpoly_ctx.get(('u0', 'u1', 'u2')); gens3 = ctx3.gens()
stats = {}
t0 = time.time()
cnt = 0
with open(IN) as f, open(PREF + '.out', 'w') as out, open(PREF + '_defer.jsonl', 'w') as dfr:
    for i, line in enumerate(f):
        if i % nparts != part:
            continue
        rec = json.loads(line)
        try:
            v = fx.classify_fixed(rec['blocks'], ctx3, gens3)
            if v.startswith('DEFER') and v != 'DEFER nvar>=3':
                v2 = fx.classify2_fixed(rec['blocks'], v[6:], ctx3, gens3)
                v = v + ' | ' + v2
                final = v2
            else:
                final = v
        except Exception as e:
            v = 'DEFER error %s' % type(e).__name__
            final = v
        stats[final] = stats.get(final, 0) + 1
        out.write('%d %s\n' % (i, v))
        if final.startswith('DEFER'):
            dfr.write(json.dumps(dict(idx=i, blocks=rec['blocks'], verdict=v)) + '\n')
        cnt += 1
        if cnt % 50000 == 0:
            print(i, cnt, stats, '(%.0fs)' % (time.time() - t0), flush=True)
    out.write('ALLDONE\n')
print('FINAL part %d of %d: %d lattices %s (%.0fs)' % (part, nparts, cnt, stats, time.time() - t0), flush=True)
