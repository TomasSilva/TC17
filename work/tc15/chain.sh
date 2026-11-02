#!/bin/zsh
# usage: chain.sh n wmin wmax bmax Wtot tag d1 nparts   -- waits for stage 1, then fill -> fast -> pass2 -> M2
cd /Users/agent/Projects/TC17
n=$1; wmin=$2; wmax=$3; bmax=$4; Wtot=$5; tag=$6; d1=$7; np=$8
until grep -q FINAL work/tc15/bigblocks_$tag.log; do sleep 60; done
for ((p=0; p<np; p++)); do nohup .venv/bin/python work/tc15/fill_triples.py $n $wmin $wmax $bmax $Wtot $tag $p $np > work/tc15/fill_${tag}_$p.log 2>&1 & done
wait
echo "fill done: $(cat work/tc15/lattices_${tag}_[0-9]*.jsonl | wc -l) lattices" > work/tc15/chain_$tag.log
for ((p=0; p<np; p++)); do nohup .venv/bin/python work/tc15/fast_real.py $n work/tc15/lattices_${tag}_$p.jsonl 0 1 > work/tc15/fast_${tag}_$p.log 2>&1 & done
wait
cat work/tc15/lattices_${tag}_[0-9]*_defer_0.jsonl > work/tc15/defer_$tag.jsonl
echo "fast done: $(wc -l < work/tc15/defer_$tag.jsonl) deferred" >> work/tc15/chain_$tag.log
nl=$(wc -l < work/tc15/defer_$tag.jsonl); per=$(( (nl + np - 1) / np )); split -l $per -d work/tc15/defer_$tag.jsonl work/tc15/defer_${tag}_part
for f in work/tc15/defer_${tag}_part[0-9][0-9]; do mv $f $f.jsonl; done
for f in work/tc15/defer_${tag}_part[0-9][0-9].jsonl; do nohup .venv/bin/python work/tc15/fast_real2.py $n $f > ${f%.jsonl}.log 2>&1 & done
wait
cat work/tc15/defer_${tag}_part[0-9][0-9]_pass2.jsonl > work/tc15/defer2_$tag.jsonl
echo "pass2 done: $(wc -l < work/tc15/defer2_$tag.jsonl) deferred to M2" >> work/tc15/chain_$tag.log
for ((p=0; p<np; p++)); do nohup .venv/bin/python work/tc15/exact_tc_lattice.py $n $d1 work/tc15/defer2_$tag.jsonl $p $np > work/tc15/tc_${tag}_$p.log 2>&1 & done
wait
cat work/tc15/defer2_${tag}_tc_[0-9]*.out > work/tc15/tc_$tag.out
echo "M2 done: $(grep -c '^LATTICE' work/tc15/tc_$tag.out) lattices, MIXED: $(grep -c MIXED work/tc15/tc_$tag.out), errors: $(grep -c ERROR work/tc15/tc_$tag.out)" >> work/tc15/chain_$tag.log
echo "CHAIN DONE" >> work/tc15/chain_$tag.log
