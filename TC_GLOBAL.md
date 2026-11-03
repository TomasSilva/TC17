# Terao's conjecture over ℚ: the non-free member as a rational dynamical system

**Status (15 Oct 2026).** Not a proof of TC(ℚ). This note looks for a *global* reason why a
counterexample over ℚ cannot exist. It finds one global object behind every non-free
realisation, and turns it into four theorems and two new results over ℚ:

- **Theorem A (§1).** Yoshinaga's criterion is a statement about rational maps.
  - A line H jumps iff it carries a rational self-map of degree d₁ − 1.
  - That map fixes every multiple point of H, with local degree ≥ m_P − 1, so points with
    m_P ≥ 3 are *superattracting* fixed points.
  - The minimal derivation of a non-free member induces such a map Φ_H on **every line at once**.
  - The Camacho–Sad index of the foliation is the holomorphic fixed-point index of Φ_H.
  - Consequence (Lemma A2): a line all of whose points are at least triple has at most e₁ points.
- **Theorem B (§2).** On a 4-point line, the jump positions are exactly the *critically fixed*
  rational maps with the given critical profile.
  - Such maps are classified by planar graphs (Cordwell–Gilbertson–Nuechterlein–Pilgrim–Pinella,
    Hlushchanka).
  - The planar-graph count reproduces the degree of every jump polynomial: all 136 balanced vectors
    with K even and K ≤ 20, no mismatch.
  - It explains the jump sets computed in `TC_RATIONAL.md`. For example (4,4,4,4) = K₄
    (equianharmonic) + six doubled 4-cycles (ℚ(√21)), and (D, D, 1, 1) = z^D for every D.
- **Theorem C (§3).** The residual inflection curve J′ = J/Q meets each line exactly in:
  - the excess ramification of Φ_H at the multiple points;
  - the fixed points of Φ_H off the arrangement;
  - the free critical points of Φ_H.

  So one quartic (at 17 lines) interpolates all seventeen line maps. In R₁₇ᵃ and R₁₇ᵇ the conic
  factor of J′ carries the free critical points.
- **Theorem E (§4).** Inside a family through free points, a non-free point is a *simultaneous
  tangency*: the jump function of every line vanishes there to order ≥ 2. So it is a singular
  point of the realisation space (the mechanism of the known Ziegler pairs), or every line's jump
  divisor pulls back non-reduced.
- **New ℚ-statements.**
  - TC(ℚ) holds for every lattice, of any size n ≡ 3 (mod 4), that has a 4-point line with
    multiplicities (D, D, 1, 1) (§2).
  - In the 17-line window, every line through the jumping point P₀ of a rational non-free member
    has exactly 7 points, one of them a double point (§1, §5).
    - Six-point lines through P₀ are critically fixed maps of degree 6. Over ℚ their 24 to 40
      positions are all irrational (exact, by msolve). For 9 of the 16 vectors they are not even
      real.
    - On seven-point lines through P₀ the vectors (4, 2⁶) and (3², 2⁵) are impossible.

§5 assembles these into the global argument over ℚ and marks, step by step, what is proved and
what is heuristic. §6 states the three precise statements that would turn it into a proof.

**Added later on 15 Oct 2026 (§7–§9).**
- **(M1) is proved for every lattice with a four-point line** (Theorem F, §7), for any number of
  lines up to 31, and for all n given simple jump roots.
  - On such a lattice freeness is constant on every irreducible component of the realisation
    space, so a counterexample must use two different components.
  - Two ingredients make this work. The four points on the line *linearise* the realisation space
    over the cross-ratio, so the component of free arrangements is a vector bundle over a curve.
    And a new lemma (F1, by Krull's height theorem) shows that a degenerating free basis collapses
    exactly at the Bourbaki point. That lemma also completes the proof of Theorem E for every line.
- **Theorem G (§8)** says where (M1) could still fail on other lattices: at singular points of a
  component, at fibres that jump in dimension, or where the family is tangent to a jump
  hypersurface. Along such a non-free divisor every line with at most five points is frozen at a
  special position.
- **(M2) is not proved (§9).** For lattices with a four-point line it reduces to a finite
  linear-algebra problem: an unforced harmonic rank drop of the concurrency matrix. Over ℚ at
  17 lines this is a targeted enumeration of four-direction arrangements, not yet run.

Notation as in `TC_RATIONAL.md` and `TC_FOLIATION.md`:
- L is a lattice of n lines with χ₀ = (t − d₁)(t − d₂);
- A₁ is free and A₂ is not;
- r = mdr(A₂) ≤ d₁ − 1, and θ ∈ D₀(A₂) is the derivation of degree r;
- for a line H, k_P = m_P − 1 are the Ziegler multiplicities of its points P, s = s_H is their number,
  and K = Σ k_P = n − 1;
- (e₁(H), e₂(H)) are the exponents of (A^H, k);
- (s : t) are coordinates on H, and α_P = s − p t for P = (p : 1).

## 0. The idea

A non-free realisation is usually pictured as a "special position", one coincidence per line,
and Yoshinaga's criterion makes these coincidences equivalent. That picture hides the structure.

The obstruction to freeness is one global object, the derivation θ of degree r < d₁. On each line
it is a rational map with prescribed superattracting fixed points. So the question becomes:

> can one incidence structure carry, in one rational realisation, a coherent system of ℚ-rational
> dynamical systems of degree d₁ − 1 (one on each line, glued by one foliation), and in another
> realisation none at all?

Dynamics on P¹ is rigid in exactly the cases that matter. Maps whose critical points are all fixed
form a finite set, classified by planar graphs (Thurston rigidity). Over ℚ, the few that are
rational sit at symmetric positions in every case computed. The rest of this note makes that
precise and says how far it goes.

## 1. Line maps (Theorem A)

For a pair of binary forms (f, g) of degree e, write h = gcd(f, g), (f, g) = h·(f′, g′), and
Φ = [f′ : g′] : P¹ → P¹. The derivation f∂_s + g∂_t sends α_P to f − p g = h·(f′ − p g′).

**Theorem A.** f∂_s + g∂_t lies in D(A^H, k)_e iff for every point P of H

  ord_P(h) + ord_P(f′ − p g′) ≥ k_P.

Here ord_P(f′ − p g′) > 0 iff Φ(P) = P, and then it equals the local degree of Φ at P. In
particular, when gcd(f, g) = 1, every multiple point of H is a fixed point of Φ of local degree
≥ k_P, and the points with m_P ≥ 3 are superattracting.

*Proof.* If g′(P) = 0 then f′(P) ≠ 0, so f′ − p g′ does not vanish at P and Φ(P) = ∞ ≠ P.
Otherwise Φ − p = (f′ − p g′)/g′ near P, which vanishes at P iff Φ(P) = P, to order equal to
the local degree. (For P = ∞ exchange the roles of s and t.) ∎

**Corollary A1 (Yoshinaga's criterion, dynamically).** A realisation of L is free iff one
(equivalently every) line H carries no nonzero (f, g) of degree d₁ − 1 as in Theorem A.

*Proof.* By Yoshinaga, freeness is e₁(H) = d₁, and e₁(H) ≤ d₁ always holds since e₁e₂ ≤ d₁d₂. ∎

**The global form.** Let K_H = θ(α_H)/α_H and θ_H = θ − K_H·E. Then θ_H is tangent to H, and its
restriction (f_H, g_H) is a nonzero element of D(A^H, k)_r (`TC_FOLIATION.md` 1.1). So **one
derivation gives a line map Φ_H on every line simultaneously.** Two dictionary entries:
- (a) The fixed points of Φ_H, i.e. the zeros of s·g_H − t·f_H, are the singular points on H of
  the foliation F_θ (`TC_FOLIATION.md` 1.1).
- (b) **Camacho–Sad = holomorphic index.** At a simple fixed point P (Φ_H′(P) ≠ 1) with h(P) ≠ 0,

  CS(F_θ, H, P) = 1 / (1 − Φ_H′(P)).

  *Proof.* Take a chart y = 1 in which P is finite and not a pole of Φ_H, with H = {w = 0}. There
  the planar field is X = (f − u g, −w g) along H.
  The tangential eigenvalue is (f − ug)′(p) = g(p)(Φ′(p) − 1), using f(p) = p g(p). The
  transverse eigenvalue is −g(p). Their ratio is the index. ∎

  So the Camacho–Sad formula Σ_{P∈H} CS = H·H = 1 *is* the holomorphic fixed-point formula
  Σ 1/(1 − Φ′) = 1. And "radial at a point with ≥ 3 lines" (`TC_FOLIATION.md` 1.3(a)) means
  CS = 1, i.e. Φ_H′(P) = 0: superattracting.

**Lemma A2 (lines without double points).** If every point of a multiarrangement on P¹ has
k_P ≥ 2, then s ≤ e₁.

*Proof.* Suppose s ≥ e₁ + 1 and take (f, g) ≠ 0 of degree D = e₁.
1. If s g − t f ≡ 0, then (f, g) = h·(s, t). The conditions give α_P^{k_P − 1} | h for every P, so
   D − 1 ≥ Σ(k_P − 1) ≥ s ≥ D + 1. This is a contradiction.
2. So W = s g − t f is a nonzero form of degree D + 1 vanishing at the s ≥ D + 1 points. Hence
   s = D + 1, and every zero of W is simple and is a point of H.
3. W = h·(s g′ − t f′). A zero P of h therefore has ord_P(f′ − p g′) = 0, which forces
   k_P ≤ ord_P h = 1. So h = 1.
4. Now Φ has degree D, and all D + 1 fixed points are superattracting.
   - D = 1 is impossible, since a Möbius map has no critical point.
   - For D ≥ 2 the holomorphic fixed-point formula gives Σ 1/(1 − 0) = D + 1 = 1. Contradiction. ∎

*Consequences.*
- In any arrangement, a line all of whose points are at least triple has s_H ≤ e₁(H) ≤ mdr.
- In the 17-line window of `TC_FILTER.md`, take A₂ (r = 7, jumping point P₀):
  - An 8-point line has a double point. This recovers the exclusion of (2⁸) in Lemma F1 there,
    without Wakefield–Yuzvinsky.
  - A 7-point line through P₀ has e₁ = 6 (`TC_FOLIATION.md` Lemma 10.3), so it too has a double
    point. The vectors (4,2,2,2,2,2,2) and (3,3,2,2,2,2,2) cannot occur on a line through P₀. This
    is new; the (6, 10) loci of 7-point lines were never computed.

**Check** (`work/global/linemaps.m2`), on R₁₇ᵃ and R₁₇ᵇ, all 34 lines:
- Φ_H has degree 7 and gcd(f_H, g_H) = 1 on every line;
- every multiple point is fixed, with local degree ≥ m_P − 1;
- where the local degree exceeds m_P − 1, the excess is accounted for by Theorem C.

## 2. Four-point lines are critically fixed maps (Theorem B)

A rational map is *critically fixed* if each of its critical points is a fixed point. Such maps
are postcritically finite, so by Thurston rigidity there are finitely many in each degree, up to
Möbius conjugacy. Cordwell, Gilbertson, Nuechterlein, Pilgrim and Pinella (2015) and
Hlushchanka (2019) classify them by the Pilgrim–Tan blow-up construction:

> critically fixed maps of degree D, up to conjugacy ⟷ connected planar loopless multigraphs with
> D − 1 edges, up to orientation-preserving homeomorphism of S².

Under this correspondence a vertex of valence v is a critical fixed point of local degree v + 1.
The other fixed points of a critically fixed map are repelling, since every attracting or
parabolic cycle attracts a critical point. So they are simple, and there are D + 1 − c of them,
where c is the number of critical points.

**Theorem B.** Let k = (k₁, …, k₄) be a balanced multiplicity on four points, with K = 2d even.
Then e₁ ∈ {d − 1, d}, and the jump set J(k) is in bijection with the pairs (Φ, λ) where:
- Φ is a critically fixed map of degree D = d − 1;
- its critical points are exactly the points with k_i ≥ 2, of local degree exactly k_i;
- λ labels the points with k_i = 1 by distinct non-critical fixed points of Φ;
- pairs are taken modulo automorphisms of Φ that fix its critical points.

These automorphisms are trivial unless c = 2 (Φ = z^D, automorphism group μ_{D−1}). The bijection
sends (Φ, λ) to the cross-ratio of the four labelled points. Hence

  |J(k)| = (number of planar graphs with valences k_i − 1) · (D + 1 − c)!/(D − 3)!  (÷ (D − 1) when c = 2).

*Proof.*
1. *e₁ ≥ d − 1.* This is Abe's bound |e₂ − e₁| ≤ s − 2 = 2.
2. *The jump gives a map with no common factor.* A jump gives (f, g) of degree D in
   D(k)_{d−1} (Theorem A). Write (f, g) = h·(f′, g′) with h = ∏ α_i^{a_i}; zeros of h away from
   the four points only waste degree. Then Φ = [f′ : g′] has degree D − e, e = Σ a_i, and needs
   ramification Σ (k_i − a_i − 1)⁺ ≥ Σ (k_i − 1) − e = 2D − 2 − e. Riemann–Hurwitz allows only
   2(D − e) − 2. So e = 0.
3. *The local degrees are exact.* Riemann–Hurwitz again: Σ (k_i − 1) = 2d − 4 = 2D − 2. So the
   local degrees are exactly k_i and there are no other critical points; Φ is critically fixed.
4. *Conversely,* such a Φ and λ give (f, g) in D(k)_{d−1} by Theorem A. The configuration
   determines Φ, because the kernel at a jump point is one-dimensional (Abe's bound). The count
   then follows from the classification. ∎

**Verification** (`work/global/charge_graphs.py`). The script enumerates the planar multigraphs
and compares the predicted |J(k)| with the number of interior roots of the jump polynomial of
`work/rational/jump4_all.out`. All roots there are simple. Result: **all 136 balanced vectors
with K even, K ≤ 20, match exactly.** (Beyond K = 20 the brute-force rotation enumeration is too
slow; it is not a limitation of the theorem.)

**What it explains.**

| vector k | graphs | jump set |
|---|---|---|
| (3,3,3,3) | the three 4-cycles | {−1, 2, ½} |
| (4,4,4,4) | K₄ (two mirror embeddings) + six doubled 4-cycles | t² − t + 1, and one S₃-orbit in ℚ(√21) |
| (5,5,5,1) | the doubled triangle, one embedding (S₃-symmetric map) | its five non-critical fixed points: −1, 2, ½ and the roots of t² − t + 1 |
| (D, D, 1, 1) | D − 1 parallel edges: Φ = z^D | μ_{D−1} ∖ {1}, the nontrivial (D − 1)-th roots of unity |

The last line holds **for every D**: J(1, 1, D, D) = μ_{D−1} ∖ {1}. The jump polynomials of
`jump4_all.out` show it for D = 3, 4, 5, 6, 7 and D = 14, e.g. Φ₁₃ at K = 30. It is a rational
statement for all n at once.

**Corollary B1 (TC(ℚ), any number of lines).** Let L be a lattice with n ≡ 3 (mod 4) lines and a
line with four points of Ziegler multiplicities (D, D, 1, 1), D = (n − 3)/2. Then all realisations
of L over ℚ have the same freeness.

*Proof.* D is even, so μ_{D−1} contains no rational number other than 1. Then J has no rational
point, and Lemma 2.1 of `TC_RATIONAL.md` applies. ∎

This extends Theorem 3.2(b) of `TC_RATIONAL.md`, which needed n ≤ 27, for this vector, to all n.

**Galois and reality.** The set of critically fixed maps with a given labelled profile is
Gal(ℚ̄/ℚ)-stable. Complex conjugation acts on the graphs by mirror image. So:
- a jump point is real only if its plane graph is achiral. K₄ is chiral, hence the non-real
  equianharmonic pair; the doubled 4-cycles are achiral and their jump points are all real;
- a jump point is rational only if its map is Galois-invariant.

All rational jump points up to K = 30 are harmonic. For vectors with a multiplicity-preserving
symmetry this has a clear source: the map commutes with an involution fixing two of the points
and swapping the other two, which forces cross-ratio −1. But (2, 8, 9, 11) and (4, 6, 7, 13) at
K = 30, with all multiplicities distinct, show that symmetry of the labelled configuration is not
the only source. Which planar graphs give Galois-invariant maps is the same kind of question as
for dessins d'enfants, and is open. This is where "rational ⟹ harmonic" for all K would have to
come from (§6, (M3)).

**The harmonic maps of the 17-line window** (`work/global/harmonic_maps.m2`). Coordinates z = x/y,
with the points at 0, ∞, 1, t in the order of the vector.

| vector (window order) | t | critical points (local degree) | non-critical fixed points other than the double point |
|---|---|---|---|
| (5,5,5,1) | −1 | ∞, 1, −1 (5 each); double point at 0 | 3, −3, ±√−3 |
| (5,5,3,3) | −1 | 1, −1 (5); 0, ∞ (3) | roots of z⁴ + 22z² + 1 (none rational) |
| (5,4,4,3) | 2 | 2 (5); ∞, 1 (4); 0 (3) | 4, 4/3, and the roots of z² − z + 1 |

By Theorem C these are exactly the points where the quartic J′ of a rational A₂ meets such a line.

## 3. The inflection curve interpolates the line maps (Theorem C)

Let J = det(E, θ, θ(θ)) be the inflection curve of the foliation of θ (`TC_FOLIATION.md` §2).
It has degree 3r, is unchanged by θ ↦ θ + aE, and factors as J = Q·J′ with deg J′ = j = 3r − n.

**Theorem C.** Let θ be a derivation of A of degree r with saturated foliation, H a line of A,
and (f, g) = θ_H|_H. Then, as binary forms on H,

  (J/α_H)|_H = c_H · (s g − t f) · Jac(f, g),  c_H ∈ ℚ*,  Jac(f, g) = f_s g_t − f_t g_s.

If gcd(f, g) = 1, then dividing by (Q/α_H)|_H = ∏_P α_P^{k_P} gives

  J′|_H = c_H · ∏_P α_P^{ν_P − k_P} · W_off · R_free,

where:
- ν_P ≥ k_P is the local degree of Φ_H at P;
- W_off (degree r + 1 − s_H) vanishes at the fixed points of Φ_H off the arrangement;
- R_free vanishes at the critical points of Φ_H off the arrangement.

**In words:** J′ ∩ H = (excess ramification at the multiple points) + (other fixed points) +
(free critical points). The total is j on every line.

*Proof.*
1. In the chart y = 1 with H = {w = 0}, let u be the coordinate along H. Then the planar field is
   X = (f − u g, −w g) along H. In the notation of `TC_FOLIATION.md` Lemma 10.4(b) this means
   A = f − u g and B = −g, and that lemma gives J = (r + 1)·w·A·(AB′ − A′B + B²) + O(w²).
2. With Φ = f/g one finds AB′ − A′B + B² = g²Φ′ = f′g − f g′.
3. Homogenising, A becomes −(s g − t f), and f′g − f g′ becomes Jac(f, g)/r (Euler's identity).
4. For the second form, s g − t f = ∏_P α_P · W_off and Jac(f, g) = ∏_P α_P^{ν_P − 1} · R_free.
   Divide by ∏ α_P^{k_P}. ∎

If gcd(f, g) = h, which happens on a line through a Bourbaki point, then
Jac(hF, hG) = ((D + 1)/D)·h²·Jac(F, G) for linear h and deg F = D. So h enters (J/α_H)|_H to the
power 3.

**Verification** (`work/global/jprime_lines.m2`). The first identity holds exactly on all
17 + 17 + 9 lines of R₁₇ᵃ, R₁₇ᵇ and B₃.

**Examples.**
- **R₁₇ᵃ, line y = 0.** It has eight points. The excess ramification sits at (4:0:1) and
  (8:0:1), exactly where the two rich lines x − y − 4z and x − 4y − 8z cross it. The two free
  critical points are 2s² − 11st + 20t² = 0, which is the trace of the conic factor
  2x² − 2xy + 2y² − 11xz + 10yz + 20z² of J′.
- **Pattern in R₁₇ᵃ and R₁₇ᵇ.** In both arrangements:
  - the conic carries the free critical points of the 7- and 8-point lines;
  - the lines with 5 or 6 points have *critically fixed* maps. Their free critical points are all
    absorbed by excess at multiple points; for example the 5-point line z of R₁₇ᵃ has excess 1 at
    the point (1:1:0).
- **The four-point lines of a rational A₂ in the 17-line window.** By §2, J′ meets such a line
  exactly in the four repelling fixed points of its critically fixed map: the last column of the
  table in §2.

**What C adds.** Yoshinaga makes the jump conditions of the n lines equivalent, so they cannot be
counted as independent. Theorem C says what does tie the lines together: a single curve of degree
j = 3r − n (a quartic at 17 lines) passes through the "dynamical residue" of every line map. On a
4-point line that residue is determined by the jump position alone. A plane quartic is fixed by
14 general points, and four lines in general position carry 16 points of it. So four small lines
of a non-free A₂ pin down J′, and every other line must reproduce it.

## 4. Inside a family, a jump is a simultaneous tangency (Theorem E)

For a line H, write Θ_H for its jump function. For d₁ = d₂ = d this is the determinant of the
K × K matrix of the degree-(d − 1) Ziegler conditions, a function of the positions on H.

**Theorem E.** Let d₁ = d₂, let C be an irreducible component of the realisation space of L that
contains a free point, and let A₀ ∈ C be non-free with C smooth at A₀. Then for every line H,
Θ_H ∘ π_H lies in m²_{A₀}. Hence:
- every component N₁ of the non-free locus of C with N₁ ⊄ Sing C appears with multiplicity ≥ 2
  in div(Θ_H ∘ π_H), for every line H;
- if, for one line H, π_H*(J_H) is reduced in the interior of C, then every smooth point of C
  is free.

*Proof.* Let γ be an arc through A₀ that is not contained in the non-free locus.
1. Say the exponents of H at A₀ are (d − j_H, d + j_H). If j_H ≥ 2, the K × K matrix has a kernel
   of dimension j_H at t = 0, so its determinant vanishes to order ≥ j_H ≥ 2.
2. If j_H = 1, `TC_RIGIDITY.md` Lemma 3 gives ord_t Θ_H(π_H(γ(t))) = ord_t c(t) ≥ 2, where c is
   the Saito determinant of the family. Its proof uses only that the family of logarithmic
   bundles is flat with generically split fibre.
3. If d(Θ_H ∘ π_H)(A₀) ≠ 0, then an arc with γ′(0) ∉ ker d(Θ_H ∘ π_H) has order 1, a
   contradiction. ∎

**Readings.**
- **Over ℂ.** A non-free point of a component C that contains free points is either a singular
  point of C itself, or a point where C is tangent to the jump locus of every line.
  - Singular points of the realisation space that are smooth points of each component through
    them do not help. Theorem E applies to each component separately. So two smooth surfaces
    crossing along a curve, as in the Ziegler pairs of Barakat–Kühne–Pokora, could only produce a
    counterexample if each surface were tangent to the jump loci along the crossing curve.
  - The tangent case never occurs in the families computed so far. In the 13- and 15-line
    families of `TC_RIGIDITY.md` §3 every jump function factors into boundary factors.
- **Proof status.** For j_H = 1 the proof uses `TC_RIGIDITY.md` Lemma 3(c). That lemma needs the
  restricted frame to remain a basis on H, which fails if H passes through the point where the
  frame collapses. Lemma F1 below shows that this point is the Bourbaki point, through which no
  line with j_H = 1 passes. So Theorem E holds as stated, for every line.
- **On a 4-point line.** All roots of the jump polynomial are simple. This is the data for
  K ≤ 30, consistent with Epstein's transversality theorem for postcritically finite maps. So tangency means the
  cross-ratio function λ_H : C → P¹ is *stationary* at A₀: dλ_H = 0. Over ℚ this is a rational
  critical point of λ_H whose critical value is harmonic.

## 5. The argument over ℚ

Let (A₁, A₂) be a counterexample over ℚ with lattice L and χ₀ = (t − d₁)(t − d₂). Each step below
is labelled by its status. Specialisations to the open 17-line class (8, 8)[B] are in brackets.

**Step 1 — A₂ is a rational dynamical system** [proved].
- D₀(A₂)_r is a ℚ-vector space, so θ can be taken rational. On every line H it induces a line
  map Φ_H ∈ ℚ(z) whose fixed points contain all multiple points, superattracting of local degree
  ≥ m_P − 1 (Theorem A).
- Its degree is r, or r − z(H) after the Bourbaki factor is removed (`TC_FOLIATION.md`
  Lemma 10.2).
- The Bourbaki scheme and J′ are defined over ℚ.
- A₁ carries no such map in degree d₁ − 1 on any line (Corollary A1).
- [17 lines: deg Φ_H = 7 on lines missing P₀ and 6 on lines through it; P₀ ∈ P²(ℚ); J′ is a
  rational quartic singular at P₀.]

**Step 2 — the small lines of A₂ are arithmetically rigid** [structure proved, rationality computed].
- **4-point lines.** Φ_H is one of the finitely many critically fixed maps of its profile
  (Theorem B), and it is ℚ-rational. For K ≤ 30 the rational ones sit only at harmonic positions
  (`TC_RATIONAL.md` Theorem 3.1).
  [17 lines: vectors (5,5,5,1), (5,5,3,3), (5,4,4,3) only, at the positions of the table in §2.]
- **5-point lines.** Φ_H has one free critical point and lies on a jump curve of geometric genus
  ≥ 3, so there are finitely many rational ones (Faltings). The ones found have small height
  (`TC_RATIONAL.md` §4).
- **Lines through P₀** [17 lines, new].
  - **Six points.** A line through P₀ has e₁ = 6, so its lowest Ziegler element is a
    critically fixed map of degree 6: Σ(k_P − 1) = 10 = 2·6 − 2, and common factors are excluded
    as in Theorem B. So it is one of finitely many, counted by planar graphs with five edges (for
    (3,3,3,3,2,2): the 24 labelled paths). This explains the "finitely many positions" of
    `TC_FILTER.md` Lemma F1.
    - **Counts.** For all sixteen 6-point vectors the planar-graph count (24, 36 or 40,
      `charge_six.out`) equals the degree of the (6, 10) locus computed directly
      (`sixpoint_modp.out`).
    - **Over ℚ** (`sixpoint_exact.m2`, exact). msolve's rational univariate representation of
      each locus has an eliminant with **no linear factor over ℚ**. The Galois orbits have sizes 4
      to 36, and for nine vectors no position is even real (`sixpoint_rational.out`).

    So **over ℚ no line through P₀ has 6 points**.
  - **Seven points.** Then the line contains a double point (Lemma A2).
  - **Conclusion** [17 lines, ℚ, proved]. With `TC_FILTER.md` (P₀ is on no 4- or 5-point line),
    every line of A₂ through P₀ has exactly 7 points, one of them double. Possibly no line of A₂
    passes through P₀ at all, as in R₁₇ᵃ and R₁₇ᵇ.

**Step 3 — one curve glues the line maps** [proved].
- On every line, J′ ∩ H is the dynamical residue of Φ_H (Theorem C).
- [17 lines: on a 4-point line J′ passes through the four repelling fixed points of the
  critically fixed map. Four small lines determine J′. Its line components are the rich lines,
  at most four (`TC_CONTRADICTION.md`).]

**Step 4 — where the free mate can be** [proved].
- **Type I** (different components): every line separates the two components (`TC_RIGIDITY.md`
  Lemma 1(b)). On a 4-point line the non-free component sits at one harmonic value, and the free
  one avoids every jump value.
- **Type II** (same component): A₂ is a simultaneous tangency (Theorem E). Either the realisation
  space is singular at A₂, or on every 4-point line the cross-ratio map has a rational critical
  point at A₂ with harmonic critical value.

**Step 5 — why this is too restrictive** [heuristic, not a proof].
- **The two worlds.** Steps 1–3 make a rational non-free member a very rigid object. On its small
  lines it is a symmetric, critically fixed configuration, and one curve of degree 3r − n
  interpolates the residues of all n line maps. Every non-free window arrangement found so far
  is of this kind and is rigid: R₁₇ᵃ and R₁₇ᵇ over ℚ, E₁₇ and the A(G₂₆) deletions over ℚ(√−3).
  Each realisation space is a single Galois orbit, and TC holds for its lattice by Galois
  invariance.
- **The free side.** The free window arrangements known so far are rigid incidence-theorem
  configurations, or belong to one of two flexible families whose jump functions have only
  boundary zeros. At
  17 lines no free window arrangement is known at all, and over F₁₁ and F₁₃ none exists with a
  4- or 5-point line (`TC_BUILD.md` §5).
- **What a counterexample would need.** One lattice realised in both worlds:
  - type I: a second, unrelated ℚ-component on which every small line is critically fixed;
  - type II: a free family that becomes stationary on every 4-point line at exactly the harmonic
    value.
- **Why this is not a proof.** Yoshinaga's criterion makes all these line conditions consequences
  of a single one. So the restrictiveness cannot be counted as many independent conditions, and
  nothing above rules out either world-crossing for a lattice without small lines. The steps
  narrow where a counterexample can live; they do not empty it.

## 6. What would finish it

(M1) and (M2) are TC(ℚ) itself, split into its two types and restated with the structure of
§1–§4 available as hypotheses. §7 proves (M1) for every lattice with a four-point line. (M3) is a self-contained statement in arithmetic dynamics. On its
own, (M3) confines a rational counterexample, for every n, to harmonic positions on every 4-point
line. Together the three give TC(ℚ).

- **(M1) No interior tangency.** On a component of a realisation space containing a free point,
  the realisation space is smooth along the non-free locus, and some line's jump divisor pulls
  back reduced. By Theorem E this forces the component to be entirely free. This is TC on the
  component in geometric form; it holds in every family computed so far (`TC_RIGIDITY.md` §3).
- **(M2) Symmetric non-free components are isolated.** Suppose a rational realisation is at a
  harmonic, critically fixed position on every 4-point line and at a rational jump point on every
  5-point line. Then its lattice has no other ℚ-component. This is type I with Steps 2–3 as
  hypotheses. It holds for every rational non-free window arrangement known.
- **(M3) Rational critically fixed maps are harmonic.** Let Φ ∈ ℚ(z) be critically fixed, with
  ≤ 4 critical points, and suppose the 4 marked points (the critical points plus, if needed,
  chosen non-critical fixed points) are rational. Then their cross-ratio is harmonic.
  - It is proved here for the family (D, D, 1, 1), via z^D, and checked for all 1,005 vectors with
    K ≤ 30.
  - It is a statement about fields of moduli of planar-graph maps, like Belyi's dessins.
  - It is the most accessible of the three, and p-adic dynamics is the natural tool. Benedetto,
    Ingram, Jones and Levy bound the height of postcritically finite maps over number fields of
    bounded degree, through the p-adic fact that a sufficiently attracting cycle attracts a
    critical point.
  - At a prime p where Φ has good reduction, a superattracting fixed point P̄ of the reduction
    has Φ̄(z) − z vanishing simply. So no other fixed point shares its residue disc.
  - Hence, *if* Φ has potentially good reduction at every p > D, the cross-ratio λ of four marked
    points of which at least three are critical satisfies: λ and 1 − λ are S-units,
    S = {p ≤ D}. This is a finite list, but it contains non-harmonic values such as λ = 3.
  - So this route bounds the problem; it does not close it.

**Concrete next computations.** Each is a computation on one projective line, not a 17-line
enumeration:
- the (6, 10) curves of the 7-point lines through P₀: their genus and rational points. Each such
  curve is a one-parameter family of degree-6 maps with one free critical point;
- the charge-graph count for K > 20, with a smarter enumeration;
- whether the free critical points of the 7- and 8-point lines of a rational A₂ always lie on the
  non-linear part of J′, as in R₁₇ᵃ and R₁₇ᵇ.

## 7. (M1) holds for every lattice with a four-point line (Theorem F)

This section proves (M1), with no extra hypothesis, for every lattice that has a line with exactly
four points, for any number of lines n (over ℂ, using the simple-root data for n ≤ 31).

**Setting.** A *type-II germ* is a family A_t over R = ℂ{t} such that:
- the lattice L is the same for all t;
- A_t is free with exponents (d, d) for t ≠ 0, and A₀ is not free.

Let θ₁, θ₂ be an R-basis of D₀(A_R)_d. Write c(t) for the Saito determinant, so that
det(E, θ₁, θ₂) = c(t)·Q_t. By `TC_RIGIDITY.md` Lemma 3, θᵢ(0) = fᵢ·η with η ∈ D₀(A₀) of least
degree r, and ord_t c ≥ 2.

**Lemma F1 (the frame collapses at the Bourbaki point).** Suppose r = d − 1, so A₀ has one
Bourbaki point P₀ and f₁, f₂ are independent linear forms. Then V(f₁, f₂) = {P₀}.

*Proof.*
1. For (a, b) ≠ (0, 0), consider s = aθ₁ + bθ₂ as a section of the rank-2 bundle E_R(d) on the
   regular threefold P² × Δ.
2. For t ≠ 0, E_t(d) ≅ O² and s(t) is a nonzero constant section, so it has no zero. Hence
   Z(s) ⊂ P² × {0}.
3. At t = 0, s(0) = (af₁ + bf₂)·η. Since η vanishes, as a section of E₀(d − 1), exactly at P₀,
   this gives Z(s) = {af₁ + bf₂ = 0} ∪ {P₀} as a set.
4. Z(s) is cut out locally by two equations in a regular scheme of dimension 3. By Krull's height
   theorem every component of Z(s) has dimension ≥ 1, so P₀ is not an isolated point of Z(s).
   Therefore P₀ lies on the line af₁ + bf₂ = 0, for every (a, b). ∎

**Corollary F2 (Lemma 3(c) and Theorem E for every line).** Let H be a line with jump j_H = 1 at
A₀; such a line misses P₀. Then ord_t Θ_H(γ(t)) = ord_t c(t) ≥ 2.

*Proof.*
1. *The restricted frame is a basis.* Restricting θ₁, θ₂ to H gives φ₁, φ₂ in the family of
   Ziegler modules. At t = 0, φᵢ(0) = fᵢ|_H·ψ, where ψ spans the degree-(d − 1) part. The forms
   f₁|_H and f₂|_H are independent because H ∌ P₀ (Lemma F1). So φ₁(0), φ₂(0) span the
   2-dimensional degree-d part, and by Nakayama (φ₁, φ₂) is an R-basis of that free module.
2. *Its cokernel.* The map O_H(−d)² → F_R given by (φ₁, φ₂) has determinant c(t)·∏ α_P^{k_P}.
   Its image at t = 0 is the summand O(−d + 1)·ψ, so the cokernel restricts to O_H(−d − 1) on
   the central fibre. A rank-one quotient with Fitting ideal (t^e) is then
   O_H(−d − 1) ⊗ R/(t^e), where e = ord c.
3. *The order of Θ_H.* ord_t Θ_H equals the length of
   coker(H⁰(O(d − 1)²) → conditions) = H¹(F_R(d − 1)) = H¹(O_H(−2) ⊗ R/(t^e)), which is e. ∎

Lines through P₀ have j_H = 2, and lines missing P₀ have j_H = 1. So with Corollary F2,
Theorem E holds as stated, for every line.

**Lemma F3 (four-point lines linearise the realisation space).** Let H have four points. Put them
at [1:0:0], [0:1:0], [1:1:0] and [λ:1:0], and write every other line as an offset in its pencil.
Then the realisations of L form an open subset (all non-incidences of L) of

  K = {(λ, v) : M(λ)·v = 0},

where M(λ) = M₀ + λM₁ is the matrix of the concurrency conditions of L (`TC_FILTER.md` Lemma F3),
modulo a 3-dimensional group acting linearly on v. Consequently:
- K has exactly one irreducible component K₀ dominating the λ-line. Every other component lies
  over one of the finitely many values where the rank of M drops (a *vertical* component).
- Near any λ₀, K₀ is the total space of a vector bundle over a disc. At λ₀ its fibre is the limit
  V₀ = lim ker M(λ), which exists because a map from a punctured disc to a Grassmannian extends.
  So K₀ is smooth and λ restricted to K₀ is a submersion.

**Theorem F.** Let L be a lattice with a line H with exactly four points and multiplicity
vector k, and suppose the jump polynomial of k has simple roots. This holds for every k with
K ≤ 30, i.e. n ≤ 31; for all K it would follow from the infinitesimal form of Thurston rigidity,
see the remark below. Then **freeness is constant on every irreducible component of the
realisation space of L.** In particular L has no type-II counterexample.

*Proof.*
- **K odd, k unbalanced, or χ not split.** Freeness is constant on the whole realisation space.
- **χ₀ = (t − d₁)(t − d₂) with d₁ = K/2 − 1.** A realisation is free iff λ ∈ J (Yoshinaga on H).
  - On K₀ the free points would form a nonempty open set (Yuzvinsky) inside the finite union of
    fibres over J, which is impossible.
  - On a vertical component λ is constant.
- **d₁ = d₂ = K/2.** A realisation is free iff λ ∉ J, so vertical components are constant and
  the generic point of K₀ is free. Suppose A₀ ∈ K₀ is not free, with λ(A₀) = λ₀ ∈ J.
  1. A 4-point line has j_H ≤ 1 by Abe's bound, so k = 1 and H misses the Bourbaki point.
     Corollary F2 gives ord Θ_H(γ(t)) ≥ 2 along every arc in K₀ from free points into A₀.
  2. K₀ is smooth at A₀ and dλ ≠ 0 there (Lemma F3). Take an arc γ in K₀ through A₀ with
     dλ(γ′(0)) ≠ 0. For t ≠ 0, γ(t) has λ ≠ λ₀ near λ₀, hence λ ∉ J, so γ(t) is free.
  3. Along γ, Θ_H(λ(γ(t))) = Θ_H′(λ₀)·(dλ(γ′(0)))·t + O(t²) has order exactly 1, since λ₀ is a
     simple root. This contradicts step 1. ∎

**Remark (simple roots for all K).** Suppose λ₀ is a double root of the jump polynomial. By
Theorem B there is then a first-order deformation (λ₀ + ε, Φ + εΦ̇) of the critically fixed map
Φ that keeps all four marked points fixed, critical with the same local degrees, while moving
their cross-ratio. The infinitesimal form of Thurston rigidity says the pull-back map on the
Teichmüller space of the postcritical set has no eigenvalue 1 at Φ (Douady–Hubbard; Epstein). That
rules out such a deformation. The data confirm simplicity for all 604 interior factors with
K ≤ 30.

**What a counterexample with a four-point line must look like.**

**Corollary F4.** If L has a four-point line (K ≤ 30), every counterexample for L is of type I:
- a non-free *vertical* component at some λ₀ ∈ J at which the rank of M drops;
- together with a free component, which is either K₀ or a vertical component at some
  λ₁ ∉ J.

Over ℚ, λ₀ is harmonic. If the free component is K₀, then:
- its limit fibre V₀ over λ₀ is entirely degenerate (Theorem F);
- at a generic point of V₀ the degeneration creates exactly one new triple point (β = 1, by
  `TC_RIGIDITY.md` Lemma 2, since Θ_H vanishes there to order 1);
- the limit arrangements are free with exponents (d − 1, d + 1), by Yoshinaga on H.

*Where harmonic rank drops come from.* Take two lines of the A-pencil and two of the B-pencil,
forming a quadrangle, and ask that its two diagonals lie in the C- and D-pencils. The conditions
read c₂ − c₁ = a₂ − a₁ and c₂ − c₁ = −λ(a₂ − a₁), so (1 + λ)(a₂ − a₁) = 0. This is the
complete-quadrangle theorem: the configuration exists non-degenerately only at λ = −1.
- When the lattice *forces* the harmonic position in this way, every realisation has λ = −1, and
  TC holds for L trivially.
- So a counterexample needs an *unforced* harmonic rank drop: the concurrency matrix gains rank at
  −1 without forcing λ = −1 on every realisation.

That is a finite linear-algebra condition on the lattice. The realisations at λ = −1 are the
arrangements whose lines lie in four directions: rows, columns, diagonals and anti-diagonals.

**Test** (`work/global/thmF_test.py`, `thmF_example.m2`). The test builds random families in which
the lines of three pencils sit at integer offsets, and each line of the fourth pencil passes
through one chosen point. Such a family lies in the dominating component, so Theorem F applies.
- **Vector (1, 2, 2, 3), jump at μ₀ = 2, 9 lines.** There are 24 distinct lattices with
  χ₀ = (t − 4)². In all 24 the lattice changes at μ₀, always with β = 1 (one new triple point),
  as Corollary F4 predicts.
- **One example checked in Macaulay2.** The generic member has Jacobian syzygies (4, 4), so it is
  free. The member at μ₀ has syzygies (3, 5): free with exponents (d − 1, d + 1).
- **Other vectors.** The naive construction produced no balanced lattice for the other five
  vectors tried. For n ≤ 14 the test cannot fail without contradicting Barakat–Kühne; what it does
  check is the code and the β = 1 prediction.

## 8. (M1) in general: where a non-free point can hide (Theorem G)

Every line H gives the same linear structure as Lemma F3, now over the (s − 3)-dimensional
configuration space M_{0,s}(H). The realisations of L form an open subset of
K_H = {(λ, v) : M_H(λ)·v = 0}, λ ∈ M_{0,s}(H). A component C lies over Z = closure of π_H(C), and
over a dense open subset of Z it is a vector bundle with linear fibres.

**Theorem G.** Let d₁ = d₂, let C be an irreducible component containing free points, and let
E ⊄ Sing C be an irreducible component of the non-free locus of C. Then E is a divisor of C, and
for every line H:
- (a) Θ_H ∘ π_H vanishes to order ≥ 2 along E;
- (b) at a generic point x ∈ E, at least one of the following holds:
  - π_H|_C is not a submersion onto Z at x;
  - Z is singular at π_H(x);
  - Z is tangent there to the jump hypersurface J_H, i.e. d(Θ_H|_Z) = 0, which includes the case
    where J_H is singular.

*Proof.* The non-free locus is the zero set of the single function Θ_H ∘ π_H, so it is a divisor.
(a) is Theorem E at the generic point of E. For (b), suppose π_H|_C is a submersion onto a smooth
Z at x. Then Θ_H ∘ π_H ∈ m_x² gives d(Θ_H|_Z)(π_H(x)) = 0. ∎

**Consequences.**
- **Four-point lines.** None of the three alternatives can occur on K₀: it is a vector bundle over
  a curve, and the roots are simple. This is Theorem F.
- **Five-point lines whose five points move freely** (Z = M_{0,5}(H)).
  - J_H is reduced: it is irreducible over ℚ (`TC_RATIONAL.md` §4).
  - So E lies over finitely many points: Sing(J_H), and the points where C is not a vector bundle.
  - Since E is a divisor and the generic fibre has codimension 2, E is a whole fibre π_H⁻¹(z₁)
    that has jumped in dimension.
  - If z₁ is a smooth point of J_H and π_H contracts E simply (π_H*m_{z₁} = I_E, as in a
    blow-up), then (a) fails. So π_H contracts E with multiplicity ≥ 2, or C is singular along E.
- **Five-point lines whose points move on a curve Z.** Then E is the fibre over a single point z₁
  of Z where Z is tangent to J_H, or Z or J_H is singular. Over ℚ, z₁ is one of the finitely many
  rational points of J_H (`TC_RATIONAL.md` §4).
- **In all cases.** Along a non-free divisor E of a free family, the positions on every line with
  at most five points are frozen: E lies over one point of each such line's configuration space,
  and that point is special for the line.

So (M1) fails, if at all, only through one of three special geometric events:
- singular components;
- fibres that jump in dimension;
- tangency between the image of the family and a jump hypersurface.

On four-point lines all three are impossible.

## 9. (M2): what is left

**Status: not proved.** Every argument above concerns one irreducible component. A type-I
counterexample places the free and the non-free realisations on different components, and nothing
in §1–§8 compares two components.

What is known about the non-free component C₂:
- Over ℚ, every rational point of C₂ sits at rational special positions on its small lines. If
  the rational points of C₂ are Zariski-dense, which is automatic when C₂ is a linear space, each
  small line is frozen at one point of the finite set J_H(ℚ).
- If L has a four-point line, C₂ is vertical: a linear space ker M(λ₀) ∩ U at an unforced
  harmonic λ₀ (Corollary F4).

Attempts that did not close it:
- **Deletion.** Deleting a line gives two non-free 16-line arrangements, about which TC says
  nothing.
- **The boundary point between the components.** Suppose the free component is K₀. The two
  components then meet, inside the closure, along V₀, where the arrangements are free with
  exponents (d − 1, d + 1) and lattice L′ = L + T.
  - T can be broken in two ways: horizontally (λ moves), which gives free arrangements, or
    vertically (λ fixed), which gives non-free ones. Both are consistent.
  - At 17 lines this does give a constraint. Imposing T on the generic free family must force
    further incidences. Otherwise L′ would be a TC counterexample in class (7, 9), which
    `TC_FOLIATION.md` Theorem 5.1 excludes.
- **Characteristic 3.** −1 ≡ 2 makes the four points of H all of P¹(F₃). But the one-line
  Frobenius criterion needs Ziegler multiplicities ≤ 3, and the window has 5.

**What would finish the 17-line case over ℚ.**
- After Theorem F, the open part of sub-case (I) of `TC_FILTER.md` is a *linear* problem over ℚ.
  It asks for the four-direction arrangements (rows, columns, diagonals, anti-diagonals) with
  vectors (5,5,5,1), (5,5,3,3), (5,4,4,3) at their harmonic values that are non-degenerate, and
  for each, whether its lattice has another component.
- That is a targeted 17-line enumeration. I have not run it, because 17-line runs need your
  explicit go-ahead.

## 11. (M1) for lines with five to eight points; the free member (added 20 Oct 2026)

This section records what the methods of §7–§8 give for the lines of a 17-line window lattice
that carry five or more multiple points, and two structural facts about the free member. Nothing
here closes n = 17; §11.5 says what is left.

### 11.1 The linear structure over any line, and the dominating component

Fix a lattice L of the window (d₁ = d₂ = 8) and a line H of L with s = s_H points and
multiplicity vector μ. Put three of the points at ∞, 0, 1 and the others at
λ = (λ₁, …, λ_{s−3}) ∈ M_{0,s}(H). Every other line of L lies in the pencil through one of the
s points, so a realisation is a pair (λ, v) with v the vector of pencil offsets, and every
concurrency of L is a linear equation in v whose coefficients are polynomials in λ
(`TC_FILTER.md` Lemma F3 and §8 above). Write M(λ) for the matrix of these equations,
K = {(λ, v) : M(λ)v = 0}, U ⊂ M_{0,s} the open set where rank M(λ) is maximal, and K₀ for the
closure of the kernel bundle over U. The realisation space R(L) is an open subset of K (the
non-incidences of L). Every irreducible component of R(L) either dominates M_{0,s}(H), in which
case it is R(L) ∩ K₀ (the *dominating component* C_H), or lies over a proper closed subset
Z_H ⊂ M_{0,s} (a *vertical* component).

**Lemma 11.1.** Let Bad_H ⊂ M_{0,s} be the indeterminacy locus of the rational map
λ ↦ ker M(λ) to the Grassmannian. Then Bad_H has codimension ≥ 2, K₀ is a vector bundle over
M_{0,s} ∖ Bad_H, and π_H : K₀ → M_{0,s} is a submersion there. For s = 4, Bad_H = ∅.

*Proof.* M_{0,s} is smooth, and a rational map from a normal variety to a projective variety
is defined outside a closed subset of codimension ≥ 2; over the locus where it is defined, K₀
is the pull-back of the tautological bundle. For s = 4 the base is a curve and the map extends
everywhere (Lemma F3). ∎

### 11.2 The jump hypersurfaces are reduced (computation)

Let Θ_μ be the determinant of the 16 × 16 matrix of the degree-7 Ziegler conditions, a
polynomial on M_{0,s}, and J_μ = {Θ_μ = 0} the locus where the exponents of the
multirestriction drop below (8, 8). Up to the degenerate factors λ_i ∈ {0, 1}, λ_i = λ_j (which
lie outside M_{0,s}), Θ_μ is **squarefree** for every multiplicity vector of the window:

| s | vectors | check | file |
|---|---|---|---|
| 4 | 5 | exact factorisation over ℚ: all roots simple | `work/as17/jump4.out`, `jump4.out` here |
| 5 | 11 | exact factorisation over ℚ: one non-degenerate irreducible factor, multiplicity 1 (degree 8–11) | `work/global/sqf5.m2`, `sqf5.out` |
| 6 | 16 | restriction to three random lines of M_{0,6} over F₃₂₀₀₃: squarefree, same degree on all three lines | `work/global/sqf678.m2`, `sqf678.out` |
| 7 | 17 | same, lines in M_{0,7} | same |
| 8 | 15 | same, lines in M_{0,8}; for (2,…,2) the non-degenerate part is constant (no jump) | same |

The restriction test is a proof: if Θ = G²·R with G non-constant, then on a line on which the
degree of Θ is attained, G restricts to a non-constant polynomial and the restriction has a square
factor. Two further remarks. For (3,2,2,2,2,2,2,1) the non-degenerate part has degree 1, so the
jump locus of such an 8-point line is a hyperplane of M_{0,8}. And at a point of J_μ where the
Ziegler kernel has dimension ≥ 2 (the (6,10)-locus, the lines through the Bourbaki point) all
first minors vanish, so Θ_μ ∈ m² there: **these points lie in Sing(J_μ)**.

### 11.3 (M1) on the dominating component of any line

**Theorem F′.** Let L be a lattice of the window, H a line of L with s_H ≥ 4 points, and C_H
the component of R(L) dominating M_{0,s_H}(H). If C_H contains a free point, then every
non-free point A₀ of C_H satisfies

  π_H(A₀) ∈ Sing(J_{μ_H}) ∪ Bad_H,

a closed subset of M_{0,s_H} of codimension ≥ 2. For s_H = 4 this set is empty (Theorem F); for
s_H = 5 it is finite: Sing(J_μ) has total Tjurina number between 12 and 34 (`work/rational/sing5.out`),
and Bad_H is finite.

*Proof.* Let λ₀ = π_H(A₀) and suppose λ₀ ∉ Sing(J_μ) ∪ Bad_H. By Lemma 11.1, C_H is smooth at
A₀ and π_H is a submersion there. Since λ₀ ∉ Sing(J_μ) and J_μ is reduced (§11.2), J_μ is
smooth at λ₀ and Θ_μ vanishes to order exactly one along it; the pull-back of a reduced smooth
hypersurface by a submersion is reduced, so Θ_H ∘ π_H = Θ_μ ∘ π_H vanishes to order exactly one
at A₀ on C_H, i.e. it is not in m²_{A₀}. This contradicts Theorem E (C_H contains free points,
A₀ is non-free, C_H is smooth at A₀). The case s_H = 4 is Theorem F; for s_H = 5, Sing(J_μ) is a
finite set because J_μ is an irreducible reduced curve, and Bad_H is finite by Lemma 11.1. ∎

Lines through the Bourbaki point P₀ of A₀ need no separate treatment: for them λ₀ lies in the
(6,10)-locus, hence in Sing(J_μ) by §11.2, and the theorem says nothing for them — as it must,
since Theorem E only gives ord ≥ 2 there.

**Theorem G′ (vertical components).** Let C be a component of R(L) lying over a proper closed
irreducible Z_H ⊂ M_{0,s_H}(H), with C → Z_H generically a vector bundle (this holds on a dense
open subset of Z_H). If C contains a free point and N ⊂ C is a component of its non-free locus
not contained in Sing C and not over the locus where the bundle structure fails, then along π_H(N)
the restriction Θ_μ|_{Z_H} vanishes to order ≥ 2: either π_H(N) ⊂ Sing(J_μ), or Z_H is tangent to
J_μ along π_H(N) (contact of order ≥ 2 along the whole subvariety).

*Proof.* As for Theorem F′, with the submersion C → Z_H in place of π_H. ∎

**What this says about a type-II counterexample** (a non-free point A₀ of a component C that
contains free points). For every one of the 17 lines H of L, simultaneously: if C dominates
M_{0,s_H}(H), then the positions of the points of H at A₀ form a singular point of the jump
hypersurface of H or an indeterminacy point of the kernel map of L for H; if not, the image of C
in M_{0,s_H}(H) is tangent to the jump hypersurface of H along the image of the non-free locus,
or lies in its singular locus. For a 4-point line the first alternative is impossible and the
second means a constant cross-ratio, so a lattice with a 4-point line has no type-II
counterexample at all (Theorem F); for a 5-point line the first alternative confines the
non-free point to finitely many positions of the five points, at each of which the realisation
space is linear and can be enumerated exactly as in `work/as17/pencil4_exact.py`.

### 11.4 Two facts about the free member

Throughout, A₁ is free with exponents (1, 8, 8), all multiplicities ≤ 6 and 4 ≤ s_H ≤ 8.

**Lemma 11.4 (external lines).** Every line L of the plane not in A₁ meets A₁ in at least nine
distinct points [Abe 2014, Cor. 1.2(2), applied to the deconing]. If some external line meets A₁ in
exactly nine points, then A₁ ∪ L is free with exponents (1, 8, 9) and L is a divisional line of it
[Terao's addition theorem: |(A₁ ∪ L)^L| = 9 = d₂ + 1]. Hence **either** every external line meets
A₁ in at least ten points — then any two multiple points P, Q of L not joined by a line of L
satisfy (m_P − 1) + (m_Q − 1) ≤ 7, which excludes unjoined pairs of multiplicities (6,4), (5,5)
as well as (6,6), (6,5) — **or** A₁ is the deletion of a free arrangement of eighteen lines with
exponents (1, 8, 9) along one of its 9-point lines.

**Lemma 11.5 (8-point lines).** A₁ has a line H with eight points if and only if N := A₁ ∖ H is
nearly free with exponents (8, 8); then the logarithmic bundle E_N = D₀(N)~ is isomorphic to
Ω¹_{P²}(−6) ≅ T_{P²}(−9), and in suitable coordinates D₀(N) is generated by

  θ₁ = yP + zQ,  θ₂ = −xP + zR,  θ₃ = −xQ − yR,

for three derivations P, Q, R of degree 7, with the single relation xθ₁ + yθ₂ + zθ₃ = 0.
For w ∈ ℂ³ put θ_w = w₁θ₁ + w₂θ₂ + w₃θ₃ = m₁P + m₂Q + m₃R, where m₁, m₂, m₃ are the three linear
forms vanishing at the point [w]. Then:
1. θ_w, as a section of E_N(8) ≅ T(−1), vanishes exactly at [w];
2. det(E, θ_w, θ_{w′}) = c·Q_N·ℓ_{ww′}, with ℓ_{ww′} the line through [w] and [w′];
3. for every line L of the plane, the foliations of the θ_w with w ∈ L̂ are pairwise tangent
   along L, and N ∪ L is free (with basis {θ_w : w ∈ L̂}) if and only if the common direction
   along L is L itself, if and only if |N ∩ L| = 8;
4. in particular D₀(A₁)_8 = {θ_w : w ∈ Ĥ}, and the extra fixed point of the line map of θ_w on
   the 8-point line H (the ninth fixed point of a degree-8 map, besides the eight points of A₁)
   is [w].

*Proof.* The deletion of a line with s_H = 8 from a free (8, 8) arrangement is plus-one generated
with exponents (8, 8) and level 16 − 8 = 8, i.e. nearly free (Abe's deletion theorem for
plus-one generated arrangements; `TC_BUILD.md` Lemma 1.3); conversely a line meeting a nearly
free (8, 8) arrangement of 16 lines in eight points gives b₂ = 72 + 8 = 80 and exponents (8, 8) on
L, so freeness by Yoshinaga (Lemma 2.3 of `paper/short`). For a nearly free N the resolution is
0 → S(−9) → S(−8)³ → D₀(N) → 0 with the relation aθ₁ + bθ₂ + cθ₃ = 0, a, b, c linear forms; if
they were dependent, eliminating one generator would exhibit a derivation of degree 7 in D₀(N),
against mdr(N) = 8. So (a, b, c) is a coordinate system, the relation is the Euler relation, the
sheaf is the cokernel of the Euler map O(−9) → O(−8)³, which is T(−9), and T ≅ Ω¹(3) in rank
two. The syzygies of (x, y, z) are generated by the Koszul relations, which gives the shape of
θ₁, θ₂, θ₃ and of θ_w. (1) The sections of T(−1) are the constant fields v mod x, vanishing
exactly at [v]. (2) The determinant has degree 17 = deg Q_N + 1 and vanishes on N and, by (1), at
[w] and [w′]. (3) On L, det(E, θ_w, θ_{w′}) = 0 says the two fields are dependent modulo E, i.e.
the foliations are tangent; N ∪ L is free iff the θ_w are tangent to L (Saito's criterion with
(2)), and Yoshinaga's criterion on L (b₂(N ∪ L) = 72 + |N ∩ L|) says this happens iff
|N ∩ L| = 8. (4) The singular points of the foliation of θ_w on the invariant line H are its
nine fixed points; eight are the points of A₁ on H, and [w] ∈ H is a zero of θ_w. ∎

So in sub-case (III) the free member is "a nearly free (8, 8) sixteen-line arrangement N plus
an 8-secant of N", and the pencil D₀(A₁)_8 is the line Ĥ inside the three-dimensional
D₀(N)_8 ≅ ℂ³ whose points are the zeros of the corresponding derivations. Lines of the plane
meeting N in eight points are therefore exactly the lines along which the common tangency of the
pencil is the line itself.

### 11.5 Status after this section

- (M1) holds on the dominating component of every line of every window lattice outside a
  codimension-two set of positions, and for 4-point lines without exception.
- Not proved: (M2) (two components with different freeness), the fibre jumps over Bad_H, and
  the tangency case of Theorem G′ for non-dominating components; and nothing here constrains
  the free member at the level of its lattice beyond Lemma 11.4.
- A computation that would finish sub-case (II) by these means: for each 5-point vector, the
  finitely many singular points of its jump curve, each a linear enumeration as in
  `pencil4_exact.py`, treat the "dominating" type-II case; the vertical and fibre-jump cases
  still need the abstract 5-partite enumeration.
- 21 Oct 2026: n = 17 was closed by another route (Riemann–Roch obstruction, covering lemma and
  the exhaustive core computation of `TC_N17.md`, computer-assisted). (M2) in general is still
  not proved.

## 10. Files (`work/global/`)

(`sqf5.m2`, `sqf5.out`, `sqf678.m2`, `sqf678.out`: the squarefreeness checks of §11.2.)

- `charge_graphs.py`: planar-graph count of critically fixed maps against the jump polynomials;
  output `charge_K20.out` (136 vectors, 0 mismatches).
- `harmonic_maps.m2`: the maps behind the rational jump points at K = 16.
- `linemaps.m2`: the line maps Φ_H of R₁₇ᵃ and R₁₇ᵇ, with local degrees and free critical points.
- `jprime_lines.m2`: Theorem C on R₁₇ᵃ, R₁₇ᵇ and B₃.
- `thmF_test.py`, `thmF_example.py`, `thmF_example.m2`: the consistency test of Theorem F.
- `charge_general.py` (`charge_six.out`): the planar-graph count for the 6-point lines.
- `sixpoint_count.m2`, `sixpoint_modp.m2` (`sixpoint_modp.out`): direct degree of the (6, 10)
  loci over ZZ/32003.
- `sixpoint_rational.m2` (`sixpoint_rational.out`): real positions via msolve.
- `sixpoint_exact.m2` (`sixpoint_exact.out`): exact rational test, using the eliminant of the
  rational univariate representation, factored over ℚ.

## References

- J. Cordwell, S. Gilbertson, N. Nuechterlein, K. Pilgrim, S. Pinella, *On the classification of
  critically fixed rational maps*, Conform. Geom. Dyn. 19 (2015).
- M. Hlushchanka, *Tischler graphs of critically fixed rational maps and their applications*,
  arXiv:1904.04759.
- K. Pilgrim, Tan Lei, *Combining rational maps and controlling obstructions*, Ergodic Theory
  Dynam. Systems 18 (1998) (blowing up arcs).
- A. Douady, J. H. Hubbard, *A proof of Thurston's topological characterization of rational
  functions*, Acta Math. 171 (1993) (rigidity).
- A. Epstein, *Transversality in holomorphic dynamics* (preprint).
- R. Benedetto, P. Ingram, R. Jones, A. Levy, *Attracting cycles in p-adic dynamics and height
  bounds for postcritically finite maps*, Duke Math. J. 163 (2014).
- M. Barakat, L. Kühne, P. Pokora, arXiv:2407.07070 (Ziegler pairs from singular realisation spaces).
- The sources of `TC_RATIONAL.md`, `TC_FOLIATION.md` and `TC_RIGIDITY.md`.
