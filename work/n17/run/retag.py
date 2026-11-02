"""Restore the original idx (with class tag) in a fast-filter defer file, using the filter's input file."""
import sys, json
src = [json.loads(l)['idx'] for l in open(sys.argv[1])]
out = []
for l in open(sys.argv[2]):
    r = json.loads(l); r['idx'] = src[r['idx']]; out.append(json.dumps(r))
open(sys.argv[3], 'w').write('\n'.join(out) + ('\n' if out else ''))
