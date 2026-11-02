#!/bin/bash
# second family pass: every component not settled in pass 1 (SLOW / NOMODEL / EXC ...), 1800 s limit, 200 plane-model tries
cd /Users/agent/Projects/TC17/work/n17/audit/ext
PY=/Users/agent/Projects/TC17/.venv/bin/python
until [ "$(for f in out/fam_*_family.jsonl; do tail -1 $f | grep -c ALLDONE; done | paste -sd+ - | bc)" -ge 300 ]; do sleep 30; done
$PY - <<'PY'
import json, glob, collections
notok = set()
for f in glob.glob('out/fam_*_family.jsonl'):
    for l in open(f):
        r = json.loads(l)
        if r.get('kind') == 'family' and r['status'] != 'OK': notok.add(str(r['idx']))
recs = []
for f in sorted(glob.glob('in/fam_*.jsonl')):
    for l in open(f):
        if str(json.loads(l)['idx']) in notok: recs.append(l)
mkdir = __import__('os').makedirs; mkdir('in2', exist_ok=True); mkdir('out2', exist_ok=True)
for k in range(len(recs)):
    open('in2/p2_%03d.jsonl' % k, 'w').write(recs[k])
print('pass 2 records', len(recs))
PY
echo 4 > MAXJOBS2
export EXTAUDIT_TRIES=200
ls in2/p2_*.jsonl | xargs -n 1 -P 4 -I{} sh -c 'b=$(basename {} .jsonl); nice -n 3 '$PY' extaudit.py {} out2/${b}_family.jsonl family 1800 > /dev/null 2> out2/${b}.err'
echo "PASS2 DONE $(date)"
