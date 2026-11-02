load "../rational/jump5.m2";
for k in {{5,5,4,1,1},{5,5,3,2,1},{5,5,2,2,2},{5,4,4,2,1},{5,4,3,3,1},{5,4,3,2,2},{5,3,3,3,2},{4,4,4,3,1},{4,4,4,2,2},{4,4,3,3,2},{4,3,3,3,3}} do (
   F := jumpCurve k;
   fs := toList factor F;
   print("k " | toString k | ": factors (degree, multiplicity) " | toString apply(select(fs, p -> first degree(p#0) > 0), p -> (first degree(p#0), p#1))));
