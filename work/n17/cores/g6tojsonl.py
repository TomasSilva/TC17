import sys, json
sys.path.insert(0, '/Users/agent/Projects/TC17/work/n17/heavy')
from g6blocks import decode
d = int(sys.argv[1])
for k, line in enumerate(sys.stdin):
    B = [b for b in decode(line, d) if len(b) >= 3]
    print(json.dumps({'idx': k, 'blocks': B}))
