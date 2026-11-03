"""Positive controls of the core classes and window checks of 17-line lattices (written from the definitions).
usage: chains.py cores b48_classes.g6 b48w_classes.g6
          the 28 cores of work/n17/validate/cores13.jsonl and every phi-max core (deletion of a 4-chain) of the 16
          lattices of work/n17/run/checked_L.jsonl must lie in the class b48; b48 must be a subset of b48w.
       chains.py window lattices.jsonl
          for every lattice: (W1) b2 = 80, (W2) m <= 6, (W3) 4-8 points per line, (W4) a double point on every
          8-point line, (W5) unjoined pairs with (m_P-1)+(m_Q-1) <= 8; phi_max over the 2,380 sets of four lines,
          number of 4-chains, number of unjoined pairs with (m_P-1)+(m_Q-1) = 8 (D-pairs)."""
import sys, json, itertools, collections
N17 = '/Users/agent/Projects/TC17/work/n17'
sys.path.insert(0, N17 + '/validate')
from canon import canon_many
def jl(f):
    for l in open(f):
        if l.strip(): yield json.loads(l)
def points(n, blocks):
    pts = [frozenset(b) for b in blocks if len(b) >= 3]
    cov = {q for P in pts for q in itertools.combinations(sorted(P), 2)}
    return pts + [frozenset(q) for q in itertools.combinations(range(n), 2) if q not in cov]
def phi(pts, s, S):
    S = frozenset(S)
    return sum(s[x] - 7 for x in S) - sum(1 for P in pts if P <= S)
def delete(n, blocks, S):
    rest = [x for x in range(n) if x not in S]; rel = {x: i for i, x in enumerate(rest)}
    out = [sorted(rel[x] for x in b if x in rel) for b in blocks]
    return [b for b in out if len(b) >= 3]
if sys.argv[1] == 'cores':
    b48 = set(l.strip() for l in open(sys.argv[2]) if l.strip())
    b48w = set(l.strip() for l in open(sys.argv[3]) if l.strip())
    c13 = [r['blocks'] for r in jl(N17 + '/validate/cores13.jsonl')]
    c13c = canon_many(13, c13)
    L16 = [r['blocks'] for r in jl(N17 + '/run/checked_L.jsonl')]
    cores, per = [], []
    for L in L16:
        pts = points(17, L); s = collections.Counter(x for P in pts for x in P)
        ch = [S for S in itertools.combinations(range(17), 4) if phi(pts, s, S) == 4]
        per.append(len(ch))
        cores += [delete(17, L, S) for S in ch]
    cc = canon_many(13, cores)
    res = dict(cores13=len(c13), cores13_in_b48=sum(1 for c in c13c if c in b48), chains_per_lattice=per,
               chain_cores=len(set(cc)), chain_cores_in_b48=sum(1 for c in set(cc) if c in b48),
               b48_subset_of_b48w=b48 <= b48w, b48w_minus_b48=len(b48w - b48), b48=len(b48), b48w=len(b48w))
    print(json.dumps(res))
else:
    out = []; ok = 0
    for r in jl(sys.argv[2]):
        L = r['blocks']; n = 17
        pts = points(n, L); s = collections.Counter(x for P in pts for x in P)
        w = dict(W1_b2=sum(len(P) - 1 for P in pts) == 80, W2_mult=max(len(P) for P in pts) <= 6,
                 W3_lines=all(4 <= s[x] <= 8 for x in range(n)),
                 W4_double=all(any(len(P) == 2 and x in P for P in pts) for x in range(n) if s[x] == 8))
        big = [P for P in pts if len(P) >= 3]; nd = 0; w5 = True
        for P, Q in itertools.combinations(big, 2):
            if not (P & Q):
                sg = len(P) + len(Q) - 2
                if sg > 8: w5 = False
                if sg == 8: nd += 1
        w['W5_unjoined'] = w5
        phis = collections.Counter(phi(pts, s, S) for S in itertools.combinations(range(n), 4))
        pm = max(phis)
        rec = dict(idx=r.get('idx'), known=r.get('known'), window=all(w.values()), conditions=w, phi_max=pm, four_chains=phis[4], D_pairs=nd,
                   profile=''.join(map(str, sorted((s[x] for x in range(n)), reverse=True))), multiplicities=dict(collections.Counter(len(P) for P in pts)))
        if rec['window'] and pm == 4 and phis[4] > 0: ok += 1
        out.append(rec)
    print(json.dumps(dict(n=len(out), window_with_4chain=ok, per=out)))
