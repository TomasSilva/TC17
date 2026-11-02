"""Chains of 8-point lines from lattice data (blocks = points with >= 3 lines; n lines 0..n-1).
A k-chain is a set S of k lines with b2(L \\ S) = b2(L) - 8k (then every deletion order removes 8 points)."""
import sys, json, itertools
def b2(n, blocks, keep):
    keep = set(keep); cov = set(); tot = 0
    for B in blocks:
        r = [i for i in B if i in keep]
        if len(r) >= 2:
            tot += len(r) - 1
            cov.update(itertools.combinations(sorted(r), 2))
    pairs = itertools.combinations(sorted(keep), 2)
    return tot + sum(1 for q in pairs if q not in cov)
def analyse(n, blocks):
    allL = list(range(n)); B0 = b2(n, blocks, allL)
    s = {i: 0 for i in allL}
    for i in allL:
        s[i] = B0 - b2(n, blocks, [j for j in allL if j != i])   # points on line i
    eight = [i for i in allL if s[i] == 8]
    res = {}
    for k in range(1, 5):
        res[k] = sum(1 for S in itertools.combinations(eight, k)
                     if b2(n, blocks, [j for j in allL if j not in S]) == B0 - 8 * k)
    return B0, sorted(s.values()), len(eight), res
if __name__ == '__main__':
  for fn in sys.argv[1:]:
    for line in open(fn):
        rec = json.loads(line)
        n = rec.get('n', 17)
        B0, svals, k8, res = analyse(n, rec['blocks'])
        tag = rec.get('source', '') + str(rec.get('sizes', rec.get('deleted', '')))
        print('%-28s b2=%d  points/line=%s  k8=%d  chains(k=1..4)=%s' % (tag[:28], B0, ''.join(str(v) for v in svals), k8, [res[k] for k in range(1,5)]))
