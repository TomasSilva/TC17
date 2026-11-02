#!/bin/zsh
# usage: feeder.sh n wmin wmax bmax tag classes workers
# Runs the streaming pipeline repeatedly on the chunk files that stage 1 has completed so far
# (pipeline.py skips chunks already done), until stage 1 has finished and every chunk is processed;
# then writes work/tc15/feeder_$tag.done.  chain2.sh waits for that marker before Macaulay2.
cd /Users/agent/Projects/TC17
n=$1; wmin=$2; wmax=$3; bmax=$4; tag=$5; classes=$6; np=$7
LOG=work/tc15/feeder_$tag.log
pass=0
while true; do
  pass=$((pass+1))
  fin=0; grep -q "^FINAL" work/tc15/bigblocks2_$tag.log 2>/dev/null && fin=1
  files=(work/tc15/bb_$tag/bb_${tag}_*.jsonl.gz(N))
  if [ ${#files} -gt 0 ]; then
    echo "$(date) pass $pass: ${#files} chunk files present, stage-1 finished: $fin" >> $LOG
    .venv/bin/python work/tc15/pipeline.py $n $wmin $wmax $bmax $tag $classes $files --workers $np >> work/tc15/pipeline_$tag.log 2>&1
  fi
  if [ $fin -eq 1 ]; then break; fi
  sleep 600
done
echo "$(date) feeder done after $pass passes" >> $LOG
touch work/tc15/feeder_$tag.done
