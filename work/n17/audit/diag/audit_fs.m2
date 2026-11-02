needsPackage "PrimaryDecomposition";
cr = (p, q) -> matrix{{p_(0,1)*q_(0,2)-p_(0,2)*q_(0,1), p_(0,2)*q_(0,0)-p_(0,0)*q_(0,2), p_(0,0)*q_(0,1)-p_(0,1)*q_(0,0)}};
R = QQ[u_0,u_1,u_2];
P0 = matrix{{1_R,0,0}}; P1 = matrix{{0_R,1,0}}; P6 = matrix{{0_R,0,1}}; P9 = matrix{{1_R,1,1}};
P4 = cr(cr(P0, P1), cr(P6, P9));
P2 = P0 + u_0 * P1;
P3 = P0 + u_1 * P1;
P7 = cr(cr(P0, P6), cr(P3, P9));
P5 = P0 + u_2 * P1;
P8 = cr(cr(P0, P6), cr(P5, P9));
P10 = cr(cr(P2, P8), cr(P4, P6));
P11 = cr(cr(P2, P8), cr(P3, P7));
P12 = cr(cr(P0, P6), cr(P4, P11));
P13 = cr(cr(P1, P12), cr(P4, P6));
bad = select({det(P0 || P1 || P6),det(P0 || P1 || P7),det(P0 || P1 || P8),det(P0 || P1 || P9),det(P0 || P1 || P10),det(P0 || P1 || P11),det(P0 || P1 || P12),det(P0 || P1 || P13),det(P0 || P2 || P6),det(P0 || P2 || P7),det(P0 || P2 || P8),det(P0 || P2 || P9),det(P0 || P2 || P10),det(P0 || P2 || P11),det(P0 || P2 || P12),det(P0 || P2 || P13),det(P0 || P3 || P6),det(P0 || P3 || P7),det(P0 || P3 || P8),det(P0 || P3 || P9),det(P0 || P3 || P10),det(P0 || P3 || P11),det(P0 || P3 || P12),det(P0 || P3 || P13),det(P0 || P4 || P6),det(P0 || P4 || P7),det(P0 || P4 || P8),det(P0 || P4 || P9),det(P0 || P4 || P10),det(P0 || P4 || P11),det(P0 || P4 || P12),det(P0 || P4 || P13),det(P0 || P5 || P6),det(P0 || P5 || P7),det(P0 || P5 || P8),det(P0 || P5 || P9),det(P0 || P5 || P10),det(P0 || P5 || P11),det(P0 || P5 || P12),det(P0 || P5 || P13),det(P0 || P6 || P9),det(P0 || P6 || P10),det(P0 || P6 || P11),det(P0 || P6 || P13),det(P0 || P7 || P9),det(P0 || P7 || P10),det(P0 || P7 || P11),det(P0 || P7 || P13),det(P0 || P8 || P9),det(P0 || P8 || P10),det(P0 || P8 || P11),det(P0 || P8 || P13),det(P0 || P9 || P10),det(P0 || P9 || P11),det(P0 || P9 || P12),det(P0 || P9 || P13),det(P0 || P10 || P11),det(P0 || P10 || P12),det(P0 || P10 || P13),det(P0 || P11 || P12),det(P0 || P11 || P13),det(P0 || P12 || P13),det(P1 || P2 || P6),det(P1 || P2 || P7),det(P1 || P2 || P8),det(P1 || P2 || P9),det(P1 || P2 || P10),det(P1 || P2 || P11),det(P1 || P2 || P12),det(P1 || P2 || P13),det(P1 || P3 || P6),det(P1 || P3 || P7),det(P1 || P3 || P8),det(P1 || P3 || P9),det(P1 || P3 || P10),det(P1 || P3 || P11),det(P1 || P3 || P12),det(P1 || P3 || P13),det(P1 || P4 || P6),det(P1 || P4 || P7),det(P1 || P4 || P8),det(P1 || P4 || P9),det(P1 || P4 || P10),det(P1 || P4 || P11),det(P1 || P4 || P12),det(P1 || P4 || P13),det(P1 || P5 || P6),det(P1 || P5 || P7),det(P1 || P5 || P8),det(P1 || P5 || P9),det(P1 || P5 || P10),det(P1 || P5 || P11),det(P1 || P5 || P12),det(P1 || P5 || P13),det(P1 || P6 || P7),det(P1 || P6 || P8),det(P1 || P6 || P9),det(P1 || P6 || P10),det(P1 || P6 || P11),det(P1 || P6 || P12),det(P1 || P6 || P13),det(P1 || P7 || P8),det(P1 || P7 || P9),det(P1 || P7 || P10),det(P1 || P7 || P11),det(P1 || P7 || P12),det(P1 || P7 || P13),det(P1 || P8 || P9),det(P1 || P8 || P10),det(P1 || P8 || P11),det(P1 || P8 || P12),det(P1 || P8 || P13),det(P1 || P9 || P10),det(P1 || P9 || P11),det(P1 || P9 || P12),det(P1 || P9 || P13),det(P1 || P10 || P11),det(P1 || P10 || P12),det(P1 || P10 || P13),det(P1 || P11 || P12),det(P1 || P11 || P13),det(P2 || P3 || P6),det(P2 || P3 || P7),det(P2 || P3 || P8),det(P2 || P3 || P9),det(P2 || P3 || P10),det(P2 || P3 || P11),det(P2 || P3 || P12),det(P2 || P3 || P13),det(P2 || P4 || P6),det(P2 || P4 || P7),det(P2 || P4 || P8),det(P2 || P4 || P9),det(P2 || P4 || P10),det(P2 || P4 || P11),det(P2 || P4 || P12),det(P2 || P4 || P13),det(P2 || P5 || P6),det(P2 || P5 || P7),det(P2 || P5 || P8),det(P2 || P5 || P9),det(P2 || P5 || P10),det(P2 || P5 || P11),det(P2 || P5 || P12),det(P2 || P5 || P13),det(P2 || P6 || P7),det(P2 || P6 || P8),det(P2 || P6 || P9),det(P2 || P6 || P10),det(P2 || P6 || P11),det(P2 || P6 || P12),det(P2 || P6 || P13),det(P2 || P7 || P8),det(P2 || P7 || P9),det(P2 || P7 || P10),det(P2 || P7 || P11),det(P2 || P7 || P12),det(P2 || P7 || P13),det(P2 || P8 || P9),det(P2 || P8 || P12),det(P2 || P8 || P13),det(P2 || P9 || P10),det(P2 || P9 || P11),det(P2 || P9 || P12),det(P2 || P9 || P13),det(P2 || P10 || P12),det(P2 || P10 || P13),det(P2 || P11 || P12),det(P2 || P11 || P13),det(P2 || P12 || P13),det(P3 || P4 || P6),det(P3 || P4 || P7),det(P3 || P4 || P8),det(P3 || P4 || P9),det(P3 || P4 || P10),det(P3 || P4 || P11),det(P3 || P4 || P12),det(P3 || P4 || P13),det(P3 || P5 || P6),det(P3 || P5 || P7),det(P3 || P5 || P8),det(P3 || P5 || P9),det(P3 || P5 || P10),det(P3 || P5 || P11),det(P3 || P5 || P12),det(P3 || P5 || P13),det(P3 || P6 || P7),det(P3 || P6 || P8),det(P3 || P6 || P9),det(P3 || P6 || P10),det(P3 || P6 || P11),det(P3 || P6 || P12),det(P3 || P6 || P13),det(P3 || P7 || P8),det(P3 || P7 || P10),det(P3 || P7 || P12),det(P3 || P7 || P13),det(P3 || P8 || P9),det(P3 || P8 || P10),det(P3 || P8 || P11),det(P3 || P8 || P12),det(P3 || P8 || P13),det(P3 || P9 || P10),det(P3 || P9 || P12),det(P3 || P9 || P13),det(P3 || P10 || P11),det(P3 || P10 || P12),det(P3 || P10 || P13),det(P3 || P11 || P12),det(P3 || P11 || P13),det(P3 || P12 || P13),det(P4 || P5 || P6),det(P4 || P5 || P7),det(P4 || P5 || P8),det(P4 || P5 || P9),det(P4 || P5 || P10),det(P4 || P5 || P11),det(P4 || P5 || P12),det(P4 || P5 || P13),det(P4 || P6 || P7),det(P4 || P6 || P8),det(P4 || P6 || P11),det(P4 || P6 || P12),det(P4 || P7 || P8),det(P4 || P7 || P9),det(P4 || P7 || P10),det(P4 || P7 || P11),det(P4 || P7 || P12),det(P4 || P7 || P13),det(P4 || P8 || P9),det(P4 || P8 || P10),det(P4 || P8 || P11),det(P4 || P8 || P12),det(P4 || P8 || P13),det(P4 || P9 || P11),det(P4 || P9 || P12),det(P4 || P10 || P11),det(P4 || P10 || P12),det(P4 || P11 || P13),det(P4 || P12 || P13),det(P5 || P6 || P7),det(P5 || P6 || P8),det(P5 || P6 || P9),det(P5 || P6 || P10),det(P5 || P6 || P11),det(P5 || P6 || P12),det(P5 || P6 || P13),det(P5 || P7 || P8),det(P5 || P7 || P9),det(P5 || P7 || P10),det(P5 || P7 || P11),det(P5 || P7 || P12),det(P5 || P8 || P10),det(P5 || P8 || P11),det(P5 || P8 || P12),det(P5 || P8 || P13),det(P5 || P9 || P10),det(P5 || P9 || P11),det(P5 || P9 || P12),det(P5 || P9 || P13),det(P5 || P10 || P11),det(P5 || P10 || P13),det(P5 || P11 || P12),det(P5 || P11 || P13),det(P5 || P12 || P13),det(P6 || P7 || P9),det(P6 || P7 || P10),det(P6 || P7 || P11),det(P6 || P7 || P13),det(P6 || P8 || P9),det(P6 || P8 || P10),det(P6 || P8 || P11),det(P6 || P8 || P13),det(P6 || P9 || P11),det(P6 || P9 || P12),det(P6 || P10 || P11),det(P6 || P10 || P12),det(P6 || P11 || P12),det(P6 || P11 || P13),det(P6 || P12 || P13),det(P7 || P8 || P9),det(P7 || P8 || P10),det(P7 || P8 || P11),det(P7 || P8 || P13),det(P7 || P9 || P10),det(P7 || P9 || P12),det(P7 || P9 || P13),det(P7 || P10 || P11),det(P7 || P10 || P12),det(P7 || P10 || P13),det(P7 || P11 || P12),det(P7 || P11 || P13),det(P7 || P12 || P13),det(P8 || P9 || P10),det(P8 || P9 || P11),det(P8 || P9 || P12),det(P8 || P9 || P13),det(P8 || P10 || P12),det(P8 || P10 || P13),det(P8 || P11 || P12),det(P8 || P11 || P13),det(P8 || P12 || P13),det(P9 || P10 || P11),det(P9 || P10 || P12),det(P9 || P11 || P12),det(P9 || P11 || P13),det(P9 || P12 || P13),det(P10 || P11 || P12),det(P10 || P11 || P13),det(P10 || P12 || P13),det(P11 || P12 || P13)}, f -> f != 0);
IC = ideal(2*u_0*u_2^2-u_1*u_2^2+u_0*u_1-u_0*u_2-3*u_1*u_2+u_2^2+u_1, 2*u_0*u_1*u_2-u_1*u_2^2-u_0*u_1-u_0*u_2-u_1*u_2+u_2^2+u_1, 2*u_0^2*u_1+2*u_0^2*u_2-u_1*u_2^2-2*u_0^2-3*u_0*u_1-u_0*u_2-u_1*u_2+u_2^2+3*u_1);
tf = (-3)*u_0+(-3)*u_1+(3)*u_2; Tsym = getSymbol "T"; RT = QQ[Tsym];
seen = new MutableHashTable;
phi = sub(50*T^2 + 150*T + 117, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^4 + 2*T^3 - 18*T + 27, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T + 3, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^4 - 3*T^3 + 18*T^2 - 54*T + 81, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(5*T^3 + 3*T^2 + 54*T + 297, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(55*T^2 + 90*T - 324, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(5*T^3 + 117*T^2 + 360*T + 459, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(40*T^3 + 48*T^2 - 18*T - 27, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(8*T^2 + 18*T + 81, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^5 - 15*T^4 + 9*T^3 - 459*T^2 - 1944*T - 5589, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(5*T + 171, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^3 - 5*T^2 + 12*T - 9, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(5*T^4 + 19*T^3 + 234*T^2 + 486*T + 729, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(20*T + 9, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(32*T^4 + 120*T^3 + 1044*T^2 + 3186*T + 3321, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^4 + 9*T^3 + 18*T^2 - 54*T - 243, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^5 + 3*T^4 + 45*T^3 + 189*T^2 + 324*T + 3159, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(2*T^4 + 27*T^3 + 117*T^2 + 162*T + 81, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(70*T + 207, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(2*T^3 - 18*T + 27, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(5*T + 9, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^4 + 15*T^3 + 72*T^2 + 108*T + 81, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(5*T^4 - 11*T^3 + 18*T^2 + 234*T + 297, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(7*T^4 + 18*T^3 + 351*T^2 + 972*T + 729, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(35*T^3 + 99*T^2 + 90*T + 27, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(5*T^4 + 87*T^3 + 108*T^2 + 270*T + 1863, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^3 - 9*T^2 - 162*T - 729, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^3 - 33*T^2 + 171*T - 351, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(10*T^2 - 45*T + 51, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(T^4 - 18*T^3 + 45*T^2 - 81, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
phi = sub(4*T^3 + 57*T^2 - 234*T + 297, {(gens RT)#0 => tf});
for q in minimalPrimes(IC + ideal phi) do (
  if dim q == 0 and all(bad, b -> b % q != 0) then (key := toString flatten entries gens gb q;
   if not seen#?key then (seen#key = 1;
    kk := numgens R; ok := false; tries := 0;
    while not ok and tries < 20 do (tries = tries + 1;
     a := apply(kk, i -> random(-7, 7));
     S := QQ[gens R | {getSymbol "TT"}, MonomialOrder => Lex]; TT := last gens S;
     J := sub(q, S) + ideal(TT - sum(kk, i -> a#i * (gens S)#i));
     G := flatten entries gens gb J;
     fl := select(G, g -> isSubset(support g, {TT}));
     if #G == kk + 1 and #fl == 1 then (
      f := first fl; d := (degree f)#0;
      nfs := apply(kk, i -> (gens S)#i % ideal G);
      if all(nfs, h -> isSubset(support h, {TT})) then (ok = true;
       print("PT " | toString apply(d + 1, j -> coefficient(TT^j, f)) | " ; " | demark(" ; ", apply(nfs, h -> toString apply(d, j -> coefficient(TT^j, h))))))));
    if not ok then print("PT-NOSHAPE"))));
print("DONE");