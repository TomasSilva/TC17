#!/bin/bash
# wait until all 157533 b51 cores have a components record, then run the b51 extension pipeline
cd /Users/agent/Projects/TC17/work/n17/run
PY=/Users/agent/Projects/TC17/.venv/bin/python
until [ "$(ps -eo args | grep 'm2compb.py 13 d51_tagged' | grep -v grep | wc -l)" -eq 0 ]; do sleep 30; done
cat ../comp/d51_comp_*.jsonl ../comp/d51b_comp_*.jsonl | $PY -c "
import sys, json
seen = {}
for l in sys.stdin:
    try: r = json.loads(l)
    except Exception: continue
    seen[r['idx']] = r
for r in seen.values(): print(json.dumps(r))
print(len(seen), file=sys.stderr)
" > comp_b51.jsonl 2> comp_b51.count
$PY runclass.py b51 6 comp_b51.jsonl > runclass_b51.log 2>&1
echo FINISHED >> runclass_b51.log
