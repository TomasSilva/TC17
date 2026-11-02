"""Write the level-1 (14-line) combinatorial extensions of given cores as jsonl blocks (size >= 3)."""
import sys, json
from branch import pts_of, candidates
for line in open(sys.argv[1]):
    r = json.loads(line)
    pts = pts_of(13, r['blocks']); b2 = sum(len(P) - 1 for P in pts); budget = 80 - b2
    k = 0
    for T in candidates(13, pts, max(2, budget - 24), min(8, budget - 6)):
        Tset = set(T)
        newb = [sorted(P | {13}) if P in Tset else sorted(P) for P in pts]
        newb = [b for b in newb if len(b) >= 3]
        print(json.dumps(dict(idx='%s/%d' % (r.get('idx'), k), blocks=newb))); k += 1
