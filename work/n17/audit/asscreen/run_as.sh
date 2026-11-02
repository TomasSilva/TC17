#!/bin/bash
cd /Users/agent/Projects/TC17/work/n17/audit/asscreen
PY=/Users/agent/Projects/TC17/.venv/bin/python
for spec in "48 ../../cores/core48.g6" "49 ../../cores/core49.g6" "50 ../../cores50/core50.g6" "51 ../../cores50/core51.g6"; do
  set -- $spec; b=$1; g=$2
  for p in 0 1; do nice -n 2 $PY as_screen.py $g 13 as$b\_p$p $p 2 > as$b\_p$p.log 2>&1 & done
  wait
  tail -qn1 as$b\_p*.log
done
echo "ALL DONE $(date)"
