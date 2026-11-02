"""For each lattice class (jsonl with 'blocks' on 17 lines), list its 4-chains and write the 13-line cores
L minus S (relabelled) to a jsonl file, deduplicated up to isomorphism."""
import sys, json, itertools
sys.path.insert(0, '.')
from latchain import b2
from pynauty import Graph, certificate
def canon(n, blocks):
    m = len(blocks); g = Graph(n + m, directed=False)
    for k, S in enumerate(blocks): g.connect_vertex(n + k, sorted(S))
    g.set_vertex_coloring([set(range(n)), set(range(n, n + m))])
    return certificate(g)
out = {}; src = {}
for fn in sys.argv[2:]:
    for li, line in enumerate(open(fn)):
        rec = json.loads(line); n = 17; blocks = rec['blocks']
        allL = list(range(n)); B0 = b2(n, blocks, allL)
        eight = [i for i in allL if B0 - b2(n, blocks, [j for j in allL if j != i]) == 8]
        for S in itertools.combinations(eight, 4):
            keep = [j for j in allL if j not in S]
            if b2(n, blocks, keep) != B0 - 32: continue
            idx = {a: i for i, a in enumerate(keep)}
            fb = [sorted(idx[a] for a in B if a in idx) for B in blocks]
            fb = [B for B in fb if len(B) >= 3]
            key = canon(13, fb)
            if key not in out:
                out[key] = fb; src[key] = (fn.split('/')[-1], li, list(S))
print(len(out), 'distinct 13-line cores')
with open(sys.argv[1], 'w') as f:
    for key, fb in out.items():
        prof = {}
        for B in fb: prof[len(B)] = prof.get(len(B), 0) + 1
        f.write(json.dumps({'blocks': fb, 'src': src[key], 'profile': prof}) + '\n')
        print(src[key], 'profile', sorted(prof.items()))
