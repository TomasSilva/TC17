#!/bin/zsh
cd /Users/agent/Projects/TC17
tag=n15_7_7; n=15; d1=7
# 1. wait for the fast filter parts
for p in 0 1 2 3 4 5; do until grep -q ALLDONE work/tc15/lattices_${tag}_fast_$p.out 2>/dev/null; do sleep 30; done; done
cat work/tc15/lattices_${tag}_defer_[0-5].jsonl > work/tc15/defer_${tag}.jsonl
echo "fast done: $(wc -l < work/tc15/defer_${tag}.jsonl) deferred" > work/tc15/chain_${tag}.log
# 2. pass 2 in 6 parts
split -n l/6 -d work/tc15/defer_${tag}.jsonl work/tc15/defer_${tag}_part
for f in work/tc15/defer_${tag}_part0[0-5]; do mv $f $f.jsonl; done
for f in work/tc15/defer_${tag}_part0[0-5].jsonl; do nohup .venv/bin/python work/tc15/fast_real2.py $n $f > ${f%.jsonl}.log 2>&1 & done
wait
cat work/tc15/defer_${tag}_part0[0-5]_pass2.jsonl > work/tc15/defer2_${tag}.jsonl
echo "pass2 done: $(wc -l < work/tc15/defer2_${tag}.jsonl) deferred to M2" >> work/tc15/chain_${tag}.log
# 3. Macaulay2 on the remainder
for p in 0 1 2 3 4 5; do nohup .venv/bin/python work/tc15/exact_tc_lattice.py $n $d1 work/tc15/defer2_${tag}.jsonl $p 6 > work/tc15/tc_${tag}_$p.log 2>&1 & done
wait
cat work/tc15/defer2_${tag}_tc_[0-5].out > work/tc15/tc_${tag}.out
echo "M2 done: $(grep -c '^LATTICE' work/tc15/tc_${tag}.out) lattices, MIXED: $(grep -c MIXED work/tc15/tc_${tag}.out), errors: $(grep -c ERROR work/tc15/tc_${tag}.out)" >> work/tc15/chain_${tag}.log
echo "CHAIN DONE" >> work/tc15/chain_${tag}.log
