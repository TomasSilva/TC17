#!/bin/zsh
# usage: chain3.sh (chain2 + part-[B] filter before Macaulay2) n wmin wmax bmax tag "0:7:9,1:8:8" workers
# Waits for stage 1 (bigblocks2.py, log work/tc15/bigblocks2_$tag.log), runs the streaming pipeline
# (fill -> fast filter -> number-field pass) over all chunk files, then Macaulay2 on the deferred
# lattices of each class.  Progress in work/tc15/chain2_$tag.log.
cd /Users/agent/Projects/TC17
n=$1; wmin=$2; wmax=$3; bmax=$4; tag=$5; classes=$6; np=$7
LOG=work/tc15/chain2_$tag.log
until grep -q "^FINAL" work/tc15/bigblocks2_$tag.log 2>/dev/null; do sleep 120; done
echo "$(date) stage 1 done: $(grep '^FINAL' work/tc15/bigblocks2_$tag.log)" >> $LOG
until [ -f work/tc15/feeder_$tag.done ]; do sleep 120; done
.venv/bin/python work/tc15/pipeline.py $n $wmin $wmax $bmax $tag $classes work/tc15/bb_$tag/bb_${tag}_*.jsonl.gz --workers $np >> work/tc15/pipeline_$tag.log 2>&1
echo "$(date) pipeline done: $(ls work/tc15/pipe_$tag/done_*.json | wc -l) chunks" >> $LOG
for spec in ${(s:,:)classes}; do
  c=${spec%%:*}; rest=${spec#*:}; d1=${rest%%:*}
  cat work/tc15/pipe_$tag/defer_*_c$c.jsonl > work/tc15/defer2_${tag}_c${c}_all.jsonl; .venv/bin/python work/tc15/filter_partB.py work/tc15/defer2_${tag}_c${c}_all.jsonl work/tc15/defer2_${tag}_c$c.jsonl 2>> $LOG
  nl=$(wc -l < work/tc15/defer2_${tag}_c$c.jsonl)
  echo "$(date) class $c (d1=$d1): $nl lattices to Macaulay2" >> $LOG
  if [ "$nl" -gt 0 ]; then
    for ((p=0; p<np; p++)); do nohup .venv/bin/python work/tc15/exact_tc_lattice.py $n $d1 work/tc15/defer2_${tag}_c$c.jsonl $p $np > work/tc15/tc_${tag}_c${c}_$p.log 2>&1 & done
    wait
    cat work/tc15/defer2_${tag}_c${c}_tc_[0-9]*.out > work/tc15/tc_${tag}_c$c.out
    echo "$(date) M2 class $c done: $(grep -c '^LATTICE' work/tc15/tc_${tag}_c$c.out) lattices, realisable: $(grep -c '^  COMP' work/tc15/tc_${tag}_c$c.out) components, MIXED: $(grep -c MIXED work/tc15/tc_${tag}_c$c.out), errors: $(grep -c ERROR work/tc15/tc_${tag}_c$c.out)" >> $LOG
  fi
done
echo "CHAIN DONE" >> $LOG
