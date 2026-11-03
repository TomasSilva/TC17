# Terao's conjecture in P²: the foliation of the minimal derivation

**Status (8 Oct 2026).** This is not a proof of Terao's conjecture (TC). It is one new tool and
what it proves. Attached to the non-free member A₂ of a counterexample is the foliation F of P²
defined by its logarithmic derivation of least degree r = mdr(A₂); every line of A₂ is invariant.
Its inflection curve J (the Jacobian of the Gauss map of F, Pereira's first extactic curve) has
degree 3r, is divisible by the product Q of the n lines, and vanishes to order ≥ 2 at every
singular point of F. Comparing the zeros of J, the singular points of F and the lattice gives an
exact identity (Theorem 4.1):

  (d₁ − r)(d₂ − r) = Σ_{P ∉ A₂} μ_P − Σ_{P ∈ A₂} d_P,

whose right-hand side counts singularities of F that are not accounted for by the lines through
them. When deg(J/Q) = 3r − n ≤ 1 the right-hand side is forced to be 0 while the left-hand side
is ≥ 1. Hence (Theorem 5.1):

> **A counterexample to TC in P² has 3·mdr(A₂) ≥ n + 2; hence d₂ ≤ 2d₁ − 6, d₁ ≥ 7 and n ≥ 15.**

**Added later on 8 Oct 2026 (§10):** the next case deg(J/Q) = 2 is impossible too, by a local
analysis along a double line of the inflection curve (Theorem 10.1). So **3·mdr(A₂) ≥ n + 3,
d₂ ≤ 2d₁ − 7**. This excludes (7, 8) at 16 lines (TC for 16 lines is now theoretical), (8, 10) and
(9, 9) with mdr 7 at 19 lines, (9, 12) at 22 lines. The first theoretically open classes are
(7, 7) at 15 lines (settled by enumeration), (8, 8) at 17 and (8, 9) at 18.

**Added later on 8 Oct 2026 (§11):** the 18-line arrangement A(6,1,3) ∖ {x, y−z, y−ζz} is an
mdr-7 member of the class (8, 9) with J/Q the product of the three deleted lines; its lattice is
rigid, and every other three-pencil lattice of the class is free (six lattices, one with a
one-parameter family, free throughout by Yoshinaga's criterion over ℚ[g]).

This removes, for every n, the two outermost exponent classes of the window of `TC_GENERAL.md` §1:
δ = d₁ − 4 (the narrow classes of `TC_GENERAL.md` §2: (6, 8), (7, 10), (8, 12), …) and δ = d₁ − 5
((6, 7), (7, 9), (8, 11), …), and inside the remaining classes it removes every value of mdr(A₂)
below (n + 2)/3. Concretely:

- 14 lines: the single class (6, 7) is excluded by theory. Together with Dimca–Ibadula–Măcinic
  (13 lines) this is a theoretical proof of TC for n ≤ 14; the Barakat–Kühne computation is no
  longer needed for the bound.
- 15 lines: (6, 8) is excluded by theory (Theorem 10.1 of `TC_ATTEMPT.md` did it by enumeration
  plus Kneser's theorem); (7, 7) survives, with mdr(A₂) = 6 forced.
- 17 lines: (7, 9) and the part r = 6 of (8, 8) — exactly the two classes the running
  enumeration covers — are excluded by theory. The only open 17-line class is part [B] of
  (8, 8): A₂ nearly free with exponents (7, 10).
- 18 lines: (7, 10) excluded; (8, 9) survives with mdr(A₂) = 7.

What is *not* proved: TC. For deg(J/Q) ≥ 2 the identity allows a nonzero right-hand side carried
by singular points of the curve J/Q, and §6 says exactly what those singularities would have to
be. Sections 1–5 are proved; §6 is analysis of the remaining cases; §7 lists the computer checks
of the structure on known free arrangements; §9 identifies the excess with the Bourbaki degree of
Nasrollah Nejad–Nouri and checks this on the Dimca–Pokora Ziegler pair.

Notation as in `TC_ATTEMPT.md` and `TC_GENERAL.md`: (A₁, A₂) a counterexample with lattice L of
n lines; A₁ free with exponents (1, d₁, d₂), d₁ ≤ d₂, δ = d₂ − d₁, n = d₁ + d₂ + 1; A₂ not free
with defining polynomial Q = ∏ α_H; S = ℂ[x, y, z], E = x∂ₓ + y∂_y + z∂_z; D₀(A₂) the derivations
with θ(α_H) ∈ (α_H) for all H and θ(Q) = 0 (the Jacobian syzygies), r = mdr(A₂) its least degree;
m_P the multiplicity of a point, s_H = |A^H| the number of multiple points on a line,
b₂ = Σ_P (m_P − 1) = d₁d₂ + n − 1.

## 0. Inputs

Two facts from `TC_ATTEMPT.md` Theorem 1 are used, nothing else from the window:

- (I1) r = mdr(A₂) ≤ d₁ − 1. (du Plessis–Wall, as in Dimca–Kühne–Pokora: τ = Σ_P (m_P − 1)² is a
  lattice invariant; among arrangements with the τ of a free lattice the free ones are exactly
  those with mdr = d₁, and a non-free one has mdr < d₁.)
- (I2) s_H ≤ d₂ + 1 for every line H. (Ziegler: the multirestriction of the free member A₁ to H
  has exponents (d₁, d₂); a 2-multiarrangement with s points and exponents (e₁, e₂) has
  s ≤ max(e₁, e₂) + 1, since a basis element not proportional to the Euler derivation E_H has a
  determinant with E_H of degree e_i + 1 vanishing at all s points.)

Also r ≥ 1, because a derivation of degree 0 in D₀(A₂) would be a constant vector field tangent
to every line, i.e. all lines through one point.

## 1. The foliation of θ and its singular points

Fix θ ∈ D₀(A₂) of degree r, θ ≠ 0, and put ω := θ × E, i.e.

  ω = (θ₂z − θ₃y, θ₃x − θ₁z, θ₁y − θ₂x),

three forms of degree r + 1 with xω₁ + yω₂ + zω₃ = 0: a section of Ω¹_{P²}(r + 2). It defines
the foliation F of P² whose tangent line at a point [x] is the line through [x] and [θ(x)]
(normal vector ω(x)); F has degree r. Singular points of F: the points with θ(x) ∈ ℂx, i.e.
ω(x) = 0. In an affine chart (say z = 1) F is given by the planar vector field
X = (θ₁ − uθ₃, θ₂ − vθ₃)(u, v, 1); at a singular point P we write L_P for its linear part,
μ_P := dim 𝒪_P/(X₁, X₂) for its Milnor number, and we call P

- *nondegenerate* if det L_P ≠ 0 (equivalently μ_P = 1), and then *radial* if L_P is a nonzero
  scalar, *non-radial* otherwise;
- *degenerate* if det L_P = 0; of *order k* if the Taylor expansion of X at P starts in degree k.

For a singular point P let m'_P be the number of lines of A₂ through P: m'_P = m_P ≥ 2 for a
multiple point of A₂, m'_P = 1 for a *free* point (on one line, not a multiple point), m'_P = 0
for an *off-line* point.

**1.1 (invariant lines, `TC_GENERAL.md` 3.1(3)).** Every line H of A₂ is F-invariant: θ(α_H) ∈ (α_H)
says that θ maps the plane H ⊂ ℂ³ into itself, so ω = θ × E is normal to H along H:

  ω|_H = f_H · n_H,   f_H := det_H(θ|_H, E|_H) ∈ Sym^{r+1}(H*),

and f_H ≠ 0 (proof below). The zeros of f_H are exactly the singular points of F on H (for P ∈ H,
f_H(P) = 0 iff θ(P) ∈ ℂP); every multiple point of A₂ on H is one (two invariant lines through P
force θ(P) ∈ H ∩ H' = ℂP). Write ν_P(H) := ord_P f_H; then Σ_{P ∈ H} ν_P(H) = r + 1.

*Proof that f_H ≠ 0.* Put K_H := θ(α_H)/α_H and θ_H := θ − K_H E; it is tangent to H and
restricts to the Ziegler multiarrangement (A₂^H, μ), μ_P = m_P − 1, and f_H = det_H(θ_H|_H, E_H).
If f_H = 0 then θ_H|_H = g E_H with g ∈ ℂ[H]_{r−1}. If g = 0, α_H divides θ_H and θ_H/α_H is a
logarithmic derivation of A₂ of degree r − 1 not proportional to E, against the minimality of r
(`TC_ATTEMPT.md` Thm 1(7), step 2). If g ≠ 0, the Ziegler conditions α_P^{μ_P} | g α_P force
α_P^{μ_P − 1} | g, so r − 1 ≥ Σ_{P ∈ H} (μ_P − 1) = n − 1 − s_H, i.e. s_H ≥ n − r ≥ d₂ + 2 by (I1),
against (I2). ∎

**1.2 Lemma (saturation).** ω₁, ω₂, ω₃ have no common factor. Hence F has isolated singular points
and

  Σ_{P ∈ Sing F} μ_P = c₂(Ω¹_{P²}(r + 2)) = r² + r + 1.

*Proof.* Suppose f | ω with deg f = k ≥ 1 and write ω = f ω'. The kernel of (a, b, c) ↦ xa + yb + zc
on triples of forms is generated by the Koszul relations, so ω' = θ' × E for a vector field θ' of
degree r − k, and then θ − fθ' is killed by × E, i.e. θ = fθ' + gE with g ∈ S_{r−1}. No α_H
divides f: otherwise ω would vanish identically on H, i.e. f_H = 0, against 1.1. Hence for every
H, θ(α_H) = fθ'(α_H) + gα_H ∈ (α_H) gives θ'(α_H) ∈ (α_H): θ' is logarithmic for A₂, of degree
r − k < r, and not a multiple of E (else ω' = 0). Subtracting its Euler component (θ'(Q) = hQ with
h ∈ S_{r−k−1}; θ' − (h/n)E ∈ D₀(A₂)) gives a nonzero element of D₀(A₂) of degree < r, a
contradiction. The count is c₂ of the rank-2 bundle Ω¹(r + 2): c(Ω¹_{P²}) = 1 − 3h + 3h², so
c₂(Ω¹(k)) = k² − 3k + 3, which is r² + r + 1 for k = r + 2; μ_P is the length of the zero scheme
of ω at P. ∎

**1.3 Local facts.** Let P be a singular point.
(a) Every line of A₂ through P is an invariant line of the planar field X at P, hence an
eigendirection of L_P. So m'_P ≥ 3 forces L_P to be scalar (radial, or L_P = 0), and m'_P = 2
forces L_P to be diagonal in the basis given by the two lines.
(b) For a line H ∋ P: ν_P(H) = 1 iff the eigenvalue ε_H(P) of L_P along H is nonzero.
(Differentiate f_H = det_H(θ|_H, E|_H) at P: with θ(P) = λP, d(f_H)_P(w) = det_H((Dθ_P − λ)w, P)
for w ∈ H, and (Dθ_P − λ)w ≡ ε_H(P)·w mod ℂP.)
(c) For a line H ∋ P with local equation v, invariance gives X₂ = v·q, and
μ_P = I_P(X₁, v) + I_P(X₁, q) = ν_P(H) + I_P(X₁, q) ≥ ν_P(H).
(d) If L_P = diag(0, e) with e ≠ 0 in a basis whose first vector is the direction of a line H of
A₂ (a *saddle-node along H*), then μ_P = ν_P(H) by (c), because q(P) = e ≠ 0.

## 2. The inflection curve of F

Let M := (∂ω_i/∂x_j) be the Jacobian matrix of ω: ℂ³ → ℂ³ and

  J := det M ∈ S_{3r}.

Projectively, ω is the Gauss map G: P² ⇢ P²*, [x] ↦ [ω(x)] = T_{[x]}F, given by the net of
degree-(r + 1) forms spanned by ω₁, ω₂, ω₃, and J is the Jacobian of this net.

**Proposition 2.1.**
1. In the chart z = 1, with X the planar field of §1: J(u, v, 1) = (r + 1)·det(X, DX·X). So J is
   the locus of inflection points of the leaves of F (where the curvature of the integral curves
   of X vanishes): the first extactic curve of F in the sense of Pereira.
2. J ≠ 0.
3. α_H | J for every line H of A₂; hence Q | J and n ≤ 3r.
4. J vanishes to order ≥ 2 at every singular point of F.

Write J = Q·J', with J' ∈ S_j, j := 3r − n ≥ 0.

*Proof.* (1) Put x = λ(u, v, 1); the change of coordinates (u, v, λ) ↦ x has Jacobian λ², and
∂ω/∂λ = (r + 1)λ^r ω̄, ∂ω/∂u = λ^{r+1}∂_u ω̄, ∂ω/∂v = λ^{r+1}∂_v ω̄ with ω̄ := ω(u, v, 1), so
J·λ² = (r + 1)λ^{3r+2} det(∂_u ω̄, ∂_v ω̄, ω̄), i.e. J(u, v, 1) = (r + 1) det(∂_u ω̄, ∂_v ω̄, ω̄). Now
ω̄ = (X₂, −X₁, vX₁ − uX₂), and adding v times the second row and u times the first row to the third
row leaves a third row (−X₂, X₁, 0), so the determinant is
X₁²∂_uX₂ − X₂²∂_vX₁ + X₁X₂(∂_vX₂ − ∂_uX₁) = det(X, DX·X), the numerator of the curvature of the
integral curves of X.
(2) If J ≡ 0 every integral curve of X has zero curvature, so every leaf of F is contained in a
line. A foliation whose leaves are lines is a pencil: its leaves form a curve Γ ⊂ P²*, and the
number of leaves through a generic point, which is 1, equals deg Γ. The pencil through [v] is
defined by the form E × v, whose coefficients are linear, so a saturated ω defining it has r = 0,
against r ≥ 1 and Lemma 1.2.
(3) On an invariant line the leaf is the line itself, of curvature zero, so J|_H = 0 by (1).
(Directly: ω maps the plane H into ℂn_H, so dω_x has a kernel on H for every x ∈ H.) The lines
are distinct, so their product divides J, and deg Q = n ≤ 3r = deg J.
(4) Euler's relation for the forms ω_i of degree r + 1 reads M(x)·x = (r + 1)ω(x). Multiply by the
adjugate: J(x)·x = (r + 1)·adj(M(x))·ω(x). At a singular point P expand in t = x − P: ω(P + t) =
M(P)t + O(|t|²) and adj(M(P + t)) = adj(M(P)) + O(|t|), so the right-hand side is
(r + 1)adj(M(P))M(P)t + O(|t|²) = (r + 1)J(P)t + O(|t|²) = O(|t|²), because J(P) = 0 (M(P) kills
P ≠ 0). Since P + t ≠ 0, J(P + t) = O(|t|²). ∎

The bound n ≤ 3·deg F for the number of invariant lines of a foliation, and the curve J, are due
to Pereira (extactic curves); the proof above is self-contained. Applied to A₂: a counterexample
has **mdr(A₂) ≥ n/3**, which is at least as strong as every lower bound on r in
`TC_GENERAL.md` (W4), with equality exactly in the narrow classes.

## 3. The multiplicity of J at the singular points

Everything in this section is local at a singular point P, computed from
J = (r + 1)·det(X, DX·X) in a chart centred at P. Write X = X_k + X_{k+1} + ⋯ with X_i
homogeneous of degree i in t = (u, v) and X_k ≠ 0 (k = 1 iff L_P ≠ 0), E₀ := u∂_u + v∂_v the
local radial field, and for a homogeneous field Y let ⟨t, Y⟩ := det(t, Y) = uY₂ − vY₁, the binary
form whose roots are the lines through P invariant under Y. A line through P invariant under X is
invariant under every X_i, so it is among the roots of the first ⟨t, X_i⟩ that is not identically
zero; such an i exists, because X = φ·E₀ with φ a unit would give J ≡ 0 near P.

**Proposition 3.1.** Let P be a singular point of F and ℓ_P the number of lines through P
invariant under F (so ℓ_P ≥ m'_P).
(a) If P is nondegenerate and non-radial: mult_P(J) = 2, and ℓ_P ≤ 2.
(b) If P is nondegenerate and radial, let i_P ≥ 2 be the least i with X_i not a multiple of E₀.
    Then mult_P(J) = i_P + 1 ≥ 3 and ℓ_P ≤ i_P + 1. In particular mult_P(J) ≥ max(3, ℓ_P).
(c) If L_P ≠ 0 is singular: mult_P(J) ≥ 3 and ℓ_P ≤ 2.
(d) If L_P = 0, of order k ≥ 2: if X_k is not a multiple of E₀ then ℓ_P ≤ k + 1 and
    mult_P(J) ≥ 3k − 1; if X_k = g·E₀ (dicritical leading term) and i_P > k is the least i with X_i
    not a multiple of E₀, then ℓ_P ≤ i_P + 1 and mult_P(J) = 2k + i_P − 1. In both cases
    mult_P(J) ≥ ℓ_P + 2.

*Proof.* Expand det(X, DX·X): DX_a·X_b has degree a + b − 1 and det(X_c, DX_a·X_b) degree
a + b + c − 1.
(a), (c): the degree-2 part is det(Lt, L²t). For L invertible with distinct eigenvalues λ₁, λ₂ and
t = αe₁ + βe₂ it is αβλ₁λ₂(λ₂ − λ₁)det(e₁, e₂) ≠ 0; for L = λ(I + N), N ≠ 0 nilpotent, λ ≠ 0, it is
λ²det(t, Nt) ≠ 0; for L scalar, for L of rank 1 (then L² ∝ L) and for L nilpotent (L² = 0) it
vanishes. A nonzero non-scalar L has at most two eigendirections, so ℓ_P ≤ 2.
(b): write X = φ·t + X_i + ⋯ with φ := c + g₁ + ⋯ + g_{i−2} the sum of the multiples of E₀
(c ≠ 0, i = i_P). Then DX·X = (φ·dφ(t) + φ² + dφ(X_i))·t + (i + 1)φX_i + (higher), using Euler
DX_i·t = iX_i, so det(X, DX·X) = ((i + 1)φ² − φ·dφ(t) − φ² − dφ(X_i))·⟨t, X_i⟩ + ⋯, whose lowest
term is i·c²·⟨t, X_i⟩, of degree i + 1, nonzero.
(d): if X_k is not a multiple of E₀ the lowest possible term is det(X_k, DX_k·X_k), of degree
3k − 1, and 3k − 1 ≥ (k + 1) + 2 ≥ ℓ_P + 2 for k ≥ 2. If X_k = gE₀ with deg g = k − 1 and i = i_P:
every X_a with k ≤ a < i is a multiple of E₀, and D(gE₀)·(hE₀) is a multiple of t, so
det(X_c, DX_a·X_b) vanishes unless one of a, b, c equals i; the lowest surviving degree is
2k + i − 1, from (c, a, b) ∈ {(i, k, k), (k, i, k), (k, k, i)}, with sum
(−k + i + 1)·g²·⟨t, X_i⟩ ≠ 0 (Euler: dg(t) = (k − 1)g, DX_i·t = iX_i). And
ℓ_P ≤ deg⟨t, X_i⟩ = i + 1 ≤ 2k + i − 3 for k ≥ 2. ∎

**Corollary 3.2 (multiplicity of J' = J/Q).** Since mult_P(Q) = m'_P ≤ ℓ_P:
- off-line points (m'_P = 0): mult_P(J') ≥ 2;
- free points (m'_P = 1): mult_P(J') ≥ 1, with equality only if P is nondegenerate non-radial;
- double points of A₂: mult_P(J') = 0 if P is nondegenerate non-radial, ≥ 1 if P is radial or
  L_P is singular and nonzero, ≥ 3 if L_P = 0;
- multiple points with m_P ≥ 3: P is radial or L_P = 0 (1.3(a)); mult_P(J') ≥ 0 in the first
  case and ≥ 2 in the second.

## 4. The excess identity

For a singular point P of F put

  d_P := Σ_{H ∈ A₂, H ∋ P} ν_P(H) − (m'_P − 1) − μ_P.

**Theorem 4.1.** (d₁ − r)(d₂ − r) = Σ_{P off-line} μ_P − Σ_{P on a line of A₂} d_P.

*Proof.* Count the zeros of all the f_H in two ways. By 1.1, Σ_H Σ_{P ∈ H} ν_P(H) = n(r + 1), and
the double sum equals Σ_P Σ_{H ∋ P} ν_P(H) = Σ_P (d_P + m'_P − 1 + μ_P) over all singular points.
Here Σ_P μ_P = r² + r + 1 (Lemma 1.2) and Σ_P (m'_P − 1) = b₂ − #{off-line points}, because the
multiple points of A₂ are exactly the singular points with m'_P ≥ 2 and contribute Σ(m_P − 1) = b₂,
free points contribute 0 and off-line points −1. For an off-line point d_P = 1 − μ_P. Hence

  n(r + 1) = Σ_{on} d_P − Σ_{off} μ_P + b₂ + r² + r + 1,

and with b₂ = d₁d₂ + n − 1 and d₁ + d₂ = n − 1 this is
d₁d₂ − r(n − 1 − r) = Σ_{off} μ_P − Σ_{on} d_P, whose left side is (d₁ − r)(d₂ − r). ∎

**Lemma 4.2 (tame points).** d_P = 0 if P is nondegenerate (whatever m'_P), and if P is a
saddle-node along a line H of A₂ (L_P = diag(0, e), e ≠ 0, zero eigendirection along H) with
m'_P ∈ {1, 2}.

*Proof.* Nondegenerate: μ_P = 1, and ν_P(H) = 1 for every H ∋ P by 1.3(b) (both eigenvalues are
nonzero), so d_P = m'_P − (m'_P − 1) − 1 = 0. Saddle-node along H: μ_P = ν_P(H) by 1.3(d); if
m'_P = 2 the other line H' is the e-eigendirection, so ν_P(H') = 1 and d_P = ν_P(H) + 1 − 1 − μ_P = 0;
if m'_P = 1, d_P = ν_P(H) − 0 − μ_P = 0. ∎

So for a counterexample the right-hand side of 4.1 is at least δ + 1 ≥ 1 (d₁ − r ≥ 1 by (I1) and
d₂ − r ≥ δ + 1), and by Lemma 4.2 it is carried entirely by off-line singular points, by free
points that are degenerate with their zero eigendirection transverse to the line, and by
degenerate points of A₂ with m'_P ≥ 3 or with L_P = 0. By Corollary 3.2 every one of these is a
point of multiplicity ≥ 2 of the curve J' = 0, of degree j = 3r − n. (Radial multiple points and
saddle-nodes along a line also lie on J' when m'_P ≤ 2, but they contribute nothing.)

For a free arrangement (d₁ = r) the identity says the right-hand side is 0; §7 checks this on
examples.

## 5. The theorem

**Theorem 5.1.** A counterexample (A₁, A₂) to Terao's conjecture in P² satisfies

  3·mdr(A₂) ≥ n + 2,  i.e.  deg(J/Q) ≥ 2.

Consequently (with (I1)) n ≤ 3d₁ − 5, i.e. d₂ ≤ 2d₁ − 6; and d₁ ≥ 7, n ≥ 15.

*Proof.* Let j = 3r − n. If j = 0, J' is a nonzero constant and mult_P(J') = 0 at every singular
point; by Corollary 3.2 there are no off-line and no free points, every double point of A₂ is
nondegenerate non-radial, and every point with m_P ≥ 3 is nondegenerate (radial). If j = 1, J' is a
linear form and mult_P(J') ≤ 1 everywhere: no off-line points; free points are nondegenerate
non-radial; double points are nondegenerate, or have L_P = diag(0, e) with e ≠ 0 in the basis of
the two lines (1.3(a)), i.e. are saddle-nodes along a line; points with m_P ≥ 3 are nondegenerate.
In both cases every singular point is tame (Lemma 4.2) and there are no off-line points, so the
right-hand side of Theorem 4.1 is 0, while (d₁ − r)(d₂ − r) ≥ δ + 1 ≥ 1. Hence j ≥ 2.
For the consequences: n + 2 ≤ 3r ≤ 3(d₁ − 1) gives n ≤ 3d₁ − 5 and δ = n − 2d₁ − 1 ≤ d₁ − 6; d₁ ≥ 6
by Abe (`TC_GENERAL.md` (W1)) and d₁ = 6 forces δ = 0, n = 13, excluded by
Dimca–Ibadula–Măcinic; so d₁ ≥ 7 and n = 2d₁ + δ + 1 ≥ 15. ∎

**Remark 5.2 (the extremal cases as a model).** The proof shows what j ∈ {0, 1} would force: a
saturated foliation of degree r with n = 3r (resp. 3r − 1) invariant lines whose singular points
are all nondegenerate multiple points of the arrangement (resp. plus nondegenerate free points on
the line J' = 0), and then Theorem 4.1 computes the lattice: (d₁, d₂) = (r, 2r − 1) with
N = r² + r + 1 (resp. (r, 2r − 2)). These are precisely the free arrangements with 3r or 3r − 1
lines whose minimal derivation is saturated: the full monomial arrangements
xyz(x^{r−1} − y^{r−1})(y^{r−1} − z^{r−1})(z^{r−1} − x^{r−1}) for j = 0, and e.g. their one-line
deletions for j = 1 (§7). So j = 0 and j = 1 do occur, but only when d₁ = r, i.e. for the free
member itself; the inequality of Theorem 5.1 is sharp in that sense.

**Corollary 5.3 (the window after Theorem 5.1).** A counterexample has d₁ ≥ 7, 0 ≤ δ ≤ d₁ − 6,
n ∈ [2d₁ + 1, 3d₁ − 5], and r = mdr(A₂) ∈ [⌈(n + 2)/3⌉, d₁ − 1]. For the classes with n ≤ 20:

| class | n | admissible r | j = 3r − n | (d₁ − r)(d₂ − r) |
|---|---|---|---|---|
| (6, 6) | 13 | – | – | excluded (Dimca–Ibadula–Măcinic) |
| (6, 7) | 14 | none | – | **excluded (5.1)**; was Barakat–Kühne (computer) |
| (6, 8) | 15 | none | – | **excluded (5.1)**; was Thm 10.1 (computer + Kneser) |
| (7, 7) | 15 | 6 | 3 | 1 |
| (7, 8) | 16 | none | – | **excluded (10.1)**; was Thm 10.4 (computer) |
| (7, 9) | 17 | none | – | **excluded (5.1)** |
| (8, 8) | 17 | 7 | 4 | 1 |
| (7, 10) | 18 | none | – | **excluded (5.1)** |
| (8, 9) | 18 | 7 | 3 | 2 |
| (8, 10) | 19 | none | – | **excluded (10.1)** |
| (9, 9) | 19 | 8 | 5 | 1 (r = 7 excluded by 10.1) |
| (8, 11) | 20 | none | – | **excluded (5.1)** |
| (9, 10) | 20 | 8 | 4 | 2 |

For (7, 7) TC is known by enumeration (`TC_ATTEMPT.md` Theorem 10.2) and (7, 8) is excluded by
Theorem 10.1 below, so the first open case overall remains 17 lines, class (8, 8) with r = 7 — which is part [B] of
`TC_ATTEMPT.md` §11 (A₂ nearly free with exponents (7, 10)), the part *not* covered by the running
enumeration. The running enumeration ((7, 9), and (8, 8) with r = 6) has become an independent
computational check of Theorem 5.1 rather than the decisive step for n = 17.

## 6. What survives: j ≥ 2

Theorem 4.1 and Corollary 3.2 turn TC (for the lattices in the window) into the statement

  (★) the singular points of the curve J' = 0, of degree j = 3r − n ≤ d₁ − δ − 4, cannot carry
      the excess (d₁ − r)(d₂ − r) ≥ δ + 1.

This is where the argument stops. What can be said about the first open values of j:

**j = 2 (classes (7, 8), (8, 10), and (9, 9) with r = 7).** J' is a conic. A smooth conic has no
singular point, so the right-hand side of 4.1 would be 0: impossible. If J' is a pair of distinct
lines, the excess is carried by their intersection point P₀ alone, with mult_{P₀}(J) = m'_{P₀} + 2
exactly; Proposition 3.1 leaves three possibilities: P₀ off-line and nondegenerate non-radial
(then μ_{P₀} = 1, the excess is 1, so δ = 0, d₁ = d₂ = r + 1, n = 2r + 3 = 3r − 2, r = 5: the
13-line class, already excluded); P₀ a free point which is a saddle-node of order δ + 2 with its
zero eigendirection transverse to its line and mult_{P₀}(J) = 3; or P₀ a degenerate point of A₂
with m_{P₀} ≥ 3 of a specific kind (non-dicritical of order 2 with m_{P₀} = 3, or dicritical of
order 2 with m_{P₀} = i_{P₀} + 1) whose blown-up singularities carry the excess. If J' is a double
line ℓ², every point of ℓ has mult_P(J') = 2 and the excess can be spread along ℓ: if ℓ is not
F-invariant, ω|_ℓ is a section of 𝒪_ℓ(r), so ℓ carries at most r singular points of F; if ℓ is
F-invariant, A₂ ∪ ℓ is a saturated arrangement of 3r − 1 invariant lines to which the j = 1
analysis applies, and the excess equals the number of singular points on ℓ not on A₂. I have not
been able to exclude the last two situations.

**j ≥ 3.** J' is a cubic or worse and (★) asks which singular curves of degree j can occur as J/Q.
The data of §3–4 give at each excess point a precise local model (a node of J' at an off-line
nondegenerate point contributes exactly 1; a saddle-node free point of order p with transverse
centre contributes p − 1 and has mult_P(J) ≥ 3; a degenerate point of A₂ with m_P ≥ 3 contributes
−d_P with mult_P(J) ≥ m_P + 2), so for the smallest open cases the excess is 1 or 2 and must sit
at one or two prescribed singularities of J'. For (7, 7) at 15 lines J' is a cubic with exactly one
unit of excess; TC holds there by Theorem 10.2, so some further global constraint kills this
configuration, but I do not know which.

**Further structure, not used above.** The cofactors K_H := θ(α_H)/α_H ∈ S_{r−1} satisfy
Σ_H K_H = 0, and at a singular point P with θ(P) = λ_P P: K_H(P) = λ_P for H ∌ P, while
K_H(P) − λ_P is the eigenvalue of L_P transverse to H for H ∋ P. Summing over H:
Σ_{H ∋ P} (transverse eigenvalue of H at P) = −n λ_P at every singular point; so θ(P) = 0 at
every off-line point, and at a radial point with m_P lines the common eigenvalue is −nλ_P/m_P. On
a line H the Lagrange relation for K_H|_H at the r + 1 zeros of f_H, combined with the
Camacho–Sad formula Σ_{P ∈ H} CS(F, H, P) = 1, reads Σ_{P ∈ H} λ_P/ε_H(P) = −1, where
ε_H(P) = −c_H ∏_{P' ≠ P} det_H(P', P) is the eigenvalue along H (f_H = c_H ∏_{P'} det_H(P', ·)).
At a radial point all ε_H(P), H ∋ P, coincide; around a cycle of lines joined at radial points
this is a Carnot-type multiplicative condition on the positions of the other singular points on
those lines. These identities constrain positions; I did not get a contradiction from them.

## 7. Computer checks of the structure

`work/foliation/inflect.m2` (Macaulay2) computes, for an arrangement over ℚ: the least-degree
Jacobian syzygy θ, ω = θ × E and its gcd, J = det(∂ω/∂x), the factorisation of J/Q, the degree of
the zero scheme of ω, the singular points off the lines and those that are not multiple points,
the profile, b₂ and Δ := b₂ − n + 1 − r(n − 1 − r), which equals (d₁ − r)(d₂ − r) when the lattice
has a free member. Results (r = syzygy degree minus (n − 1); the 15-line example, which needs √−1, is computed over
𝔽₁₀₁ with i = 10):

| arrangement | n | r | j | J/Q | deg Z(ω) | off-line | non-multiple | Δ |
|---|---|---|---|---|---|---|---|---|
| xyz(x²−y²)(y²−z²)(z²−x²), exp. (3, 5) | 9 | 3 | 0 | const | 13 = r²+r+1 | 0 | 0 | 0 |
| xyz(x⁴−y⁴)(y⁴−z⁴)(z⁴−x⁴), exp. (5, 9) | 15 | 5 | 0 | const | 31 | 0 | 0 | 0 |
| xyz(x−y)(x−z), exp. (2, 2) | 5 | 2 | 1 | a line | 7 | 0 | 1 | 0 |
| xy(x²−y²)(z²−x²)(z²−y²), exp. (3, 4) | 8 | 3 | 1 | z | 13 | 0 | 2 | 0 |
| B₃ minus x = 0, exp. (3, 4) | 8 | 3 | 1 | x (the deleted line) | 13 | 0 | 2 | 0 |
| xyz(x−y)(x−z)(y−z)(x+y−z)(x−y+z)(x−y−z) | 9 | 3 | 0 | const | 13 | 0 | 0 | 0 |

The last arrangement was entered as a non-free guess; Theorem 4.1 with j = 0 predicts that any
saturated extremal arrangement is free with exponents (r, 2r − 1) and N = r² + r + 1, and indeed
its profile came out as 3 quadruple, 4 triple, 6 double points, b₂ = 23, χ₀(0) = 15 = 3·5.
Arrangements with a line carrying ≥ n − r points (generic arrangements, arrangements with a point
of multiplicity > n/2, one-line perturbations of the examples above) have an unsaturated minimal
derivation (gcd(ω) ≠ 1) and are outside the scope of §1–5, as expected: saturation was proved from
(I1) and (I2), which hold in a counterexample but not in general.

## 8. Conclusion

- New theorem: a counterexample to TC in P² has 3·mdr(A₂) ≥ n + 2, hence d₂ ≤ 2d₁ − 6, d₁ ≥ 7,
  n ≥ 15. The narrow classes of `TC_GENERAL.md` §2 and the next classes δ = d₁ − 5 are gone for
  every n; the 14-line case has a theoretical proof; at 17 lines only the nearly-free part [B] of
  (8, 8) is open.
- The tool is geometric, not numerical: the inflection curve J of the foliation of the minimal
  derivation, J = Q·J', and the identity (d₁ − r)(d₂ − r) = excess of J'. It is the first
  constraint in this project that mixes the lattice numbers with the *positions* (through the
  singular points of J'), which is what `TC_GENERAL.md` §5 said a proof needs.
- TC itself is not proved. Within this framework it is equivalent, for the window lattices, to
  (★): the singular points of a curve of degree 3r − n ≤ d₁ − δ − 4 cannot carry excess
  (d₁ − r)(d₂ − r). §10 settles j = 2 (3·mdr(A₂) ≥ n + 3); the first open instances are j = 3
  with Bour = 2 ((8, 9), 18 lines) and j = 4 with Bour = 1 ((8, 8), 17 lines).

## 9. The excess is the Bourbaki degree (Nasrollah Nejad–Nouri)

Nasrollah Nejad and Nouri (arXiv:2609.22453) study the *Bourbaki degree* of a line arrangement:
for a minimal Jacobian syzygy ν of degree e = mdr, the cokernel of R(−e) → Syz(J) is an ideal
I_ν twisted, and Bour := deg(R/I_ν) (0 iff free). Their Theorem 2.1 is Bour = χ̄(e) with
χ̄(t) = t² − (n − 1)t + b₂ − (n − 1) the reduced characteristic polynomial (our n). For the
non-free member of a counterexample, χ̄(t) = (t − d₁)(t − d₂), so

  Bour(A₂) = (d₁ − r)(d₂ − r):

the left-hand side of Theorem 4.1 is the Bourbaki degree of A₂, and Theorem 4.1 says where the
Bourbaki scheme B_θ := Proj(R/I_θ) lives. Precisely:

1. The Bourbaki map sends η ∈ D₀(A₂) to h_η with θ × η = h_η·∇Q. For the syzygy ρ_p of a
   multiple point p (their Prop. 1.1, ρ_p ≡ −n·(∏_{H∌p} α_H)·∂_p mod E) one finds
   h_{ρ_p} = det(θ, E, p)/∏_{H∋p} α_H = R'_p, the residual polar curve of p (degree r + 1 − m_p):
   this is their u_p ∈ (I_θ)_{r+1−m_p}. Since (K_H − K_{H'})·α_Hα_{H'} = det(θ, E, p) for
   p = H ∩ H', all cofactor differences lie in I_θ, and with Σ_H K_H = 0 so do the cofactors:
   I_θ ⊇ (K_H : H ∈ A₂). The common zeros of the cofactors are exactly the singular points P of
   F with θ(P) = 0 and vanishing transverse eigenvalue along every line through P, i.e. the
   points with d_P ≠ 0 or off the lines — the excess points of §4. So Supp(B_θ) ⊆ excess points
   ⊆ Sing(J') (Corollary 3.2), and at an off-line point the local length of B_θ is μ_P (there
   Syz(J) ≅ T_{P²}(r − 1) locally).
2. Their Lemma 2.3 gives reg(I_θ) ≤ r − 1, hence Bour ≤ C(r, 2) and B_θ imposes independent
   conditions in degree r − 2; their Theorem 2.5 gives the type t = indeg I_θ ≤ r − m₂ + 1 (the
   residual polar curve of the second-largest point), with Bour ≤ C(r, 2) − C(m₂ − 1, 2).
3. Their Terao criterion (Theorem 2.18) reads, in our notation, C(d₁ + 1, 2) < n − 1 + C(m₂ − 1, 2)
   ⇒ TC. Inside the window (m ≤ d₁ − 1) the right-hand side is at most n − 1 + C(d₁ − 2, 2), so the
   criterion needs n ≥ 3d₁ − 1, outside Abe's range n ≤ 3d₁ − 3; it is weaker there than (W1),
   and Theorem 5.1 (n ≤ 3d₁ − 5) is strictly stronger. What their paper adds is the algebraic
   object and its homological constraints, not a new bound.

**Check on the Dimca–Pokora nine-line pair** (`work/foliation/bourbaki.m2`; the pair of
arXiv:2607.01985, same lattice (n₂, n₃, n₄) = (9, 7, 1), χ̄(t) = t² − 8t + 18, mdr 4 and 5, Bourbaki
degrees 2 and 3 by their Theorem 4.2). Both minimal foliations are saturated, Z(ω) has degree
r² + r + 1 (21 and 31), and the Bourbaki scheme computed from the syzygies is:
- mdr 4: J/Q = x·(conic); B_θ = the two points x = y² − 3yz − z² = 0, which are exactly the two
  nodes of J/Q and the two off-line singular points of F; Bour = 2 = Σ_off μ_P.
- mdr 5: J/Q = y·(quintic); B_θ = three reduced points: the two off-line singular points of F
  plus the double point [1:0:0] = {y + z = 0} ∩ {z = 0}, at which J/Q has multiplicity 3 and the
  foliation has L_P = 0 (μ_P = 4, ν = 2 on both lines, d_P = −1); Bour = 3 = 2 + 1.
In both cases B_θ ⊆ Sing(J/Q) scheme-theoretically and the off-line part of B_θ equals the
off-line singular scheme of ω. So on a genuine Ziegler pair the Bourbaki scheme is the excess
scheme of §4, with a degenerate on-line point contributing as Theorem 4.1 predicts.

**What this suggests.** TC for the window lattices is the statement B_θ = ∅ for the minimal
syzygy of every realisation; the two descriptions constrain B_θ from different sides — degree
(d₁ − r)(d₂ − r) and regularity ≤ r − 1 (algebra), support inside Sing(J') ∩ ⋂_p R'_p with the
local models of §3 (geometry). Neither side alone forces B_θ = ∅ when deg J' ≥ 2; a proof would
have to show that a scheme of that degree cannot sit at the singular points of a curve of degree
3r − n while lying on every residual polar curve.

## 10. The next step: deg(J/Q) = 2 is impossible

**Theorem 10.1.** A counterexample to TC in P² satisfies 3·mdr(A₂) ≥ n + 3, i.e. deg(J/Q) ≥ 3.
Consequently n ≤ 3d₁ − 6, δ ≤ d₁ − 7, and the classes (7, 8) [16 lines], (8, 10) [19 lines],
(9, 9) with mdr(A₂) = 7 [19 lines], (9, 12) [22 lines], … contain no counterexample. In particular
TC for 16 lines has a theoretical proof (Theorem 10.4 of `TC_ATTEMPT.md` was by enumeration).

The proof needs three lemmas that are of independent use. Throughout, E := D̃₀(A₂) is the sheaf of
Jacobian syzygies of A₂, a rank-2 bundle on P² with c₁(E) = −(n − 1) and c₂(E) = (n − 1)² − τ (from
0 → E → O³ → I_Σ(n − 1) → 0, Σ the singular scheme of A₂, length τ), and θ ∈ H⁰(E(r)) is the minimal
derivation; its zero scheme is the Bourbaki scheme B_θ of §9, of length (d₁ − r)(d₂ − r).

**Lemma 10.2 (the restriction of E to a line of A₂ is the Ziegler module).** For every H ∈ A₂,

  E|_H ≅ O_H(−e₁(H)) ⊕ O_H(−e₂(H)),

where (e₁(H), e₂(H)) are the exponents of the Ziegler multirestriction (A₂^H, μ). Consequently, for
r < e₂(H) (always true here: e₂ ≥ n − 1 − r ≥ d₂ + 1 > r), the restriction θ|_H ∈ H⁰(E(r)|_H) has the
form (g_H, 0) with g_H a binary form of degree r − e₁(H) on H, g_H ≠ 0, and

  Supp(B_θ) ∩ H = Z(g_H),   length(B_θ ∩ H) ≤ r − e₁(H).

In particular H contains a Bourbaki point iff e₁(H) ≤ r − 1, and f_H = g_H · f₁^H where
f₁^H := det_H(θ₁^H, E_H) is the form of degree e₁(H) + 1 of the lowest Ziegler basis element.

*Proof.* Let D_H(A₂) := {θ ∈ D(A₂) : θ(α_H) = 0}; it is a complement of S·E in D(A₂), hence
D_H ≅ D₀(A₂) as graded S-modules and D̃_H ≅ E. Ziegler's restriction θ ↦ θ|_H (a derivation
tangent to the plane H restricts to a vector field on H) is S-linear from D_H(A₂) to the
multiarrangement module D(A₂^H, μ) — the multiplicity condition holds because θ(α_H) = 0: at a
point P ∈ H with lines v = 0 (H) and v = c_iu through it, θ = a∂_u + b∂_v with b = 0, and
θ(v − c_iu) = −c_ia ∈ (v − c_iu) for all i forces a(u, 0) ∈ (u^{m_P − 1}). The map kills α_H D_H, so
it is a map of sheaves on H, E|_H → D̃(A₂^H, μ), between locally free sheaves of rank 2 (the
multiarrangement module is a reflexive graded module over ℂ[H], hence free, with exponents
(e₁, e₂), e₁ + e₂ = |μ| = n − 1). At a point of H that is not a multiple point both sides are the
vector fields tangent to the plane H, and the map is the identity; so it is injective. Both sides
have degree −(n − 1) (c₁(E) = −(n − 1); e₁ + e₂ = n − 1), and an injective map of bundles of the
same rank and degree on a curve is an isomorphism. The rest: θ|_H ∈ H⁰(O(r − e₁)) ⊕ H⁰(O(r − e₂))
and the second summand is 0; g_H = 0 would mean θ ∈ H⁰(E(r)(−H)) = H⁰(E(r − 1)) = D₀(A₂)_{r−1} = 0.
The zero scheme of the restricted section contains B_θ ∩ H and has the same support; the
factorisation f_H = g_H f₁^H is θ|_H = g_H·θ₁^H in the Ziegler module. ∎

**Lemma 10.3 (Bourbaki points on lines).** Let j = 3r − n. For every line H of A₂,
r − e₁(H) ≤ ⌊j/3⌋. Hence: for j ≤ 2 no Bourbaki point lies on a line of A₂; for 3 ≤ j ≤ 5 every
line carries at most one Bourbaki point, and a line through a Bourbaki point has e₁(H) = r − 1 and
n + 3 − 2r ≤ s_H ≤ r multiple points (so s_H = r when j = 3; s_H ∈ {r − 1, r} when j = 4).

*Proof.* If e₁(H) = r − k, Abe's gap bound e₂ − e₁ ≤ s_H − 2 for the (balanced) Ziegler
multirestriction gives s_H ≥ n + 1 − 2(r − k), while s_H ≤ e₁(H) + 1 = r − k + 1 (the form f₁^H of
degree e₁ + 1 vanishes at the s_H points and is nonzero, `TC_ATTEMPT.md` Thm 1(7) step 3). So
n + 1 − 2r + 2k ≤ r − k + 1, i.e. 3k ≤ j. For k = 1 the bounds read n + 3 − 2r ≤ s_H ≤ r; for j = 3
they coincide, s_H = r = e₁(H) + 1, so f₁^H has simple zeros exactly at the multiple points and the
one Bourbaki point on H is the zero of the linear form g_H. ∎

**Lemma 10.4 (lines in the inflection curve).** Let ℓ be a line and P ∈ ℓ a nondegenerate singular
point of F whose linear part L_P has ℓ as an eigendirection, with eigenvalue λ₁ along ℓ and λ₂
transverse. Write, in affine coordinates (u, v) centred at P with ℓ = {v = 0}, X₂(u, 0) = βu^k + ⋯
(k ≥ 2, β ≠ 0) if ℓ is not invariant.
(a) If ℓ is not invariant, then J|_ℓ = λ₁((k − 1)λ₁ + λ₂)·β·u^{k+1} + O(u^{k+2}) near P. So ℓ | J
    forces (k − 1)λ₁ + λ₂ = 0; if L_P is a Jordan block (λ₁ = λ₂ = λ ≠ 0) this is impossible, and ℓ
    is invariant.
(b) If ℓ is invariant, write X₁(u, 0) = A(u), X₂ = v·B̃(u, v), B(u) := B̃(u, 0) (the transverse
    eigenvalue function along ℓ). Then J = (r + 1)·v·A·(AB′ − A′B + B²) + O(v²), so ℓ² | J iff
    φ := B/A satisfies φ′ = −φ², i.e. iff φ ≡ 0 or φ = 1/(u − c) in every affine coordinate u on ℓ.
    In the second case ℓ carries exactly one singular point with nonzero transverse eigenvalue
    (and its Camacho–Sad index is 1); in the first case none.

*Proof.* J = (r + 1)·D with D = X₁²∂_uX₂ − X₂²∂_vX₁ + X₁X₂(∂_vX₂ − ∂_uX₁) (Proposition 2.1(1)).
(a) With X₁ = λ₁u + v·(…) + O(2), X₂ = λ₂v + b(u, v), b ∈ 𝔪², on v = 0: A := X₁(u, 0) = λ₁u + O(u²),
B := X₂(u, 0) = βu^k + ⋯, ∂_uX₂(u, 0) = B′, ∂_vX₂(u, 0) = λ₂ + O(u), ∂_uX₁(u, 0) = λ₁ + O(u) and
∂_vX₁(u, 0) = O(1). Hence D|_{v=0} = A²B′ − B²·O(1) + AB(λ₂ − λ₁ + O(u)) =
kβλ₁²u^{k+1} + λ₁β(λ₂ − λ₁)u^{k+1} + O(u^{k+2}) = λ₁((k − 1)λ₁ + λ₂)βu^{k+1} + O(u^{k+2}). For a
Jordan block the coefficient is kλ²β ≠ 0, so J does not vanish on ℓ near P unless β = 0, i.e.
X₂|_ℓ ≡ 0 near P, which (ℓ being a line, X₂|_ℓ a polynomial) means ℓ is invariant.
(b) X₂ = vB̃ gives ∂_uX₂ = v∂_uB̃, ∂_vX₂ = B̃ + v∂_vB̃, X₂² = O(v²), so D = v·X₁(X₁∂_uB̃ + B̃² − B̃∂_uX₁)
+ O(v²), and on v = 0 the bracket is AB′ + B² − BA′. As A ≢ 0 (otherwise X ≡ 0 on ℓ), ℓ² | J iff
AB′ − A′B + B² ≡ 0 iff (B/A)′ = −(B/A)². The solutions of φ′ = −φ² are φ ≡ 0 and φ = 1/(u − c).
In the second case A = (u − c)B: the zeros of A (the singular points on ℓ in the chart) are c and
the zeros of B; at the zeros of B the transverse eigenvalue vanishes, and at c it is B(c) ≠ 0
with A′(c) = B(c), so CS(F, ℓ, c) = B(c)/A′(c) = 1. ∎

*Proof of Theorem 10.1.* Let j = 2, so n = 3r − 2 and, by (I1), r ≥ 6 once n ≥ 16 (n = 13 is the
class (6, 6), excluded by Dimca–Ibadula–Măcinic). By Lemma 10.3 no Bourbaki point lies on a line
of A₂; so B_θ is supported at off-line singular points, where its length is μ_P (§9), and
Bour = Σ_{P off-line} μ_P = (d₁ − r)(d₂ − r) ≥ 1. Every Bourbaki point P is a singular point of the
conic J′ (Corollary 3.2), with mult_P(J′) = mult_P(J).
- J′ smooth: no singular point, Bour = 0. Contradiction.
- J′ = ℓ₁ℓ₂, two lines: B_θ is supported at the node P₀, where mult_{P₀}(J) = 2, so P₀ is
  nondegenerate and μ_{P₀} = 1: Bour = 1, i.e. d₁ = d₂ = r + 1, n = 2r + 3 = 3r − 2, r = 5, n = 13.
  Contradiction.
- J′ = ℓ², a double line: B_θ ⊆ ℓ, and at each of its points mult_P(J) = 2, so P is nondegenerate
  non-radial with μ_P = 1; thus B_θ consists of b := (d₁ − r)(d₂ − r) ≥ 2 distinct points of ℓ
  (b = 1 is the previous case). At such a P the degree-2 part of J is Q(P)·ℓ_P², a double line;
  by Proposition 3.1 that part is det(L_Pt, L_P²t), which is the product of the two distinct
  eigen-coordinates when the eigenvalues are distinct and λ²det(t, Nt) = c·η(t)² when
  L_P = λ(I + N), N = w ⊗ η nilpotent — a double line only in the Jordan case, with the line
  {η = 0} = ℂw the eigendirection. So every Bourbaki point is a Jordan point with eigendirection
  ℓ. By Lemma 10.4(a), ℓ is invariant. By Lemma 10.4(b), in an affine coordinate on ℓ in which the
  b Jordan points are finite, φ = B/A is either 0 or 1/(u − c); but at a Jordan point A = 0 and
  B = λ ≠ 0, so φ has a pole there: φ ≠ 0, and φ = 1/(u − c) has a single pole. Hence b ≤ 1.
  Contradiction.
So j ≠ 2, and with Theorem 5.1, j ≥ 3. The consequences follow from r ≤ d₁ − 1:
n + 3 ≤ 3r ≤ 3d₁ − 3 and δ = n − 2d₁ − 1 ≤ d₁ − 7; the classes listed have n = 3d₁ − 5 (or, for
(9, 9), the value r = 7 gives j = 2). ∎

**Remark 10.5.** Two by-products. (i) For any arrangement with 3·mdr = n + 2 whose minimal
derivation has a saturated foliation and balanced Ziegler restrictions, the same proof gives
χ̄(mdr) ≤ 1: such arrangements are free or nearly free. (ii) Lemma 10.4(b) says that an invariant
line which is a double component of the inflection curve carries at most one singular point with
nonzero transverse eigenvalue, and that one has Camacho–Sad index 1.

**What j = 3 looks like (classes (7, 7) at 15 lines, (8, 9) at 18, (9, 11) at 21, (10, 10) at 21).**
J′ is a cubic and Bour = a(r − 4 − a) with a = d₁ − r (so 1, 2, 3, 4 for the four classes). By
Lemma 10.3 a line carries at most one Bourbaki point, and only if it has exactly r multiple points
and e₁(H) = r − 1; such a point is a multiple point with ν_P(H) = 2 (then L_P = 0) or a free
saddle-node of order 2 with transverse centre (contribution 1, J′ nodal there with branches H and
the centre direction, by the tangent-cone computation of Proposition 3.1). Off-line Bourbaki points
are singular points of the cubic; at a node μ_P = 1; at a triple point of three concurrent lines
μ_P ≤ 2 (radial, or a saddle-node of order 2). Lemma 10.4 applies to every line component of J′
through a nondegenerate Bourbaki point. I have not completed the case analysis; the case
Bour = 1 at 15 lines is Theorem 10.2 of `TC_ATTEMPT.md` (enumeration), and Bour = 2 at 18 lines
is open.

## 11. The (8, 9) class at 18 lines: the full-monomial seed and its three-pencil neighbourhood

**11.1 The seed.** Let ζ be a primitive sixth root of unity and

  Q = yz (x⁶ − y⁶)(z⁶ − x⁶) ∏_{b ∈ μ₆ ∖ {1, ζ}} (y − bz),

eighteen lines. This is the full monomial arrangement A(6,1,3) = xyz(x⁶−y⁶)(y⁶−z⁶)(z⁶−x⁶)
(21 lines, free with exponents (7, 13)) with the three lines x, y − z, y − ζz removed. Computer
check (`work/pencil/seed18.m2`, over F₁₀₀₀₉ with ζ = 1045): point profile 2²⁴ 3²⁴ 6¹ 7²,
b₂ = 89, χ̄ = (t − 8)(t − 9); Jacobian syzygies of degrees 7, 11, 12, so mdr = 7 and
j = 3r − n = 3; Z(ω) has degree 57 = r² + r + 1 (saturated); the Bourbaki scheme is the two
reduced points [0:1:1], [0:ζ:1], which lie on no line of the arrangement and are exactly the
off-line singular points of ω (as Lemma 10.3 predicts for j = 3: no line has 7 points and
e₁ = 6); and

  J/Q = x (y − z)(y − ζz),

the product of the three deleted lines, with the Bourbaki points two of its three vertices. The
same holds for the two other deletion patterns (y − z, y − ζ²z and y − z, y + z removed).

The explanation is general. The degree-7 derivation of A(6,1,3) is a derivation of every
subarrangement, so mdr(A₂) ≤ 7 for every subarrangement A₂, with equality here by Theorem 10.1
(3·7 = 18 + 3). Its foliation has 21 = 3·7 invariant lines, the maximum allowed by Pereira's
bound, so its inflection curve is the product of the 21 lines and J/Q is the product of the
deleted ones. Deleting a line lowers b₂ by the number of points on it; to go from
b₂(A(6,1,3)) = 111 to 89 one needs 22 = 8 + 7 + 7, which forces a coordinate line and two
lines of the pencil that meets it in double points: the three arrangements above are the only
3-line deletions of A(6,1,3) in the class (8, 9).

**Rigidity.** Normalizing the three pencil centres to the coordinate points, every realization
of the lattice is given by nonzero numbers a_i (x = a_i y), c_j (z = c_j x), b_k (y = b_k z)
with a_i c_j b_k = 1 for the 24 triple points. Over ℚ this binomial scheme has 6 points in 4
components (`work/pencil/real18.m2`); the only non-degenerate ones are the Galois pair
ζ₆^{±1}. So the lattice has one realization up to projective equivalence and conjugation, and
no lattice-mate at all: Terao's conjecture holds for it trivially. Kneser's theorem says the
same without computation: six lines through [0:0:1], six through [0:1:0], four through
[1:0:0] with all 24 triple points force A and B to be cosets of μ₆ in ℂ*.

**11.2 Three-pencil lattices.** Call a lattice *three-pencil* if its lines are x = a y
(a ∈ A), z = c x (c ∈ B), y = b z (b ∈ C) and a subset K of the coordinate lines; the triple
points are the triples with abc = 1, every other intersection is double, and the realization
space is the group {a_i c_j b_k = 1} modulo the diagonal torus, whose components are indexed by
the torsion of Z^{|A|+|B|+|C|}/(relations) and are explicitly parametrized (Smith normal form).
This is the natural "neighbourhood" of the seed in which the cyclic relations can be weakened.
For n = 18 and χ̄ = (t − 8)(t − 9) the multiplicities m of the three centres and the number t of
triple points satisfy Σ C(m − 1, 2) + t = 64, and m ≤ 7 by (W3), which leaves six patterns
(|A|, |B|, |C|; K; t): (5,5,5; xyz; 19), (6,6,4; yz; 24), (6,5,5; yz; 24), (6,6,5; x; 28),
(6,5,6; x; 29), (6,6,6; ∅; 34).

- (6,6,4; yz; 24) is the seed: Kneser forces μ₆-cosets, and the three variants are the only
  lattices. Rigid, mdr 7.
- (6,5,5), (6,6,5), (6,5,6), (6,6,6) appear to have no realizations (Kneser-type argument
  sketched here, not written out in full): with S the sumset of two of the sets
  and H its stabilizer, Kneser's bound |S| ≥ |A+H| + |B+H| − |H| together with the required
  number of triples gives a contradiction for every order of H (for the collinear-centres
  version of (6,6,6), Cauchy–Davenport in the torsion-free group (ℂ, +) does it). The
  enumeration over all the group structures listed below confirms this: zero lattices.
- (5,5,5; xyz; 19): the enumeration over A, B, C ⊂ Z/N (N ≤ 30), Z, Z×Z/N (N ≤ 9), Z², Z²×Z/2
  (`work/pencil/pencil_enum.py`, with and without `--wide`) finds exactly six lattices up to isomorphism
  (`pencil_iso.py`): three with realization space a single Galois orbit of 7-th roots of unity,
  two with 8-th roots of unity, and one with a one-dimensional realization space,

    x = gⁱ y (0 ≤ i ≤ 4),  z = gʲ x (0 ≤ j ≤ 4),  y = g⁻ᵏ z (2 ≤ k ≤ 6),  x, y, z,

  the 19 triple points being the pairs (i, j) with 2 ≤ i + j ≤ 6. No lattice has two
  components. **All six are free with exponents (8, 9)** (`pencil_mdr_P1.out`): the five rigid
  ones directly, and the family at every point of ℂ* ∖ {degenerations}: by Yoshinaga's
  criterion a member is free iff the Ziegler multirestriction on the line x (multiplicities
  6, 6, 1, 1, 1, 1, 1) has exponents (8, 9), i.e. iff the 17 × 16 matrix of its degree-7
  derivations has full rank; the ideal of its 16-minors in ℚ[g], saturated by the binomials
  where the lattice changes, is (g⁴⁵) (`jump_P1_3_QQ.m2`), so no non-degenerate member is
  non-free.

So, within the groups and boxes searched, Terao's conjecture holds for the three-pencil
lattices with 18 lines in the class (8, 9): the only non-free ones found are the seed and its two
variants, and they have no lattice-mates. *(Correction 10 Oct 2026: the enumeration over
Z/N, Z, Z×Z/N, Z² is bounded, so this is not a classification of all three-pencil lattices.)* To
find a lattice with a free and a non-free realization one has to leave the monomial world, where
realization spaces stop being tori and the enumeration of `TC_ATTEMPT.md` §10 is the only
general tool.

**11.3 Sub-arrangements of free arrangements.** The seed also illustrates a general source of
mdr-7 members of the class (8, 9): if A₂ ⊂ A′ with A′ free with exponents (7, d₂′) and
n′ = 8 + d₂′ lines, then mdr(A₂) ≤ 7, hence = 7 when A₂ has 18 lines (Theorem 10.1), and the
k = n′ − 18 deleted lines must carry 8k − 2 points in total (counted successively). The
inflection curve of such an A₂ contains the deleted lines whenever the degree-7 derivation of A′
remains the minimal one. Supersolvable A′ with a modular point of multiplicity 8 give families
with moduli; whether any of their deletions has a free lattice-mate is not known to me.

## 12. The Bourbaki scheme lies scheme-theoretically in Sing(J/Q) (added 9 Oct 2026)

A note supplied by the user (an "integrated proof attempt") strengthens the support inclusion of
§9 to a scheme-theoretic one and draws numerical consequences. I checked the argument and tested
it; this section records what it adds. Notation: θ the minimal derivation of A₂, r = mdr(A₂),
B = B_θ its Bourbaki scheme of length ac = (d₁ − r)(d₂ − r), C = J/Q the residual inflection
curve of degree j = 3r − n.

**Lemma 12.1 (scheme-theoretic inclusion).** B ⊆ Sing(C) as schemes: at every point the local
equation of C lies in the square of the local Bourbaki ideal I, hence (C, C_u, C_v) ⊆ I.

*Proof (as in the note, verified).* Off the arrangement write the affine field as X = (A, B);
the Bourbaki ideal is (A, B) and the affine inflection equation is A²B_u − B²A_v + AB(B_v − A_u)
∈ (A, B)². At a point P of multiplicity m of the arrangement, with q the product of the m line
germs through P, Saito's criterion gives the local frame R = u∂_u + v∂_v, H = q_v∂_u − q_u∂_v of
the logarithmic tangent sheaf (det(R, H) = −mq), so X = fR + gH and I = (f, g). One has
∇_X R = X, ∇_R H = (m − 1)H, det(R, ∇_H H) = 0 (differentiate det(R, H) = −mq along H and use
H(q) = 0) and q | det(H, ∇_H H) (H and its acceleration are tangent to every line through P).
Expanding det(X, ∇_X X) gives

  D/q = −m·(f X(g) − g X(f) + (m − 1) f² g) + κ g³,   κ = det(H, ∇_H H)/q,

and since X(g) = fR(g) + gH(g) and X(f) = fR(f) + gH(f), every term lies in (f, g)². The local
equations of J and C differ from D and D/q by units. ∎

*Tests* (`work/foliation/schemelemma.m2`, `nonreduced.m2`): the inclusion Tjurina(C) ⊆ I and
the membership C ∈ (I²)^{sat} hold for every deletion of A(3,1,3) and A(4,1,3) tried (Bourbaki
lengths 0, 1, 2), for the Dimca–Pokora pair (one Bourbaki point on a line), and for six random
arrangements over F₁₀₁ whose Bourbaki schemes have non-reduced components of length 2, 3 and 5.

**Corollary 12.2.** If C is reduced then ac ≤ τ(C) ≤ (j − 1)², and ac ≤ (j − 1)(j − 2) if C is
irreducible. For j = 3 this gives ac ≤ 4, and the note's line-intersection argument (a line
meets B in length ≤ 1 by Lemma 10.3) together with the local normal form at a triple point of
three concurrent lines improves it to ac ≤ 3. So, when C is reduced, the j = 3 classes are
(7, 7) at 15 lines (ac = 1), (8, 9) at 18 (ac = 2) and (9, 11) at 21 (ac = 3), and B is the node
set of a triangle, the nodes of a conic plus a secant, the length-2 or 3 scheme of a cusp or a
tacnode, or a sub-scheme of these. The seed of §11.1 (triangle, two of its nodes) shows that this
local geometry does occur, so the corollary cannot exclude these classes by itself.

**What the inclusion does not give.** (i) Nothing when C is not reduced: Sing(C) then contains
the multiple component. For j = 3 and C = ℓ²ℓ′, every Bourbaki point lies on ℓ; an off-line
Bourbaki point P ∈ ℓ ∖ ℓ′ has mult_P(J) = 2 with tangent cone ℓ², so by the tangent-cone
computation of Proposition 3.1 it is a Jordan-block point with eigendirection ℓ, ℓ is invariant
(Lemma 10.4(a)), and Lemma 10.4(b) allows at most one such point on ℓ, each of Bourbaki length
μ_P = 1. The point ℓ ∩ ℓ′, Bourbaki points on arrangement lines, and the case C = ℓ³ (every point
of ℓ has mult_P(J) ≥ 3, so is radial or degenerate) are not covered by this argument; I have not
completed them. (ii) No relation to the free lattice-mate A₁: the inclusion is a statement about
A₂ alone, like everything in §§1–10. The note formulates the missing step exactly: for the
matroid M with realization space Σ_M and the Fitting ideal 𝔑_M of the degree-d₁ logarithmic
conditions, Terao's conjecture for M is the saturation statement 𝔑_M·O(Σ_M) = O(Σ_M), i.e.
the non-free determinantal locus is supported on the incidence boundary. On an irreducible
component with a free point this is the absence of an internal rank-drop locus; across components
it is a comparison that no semicontinuity argument makes. This is where the attempt stops.

## Sources

- J. V. Pereira, Vector fields, invariant varieties and linear systems, Ann. Inst. Fourier 51
  (2001) 1385–1405 (extactic curves; the bound 3·deg F on invariant lines).
- C. Camacho, P. Sad, Invariant varieties through singularities of holomorphic vector fields,
  Ann. of Math. 115 (1982) (the index formula quoted in §6).
- M. Brunella, Birational geometry of foliations, IMPA (Milnor numbers under blow-up, used in the
  j = 2 discussion of §6).
- The sources of `TC_ATTEMPT.md` for (I1), (I2) and the window.
- A. Nasrollah Nejad, S. Nouri, The Bourbaki degree of line arrangements, arXiv:2609.22453 (§9).
- A. Dimca, P. Pokora, A nine-line counterexample to a conjecture on the minimal degree of Jacobian relations, arXiv:2607.01985 (the pair of §9).
