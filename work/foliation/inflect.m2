R = QQ[x,y,z];
uniqIdeals = L -> ( out := {}; scan(L, p -> if not any(out, q -> q == p) then out = append(out, p)); out );
analyse = (name, lines) -> (
  Q := product lines; n := #lines;
  jac := matrix{{diff(x,Q), diff(y,Q), diff(z,Q)}};
  S := mingens image syz jac;
  degs := apply(numcols S, i -> first (degrees source S)#i - (n-1));
  r := min degs; i := position(degs, d -> d == r);
  th := S_{i}; a := th_(0,0); b := th_(1,0); c := th_(2,0);
  w1 := b*z - c*y; w2 := c*x - a*z; w3 := a*y - b*x;
  g := gcd(gcd(w1,w2),w3);
  W := matrix{{w1,w2,w3}}; J := det jacobian W;
  Zw := ideal(w1,w2,w3);
  pts := uniqIdeals apply(subsets(lines,2), p -> radical ideal p);
  ms := apply(pts, p -> number(lines, l -> isSubset(ideal l, p)));
  b2 := sum apply(ms, m -> m-1); N := #ms;
  chi0 := b2 - n + 1; Delta := chi0 - r*(n-1-r);
  multI := intersect pts;
  off := saturate(Zw, Q);
  freepts := saturate(Zw, multI);
  prof := tally ms;
  << "== " << name << ": n=" << n << " syz degs=" << degs << " r=" << r << " j=" << 3*r-n << " gcd(omega)=" << g
    << " | N=" << N << " profile=" << prof << " b2=" << b2 << " chi0(0)=" << chi0 << endl;
  << "   Z(omega)=" << (if dim Zw <= 1 then degree Zw else "curve") << " (r^2+r+1=" << r^2+r+1 << ")"
    << "  off-line=" << (if dim off <= 0 then 0 else degree off)
    << "  free=" << (if dim freepts <= 0 then 0 else degree freepts)
    << "  Delta=chi0-r(n-1-r)=" << Delta << endl;
  if dim off <= 0 and dim off >= 0 and degree off > 0 then << "   off-line points: " << off << endl;
  if J != 0 then (<< "   J/Q = " << (if J % Q == 0 then factor(J // Q) else "Q does not divide J") << endl);
);
-- the six arrangements of TC_FOLIATION.md section 7 (all free; minimal derivation saturated)
analyse("A3^0(2) = B3: xyz(x^2-y^2)(y^2-z^2)(z^2-x^2), exp (3,5), n=3r", {x,y,z,x-y,x+y,y-z,y+z,z-x,z+x});
analyse("5 lines xyz(x-y)(x-z), exp (2,2), n=3r-1", {x,y,z,x-y,x-z});
analyse("8 lines (3,4) supersolvable, n=3r-1", {x,y,x-y,x+y,z-x,z+x,z-y,z+y});
analyse("B3 minus x=0, exp (3,4), n=3r-1", {y,z,x-y,x+y,y-z,y+z,z-x,z+x});
analyse("Pappus-like 9 lines (turns out free (3,5)), n=3r", {x,y,z,x-y,x-z,y-z,x+y-z,x-y+z,x-y-z});
-- negative controls: a point of multiplicity > n/2 makes the minimal derivation unsaturated (gcd != 1)
P = {{1,0,0},{0,1,0},{0,0,1},{1,1,1},{1,2,5}};
joinL = (p,q) -> ( v := {p#1*q#2-p#2*q#1, p#2*q#0-p#0*q#2, p#0*q#1-p#1*q#0}; v#0*x+v#1*y+v#2*z );
analyse("10 lines joining 5 general points (unsaturated)", apply(subsets(P,2), s -> joinL(s#0,s#1)));
-- the 15-line Fermat arrangement needs i = sqrt(-1); over ZZ/101 one has 10^2 = -1
R = ZZ/101[x,y,z];
analyse("A3^0(4) over ZZ/101 (i=10): xyz(x^4-y^4)(y^4-z^4)(z^4-x^4), exp (5,9), n=3r", {x,y,z,x-y,x+y,x-10*y,x+10*y,y-z,y+z,y-10*z,y+10*z,z-x,z+x,z-10*x,z+10*x});
