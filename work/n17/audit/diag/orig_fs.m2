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
tf = (4)*u_0+(0)*u_1+(-2)*u_2; Tsym = getSymbol "T"; RT = QQ[Tsym];
seen = new MutableHashTable;
phi = sub(5*T^2 - 14*T + 10, {(gens RT)#0 => tf});
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
phi = sub(T^3 - 8*T^2 + 28*T - 40, {(gens RT)#0 => tf});
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
phi = sub(T - 2, {(gens RT)#0 => tf});
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
phi = sub(1377*T^6 - 16992*T^5 + 94120*T^4 - 286608*T^3 + 511312*T^2 - 528192*T + 254016, {(gens RT)#0 => tf});
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
phi = sub(T^3 + 4*T^2 + 12*T - 40, {(gens RT)#0 => tf});
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
phi = sub(5*T^2 - 16, {(gens RT)#0 => tf});
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
phi = sub(5*T^3 - 36*T^2 + 76*T - 56, {(gens RT)#0 => tf});
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
phi = sub(5*T^3 - 8*T^2 - 4*T + 8, {(gens RT)#0 => tf});
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
phi = sub(T^2 - 3*T + 4, {(gens RT)#0 => tf});
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
phi = sub(T^5 + 20*T^3 - 192*T^2 + 480*T - 416, {(gens RT)#0 => tf});
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
phi = sub(5*T - 18, {(gens RT)#0 => tf});
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
phi = sub(T^3 + 4*T + 8, {(gens RT)#0 => tf});
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
phi = sub(T^4 - 2*T^3 + 36*T^2 - 88*T + 80, {(gens RT)#0 => tf});
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
phi = sub(T^4 + 20*T^2 - 72*T + 64, {(gens RT)#0 => tf});
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
phi = sub(T^4 - 6*T^3 + 20*T^2 + 56*T - 144, {(gens RT)#0 => tf});
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
phi = sub(T^5 - 2*T^4 + 32*T^3 - 136*T^2 + 336*T - 352, {(gens RT)#0 => tf});
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
phi = sub(T^4 - 13*T^3 + 72*T^2 - 140*T + 88, {(gens RT)#0 => tf});
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
phi = sub(5*T - 9, {(gens RT)#0 => tf});
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
phi = sub(T^3 - 2*T^2 + 16*T - 28, {(gens RT)#0 => tf});
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
phi = sub(5*T^2 - 12*T + 20, {(gens RT)#0 => tf});
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
phi = sub(T^4 - 14*T^3 + 68*T^2 - 136*T + 112, {(gens RT)#0 => tf});
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
phi = sub(15*T^4 - 86*T^3 + 268*T^2 - 440*T + 272, {(gens RT)#0 => tf});
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
phi = sub(T^4 + 44*T^2 - 144*T + 112, {(gens RT)#0 => tf});
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
phi = sub(5*T^3 - 16*T^2 + 20*T - 8, {(gens RT)#0 => tf});
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
phi = sub(5*T^4 - 46*T^3 + 140*T^2 - 248*T + 208, {(gens RT)#0 => tf});
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
phi = sub(T^3 - 12*T^2 + 52*T - 72, {(gens RT)#0 => tf});
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
phi = sub(T^3 + 6*T^2 - 4*T - 56, {(gens RT)#0 => tf});
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
phi = sub(T^2 + 5*T + 10, {(gens RT)#0 => tf});
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
phi = sub(T^4 + 4*T^2 - 32*T + 16, {(gens RT)#0 => tf});
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
phi = sub(T^3 - 4*T^2 + 4*T - 32, {(gens RT)#0 => tf});
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