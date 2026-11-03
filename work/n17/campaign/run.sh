#!/bin/bash
# launch the campaign detached (survives the end of the terminal session); stages already done are skipped
C=/Users/agent/Projects/TC17/work/n17/campaign
cd $C && rm -f STOP && nohup /Users/agent/Projects/TC17/.venv/bin/python campaign.py "$@" >> campaign.out 2>&1 &
echo "campaign started (pid $!); follow with: $C/status.sh"
