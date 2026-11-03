#!/bin/bash
# Complete re-verification with the corrected filters: both classes, 10 workers each, then Macaulay2.
set -u
D=/Users/agent/Projects/TC17/work/tc15/recheck_resultant
PY=/Users/agent/Projects/TC17/.venv/bin/python
TC=/Users/agent/Projects/TC17/work/tc15
NP=10
cd $D/full
echo "START $(date)"
for cls in "15 $TC/lattices_n15_7_7.jsonl n15_7_7" "16 $TC/lattices_n16_7_8.jsonl n16_7_8"; do
  set -- $cls; n=$1; IN=$2; tag=$3
  echo "== class $tag: corrected passes 1+2 on $NP workers, $(date)"
  for ((p = 0; p < NP; p++)); do
    nohup $PY $D/full_recheck.py $n $IN $p $NP $D/full/${tag}_p$p > $D/full/${tag}_p$p.log 2>&1 &
  done
  wait
  echo "== class $tag: filters done, $(date)"
  grep -h FINAL $D/full/${tag}_p*.log
  cat $D/full/${tag}_p*_defer.jsonl > $D/full/${tag}_defer_all.jsonl
  echo "deferred to Macaulay2: $(wc -l < $D/full/${tag}_defer_all.jsonl)"
  echo "== class $tag: Macaulay2 on $NP workers, $(date)"
  for ((p = 0; p < NP; p++)); do
    nohup $PY $TC/exact_tc_lattice.py $n 7 $D/full/${tag}_defer_all.jsonl $p $NP > $D/full/${tag}_m2_p$p.log 2>&1 &
  done
  wait
  echo "== class $tag: Macaulay2 done, $(date)"
  cat $D/full/${tag}_defer_all_tc_*.out | grep "^LATTICE" | awk '{print $3, $5}' | sort | uniq -c | sort -rn | head
  echo "good components (realisable lattices): $(cat $D/full/${tag}_defer_all_tc_*.out | grep '^LATTICE' | awk '$5 > 0' | wc -l)"
  cat $D/full/${tag}_defer_all_tc_*.out | grep "COMP" | sort | uniq -c
done
echo "ALL DONE $(date)"
