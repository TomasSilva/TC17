import sys, time, itertools, collections
sys.argv = ['pencil5.py', sys.argv[1], sys.argv[2], sys.argv[3]]
src = open('pencil5.py').read()
# run step 1 only, then probe step 2 on the requested heavy set with a node/solution counter and time limit
s1 = src[:src.index("# Step 2")]
exec(s1)
hsl = list(uniq.values())
which = int(sys.argv[2]); tlim = float(sys.argv[3])
hs = hsl[which]
Woff = sum(wt(S) for S in hs); W = W0 + Woff
t5 = t5_0 + sum(1 for S in hs if len(S) == 5); t6 = t6_0 + sum(1 for S in hs if len(S) == 6)
t2 = 3 * W - 32 - t5 - 3 * t6; t2_off = t2 - b0
print('heavy set', which, 'of', len(hsl), hs, 'W', W, 't2_off', t2_off)
covered = set(); noff = [0] * 16
for S in hs:
    for p in itertools.combinations(S, 2): covered.add(p)
    for x in S: noff[x] += 1
rem = [p for p in cross if p not in covered]
tri_ok = [T for T in transversals(3) if not any(p in covered for p in itertools.combinations(T, 2))]
by_pair = collections.defaultdict(list)
for T in tri_ok:
    for p in itertools.combinations(T, 2): by_pair[p].append(T)
cov = set(covered); nd = [0]; nodes = [0]; nsol = [0]; t0 = time.time()
class Stop(Exception): pass
def rec():
    nodes[0] += 1
    if time.time() - t0 > tlim: raise Stop
    best = None; bo = None
    for p in rem:
        if p in cov: continue
        opts = [T for T in by_pair[p] if not any(q in cov for q in itertools.combinations(T, 2)) and all(noff[x] < 6 for x in T)]
        nopt = len(opts) + (1 if (nd[0] < t2_off and noff[p[0]] < 6 and noff[p[1]] < 6) else 0)
        if nopt == 0: return
        if best is None or nopt < bo[0]:
            best, bo = p, (nopt, opts)
            if nopt == 1: break
    if best is None:
        nsol[0] += 1; return
    p = best
    for T in bo[1]:
        for q in itertools.combinations(T, 2): cov.add(q)
        for x in T: noff[x] += 1
        rec()
        for x in T: noff[x] -= 1
        for q in itertools.combinations(T, 2): cov.discard(q)
    if nd[0] < t2_off and noff[p[0]] < 6 and noff[p[1]] < 6:
        cov.add(p); noff[p[0]] += 1; noff[p[1]] += 1; nd[0] += 1
        rec()
        nd[0] -= 1; noff[p[0]] -= 1; noff[p[1]] -= 1; cov.discard(p)
try:
    rec(); print('complete: nodes', nodes[0], 'solutions', nsol[0], '%.1fs' % (time.time() - t0))
except Stop:
    print('stopped: nodes', nodes[0], 'solutions so far', nsol[0], '%.1fs' % (time.time() - t0))
