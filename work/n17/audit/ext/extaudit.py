"""Audit rerun of the extension step of the 17-line proof (22 Oct 2026).

Every component of every realisable core and child is extended again, with the geometry of
work/n17/comp (extend.py, famext.py, famspecial2.py, planemodel.py) and four changes:
  1. exact memoisation in the rigid search: a hit on the mod-p key of a set of added lines is accepted
     only if the stored lines are equal to the current ones exactly; otherwise the branch is explored;
  2. every 17-line lattice found is recorded with its window verdict (accepted, or the rule rejecting it),
     generic and special lattices of families alike;
  3. one output record per component, written when the component is finished (completion marker);
  4. for families: a check that the parametrisation stored with the component equals the one rebuilt by
     exact_tc_lattice.setup (which famspecial2.points_over uses), and counts of the special points at
     which B degenerates or that have no shape lemma.
usage: extaudit.py records.jsonl out.jsonl [rigid|family|all] [famtimeout] [allspecial]"""
import sys, json, time, collections, os, signal
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/comp')
sys.path.insert(0, '/Users/agent/Projects/TC17/work/tc15')
IN, OUT = sys.argv[1], sys.argv[2]
KIND = sys.argv[3] if len(sys.argv) > 3 else 'all'
FAMTO = int(sys.argv[4]) if len(sys.argv) > 4 else 600
ALLSP = len(sys.argv) > 5 and sys.argv[5] == 'allspecial'
_saved = list(sys.argv); sys.argv = ['x', '13', '6', '/dev/null', '0', '1']
import exact_tc_lattice as ex
sys.argv = _saved
import extend as eg
import famext as fe
from planemodel import plane_model
from famspecial2 import points_over
fe.ALLSPECIAL = ALLSP

def search_exact(F, lines, pts, budget, depth, found, added, akeys, avecs, visited, phicap, stats):
    n = len(lines)
    stats['nodes'] += 1
    if added and eg.phi_reaches([L for Q, L in pts], n, phicap):
        stats['phipruned'] += 1; return
    if depth == 0:
        if budget == 0: found.append([sorted(L) for Q, L in pts])
        return
    s = collections.Counter()
    for Q, L in pts:
        for x in L: s[x] += 1
    cmax = min(8, budget - 2 * (depth - 1)); cmin = max(2, budget - 8 * (depth - 1))
    if cmax < cmin: return
    cand = {}
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if pts[i][1] & pts[j][1]: continue
            N = eg.cross(F, pts[i][0], pts[j][0])
            k = eg.keyp(F, N)
            if k is None:
                if eg.iszerovec(F, N): continue
                k = ('deg', i, j)
            if k in cand:
                if any(eg.iszerovec(F, eg.cross(F, N, M)) for M in cand[k]): continue
                cand[k].append(N); stats['samekey distinct candidates'] += 1
            else:
                cand[k] = [N]
    lkeys = set(eg.keyp(F, X) for X in lines)
    for k, N in [(k, N) for k, Ns in cand.items() for N in Ns]:
        if k in lkeys and any(eg.iszerovec(F, eg.cross(F, N, X)) for X in lines): continue
        T = [t for t, (Q, L) in enumerate(pts) if eg.dotp(F, N, Q) == 0 and F.iszero(eg.dot(F, N, Q))]
        if len(T) < 2: continue
        covered = set(); okd = True
        for t in T:
            L = pts[t][1]
            if covered & L: okd = False; break
            covered |= L
            if len(L) > 5: okd = False; break
        if not okd: continue
        c = len(T) + n - len(covered)
        if not (cmin <= c <= cmax): continue
        if any(s[x] + 1 > 8 for x in range(n) if x not in covered): continue
        keys_here = akeys + [k]
        if len(set(keys_here)) == len(keys_here):
            st = frozenset(keys_here)
            prev = visited.get(st)
            if prev is not None:
                cur = dict(zip(akeys, avecs)); cur[k] = N
                if all(eg.iszerovec(F, eg.cross(F, prev[x], cur[x])) for x in keys_here):
                    stats['memo hits'] += 1; continue
                stats['memo key collisions (explored)'] += 1
            else:
                cur = dict(zip(akeys, avecs)); cur[k] = N
                visited[st] = cur
        else:
            stats['repeated key in branch (explored)'] += 1
        newpts = []
        Tset = set(T)
        for t, (Q, L) in enumerate(pts):
            newpts.append((Q, L | {n}) if t in Tset else (Q, L))
        for x in range(n):
            if x not in covered:
                newpts.append((eg.cross(F, N, lines[x]), frozenset((x, n))))
        search_exact(F, lines + [N], newpts, budget - c, depth - 1, found, added + [k], keys_here, avecs + [N], visited, phicap, stats)

def verdicts(found):
    out = {}
    for blocks in found:
        key = json.dumps(sorted(sorted(b) for b in blocks if len(b) >= 3))
        if key in out: continue
        ok, why = eg.window_ok(blocks)
        out[key] = dict(L=json.loads(key), ok=ok, why=why)
    return list(out.values())

def b2_of(pts): return sum(len(L) - 1 for Q, L in pts)

def rigid(rec, ci, comp, cap):
    res = dict(idx=rec['idx'], comp=ci, kind='rigid', n=len(rec['lines']) + 4)
    if 'g' not in comp:
        res['status'] = 'NOSHAPE'; return res
    F = eg.Field(eg.parse_list(comp['f']))
    lines = eg.realise(F, rec, comp)
    pts = eg.points_of(F, lines)
    if eg.lattice_blocks(pts) != sorted(sorted(b) for b in rec['blocks']):
        res['status'] = 'LATTICE-MISMATCH'; return res
    found = []; stats = collections.Counter()
    search_exact(F, lines, pts, 80 - b2_of(pts), 17 - len(lines), found, [], [], [], {}, cap, stats)
    res.update(status='OK', stats=dict(stats), found=verdicts(found))
    return res

def family(rec, ci, comp, cap):
    res = dict(idx=rec['idx'], comp=ci, kind='family', n=len(rec['lines']) + 4)
    frame, nvar, lns_setup, eqs, bad, pts0 = (None,) * 6
    try:
        ex.n = len(rec['lines']) + 4
        frame, nvar, lns_setup, eqs, bad, pts0 = ex.setup(rec['blocks'])
        res['param_ok'] = (list(frame) == list(rec['frame']) and list(lns_setup) == list(rec['lines']) and nvar == rec['nvar'])
    except Exception as e:
        res['param_ok'] = 'EXC ' + repr(e)[:100]
    def _alarm(sig, frm): raise TimeoutError('family time limit')
    signal.signal(signal.SIGALRM, _alarm); signal.alarm(FAMTO)
    t0 = time.time()
    try:
        pm = plane_model(rec['nvar'], comp['gens'], tag='a%d_%d' % (os.getpid(), ci))
        if pm['kind'] not in ('A1', 'plane'):
            pm = plane_model(rec['nvar'], comp['gens'], tag='a%d_%d' % (os.getpid(), ci), tries=int(os.environ.get('EXTAUDIT_TRIES', '40')))
        if pm['kind'] not in ('A1', 'plane'):
            res['status'] = 'NOMODEL'; return res
        C = fe.Curve(pm)
        fe.REMOVED.clear(); fe.special_cache.clear(); fe.FACTOR_CACHE.clear()
        lines, cs = fe.realise_sym(C, rec, pm)
        pts = fe.points_sym(C, lines)
        if sorted(sorted(L) for Q, L in pts if len(L) >= 3) != sorted(sorted(b) for b in rec['blocks']):
            res['status'] = 'LATTICE-MISMATCH'; return res
        b2 = b2_of(pts)
        found = []; special = {}; stats = collections.Counter()
        fe.gsearch(C, lines, pts, 80 - b2, 17 - len(lines), found, special, stats, cap)
        for c in cs + fe.REMOVED:
            if not c.is_constant():
                r = C.res(c)
                if not r.is_zero() and not r.is_constant(): special[str(r)] = r
        facs = {}
        for r in special.values():
            if r.is_constant(): continue
            for f, mult in r.factor()[1]:
                if f.degrees()[1] == 0 and not f.is_constant(): facs[str(f)] = f
        res['generic'] = verdicts(found)
        ok, sp, err = points_over(rec, comp, pm, list(facs.keys()), tag='a%d_%d' % (os.getpid(), ci), nlines=len(lines))
        if not ok:
            res['status'] = 'SPECIAL-ERROR'; res['err'] = err; return res
        allfound = []; nosh = 0; degen = 0; sstats = collections.Counter()
        for spc in sp:
            if spc.get('noshape'): nosh += 1; continue
            F = eg.Field(eg.parse_list(spc['f']))
            lns = eg.realise(F, rec, spc)
            ps = eg.points_of(F, lns)
            if eg.lattice_blocks(ps) != sorted(sorted(b) for b in rec['blocks']):
                degen += 1; continue
            search_exact(F, lns, ps, 80 - b2, 17 - len(lns), allfound, [], [], [], {}, cap, sstats)
        res.update(status='OK', gnodes=stats['nodes'], special_factors=len(facs), special_points=len(sp),
                   special_noshape=nosh, special_degenerate=degen, sstats=dict(sstats), special=verdicts(allfound))
    except TimeoutError:
        res['status'] = 'SLOW'
    except Exception as e:
        res['status'] = 'EXC'; res['err'] = repr(e)[:300]
    finally:
        signal.alarm(0)
        res['time'] = round(time.time() - t0, 1)
    return res

if __name__ == '__main__':
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            try:
                r = json.loads(l); done.add((str(r['idx']), r['comp']))
            except Exception: pass
    with open(OUT, 'a') as out:
        for line in open(IN):
            rec = json.loads(line)
            if rec.get('status') != 'REAL': continue
            cap = eg.CAP.get(str(rec['idx']).split(':')[0])
            for ci, comp in enumerate(rec['comps']):
                if (str(rec['idx']), ci) in done: continue
                t0 = time.time()
                if comp['dim'] == 0:
                    if KIND == 'family': continue
                    try: r = rigid(rec, ci, comp, cap)
                    except Exception as e: r = dict(idx=rec['idx'], comp=ci, kind='rigid', status='EXC', err=repr(e)[:300])
                elif comp['dim'] == 1:
                    if KIND == 'rigid': continue
                    r = family(rec, ci, comp, cap)
                else:
                    if KIND == 'family': continue
                    r = dict(idx=rec['idx'], comp=ci, kind='dim>=2', n=len(rec['lines']) + 4, status='DIM>=2')
                r['src'] = rec.get('_source', 'core'); r['cap'] = cap; r['wall'] = round(time.time() - t0, 2)
                out.write(json.dumps(r) + '\n'); out.flush()
        out.write(json.dumps(dict(ALLDONE=IN)) + '\n')
