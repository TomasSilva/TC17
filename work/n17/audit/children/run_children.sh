#!/bin/bash
cd /Users/agent/Projects/TC17/work/n17/audit/children
PY=/Users/agent/Projects/TC17/.venv/bin/python
(for b in b51_n13; do $PY children_check.py $b; done > out_a.txt 2>&1) &
(for b in b50_n13 b50_n14 b50_n15 b51_n14 b49slow_n13 b50slow13_n13 b50slow13_n14 b50slow13_n15 b50slow14_n14 b50slow14_n15 b50slow15_n15 b51to2_n14 b49d2n15_n15 dim2_b4849 d2c_dim2; do $PY children_check.py $b; done > out_b.txt 2>&1) &
wait; echo ALLDONE >> out_b.txt
