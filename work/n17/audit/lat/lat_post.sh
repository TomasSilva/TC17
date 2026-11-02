#!/bin/bash
# post-processing of the lattice-level step for the 7 components
cd /Users/agent/Projects/TC17/work/n17/audit/lat
PY=/Users/agent/Projects/TC17/.venv/bin/python
for ch in L1[34]_n1[3456]_ch.jsonl; do
  [ -f "$ch" ] || continue
  b=${ch%_ch.jsonl}
  $PY children_check_lat.py $b
done > screen.out 2>&1
cat L1[34]_n1[3456]_chcomp_*.jsonl 2>/dev/null > children_all.jsonl
n=$(grep -c '"status": "REAL"' children_all.jsonl)
echo "realisable children: $n" >> screen.out
split -l 40 children_all.jsonl part_
ls part_* | xargs -n 1 -P 10 -I{} $PY ../ext/extaudit.py {} {}.ext.jsonl all 600
echo POSTDONE >> screen.out
