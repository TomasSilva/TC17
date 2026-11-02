"""Combinatorics of a line arrangement over F_p and chain search for 8-point lines.
usage: arr.py p name  (lines are built in build_*)"""
import sys, itertools, subprocess, json
p = int(sys.argv[1])
def inv(a): return pow(a % p, p - 2, p)
def norm(v):
    v = [c % p for c in v]
    for c in v:
        if c:
            i = inv(c); return tuple(x * i % p for x in v)
    raise ValueError('zero')
def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def sqrtm3():
    # w with w^2 - w + 1 = 0
    for w in range(2, p):
        if (w*w - w + 1) % p == 0: return w
def build(name):
    if name == 'E17':
        w = sqrtm3()
        L = [(0,0,1)]
        L += [(0,1,-a) for a in (0,1,w-1,w)]          # y = a z
        L += [(1,0,-b) for b in (0,1,w,1-w)]          # x = b z
        L += [(1,1,-c) for c in (0,1,w,w+1)]          # x + y = c z
        L += [(1,w,-d) for d in (0,1,w-1,w)]          # x + w y = d z
        return [norm(l) for l in L]
    if name == 'G17':
        L = [(0,0,1)]
        L += [(0,1,-a) for a in range(0,4)]
        L += [(1,0,-b) for b in range(2,6)]
        L += [(1,-1,-c) for c in range(0,4)]
        L += [(1,1,-d) for d in range(3,7)]
        return [norm(l) for l in L]
    if name == 'R17a':
        # H = z; y = -a (a=0..3); x = 0,2,4; x - y = 2,3,5; 3x - 4y = 12; x - 2y = 2,4,5,6,8
        L = [(0,0,1)]
        L += [(0,1,a) for a in range(0,4)]
        L += [(1,0,-b) for b in (0,2,4)]
        L += [(1,-1,-c) for c in (2,3,5)]
        L += [(3,-4,-12)]
        L += [(1,-2,-d) for d in (2,4,5,6,8)]
        return [norm(l) for l in L]
    raise ValueError(name)
def points(L):
    P = {}
    for i, j in itertools.combinations(range(len(L)), 2):
        q = norm(cross(L[i], L[j]))
        P.setdefault(q, set()).update((i, j))
    return P
def scount(L, idx):
    """number of points on each line of the sub-arrangement idx"""
    sub = [L[i] for i in idx]
    P = points(sub)
    s = {i: 0 for i in range(len(idx))}
    for q, S in P.items():
        for i in S: s[i] += 1
    return {idx[i]: s[i] for i in s}, P
if __name__ == '__main__':
    L = build(sys.argv[2])
    idx = list(range(len(L)))
    s, P = scount(L, idx)
    prof = {}
    for q, S in P.items(): prof[len(S)] = prof.get(len(S), 0) + 1
    b2 = sum(len(S) - 1 for S in P.values())
    print('lines', len(L), 'profile', sorted(prof.items()), 'b2', b2)
    print('points per line', [s[i] for i in idx])
    eight = [i for i in idx if s[i] == 8]
    print('8-point lines', eight)
    # chains: sequences H1..Hk with H_i having 8 points in L minus earlier ones
    chains = []
    def ext(ch, rem):
        chains.append(list(ch))
        if len(ch) == 4: return
        cur = [i for i in idx if i not in ch]
        sc, _ = scount(L, cur)
        for h in rem:
            if sc[h] == 8 and (not ch or h > max(ch) or True):
                if h not in ch:
                    ext(ch + [h], [r for r in rem if r != h])
    ext([], eight)
    # keep chains as sets (order matters for the definition; record ordered ones, dedupe by set)
    seen = {}
    for ch in chains:
        seen.setdefault(frozenset(ch), ch)
    out = [seen[k] for k in sorted(seen, key=lambda k: (len(k), sorted(k)))]
    print('chain sets by length', {k: sum(1 for c in out if len(c) == k) for k in range(5)})
    json.dump({'p': p, 'lines': L, 'chains': out}, open(sys.argv[2] + '_chains.json', 'w'))
