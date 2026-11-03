"""Level 1 of the (gamma) search: assignments of delta (0..4) to the lines through the points of H0,
up to symmetry (non-decreasing within a group; groups of equal size in lexicographic order), satisfying
 (a) Delta <= 32 - max(11, W(H0));  (b) k_i = 3: sum over the group >= 3; k_i >= 4: three smallest >= 4;
 (c) heavy P_i: Delta - lambda_i + B_i >= (16 - k_i)(4 - sigma_i),  B_i <= min(t2max, b0 + bmax(A) + bmax(B))
     (A, B the two lines of smallest delta at P_i);
 (d) triple P_i = {A,B}: 13 lambda_i + Delta + B_i >= 42, same B_i bound.
 t2max = 64 - 3 Delta - t5 - 3 t6.  bmax(X) = floor((5s - 21 + k)/4) with s = 8 - delta, capped by s - 3 + [k>=2].
"""
import itertools, sys
from gamma_ilp import vectors
def bmax(d, k):
    s = 8 - d
    return min((5 * s - 21 + k) // 4, s - 3 + (1 if k >= 2 else 0))
def bmin(d, k):
    s = 8 - d
    v = 2 * s - 18 + k
    if s == 8 and k != 1: v = max(v, 1)
    return max(v, 0)
def group_tuples(ki, thr=4):
    """non-decreasing delta tuples for a group of size ki, with b-range feasibility"""
    out = []
    for tup in itertools.combinations_with_replacement(range(5), ki):
        if any(bmin(d, ki) > bmax(d, ki) for d in tup): continue
        if ki == 3 and sum(tup) < thr - 1: continue
        if ki >= 4 and sum(tup[:3]) < thr: continue
        out.append(tup)
    return out
def survivors(k, thr=4):
    W0 = sum((ki - 1) * (ki - 2) // 2 for ki in k)
    t5 = sum(1 for ki in k if ki == 4); t6 = sum(1 for ki in k if ki == 5)
    b0 = sum(1 for ki in k if ki == 1)
    Dmax = 32 - max(11, W0)
    opts = [group_tuples(ki, thr) for ki in k]
    res = []
    def rec(i, chosen, tot):
        if tot > Dmax: return
        if i == len(k):
            Delta = tot
            t2max = 64 - 3 * Delta - t5 - 3 * t6
            if t2max < b0: return
            for j, ki in enumerate(k):
                tup = chosen[j]
                lam = sum(tup)
                if ki >= 3:
                    sig = tup[0] + tup[1]
                    B = min(t2max, b0 + bmax(tup[0], ki) + bmax(tup[1], ki))
                    if Delta - lam + B < (16 - ki) * (thr - sig): return
                if ki == 2:
                    B = min(t2max, b0 + bmax(tup[0], ki) + bmax(tup[1], ki))
                    if 13 * lam + Delta + B < 14 * thr - 14: return
            res.append((Delta, tuple(chosen)))
            return
        for tup in opts[i]:
            if i > 0 and k[i] == k[i - 1] and tup < chosen[i - 1]: continue
            rec(i + 1, chosen + [tup], tot + sum(tup))
    rec(0, [], 0)
    return res
if __name__ == '__main__':
    tot = 0
    for k in vectors():
        S = survivors(k)
        tot += len(S)
        Ds = sorted(set(D for D, _ in S))
        print(''.join(map(str, k)), len(S), 'Delta in', Ds[:3], '...', Ds[-3:] if Ds else '')
    print('total', tot)
