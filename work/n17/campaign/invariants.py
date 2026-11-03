"""Independent invariant checks of a lattice list (jsonl with 'blocks' on n lines), written from the definitions:
linear space (two lines in at most one block, blocks of size >= 3, elements in range), b2 = sum over all points
of (m_P - 1) with the double points included, multiplicities <= mmax, points per line in [smin, smax], the
unjoined-pair cut (no two unjoined points with (m_P - 1) + (m_Q - 1) > 8) with --cut, a double point on every
8-point line with --w4, and pairwise non-isomorphism (pynauty certificates of the line/point incidence graph,
lines and points coloured differently).
usage: invariants.py n file.jsonl b2 smin smax mmax [--cut] [--w4] [--procs k]   -> JSON summary on stdout"""
import sys, json, itertools, collections, hashlib, multiprocessing
import pynauty
n, path, b2exp, smin, smax, mmax = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
CUT = '--cut' in sys.argv; W4 = '--w4' in sys.argv
procs = int(sys.argv[sys.argv.index('--procs') + 1]) if '--procs' in sys.argv else 10

def analyse(blocks):
    viol = []
    bl = [tuple(sorted(b)) for b in blocks]
    cov = {}
    for i, b in enumerate(bl):
        if len(b) < 3: viol.append('block of size < 3')
        if len(set(b)) != len(b) or any(x < 0 or x >= n for x in b): viol.append('bad element')
        for q in itertools.combinations(b, 2):
            if q in cov: viol.append('two lines in two blocks')
            cov[q] = i
    pts = [set(b) for b in bl] + [set(q) for q in itertools.combinations(range(n), 2) if q not in cov]
    b2 = sum(len(P) - 1 for P in pts)
    if b2 != b2exp: viol.append('b2 != %d' % b2exp)
    if max(len(P) for P in pts) > mmax: viol.append('multiplicity > %d' % mmax)
    s = collections.Counter(x for P in pts for x in P)
    if any(not (smin <= s[x] <= smax) for x in range(n)): viol.append('points per line outside [%d, %d]' % (smin, smax))
    if W4 and any(s[x] == 8 and not any(len(P) == 2 and x in P for P in pts) for x in range(n)): viol.append('8-point line without a double point')
    if CUT:
        big = [P for P in pts if len(P) >= 4]
        if any(not (P & Q) and len(P) + len(Q) - 2 > 8 for P, Q in itertools.combinations(big, 2)): viol.append('unjoined pair with (m_P-1)+(m_Q-1) > 8')
    nb = len(bl)
    adj = {n + k: list(B) for k, B in enumerate(bl)}
    g = pynauty.Graph(n + nb, adjacency_dict=adj, vertex_coloring=[set(range(n)), set(range(n, n + nb))] if nb else [set(range(n))])
    cert = hashlib.sha1(pynauty.certificate(g)).digest()
    prof = ''.join(map(str, sorted((s[x] for x in range(n)), reverse=True)))
    mult = tuple(sorted((len(P) for P in pts if len(P) >= 3), reverse=True))
    return cert, tuple(viol), prof, mult, max(s[x] for x in range(n))

def gen():
    with open(path) as f:
        for l in f:
            if l.strip(): yield json.loads(l)['blocks']

if __name__ == '__main__':
    certs = set(); total = 0; viol = collections.Counter(); profiles = collections.Counter(); maxs = collections.Counter(); mults = collections.Counter()
    with multiprocessing.Pool(procs) as pool:
        for cert, v, prof, mult, mx in pool.imap(analyse, gen(), chunksize=1000):
            total += 1; certs.add(cert); maxs[mx] += 1; profiles[prof] += 1; mults[mult] += 1
            for x in v: viol[x] += 1
    print(json.dumps(dict(n=n, b2=b2exp, points_per_line=[smin, smax], mmax=mmax, cut=CUT, w4=W4, total=total, distinct=len(certs),
                          violations=dict(viol), max_points_on_a_line=dict(sorted(maxs.items())),
                          line_profiles=len(profiles), multiplicity_profiles=len(mults),
                          commonest_profiles=[(k, v) for k, v in profiles.most_common(5)])))
