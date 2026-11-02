"""Full exact treatment of the 1-dimensional family components of the core realisation spaces:
plane model -> generic search on the curve (famext) -> points over the special factors (Macaulay2) ->
exact rigid search at every special point (extend).  Output jsonl: one record per component with the
17-line lattices found generically and at special points, and every point count, for the record."""
import sys, json, time, collections, os
sys.path.insert(0, '/Users/agent/Projects/TC17/work/tc15')
sys.argv_saved = list(sys.argv)
sys.argv = ['x', '13', '6', '/dev/null', '0', '1']
import exact_tc_lattice as ex
sys.argv = sys.argv_saved
import famext as fe
import extend as eg
from planemodel import plane_model
from famspecial2 import points_over
IN, OUT, part, nparts = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
if len(sys.argv) > 5 and sys.argv[5] == 'all': fe.ALLSPECIAL = True
SKIP = set()
for f in sys.argv[5:]:
    if f != 'all':
        try:
            for l in open(f):
                try:
                    r = json.loads(l)
                    if r.get('status') in ('OK', 'DIM>=2'): SKIP.add((str(r['idx']), r['comp']))
                except Exception: pass
        except FileNotFoundError: pass
with open(OUT, 'a') as out:
    for li, line in enumerate(open(IN)):
        if li % nparts != part: continue
        rec = json.loads(line)
        if rec.get('status') != 'REAL': continue
        for ci, comp in enumerate(rec.get('comps', [])):
            if comp['dim'] == 0: continue
            if (str(rec['idx']), ci) in SKIP: continue
            t0 = time.time()
            res = dict(idx=rec['idx'], comp=ci, dim=comp['dim'], gens=comp['gens'])
            if comp['dim'] > 1:
                res['status'] = 'DIM>=2'; out.write(json.dumps(res) + '\n'); out.flush(); continue
            import signal
            def _alarm(sig, frm): raise TimeoutError('family time limit')
            signal.signal(signal.SIGALRM, _alarm); signal.alarm(int(os.environ.get('FAM_TIMEOUT', '180')))
            try:
                pm = plane_model(rec['nvar'], comp['gens'], tag='%d_%d_%d' % (part, li, ci))
                if pm['kind'] not in ('A1', 'plane'):
                    pm = plane_model(rec['nvar'], comp['gens'], tag='%d_%d_%d' % (part, li, ci), tries=40)
                if pm['kind'] not in ('A1', 'plane'):
                    res['status'] = 'NOMODEL'; out.write(json.dumps(res) + '\n'); out.flush(); continue
                C = fe.Curve(pm)
                fe.REMOVED.clear(); fe.special_cache.clear(); fe.FACTOR_CACHE.clear()
                lines, cs = fe.realise_sym(C, rec, pm)
                pts = fe.points_sym(C, lines)
                if sorted(sorted(L) for Q, L in pts if len(L) >= 3) != sorted(sorted(b) for b in rec['blocks']):
                    res['status'] = 'LATTICE-MISMATCH'; out.write(json.dumps(res) + '\n'); out.flush(); continue
                b2 = sum(len(L) - 1 for Q, L in pts)
                found = []; special = {}; stats = collections.Counter()
                cap = eg.CAP.get(str(rec['idx']).split(':')[0])
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
                res['generic_L'] = []
                for blocks in found:
                    okw, why = eg.window_ok(blocks)
                    if okw: res['generic_L'].append([b for b in blocks if len(b) >= 3])
                    else: res.setdefault('rejected', []).append(dict(L=[b for b in blocks if len(b) >= 3], why=why))
                ok, sp, err = points_over(rec, comp, pm, list(facs.keys()), tag='%d_%d_%d' % (part, li, ci), nlines=len(lines))
                if not ok:
                    res['status'] = 'SPECIAL-ERROR'; res['err'] = err; out.write(json.dumps(res) + '\n'); out.flush(); continue
                Ls = {}
                nosh = 0
                for spc in sp:
                    if spc.get('noshape'): nosh += 1; continue
                    F = eg.Field(eg.parse_list(spc['f']))
                    lns = eg.realise(F, rec, spc)
                    ps = eg.points_of(F, lns)
                    if eg.lattice_blocks(ps) != sorted(sorted(b) for b in rec['blocks']):
                        continue   # special point at which B itself degenerates: not a realisation of B
                    fnd = []
                    eg.search(F, lns, ps, 80 - b2, 17 - len(lns), fnd, [], {}, cap)
                    for keys, blocks in fnd:
                        okw, why = eg.window_ok(blocks)
                        if okw:
                            key = json.dumps(sorted(sorted(b) for b in blocks if len(b) >= 3))
                            Ls[key] = [b for b in blocks if len(b) >= 3]
                        else:
                            res.setdefault('rejected', []).append(dict(L=[b for b in blocks if len(b) >= 3], why=why))
                res.update(status='OK', nodes=stats['nodes'], special_factors=len(facs), special_points=len(sp),
                           special_noshape=nosh, special_L=list(Ls.values()), time=round(time.time() - t0, 1))
            except TimeoutError:
                res['status'] = 'SLOW'
            except Exception as e:
                res['status'] = 'EXC'; res['err'] = repr(e)[:300]
            signal.alarm(0)
            out.write(json.dumps(res) + '\n'); out.flush()
