#!/bin/bash
# full (17;8,8) window: m<=6, 4..8 points per line (h in [8,12]), X=56, Wmin=10, (W5) + at most 4 D-pairs
cd "$(dirname "$0")"
for r in $(seq 0 9); do
  ./heavyaug_p 17 6 8 12 56 10 100 1 10 $r 4 6 > /dev/null 2> full_r$r.log &
done
wait
echo ALLDONE > full_done.flag
