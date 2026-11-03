#!/bin/bash
# status of the campaign: stages done, last log lines, running processes
C=/Users/agent/Projects/TC17/work/n17/campaign
echo "== campaign status $(date)"
echo "-- stages done / failed:"; /bin/ls $C/done 2>/dev/null | sed 's/^/   /'
echo "-- last log lines:"; tail -n ${1:-25} $C/campaign.log
N=$(ps -eo args | grep -E "campaign.py|runclass.py|extend.py|famrun.py|m2compb.py|M2 --script|full_recheck.py|lsgen3|heavyaug_p|as_screen.py|as_jsonl.py|indep_rigid.py|pencil5c.py|farkas.py|propcheck.py|level2.py|fill_triples.py|exact_tc_lattice.py|freecheck.py|labelg" | grep -v grep | wc -l | tr -d ' ')
echo "-- processes of the campaign running: $N"
uptime
