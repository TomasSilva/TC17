-- search for arrangements whose minimal-syzygy Bourbaki scheme has a NON-REDUCED component, and test the scheme lemma there
load "schemelemma_fun.m2";
kk = ZZ/101; R = kk[x,y,z];
setRandomSeed 7;
found = 0; tried = 0;
while found < 6 and tried < 400 do (
  tried = tried + 1;
  -- build an arrangement with forced triple points: choose 4-5 base points, take 2-3 lines through each, plus 2-3 random lines
  P := apply(4, i -> {random kk, random kk, 1_kk});
  lns := {};
  scan(P, p -> ( k := 2 + random 2; scan(k, i -> ( d := {random kk, random kk}; -- line through p with direction d: a x + b y + c z with a p0 + b p1 + c = 0
      aa := d#0; bb := d#1; cc := -(aa*p#0 + bb*p#1); lns = append(lns, aa*x + bb*y + cc*z)))));
  lns = lns | apply(2, i -> (random kk)*x + (random kk)*y + (random kk)*z);
  lns = unique lns;
  if any(lns, l -> l == 0) then continue;
  if #(unique apply(lns, l -> ideal l)) != #lns then continue;
  res := try analyseNR("try " | toString tried, lns) else null;
  if res === null then continue;
  if res then found = found + 1;
);
<< "tried " << tried << " found " << found << endl;
