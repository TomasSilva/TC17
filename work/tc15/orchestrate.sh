#!/bin/zsh
# usage: orchestrate.sh n wmin wmax bmax Wtot tag d1 nparts
cd /Users/agent/Projects/TC17
n=$1; wmin=$2; wmax=$3; bmax=$4; Wtot=$5; tag=$6; d1=$7; np=$8
until grep -q FINAL work/tc15/bigblocks_$tag.log; do sleep 30; done
for ((p=0; p<np; p++)); do
  nohup .venv/bin/python work/tc15/fill_triples.py $n $wmin $wmax $bmax $Wtot $tag $p $np > work/tc15/fill_${tag}_$p.log 2>&1 &
done
wait
cat work/tc15/lattices_${tag}_*.jsonl > work/tc15/lattices_$tag.jsonl
echo "LATTICES $(wc -l < work/tc15/lattices_$tag.jsonl)" >> work/tc15/fill_${tag}_0.log
for ((p=0; p<np; p++)); do
  nohup .venv/bin/python work/tc15/exact_tc_lattice.py $n $d1 work/tc15/lattices_$tag.jsonl $p $np > work/tc15/tc_${tag}_$p.log 2>&1 &
done
wait
cat work/tc15/lattices_${tag}_tc_*.out > work/tc15/tc_$tag.out
echo "ORCHESTRATION DONE $tag" >> work/tc15/tc_$tag.out
