"""Re-certification of 17-line lattices with the exact code of Anghel-Stan (arXiv:2610.25868, ancillary files):
realisation space (construction over Z[t]) and, on every irreducible component of dimension 0, freeness by the
rank of the Ziegler multirestriction (d1 = 8: full rank 16 means free).
usage: as_recertify.py lattices.jsonl out.jsonl"""
import sys, json, flint
sys.path.insert(0, '/Users/agent/Projects/TC17/third_party/anghel_stan_anc/anc')
from realize import Matroid
from exact import realization_space, certify_component, Degenerate
with open(sys.argv[2], 'w') as out:
    for l in open(sys.argv[1]):
        if not l.strip(): continue
        r = json.loads(l)
        res = dict(idx=r.get('idx'), known=r.get('known'))
        try:
            M = Matroid(17, [frozenset(b) for b in r['blocks'] if len(b) >= 3])
            R = realization_space(M)
            res['status'] = R['status']; res['cost'] = R.get('cost')
            if R['status'] == 'points':
                res['comps'] = [(c.degree(), certify_component(M, R['lines'], c, 8)[0]) for c in R['comps']]
            elif R['status'] == 'family' and all(c.degree() <= 0 for v in R['lines'] for c in v):
                res['status'] = 'family-point'
                res['comps'] = [(1, certify_component(M, R['lines'], flint.fmpz_poly([0, 1]), 8)[0])]
        except Degenerate:
            res['status'] = 'empty-degenerate'
        except Exception as e:
            res['status'] = 'error'; res['error'] = repr(e)[:300]
        out.write(json.dumps(res) + '\n'); print(json.dumps(res), flush=True)
