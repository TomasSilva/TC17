"""Compare a core class enumerated by heavyaug+lsgen3 (graph6, canonical) with the same class
enumerated by bigblocks.py+fill_triples.py: canonical forms, set differences, and for lattices found
only by our enumerator whether they contain two heavy points not joined by a line with
(m_P - 1) + (m_Q - 1) > 8 (the cut that heavyaug_p applies).
usage: compare.py core.g6 tag   (our files: lattices_<tag>_*.jsonl)"""
import sys, json, glob, subprocess, itertools
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/validate')
from canon import canon_many
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/heavy')
from g6blocks import decode
G6, tag = sys.argv[1], sys.argv[2]
d = 13
def recanon(lines):
    r = subprocess.run(['labelg', '-q', '-f' + 'a' * d], input=''.join(lines), capture_output=True, text=True)
    return r.stdout.split('\n')[:len(lines)]
A = set()
buf = []
for line in open(G6):
    buf.append(line if line.endswith('\n') else line + '\n')
    if len(buf) == 200000:
        A.update(recanon(buf)); buf = []
if buf: A.update(recanon(buf))
B = {}
for f in sorted(glob.glob('lattices_%s_*.jsonl' % tag)):
    recs = [json.loads(l)['blocks'] for l in open(f)]
    for k in range(0, len(recs), 200000):
        part = recs[k:k + 200000]
        for c, bl in zip(canon_many(d, part), part):
            B[c] = bl
nA, nB = len(A), len(B)
onlyA = A - B.keys(); onlyB = [c for c in B if c not in A]
def cut(bl):
    big = [set(b) for b in bl if len(b) >= 4]
    for P, Q in itertools.combinations(big, 2):
        if not (P & Q) and len(P) + len(Q) - 2 > 8: return True
    return False
expl = sum(1 for c in onlyB if cut(B[c]))
print('%s: heavyaug+lsgen3 %d distinct, ours %d distinct, common %d, only heavyaug %d, only ours %d (of which with an unjoined heavy pair t > 8: %d)'
      % (tag, nA, nB, len(A & B.keys()), len(onlyA), len(onlyB), expl))
with open('diff_%s.jsonl' % tag, 'w') as out:
    for c in onlyA: out.write(json.dumps({'side': 'heavyaug_only', 'g6': c, 'blocks': [b for b in decode(c, d) if len(b) >= 3]}) + '\n')
    for c in onlyB:
        if not cut(B[c]): out.write(json.dumps({'side': 'ours_only_unexplained', 'g6': c, 'blocks': B[c]}) + '\n')
