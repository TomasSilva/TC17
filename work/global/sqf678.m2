-- Squarefreeness of the (7,9)-jump determinant of s-point multiarrangements (s = 6, 7, 8, parts <= 5, sum 16),
-- tested on random lines in the moduli space over ZZ/32003: a squarefree restriction of full degree certifies
-- that the determinant has no square factor.  Degenerate linear factors (t_i = 0, 1, t_i = t_j) are reported separately.
kk = ZZ/32003;
setRandomSeed 7;
buildM = (mu, e, P, S, pts) -> (
  nunk := 2*(e+1); rows := {};
  u := S_0; v := S_1;
  for i from 0 to #mu-1 do (
    p := pts#i; m := mu#i;
    for k from 0 to m-1 do (
      row := for j from 0 to nunk-1 list (
        fj := if j <= e then u^j*v^(e-j) else 0_S;
        gj := if j <= e then 0_S else u^(j-e-1)*v^(2*e+1-j);
        if p === "inf" then lift(sub(diff(v^k, gj), {u => 1_S, v => 0_S}), P)
        else lift(sub(diff(u^k, fj - p*gj), {u => sub(p,S), v => 1_S}), P));
      rows = append(rows, row)));
  matrix rows);
partsOf = (n, k, mx) -> ( if k == 0 then (if n == 0 then {{}} else {}) else flatten for a from 1 to min(mx, n) list apply(partsOf(n - a, k - 1, a), p -> prepend(a, p)) );
P = kk[s];
S = P[u, v];
for sz from 6 to 8 do for mu in partsOf(16, sz, 5) do (
  nv := sz - 3;
  res := {};
  for trial from 1 to 3 do (
    pts := {"inf", 0_P, 1_P} | apply(nv, i -> (random kk) + (random kk) * s);
    M := buildM(mu, 7, P, S, pts);
    F := det M;
    if F == 0 then (res = append(res, "ZERO")) else (
      -- strip the degenerate factors: positions coinciding with 0, 1 or each other along the line
      G := F;
      for i from 0 to nv-1 do (
        for q in {pts#(i+3), pts#(i+3) - 1} do while G % q == 0 do G = G // q;
        for j from i+1 to nv-1 do (q := pts#(i+3) - pts#(j+3); while G % q == 0 do G = G // q));
      sq := gcd(G, diff(s, G));
      res = append(res, toString(first degree F) | "/" | toString(first degree G) | (if first degree sq == 0 then " squarefree" else " SQUARE FACTOR deg " | toString(first degree sq)))));
  print("s=" | toString sz | " mu=" | toString mu | " : " | toString res));
