"""Compare the rigid reruns of rerun/ (made after the memoisation change of TC_N17.md section 7) with the
original runs: distinct lattices up to isomorphism.  Output: rerun/compare.out."""
import json, sys, glob
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/validate')
from canon import canon_many
R = '/Users/agent/Projects/TC17/work/n17/run/'
def lat(files):
    out = []
    for f in files:
        for l in open(f):
            r = json.loads(l)
            if 'L' in r: out.append(r['L'])
            out += r.get('generic_L', []) + r.get('special_L', [])
    return out
final = set(json.loads(l)['canon'] for l in open(R + 'checked_L.jsonl'))
pairs = [('b4849', ['ext_b4849_rigid.jsonl'], ['rerun/r_b4849_ext.jsonl']),
         ('d2c', ['d2c_rigid_ext.jsonl'], ['rerun/r_d2c_ext.jsonl']),
         ('b49d2', sorted(glob.glob(R + 'b49d2n15_n1[56]_ext_*.jsonl')), ['rerun/r_b49d2_ext.jsonl']),
         ('b50n13', sorted(glob.glob(R + 'b50_n13_ext_*.jsonl')), ['rerun/r_b50n13_ext.jsonl'])]
for name, orig, new in pairs:
    o = lat([f if f.startswith('/') else R + f for f in orig]); n = lat([R + f for f in new])
    co = set(canon_many(17, o)) if o else set(); cn = set(canon_many(17, n)) if n else set()
    print(name, 'orig records', len(o), 'distinct', len(co), '| rerun records', len(n), 'distinct', len(cn),
          '| rerun subset of orig', cn <= co, '| equal', cn == co, '| all in final 16', (co | cn) <= final)
