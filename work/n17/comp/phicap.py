"""phi_max >= cap test for a partial arrangement (list of line sets of its points)."""
import itertools, collections
def phi_reaches(linesets, n, cap):
    if cap is None: return False
    s = collections.Counter()
    for L in linesets:
        for x in L: s[x] += 1
    cand = [x for x in range(n) if s[x] >= 6]
    if len(cand) < 4: return False
    small = collections.defaultdict(int)
    for L in linesets:
        if len(L) <= 4: small[frozenset(L)] += 1
    for S in itertools.combinations(cand, 4):
        w = sum(s[x] - 7 for x in S)
        if w < cap: continue
        f = 0
        for k in (2, 3, 4):
            for T in itertools.combinations(S, k):
                f += small.get(frozenset(T), 0)
        if w - f >= cap: return True
    return False
CAP = {'b48': None, 'b49': 4, 'b50': 3, 'b51': 2}
