#!/bin/bash
cd /Users/agent/Projects/TC17/work/n17/audit/n8zero
for v in 53332 44431 44422 44332 43333 55321 55222 54421 54331 54322 55411; do
  (time /Users/agent/Projects/TC17/.venv/bin/python pencil5c.py $v > p5c_$v.jsonl) 2> p5c_$v.log
done
echo ALLDONE > run5c.done
