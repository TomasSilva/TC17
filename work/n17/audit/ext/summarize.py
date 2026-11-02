"""Summary of the extension rerun outputs so far."""
import json, glob, collections
c = collections.Counter(); why = collections.Counter(); st = collections.Counter(); fams = collections.Counter()
done_files = 0; acc = []; rej = []
for f in sorted(glob.glob('out/*.jsonl')):
    for l in open(f):
        r = json.loads(l)
        if 'ALLDONE' in r: done_files += 1; continue
        c[(r['kind'], r['status'])] += 1
        for k, v in r.get('stats', {}).items(): st[k] += v
        for k, v in r.get('sstats', {}).items(): st['special ' + k] += v
        if r['kind'] == 'family' and r['status'] == 'OK':
            fams['param_ok ' + str(r.get('param_ok'))] += 1
            fams['special points'] += r.get('special_points', 0); fams['special degenerate'] += r.get('special_degenerate', 0)
            fams['special noshape'] += r.get('special_noshape', 0)
        for grp in ('found', 'generic', 'special'):
            for x in r.get(grp, []):
                why[(grp, x['why'] or 'accepted')] += 1
                (acc if x['ok'] else rej).append((r['idx'], r['comp'], grp, x['why'], x['L']))
print('files done', done_files, dict(sorted(c.items())))
print('lattices by verdict', dict(sorted(why.items())))
print('search stats', dict(st)); print('families', dict(fams))
json.dump(rej, open('rejected_so_far.json', 'w')); json.dump(acc, open('accepted_so_far.json', 'w'))
