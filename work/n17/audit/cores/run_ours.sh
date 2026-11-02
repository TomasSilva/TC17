#!/bin/bash
# Independent enumeration of the 13-line core classes with the 15/16-line enumerator (no W5 cut).
cd /Users/agent/Projects/TC17/work/n17/audit/cores
PY=/Users/agent/Projects/TC17/.venv/bin/python
NP=${NP:-3}
for spec in "a49 4 9 29" "a50 4 9 28" "a51 4 9 27"; do
  set -- $spec; tag=$1; wmin=$2; wmax=$3; X=$4
  echo "== $tag bigblocks $(date)"
  $PY bigblocks.py 13 $wmin $wmax 6 $X $tag > bigblocks_$tag.log 2>&1
  tail -1 bigblocks_$tag.log
  for ((p = 0; p < NP; p++)); do
    nice -n 2 $PY fill_triples.py 13 $wmin $wmax 6 $X $tag $p $NP > fill_${tag}_$p.log 2>&1 &
  done
  wait
  grep -h FINAL fill_${tag}_*.log
done
echo "ALL DONE $(date)"
