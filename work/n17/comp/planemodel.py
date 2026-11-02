"""Plane model of a 1-dimensional component C = V(IC) of a core realisation space (Macaulay2).
Output: F(T,Y) (or F = 0 when C is the whole u_0-line, nvar = 1) and, for every variable u_i,
u_i = d_i(T,Y)/c_i(T,Y) on C, where T, Y are linear forms in u.  Used by famext.py."""
import subprocess, os
M2 = '/opt/homebrew/bin/M2'
def plane_model(nvar, gens, tag='pm', tries=8):
    if nvar <= 1 and gens.strip('{} ').replace('0', '').replace(',', '').strip() == '':
        return dict(kind='A1')
    s = ['R = QQ[%s];' % ','.join('u_%d' % i for i in range(max(nvar, 1)))]
    s.append('IC = ideal(%s);' % gens.strip('{}'))
    s.append('kk = numgens R;')
    s.append('''ok = false; tries = 0;
while not ok and tries < %d do (tries = tries + 1;
  a := apply(kk, i -> random(-5, 5)); b := apply(kk, i -> random(-5, 5));
  if tries == 1 and kk == 2 then (a = {1, 0}; b = {0, 1});
  S := QQ[gens R | {getSymbol "YY", getSymbol "TT"}, MonomialOrder => Lex];
  YY := (gens S)#kk; TT := (gens S)#(kk + 1);
  J := sub(IC, S) + ideal(YY - sum(kk, i -> b#i * (gens S)#i), TT - sum(kk, i -> a#i * (gens S)#i));
  G := flatten entries gens gb J;
  Fl := select(G, g -> isSubset(support g, {YY, TT}));
  if #Fl == 1 and member(YY, support first Fl) and member(TT, support first Fl) then (
     lin := apply(kk, i -> select(G, g -> member((gens S)#i, support g) and degree((gens S)#i, g) == 1 and isSubset(support g, {(gens S)#i, YY, TT})));
     lin = apply(kk, i -> if #(lin#i) > 0 then lin#i else (
        Ei := flatten entries gens eliminate(delete((gens S)#i, take(gens S, kk)), J);
        select(Ei, g -> member((gens S)#i, support g) and degree((gens S)#i, g) == 1 and isSubset(support g, {(gens S)#i, YY, TT}))));
     if all(lin, l -> #l >= 1) then (ok = true;
        print("TFORM " | toString a); print("YFORM " | toString b);
        print("F " | toString first Fl);
        for i from 0 to kk - 1 do (g := first lin#i; v := (gens S)#i; c := diff(v, g); d := -sub(g, {v => 0_S});
           print("U " | toString i | " ; " | toString c | " ; " | toString d)))));
if not ok then print("NOMODEL");
print("DONE");''' % tries)
    path = '/tmp/claude-502/pm_%s_%d.m2' % (tag, os.getpid())
    os.makedirs('/tmp/claude-502', exist_ok=True)
    open(path, 'w').write('\n'.join(s))
    r = subprocess.run([M2, '--script', path], capture_output=True, text=True, timeout=300)
    os.remove(path)
    out = dict(kind='plane', U={})
    for ln in r.stdout.split('\n'):
        if ln.startswith('TFORM '): out['a'] = ln[6:]
        elif ln.startswith('YFORM '): out['b'] = ln[6:]
        elif ln.startswith('F '): out['F'] = ln[2:]
        elif ln.startswith('U '):
            i, c, d = ln[2:].split(' ; '); out['U'][int(i)] = (c, d)
        elif ln.startswith('NOMODEL'): out['kind'] = 'nomodel'
    if 'DONE' not in r.stdout: out['kind'] = 'error'; out['err'] = r.stderr[-400:]
    return out
if __name__ == '__main__':
    import json, sys
    for l in open(sys.argv[1]):
        r = json.loads(l)
        for c in r.get('comps', []):
            if c['dim'] == 1:
                pm = plane_model(r['nvar'], c['gens'])
                print(r['idx'], r['nvar'], c['gens'][:60], '->', pm.get('kind'), pm.get('F', '')[:60], {k: v for k, v in list(pm.get('U', {}).items())[:3]})
