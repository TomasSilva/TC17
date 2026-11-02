#!/bin/bash
cd /Users/agent/Projects/TC17/work/n17/audit/dim2gen
R=/Users/agent/Projects/TC17/work/n17/run
PY=/Users/agent/Projects/TC17/.venv/bin/python
for b in b49d2n15_n15 b49slow_n13 b50_n13 b50_n14 b50_n15 b50slow13_n13 b50slow13_n14 b50slow13_n15 b50slow14_n14 b50slow14_n15 b50slow15_n15 b51_n13 b51_n14 b51to2_n14; do
  $PY /Users/agent/Projects/TC17/work/n17/comp/dim2gen.py $R/${b}_r2.jsonl ${b}_ch.jsonl 2> ${b}.log
  $PY - $b <<'PY'
import sys, json
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/validate')
from canon import canon_many
b = sys.argv[1]; R = '/Users/agent/Projects/TC17/work/n17/run/'
def cs(f):
    recs = [json.loads(l) for l in open(f)]
    out = set()
    for n in set(r['n'] for r in recs):
        out |= set(canon_many(n, [r['blocks'] for r in recs if r['n'] == n]))
    return out
a, c = cs(R + b + '_ch.jsonl'), cs(b + '_ch.jsonl')
print(b, 'original', len(a), 'regenerated', len(c), 'identical', a == c, flush=True)
PY
done
$PY /Users/agent/Projects/TC17/work/n17/comp/dim2gen.py $R/dim2_b4849.jsonl dim2_b4849_ch.jsonl 2> dim2_b4849.log
$PY /Users/agent/Projects/TC17/work/n17/comp/dim2gen.py $R/d2c_dim2.jsonl d2c_dim2_ch.jsonl 2> d2c_dim2.log
echo ALLDONE
