-- Bourbaki scheme of the minimal Jacobian syzygy versus the excess singular points of its foliation
-- (TC_FOLIATION.md section 9); the two nine-line arrangements are the Dimca-Pokora Ziegler pair, arXiv:2607.01985.
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
  chi := t -> t^2 - (n-1)*t + b2 - (n-1);
  multI := intersect pts;
  off := saturate(Zw, Q);
  freepts := saturate(Zw, multI);
  -- Bourbaki ideal of the minimal syzygy theta: h_eta = (theta x eta)_1 / Q_x
  Qx := diff(x,Q);
  hs := for k from 0 to numcols S - 1 list (
     e := S_{k}; a2 := e_(0,0); b2' := e_(1,0); c2 := e_(2,0);
     cr1 := b*c2 - c*b2';   -- x-component of theta x eta
     cr1 // Qx );
  Inu := ideal hs;
  Inus := saturate Inu;
  << "== " << name << ": n=" << n << " syz degs=" << degs << " r=" << r << " j=3r-n=" << 3*r-n << " gcd(omega)=" << g
    << " | profile=" << tally ms << " b2=" << b2 << " chibar(r)=" << chi r << endl;
  << "   Z(omega)=" << (if dim Zw <= 1 then degree Zw else "curve") << " (r^2+r+1=" << r^2+r+1 << ")"
    << "  off-line=" << (if dim off == 1 then degree off else 0)
    << "  non-multiple=" << (if dim freepts == 1 then degree freepts else 0) << endl;
  << "   Bourbaki ideal: dim R/I=" << dim Inus << " degree=" << degree Inus << "  generator degrees=" << sort apply(hs, h -> if h == 0 then -1 else first degree h) << endl;
  << "   Bourbaki scheme components: " << apply(primaryDecomposition Inus, p -> (degree p, radical p)) << endl;
  << "   off-line singular points: " << (if dim off == 1 then primaryDecomposition off else "none") << endl;
  << "   J/Q = " << (if J % Q == 0 then factor(J // Q) else "not divisible") << endl;
  -- is the Bourbaki scheme contained in the singular locus of J' ?
  offB := saturate(Inus, Q); << "   off-line part of the Bourbaki scheme = off-line singular scheme of omega? " << (offB == off) << endl;
  if J % Q == 0 then ( Jp := J // Q; sj := ideal(Jp, diff(x,Jp), diff(y,Jp), diff(z,Jp));
     << "   Bourbaki scheme inside Sing(J/Q)? " << isSubset(saturate sj, Inus) << "   (radical test: " << isSubset(radical saturate sj, radical Inus) << ")" << endl; );
);
analyse("Dimca-Pokora A (mdr 4)", {y-z, y+2*z, 2*y+z, x-2*y-z, x-y-2*z, x-y+z, x+y-z, x+y+2*z, 2*x-y-2*z});
analyse("Dimca-Pokora B (mdr 5)", {x, x-y, x+y, x-y-z, y+z, z, x-z, x+y+2*z, x-2*y-z});
-- equality test: is the off-line part of the Bourbaki scheme the off-line singular scheme of omega?
