"""Counting test for case (gamma): every 4-set of long lines (7 or 8 points) must contain a 'full' point
(a double point between two of them, a triple point all of whose 3 lines are among them, or a 4-fold
point all of whose 4 lines are among them).  Double points hit C(n-2,2) 4-sets, full triples n-3,
full quads 1.  Numerics: W = t4+3t5+6t6, t3 = 56-3t4-6t5-10t6, t2 = 3W-32-t5-3t6 (>=0), W<=2k8+k7-2,
W>=11 (and W<=31), double points on long lines: 8-line <= 6, 7-line <= 4.  Triples among long lines are
edge-disjoint triangles (<= C(n,2)/3)."""
from math import comb
feasible = []
for t6 in range(0, 4):
    for t5 in range(0, 11):
        for t4 in range(0, 33):
            W = t4 + 3 * t5 + 6 * t6
            if W < 11 or W > 31: continue
            t3 = 56 - 3 * t4 - 6 * t5 - 10 * t6
            t2 = 3 * W - 32 - t5 - 3 * t6
            if t3 < 0 or t2 < 0: continue
            for k8 in range(0, 18):
                for k7 in range(0, 18 - k8):
                    n = k8 + k7
                    if n < 4 or W > 2 * k8 + k7 - 2: continue
                    D = min(t2, (6 * k8 + 4 * k7) // 2, comb(n, 2))
                    T = min(t3, comb(n, 2) // 3)
                    Q = t4
                    if D * comb(n - 2, 2) + T * (n - 3) + Q >= comb(n, 4):
                        feasible.append((W, t4, t5, t6, k8, k7))
print(len(feasible), 'parameter tuples pass the counting test')
import collections
print('by n=k8+k7:', sorted(collections.Counter(k8 + k7 for _, _, _, _, k8, k7 in feasible).items()))
print('by W:', sorted(collections.Counter(W for W, *_ in feasible).items()))
