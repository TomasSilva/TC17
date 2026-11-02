"""For chains stored in NAME_chains.json, delete each chain (sample) and report the degrees of the
minimal generators of the Jacobian syzygy module (via Macaulay2)."""
import sys, json, subprocess, random
name = sys.argv[1]; nper = int(sys.argv[2])
D = json.load(open(name + '_chains.json'))
p, L, chains = D['p'], D['lines'], D['chains']
random.seed(1)
bylen = {}
for c in chains: bylen.setdefault(len(c), []).append(c)
jobs = []
for k in sorted(bylen):
    cs = bylen[k]
    jobs += [c for c in (cs if len(cs) <= nper else random.sample(cs, nper))]
m2 = ['R = ZZ/%d[x,y,z];' % p, 'f = method(); f List := S -> (',
      '  Q := product(S, l -> l#0*x + l#1*y + l#2*z);',
      '  J := matrix{{diff(x,Q), diff(y,Q), diff(z,Q)}};',
      '  K := syz J; M := image K; G := mingens M;',
      '  sort apply(numcols G, i -> (degrees source G)#i#0 - (first degree Q) + 1));']
for c in jobs:
    S = [L[i] for i in range(len(L)) if i not in c]
    m2.append('print(toString(%s) | " : " | toString(f(%s)));' % (json.dumps(c).replace('[','{').replace(']','}'),
              json.dumps([list(l) for l in S]).replace('[','{').replace(']','}')))
open(name + '_syz.m2', 'w').write('\n'.join(m2) + '\n')
out = subprocess.run(['/opt/homebrew/bin/M2', '--script', name + '_syz.m2'], capture_output=True, text=True)
print(out.stdout[-6000:], out.stderr[-2000:])
