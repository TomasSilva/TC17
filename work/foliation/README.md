# Inflection curve of the minimal-derivation foliation

`inflect.m2` (Macaulay2, `M2 --script work/foliation/inflect.m2`): for a line arrangement over ℚ it
computes the least-degree Jacobian syzygy θ, the 1-form ω = θ × E, its gcd (saturation test),
J = det(∂ω/∂x) and the factorisation of J/Q, the degree of the zero scheme of ω, the singular
points of ω off the lines and those that are not multiple points of the arrangement, the point
profile, b₂, and Δ = b₂ − n + 1 − r(n − 1 − r). See `TC_FOLIATION.md` §7 for the results and what
they check.
