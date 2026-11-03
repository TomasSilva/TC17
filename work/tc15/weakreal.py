# Weak realisability of a big-block configuration (blocks of size >= 4 only): is there a point
# configuration in P^2 (dual: points = lines of A) in which every big block is collinear and no
# point lies on the line of a big block it does not belong to?  This is a necessary condition for
# every completion of the configuration by triples, so it can prune stage 2 (and stage 1) exactly.
# Output per configuration: NONREAL, or REAL <#good components> <dims>.
import sys, json, itertools, subprocess, time, os

n = int(sys.argv[1]); IN = sys.argv[2]; part = int(sys.argv[3]); nparts = int(sys.argv[4])
OUT = IN.replace('.jsonl', '_weak_%d.out' % part)
M2 = '/opt/homebrew/bin/M2'


def setup(blocks):
    blocks = [tuple(B) for B in blocks]
    inblock = {}
    for B in blocks:
        for p in itertools.combinations(sorted(B), 2):
            inblock[p] = B

    def collinear(a, b, c):
        B = inblock.get((min(a, b), max(a, b)))
        return B is not None and c in B
    frame = next(f for f in itertools.combinations(range(n), 4)
                 if not any(collinear(*t) for t in itertools.combinations(f, 3)))
    coords = {e: True for e in frame}
    lines, nvar, order = [], 0, list(frame)
    todo = [e for e in range(n) if e not in coords]
    while todo:
        best = None
        for e in todo:
            det_lines = []
            for B in blocks:
                if e in B:
                    D = [x for x in B if x in coords]
                    if len(D) >= 2:
                        det_lines.append((D[0], D[1]))
            if best is None or len(det_lines) > best[1]:
                best = (e, len(det_lines), det_lines)
        e, score, det_lines = best
        todo.remove(e); order.append(e); coords[e] = True
        if score >= 2:
            (a1, b1), (a2, b2) = det_lines[0], det_lines[1]
            lines.append('P%d = cr(cr(P%d, P%d), cr(P%d, P%d));' % (e, a1, b1, a2, b2))
        elif score == 1:
            a1, b1 = det_lines[0]
            lines.append('P%d = P%d + u_%d * P%d;' % (e, a1, nvar, b1)); nvar += 1
        else:
            lines.append('P%d = matrix{{u_%d, u_%d, 1_R}};' % (e, nvar, nvar + 1)); nvar += 2
    eqs, bad = [], []
    for B in blocks:
        Bs = sorted(B, key=lambda x: order.index(x))
        for c in Bs[2:]:
            eqs.append('det(P%d || P%d || P%d)' % (Bs[0], Bs[1], c))
        for x in range(n):
            if x not in B:
                bad.append('det(P%d || P%d || P%d)' % (Bs[0], Bs[1], x))
    return frame, nvar, lines, eqs, bad


def m2_script(items):
    out = ['cr = (p, q) -> matrix{{p_(0,1)*q_(0,2)-p_(0,2)*q_(0,1), p_(0,2)*q_(0,0)-p_(0,0)*q_(0,2), p_(0,0)*q_(0,1)-p_(0,1)*q_(0,0)}};']
    for idx, blocks in items:
        frame, nvar, lines, eqs, bad = setup(blocks)
        s = ['R = QQ[%s];' % (','.join('u_%d' % i for i in range(max(nvar, 1))))]
        s.append('P%d = matrix{{1_R,0,0}}; P%d = matrix{{0_R,1,0}}; P%d = matrix{{0_R,0,1}}; P%d = matrix{{1_R,1,1}};' % frame)
        s += lines
        if nvar == 0:
            eqs = eqs + ['u_0']
        s.append('I = ideal(%s);' % (','.join(eqs) if eqs else 'u_0'))
        s.append('if I == ideal(1_R) then print("CONF %d NONREAL") else (' % idx)
        s.append('bad = {%s}; bad = select(bad, f -> f != 0); zb = %d - #bad;' % (','.join(bad), len(bad)))
        s.append('cs = minimalPrimes I; good = if zb > 0 then {} else select(cs, c -> all(bad, f -> f % c != 0));')
        s.append('print("CONF %d " | (if #good == 0 then "NONREAL" else "REAL " | toString(#good) | " " | toString(apply(good, dim))));' % idx)
        s.append(');')
        out.append('\n'.join(s))
    return '\n'.join(out) + '\nprint("DONE");\n'


def run():
    recs = [json.loads(l) for l in open(IN)]
    mine = [(i, r['blocks']) for i, r in enumerate(recs) if i % nparts == part]
    out = open(OUT, 'w'); t0 = time.time(); B = 40
    for start in range(0, len(mine), B):
        path = IN.replace('.jsonl', '_weak_%d_%d.m2' % (part, start))
        open(path, 'w').write(m2_script(mine[start:start + B]))
        res = subprocess.run([M2, '--script', path], capture_output=True, text=True)
        out.write(res.stdout)
        if 'DONE' not in res.stdout:
            out.write('ERROR batch %d: %s\n' % (start, res.stderr[-1500:]))
        out.flush(); os.remove(path)
        if (start // B) % 25 == 0:
            print('part %d: %d/%d (%.0fs)' % (part, min(start + B, len(mine)), len(mine), time.time() - t0), flush=True)
    out.write('ALLDONE\n'); out.close()


if __name__ == '__main__':
    run()
