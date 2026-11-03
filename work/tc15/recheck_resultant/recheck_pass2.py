"""Re-run the corrected second pass on every lattice that the original second pass rejected with
'NONREAL res2'.  usage: recheck_pass2.py prefix parts out.jsonl   (prefix = .../defer_n15_7_7_part)"""
import sys, json, time, flint
ARGV = list(sys.argv)
sys.argv = ['x', ARGV[1]]          # n for fast_real_fix
sys.path.insert(0, '/private/tmp/claude-502/-Users-agent-Projects-TeraoHunter/ef50d01d-f066-4ad9-b062-74af46b2f798/scratchpad')
import fast_real_fix as fx
prefix, parts, OUT = ARGV[2], int(ARGV[3]), ARGV[4]
ctx3 = flint.fmpz_mpoly_ctx.get(('u0', 'u1', 'u2')); gens3 = ctx3.gens()
stats = {}; t0 = time.time(); n = 0
with open(OUT, 'w') as out:
    for p in range(parts):
        want = {}
        for l in open('%s%02d_pass2.out' % (prefix, p)):
            s = l.split()
            if len(s) >= 3 and s[1] == 'NONREAL' and s[2] == 'res2':
                want[int(s[0])] = True
        for i, line in enumerate(open('%s%02d.jsonl' % (prefix, p))):
            rec = json.loads(line)
            if rec.get('idx', i) not in want:
                continue
            v = fx.classify2_fixed(rec['blocks'], 'res-nonconst', ctx3, gens3)
            stats[v] = stats.get(v, 0) + 1
            out.write(json.dumps(dict(part=p, i=i, idx=rec.get('idx'), verdict=v, blocks=rec['blocks'])) + '\n')
            n += 1
            if n % 20000 == 0:
                print(n, stats, '(%.0fs)' % (time.time() - t0), flush=True)
print('DONE', n, stats, '(%.0fs)' % (time.time() - t0), flush=True)
