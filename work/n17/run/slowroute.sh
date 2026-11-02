#!/bin/bash
# route family records that were slow or failed (status SLOW/EXC/NOMODEL/LATTICE-MISMATCH/SPECIAL-ERROR)
# through the lattice-level step: TAG = name, N = number of lines of these records, then the family output files
cd /Users/agent/Projects/TC17/work/n17/run
PY=/Users/agent/Projects/TC17/.venv/bin/python
TAG=$1; N=$2; INPUTREC=$3; shift 3
$PY - "$INPUTREC" "$@" > ${TAG}_slowrecs.jsonl <<'PYEOF'
import sys, json
recs = {}
for l in open(sys.argv[1]):
    r = json.loads(l); recs[str(r['idx'])] = r
bad = set()
for f in sys.argv[2:]:
    for l in open(f):
        try: r = json.loads(l)
        except Exception: continue
        if r.get('status') in ('SLOW', 'EXC', 'NOMODEL', 'LATTICE-MISMATCH', 'SPECIAL-ERROR'): bad.add(str(r['idx']))
for k in sorted(bad):
    r = dict(recs[k]); r['comps'] = [dict(c, dim=max(c['dim'], 2)) for c in r['comps']]   # force the lattice-level step
    print(json.dumps(r))
print(len(bad), file=sys.stderr)
PYEOF
$PY runclass.py $TAG 3 --n=$N ${TAG}_slowrecs.jsonl > runclass_$TAG.log 2>&1
