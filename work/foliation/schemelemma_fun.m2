uniqIdeals = L -> ( out := {}; scan(L, p -> if not any(out, q -> q == p) then out = append(out, p)); out );
-- returns true iff a non-reduced Bourbaki component was found (and prints the lemma tests in that case)
analyseNR = (name, lns) -> (
  R := ring first lns; x := R_0; y := R_1; z := R_2;
  Q := product lns; n := #lns;
  jac := matrix{{diff(x,Q), diff(y,Q), diff(z,Q)}};
  S := mingens image syz jac;
  degs := apply(numcols S, i -> first (degrees source S)#i - (n-1));
  r := min degs; i := position(degs, d -> d == r);
  th := S_{i}; a := th_(0,0); b := th_(1,0); c := th_(2,0);
  w1 := b*z - c*y; w2 := c*x - a*z; w3 := a*y - b*x;
  g := gcd(gcd(w1,w2),w3);
  if g != 1 then return false;
  W := matrix{{w1,w2,w3}}; J := det jacobian W;
  Qx := diff(x,Q);
  hs := for k from 0 to numcols S - 1 list (e := S_{k}; cr1 := b*e_(2,0) - c*e_(1,0); cr1 // Qx);
  I := saturate ideal hs;
  if dim I > 1 then return false;
  comps := primaryDecomposition I;
  nonred := select(comps, P -> P != radical P);
  if #nonred == 0 then return false;
  if J % Q != 0 then return false;
  C := J // Q;
  Tj := saturate ideal(C, diff(x,C), diff(y,C), diff(z,C));
  I2 := saturate(I^2);
  online := apply(comps, P -> any(lns, l -> isSubset(ideal l, radical P)));
  << "== " << name << ": n=" << n << " syz=" << sort degs << " r=" << r << " j=" << 3*r-n << " length(B)=" << degree I << " deg C=" << first degree C << endl;
  << "   B components (length, on a line?, reduced?): " << apply(#comps, k -> (degree comps#k, online#k, comps#k == radical comps#k)) << endl;
  << "   non-reduced component ideals: " << apply(nonred, P -> toString mingens P) << endl;
  << "   supp B in Sing C: " << isSubset(radical Tj, radical I) << " | scheme: Tjurina(C) in I: " << isSubset(Tj, I) << " | C in (I^2)^sat: " << (C % I2 == 0) << endl;
  -- local check at each non-reduced component: Tjurina ideal localized contains I? test per component: Tj subset of P-primary part
  scan(nonred, P -> ( << "   at " << toString radical P << ": Tjurina(C) in this primary component: " << isSubset(Tj, P) << endl));
  true
);
