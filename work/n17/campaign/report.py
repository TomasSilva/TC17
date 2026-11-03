"""Build REPORT.md from done/*.json and done/*.FAILED of the campaign."""
import json, glob, os, time, collections
C = '/Users/agent/Projects/TC17/work/n17/campaign'
ORDER = ['prep', 'cover', 'n8zero', 'cores', 'indep_cores', 'filters', 'as_cores', 'm2', 'ext_b48', 'ext_b48w', 'ext_b49', 'ext_b50', 'ext_b51', 'route_timeouts', 'as_children', 'indep_rigid', 'final', 'report']
DESC = {'prep': 'tools, compiled enumerators, SHA-256 of the code of record', 'cover': 'covering lemma (ILP: level 1, Farkas certificates, propagation, glpsol, validation)',
        'n8zero': 'no 8-point line (K4444, five-point vectors, screening, Anghel-Stan)', 'cores': 'core classes b48, b48w, b49, b50, b51 (heavyaug_p + lsgen3 + labelg), invariants, positive controls',
        'indep_cores': 'second enumerator (bigblocks + fill_triples) and comparison', 'filters': 'exact fast filters on every core', 'as_cores': "Anghel-Stan's code on every core",
        'm2': 'Macaulay2 components of the deferred cores; comparison with Anghel-Stan; filter-only cores confirmed', 'ext_b48': 'extension of class b48', 'ext_b48w': 'extension of class b48w (8-point lines allowed; the class the manuscript leaves open)',
        'ext_b49': 'extension of class b49', 'ext_b50': 'extension of class b50', 'ext_b51': 'extension of class b51',
        'route_timeouts': 'the cores/children on which Macaulay2 timed out, routed through the lattice-level step (as in October 2026); their children screened with Anghel-Stan', 'as_children': "Anghel-Stan's code on every child of the lattice-level step",
        'indep_rigid': 'independent numeric rigid search on every rigid component', 'final': 'collection of the lattices found, exact realisation spaces and freeness, syzygy degrees, Anghel-Stan re-certification', 'report': 'this report'}
lines = ['# Campaign report: rerun of the 17-line proof', '', 'Generated %s by `work/n17/campaign/report.py` from `done/*.json`. Log: `campaign.log`.' % time.strftime('%Y-%m-%d %H:%M:%S'), '']
mism, status = [], {}
for st in ORDER:
    f = C + '/done/%s.json' % st; ff = C + '/done/%s.FAILED' % st
    if os.path.exists(f): status[st] = ('done', json.load(open(f)))
    elif os.path.exists(ff): status[st] = ('FAILED', json.load(open(ff)))
    else: status[st] = ('not run', {})
lines += ['## Stages', '', '| stage | status | finished | seconds | what |', '|---|---|---|---|---|']
for st in ORDER:
    s, info = status[st]
    lines.append('| %s | %s | %s | %s | %s |' % (st, s, info.get('_finished', ''), info.get('_seconds', ''), DESC.get(st, '')))
for st in ORDER:
    s, info = status[st]
    for k, v in info.items():
        if isinstance(v, dict) and 'ok' in v and v['ok'] is False: mism.append((st, k, v['got'], v['expected']))
EXPLAIN = {('cover', 'propagation check: infeasible'): 'the figure 2,435 in the manuscripts came from an incomplete run of propcheck.py (its output files stop at system 614 of 2,471); the complete, deterministic run gives 2,333 refuted and 138 open, all 138 settled by the exact Farkas certificates. Both manuscripts corrected on 2 Nov 2026.',
           ('cover', 'propagation check: open (settled by Farkas)'): 'same cause as the line above.',
           ('ext_b51', 'Macaulay2 timeouts/errors among cores and children'): 'the expectation 0 was wrong: the run of October 2026 also had exactly two Macaulay2 timeouts, on the same two 14-line children of b51 (same canonical forms); the stage route_timeouts routes them through the lattice-level step as in October (142 children with 15 lines, none realisable, no 17-line lattice).'}
lines += ['', '## Mismatches against the recorded values of 21-23 October 2026', '']
if mism:
    lines += ['| stage | check | got | expected |', '|---|---|---|---|'] + ['| %s | %s | %s | %s |' % (st, k, json.dumps(g)[:120], json.dumps(e)[:120]) for st, k, g, e in mism]
    lines += ['', 'Explanations:', ''] + ['- **%s / %s:** %s' % (st, k, EXPLAIN.get((st, k), 'unexplained')) for st, k, g, e in mism]
else:
    lines.append('None: every check with a recorded value reproduced it' + (' (some stages failed or did not run: see the table).' if any(s != 'done' for s, _ in status.values()) else '.'))
lines += ['', '## Checks, stage by stage', '']
for st in ORDER:
    s, info = status[st]
    if s == 'not run': continue
    lines += ['### %s (%s)' % (st, s), '']
    if '_error' in info: lines += ['**Error:** `%s`' % info['_error'], '']
    rows = []
    for k, v in info.items():
        if k.startswith('_'): continue
        if isinstance(v, dict) and 'ok' in v and 'got' in v:
            rows.append('| %s | %s | %s | %s |' % (k, json.dumps(v['got'])[:140], 'n/a' if v['expected'] is None else json.dumps(v['expected'])[:100], 'OK' if v['ok'] else '**MISMATCH**'))
        else:
            txt = json.dumps(v)
            rows.append('| %s | %s | | recorded |' % (k, (txt[:300] + ('...' if len(txt) > 300 else '')).replace('|', '\\|')))
    if rows: lines += ['| check | value | recorded value (Oct 2026) | |', '|---|---|---|---|'] + rows + ['']
open(C + '/REPORT.md', 'w').write('\n'.join(lines) + '\n')
print('REPORT.md written:', len(mism), 'mismatches;', {st: s for st, (s, _) in status.items()})
