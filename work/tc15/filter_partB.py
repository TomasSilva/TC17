#!/usr/bin/env python3
"""Keep only the deferred 17-line (8,8) lattices that belong to part [B] and survive the new combinatorial filters
(TC_FILTER.md): some line with 4, 5 or 8 points; every 8-point line carries a point of multiplicity >= 4 (no all-triple
8-point line, Lemma F1); no 4-point line with multiplicities 6,6,6,2 (Proposition F4).  Usage: filter_partB.py in.jsonl out.jsonl"""
import json, sys
from collections import Counter
inp, out = sys.argv[1], sys.argv[2]
kept = 0; reasons = Counter(); total = 0
with open(inp) as f, open(out, 'w') as g:
    for line in f:
        total += 1
        rec = json.loads(line)
        blocks = rec['blocks']; s = rec['s']; n = len(s)
        if min(s) >= 6 and max(s) <= 7: reasons['all lines 6-7 (part [A], done)'] += 1; continue
        # multiplicity vectors per line
        mult = {}
        for i in range(n):
            mult[i] = sorted((len(B) - 1 for B in blocks if i in B), reverse=True)
        bad = None
        for i in range(n):
            if s[i] == 8:
                if max(mult[i]) < 3: bad = 'all-triple 8-point line'; break   # entries are m_P - 1; big block iff >= 3
            if s[i] == 4 and mult[i] == [5,5,5,1]: bad = '4-point line (6,6,6,2)'; break
        if bad: reasons[bad] += 1; continue
        kept += 1; g.write(line)
print(f'{total} lattices: kept {kept}; removed {dict(reasons)}', file=sys.stderr)
