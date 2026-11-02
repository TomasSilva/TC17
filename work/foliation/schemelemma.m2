-- Test of the scheme-theoretic Bourbaki-inflection lemma: for the minimal syzygy theta of an arrangement, with Bourbaki ideal I
-- (saturated) and residual inflection curve C = J/Q, check (i) supp B subset Sing C, (ii) Tjurina ideal of C subset I (scheme inclusion),
-- (iii) C in (I^2)^sat.  Also records whether Bourbaki points lie on arrangement lines and whether B is reduced.
uniqIdeals = L -> ( out := {}; scan(L, p -> if not any(out, q -> q == p) then out = append(out, p)); out );
analyse = (name, lns) -> (
  R := ring first lns;
  Q := product lns; n := #lns;
  jac := matrix{{diff(R_0,Q), diff(R_1,Q), diff(R_2,Q)}};
  S := mingens image syz jac;
  degs := apply(numcols S, i -> first (degrees source S)#i - (n-1));
  r := min degs; i := position(degs, d -> d == r);
  th := S_{i}; a := th_(0,0); b := th_(1,0); c := th_(2,0);
  x := R_0; y := R_1; z := R_2;
  w1 := b*z - c*y; w2 := c*x - a*z; w3 := a*y - b*x;
  g := gcd(gcd(w1,w2),w3);
  W := matrix{{w1,w2,w3}}; J := det jacobian W;
  pts := uniqIdeals apply(subsets(lns,2), p -> radical ideal p);
  ms := apply(pts, p -> number(lns, l -> isSubset(ideal l, p)));
  b2 := sum apply(ms, m -> m-1);
  chi := t -> t^2 - (n-1)*t + b2 - (n-1);
  Qx := diff(x,Q);
  hs := for k from 0 to numcols S - 1 list (e := S_{k}; cr1 := b*e_(2,0) - c*e_(1,0); cr1 // Qx);
  I := saturate ideal hs;
  if J % Q != 0 then (<< "== " << name << ": J not divisible by Q (gcd=" << g << ")" << endl; return);
  C := J // Q;
  if C == 0 then (<< "== " << name << ": C = 0" << endl; return);
  Tj := saturate ideal(C, diff(x,C), diff(y,C), diff(z,C));
  comps := primaryDecomposition I;
  online := apply(comps, P -> any(lns, l -> isSubset(ideal l, radical P)));
  reduced := apply(comps, P -> P == radical P);
  I2 := saturate(I^2);
  << "== " << name << ": n=" << n << " syz=" << sort degs << " r=" << r << " j=" << 3*r-n << " gcd=" << g
     << " Bour=chibar(r)=" << chi r << " length(B)=" << (if dim I <= 1 then degree I else "curve")
     << " C=" << factor C << endl;
  << "   B components (length, on a line?, reduced?): " << apply(#comps, k -> (degree comps#k, online#k, reduced#k)) << endl;
  << "   supp B in Sing C: " << isSubset(radical Tj, radical I)
     << " | scheme: Tjurina(C) in I: " << isSubset(Tj, I)
     << " | C in (I^2)^sat: " << (C % I2 == 0) << endl;
);
R = QQ[x,y,z];
-- A(4,1,3) = xyz(x^4-y^4)(y^4-z^4)(z^4-x^4): 15 lines, free (5,9); various deletions
w = 1; -- over QQ, use the real form: x^4 - y^4 = (x-y)(x+y)(x^2+y^2): keep only linear factors over QQ? Use i via ZZ/p instead.
kk = ZZ/10009; i4 = 1045^(3) ; -- 1045 has order 6 mod 10009; need order 4: find
R = kk[x,y,z];
i4 = (for a from 2 to 10008 do (if (a^4 % 10009 == 1) and (a^2 % 10009 != 1) then break a));
i4 = sub(i4, kk);
A4 = {x, y, z} | apply(4, k -> x - i4^k*y) | apply(4, k -> y - i4^k*z) | apply(4, k -> z - i4^k*x);
analyse("A(4,1,3) minus x", delete(x, A4));
analyse("A(4,1,3) minus x, y", delete(y, delete(x, A4)));
analyse("A(4,1,3) minus x and y-z", delete(y - z, delete(x, A4)));
analyse("A(4,1,3) minus x, y-z, y-i z", delete(y - i4*z, delete(y - z, delete(x, A4))));
analyse("A(4,1,3) minus x, y-z, y+z", delete(y + z, delete(y - z, delete(x, A4))));
analyse("A(4,1,3) minus x-y, y-z, z-x", delete(z - x, delete(y - z, delete(x - y, A4))));
analyse("A(4,1,3) minus x-y, x-i y", delete(x - i4*y, delete(x - y, A4)));
analyse("A(4,1,3) minus x, y, z", delete(z, delete(y, delete(x, A4))));
analyse("A(4,1,3) minus x, x-y", delete(x - y, delete(x, A4)));
-- A(3,1,3) deletions (12 lines, free (4,7)): need cube roots: 10009 = 1 mod 3
w3 = (for a from 2 to 10008 do (if (a^3 % 10009 == 1) and (a != 1) then break a)); w3 = sub(w3, kk);
A3 = {x, y, z} | apply(3, k -> x - w3^k*y) | apply(3, k -> y - w3^k*z) | apply(3, k -> z - w3^k*x);
analyse("A(3,1,3) minus x", delete(x, A3));
analyse("A(3,1,3) minus x, y-z", delete(y - z, delete(x, A3)));
analyse("A(3,1,3) minus x-y, y-z", delete(y - z, delete(x - y, A3)));
analyse("A(3,1,3) minus x, y", delete(y, delete(x, A3)));
-- Dimca-Pokora pair
R = QQ[x,y,z];
analyse("DP A (mdr 4)", {y-z, y+2*z, 2*y+z, x-2*y-z, x-y-2*z, x-y+z, x+y-z, x+y+2*z, 2*x-y-2*z});
analyse("DP B (mdr 5)", {x, x-y, x+y, x-y-z, y+z, z, x-z, x+y+2*z, x-2*y-z});
-- Ziegler pair style: 9 lines with 6 triple points on/off a conic? use a generic-ish arrangement with a quadruple point
analyse("random-ish 10 lines", {x, y, z, x+y+z, x-y+2*z, 2*x+y-z, x+2*y+3*z, x-3*y+z, 3*x+y+2*z, x+y-z});
