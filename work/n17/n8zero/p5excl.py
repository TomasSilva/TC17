"""Exclusion of the multiplicity vectors of a 5-point line H0 (no 8-point and no 4-point line) that admit no
lattice: pencil5c.py, the complete enumeration with H0 fixed, is run for every one of the eleven vectors, and
the number of heavy configurations, quota systems and lattices is reported.  A vector is excluded when no
lattice exists.  (Until 22 Oct 2026 this file only listed the vectors and did not run the check: audit F2.)
usage: p5excl.py            (from work/n17/n8zero; writes p5c_<vector>.jsonl / .log)"""
import subprocess, sys, re, os
PY = '/Users/agent/Projects/TC17/.venv/bin/python'
vecs = []
def rec(prefix, remaining, slots, maxv):
    if slots == 0:
        if remaining == 0: vecs.append(tuple(prefix))
        return
    for v in range(min(maxv, remaining - (slots - 1)), 0, -1):
        rec(prefix + [v], remaining - v, slots - 1, v)
rec([], 16, 5, 5)
here = os.path.dirname(os.path.abspath(__file__))
print('vector   W(H0)  heavy sets  quota systems  lattices')
for v in vecs:
    name = ''.join(map(str, v))
    with open(os.path.join(here, 'p5c_%s.jsonl' % name), 'w') as out, open(os.path.join(here, 'p5c_%s.log' % name), 'w') as log:
        subprocess.run([PY, os.path.join(here, 'pencil5c.py'), name], stdout=out, stderr=log, cwd=here, check=True)
    txt = open(os.path.join(here, 'p5c_%s.log' % name)).read()
    w0 = re.search(r'W0 (\d+)', txt); hs = re.search(r'heavy sets (\d+)', txt); qs = re.search(r"'quota systems': (\d+)", txt)
    nl = sum(1 for _ in open(os.path.join(here, 'p5c_%s.jsonl' % name)))
    print('%s    %3s     %8s     %8s     %6d%s' % (name, w0.group(1) if w0 else '?', hs.group(1) if hs else '?', qs.group(1) if qs else '0', nl, '   excluded' if nl == 0 else ''))
