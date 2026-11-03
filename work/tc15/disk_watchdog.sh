#!/bin/zsh
# Stop my own long computations before they can fill the disk.
while true; do
  free=$(df -g /Users | tail -1 | awk '{print $4}')
  if [ "$free" -lt 15 ]; then
    pkill -f "bigblocks2.py"; pkill -f "pipeline.py"; pkill -f "bigblocks.py"; pkill -f "fill_triples.py"; pkill -f "exact_tc_lattice.py"; pkill -x M2
    echo "$(date) stopped the n=17 computations at ${free}G free" >> /Users/agent/Projects/TC17/work/tc15/watchdog.log
  fi
  sleep 300
done
