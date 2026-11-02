"""Collect all 17-line lattices found by the extension runs, dedup up to isomorphism, compare with the
known window lattices, and write the new ones (not yet TC-checked) to todo_L.jsonl."""
import json, sys, glob, os
sys.path.insert(0, '../validate')
from canon import canon_many
known = []
for f in ['../../build/del17.jsonl', '../../build/census5_classes.jsonl']:
    for i, l in enumerate(open(f)):
        known.append((os.path.basename(f) + ':%d' % i, json.loads(l)['blocks']))
kc = dict(zip(canon_many(17, [b for _, b in known]), [n for n, _ in known]))
found = {}
for f in sys.argv[1:]:
    for l in open(f):
        r = json.loads(l)
        for key in ('L',):
            if key in r: found.setdefault('x', []).append((r['idx'], r['L']))
        for L in r.get('generic_L', []) + r.get('special_L', []):
            found.setdefault('x', []).append((r['idx'], L))
allL = found.get('x', [])
cs = canon_many(17, [L for _, L in allL]) if allL else []
distinct = {}
src = {}
for (idx, L), c in zip(allL, cs):
    distinct.setdefault(c, L); src.setdefault(c, set()).add(idx)
done = {}
if os.path.exists('checked_L.jsonl'):
    for l in open('checked_L.jsonl'):
        r = json.loads(l); done[r['canon']] = r
todo = []
for c, L in distinct.items():
    status = 'known ' + kc[c] if c in kc else ('checked' if c in done else 'NEW')
    print(status, 'from', len(src[c]), 'cores e.g.', sorted(map(str, src[c]))[:3])
    if c not in done: todo.append(dict(canon=c, blocks=L, known=kc.get(c)))
with open('todo_L.jsonl', 'w') as f:
    for k, t in enumerate(todo):
        t['idx'] = k; f.write(json.dumps(t) + '\n')
print('distinct', len(distinct), 'known', sum(1 for c in distinct if c in kc), 'to check', len(todo))
