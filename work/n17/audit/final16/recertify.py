"""Re-certify the 16 realisable window lattices with the exact code of Anghel-Stan (arXiv:2610.25868,
ancillary files): realisation space (construction over Z[t]) and freeness on every Galois orbit
(Ziegler multirestriction rank over the residue field; d1 = 8, so full rank is 16).
usage: recertify.py /path/to/anghel-stan/anc"""
import sys, json, flint
sys.path.insert(0, sys.argv[1])
from realize import Matroid
from exact import realization_space, certify_component
names = {'census5_classes.jsonl:0': 'R17a', 'census5_classes.jsonl:4': 'R17b', 'del17.jsonl:10': 'E17'}
k = 0
for l in open('/Users/agent/Projects/TC17/work/n17/run/checked_L.jsonl'):
    r = json.loads(l)
    M = Matroid(17, [frozenset(b) for b in r['blocks'] if len(b) >= 3])
    R = realization_space(M)
    if r['known'] in names: lab = names[r['known']]
    elif r['known']: lab = r['known']
    else: k += 1; lab = 'N%d' % k
    if R['status'] == 'points':
        out = [(c.degree(), certify_component(M, R['lines'], c, 8)) for c in R['comps']]
    elif R['status'] == 'family' and all(c.degree() <= 0 for v in R['lines'] for c in v):   # cost 0: one point
        out = [(1, certify_component(M, R['lines'], flint.fmpz_poly([0, 1]), 8))]
    else:
        out = R['status']
    print(lab, R['status'], out)
