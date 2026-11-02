import sys, json, random, subprocess
name, k, nsamp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
D = json.load(open(name + '_chains.json')); p, L = D['p'], D['lines']
random.seed(k)
subs = set()
while len(subs) < nsamp:
    subs.add(tuple(sorted(random.sample(range(len(L)), k))))
m2 = ['R = ZZ/%d[x,y,z];' % p, 'f = method(); f List := S -> (',
      '  Q := product(S, l -> l#0*x + l#1*y + l#2*z);',
      '  J := matrix{{diff(x,Q), diff(y,Q), diff(z,Q)}};',
      '  G := mingens image syz J;',
      '  sort apply(numcols G, i -> (degrees source G)#i#0 - (first degree Q) + 1));']
for c in sorted(subs):
    S = [L[i] for i in range(len(L)) if i not in c]
    m2.append('print(toString(%s) | " : " | toString(f(%s)));' % (str(list(c)).replace('[','{').replace(']','}'),
              json.dumps([list(l) for l in S]).replace('[','{').replace(']','}')))
open('rd.m2', 'w').write('\n'.join(m2) + '\n')
out = subprocess.run(['/opt/homebrew/bin/M2', '--script', 'rd.m2'], capture_output=True, text=True)
print(out.stdout, out.stderr[-1500:])
