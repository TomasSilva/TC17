#!/bin/bash
# collect all lattices from every extension output, dedup, exact TC check of the new ones, summary
cd /Users/agent/Projects/TC17/work/n17/run
PY=/Users/agent/Projects/TC17/.venv/bin/python
# every rigid and family output, also those of rerun/ (the list used for final_files.txt on 21 Oct, 19:59;
# an earlier version of this script used a narrower ls pattern)
find . -maxdepth 2 -name "*.jsonl" | grep -E "ext|fam|L17|famall" | grep -v -E "slowrecs|_r[0-2]\.jsonl|famall_b4849\.jsonl|fam_b4849\.jsonl|d2c_fam\.jsonl|famall_done|fam_done|chdefer|chcomp" | sort > final_files.txt
$PY collectL.py $(cat final_files.txt) > final_collect.txt
tail -1 final_collect.txt
$PY checkL.py 3600 >> final_check.log
$PY - <<'PYEOF'
import json
n = 0; cex = 0
for l in open('checked_L.jsonl'):
    r = json.loads(l); n += 1; cex += r['counterexample']
print('checked lattices:', n, 'counterexamples:', cex)
PYEOF
