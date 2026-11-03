# Terao's conjecture: what a counterexample must satisfy, and what can be proved

**Bottom line.** I could not prove Terao's conjecture (TC) in P² or P³. It remains open, and
nothing here closes it. What I can do:

1. Pin down what a P² counterexample would have to look like. Most conditions are in the
   literature; one refinement (Theorem 1(7)) and one principle (Theorem 1(8)) I prove here (§1).
2. Prove TC exactly, on the full complex realisation space, for the most dangerous lattices my
   searches found:
   - a free, non-divisionally-free 15-line lattice with moduli, beyond the 14-line range where
     TC is verified (§2);
   - a free, non-DF 26-plane arrangement in P³ (§5).
3. Prove TC for all arrangements of 15 and of 16 lines in P²_ℂ, two beyond the published range,
   by an exhaustive enumeration of the candidate lattices and exact realisation-space computations
   (§10). The 15-line analysis of §3 is superseded by this.
4. Prove TC over finite fields in two cases (§4):
   - all line arrangements over F_q with q ≤ 7 (a direct combination of known theorems);
   - "covering" lattices in every rank (rank ≥ 4 is new).
5. Reduce P³ to P² plus one statement about multirestrictions (§5).
6. Say exactly where every argument stops (§6).

Notation (P²). L is a rank-3 lattice with n lines. A₁ is a free realisation with exponents
(1, d₁, d₂), d₁ ≤ d₂, δ = d₂ − d₁. A₂ is a non-free realisation of the same L. Both are over ℂ
(any field of characteristic 0). For a line H, s_H = |A^H| is the number of multiple points on H,
and m is the largest point multiplicity.

## 1. Anatomy of a counterexample in P²

**Theorem 1.** If (A₁, A₂) is a counterexample, then:

1. n ≥ 15. [Barakat–Kühne 2023: TC holds for ≤ 14 lines, any characteristic.]
2. L is not divisionally free: s_H ∉ {d₁ + 1, d₂ + 1} for every H. [Abe 2016: DF lattices
   satisfy TC; in rank 3, DF ⟺ some s_H − 1 is a root of χ.]
3. s_H ≤ d₁ for every line H. [Abe 2014, Cor. 1.2: a free line arrangement has s_H ≤ d₁ + 1
   or s_H = d₂ + 1; then apply (2).]
4. No point has multiplicity > (n + 1)/2, and s_H ≥ δ + 4 for every line H. [Abe 2012:
   Prop. 4.2 handles an unbalanced Ziegler restriction, i.e. such a heavy point; for balanced
   restrictions, Thm. 0.1 gives |e₁ − e₂| ≤ s − 2 and Cor. 0.4 the bound on s_H.]
5. Hence δ + 4 ≤ d₁, i.e. d₂ ≤ 2d₁ − 4, and d₁ ≥ 6. [Abe 2014, Cor. 5.4 and 5.5.]
6. m ≤ d₁ − 1. If d₁ = m + 1, then A₂ is plus-one generated with exponents
   (m, n − m, 2n − 3m − 3). [Dimca–Kühne–Pokora 2025: TC holds when d₁ ∈ {m − 1, m} or
   d₁ = n − m; their Thm. 2.10 gives the d₁ = m + 1 case.]
7. **(refinement)** A₂ has a logarithmic derivation of degree r = mdr(A₂) with m ≤ r ≤ d₁ − 1.
   Every line satisfies
     n + 1 − 2r ≤ s_H ≤ r + 1,
   and every Ziegler restriction of A₂ has exponents (e₁, e₂) with s_H − 1 ≤ e₁ ≤ r < d₁.
8. **(rigidity principle)** Suppose that for some line H, the points of A^H with their
   multiplicities are the same up to PGL(2) and field automorphisms for all realisations of L —
   for example s_H ≤ 3, or the moduli of L do not move the points of H. Then TC holds for L. So in
   a counterexample the moduli must move the points on *every* line.

*Proof of (7).* Write mdr for the least degree of a derivation that is not a multiple of E.
1. *m ≤ r ≤ d₁ − 1.* This is in Dimca–Kühne–Pokora. It comes from the du Plessis–Wall bounds:
   τ(A) = Σ_P (m_P − 1)² is combinatorial, and among arrangements with this τ the free ones are
   exactly those with mdr = d₁, while a non-free one must have mdr < d₁.
2. *e₁ ≤ r.* Fix H. Write D₀^H(A₂) for the derivations with θ(α_H) = 0; it complements S·E, so
   its least degree is r. An element of degree r restricts to a nonzero element of the Ziegler
   multirestriction (A₂^H, μ), where μ_P = m_P − 1. Indeed, the kernel of restriction is
   α_H·D₀^H(A₂), which lives in degrees ≥ r + 1. So e₁ ≤ r.
3. *s_H ≤ e₁ + 1.* For any 2-multiarrangement with s points and multiplicities μ, either
   s ≤ e₁ + 1 or s = e₂ + 1:
   - if the lowest basis element θ₁ is not a multiple of E_H, then det(θ₁, E_H) is a nonzero form
     of degree e₁ + 1 vanishing at all s points;
   - otherwise θ₁ = gE_H with α_P^{μ_P − 1} | g. Then e₁ − 1 ≥ Σ_P (μ_P − 1) = (n − 1) − s, so
     e₂ ≤ s − 1, while θ₂ (not a multiple of E_H) gives s ≤ e₂ + 1.
   The case s_H = e₂ + 1 > d₁ contradicts (3). So s_H ≤ e₁ + 1 ≤ r + 1.
4. *s_H ≥ n + 1 − 2r.* Abe's bound e₂ − e₁ ≤ s_H − 2 gives s_H ≥ n + 1 − 2e₁ ≥ n + 1 − 2r. ∎

*Proof of (8).*
- Yoshinaga's criterion: A is free iff the Ziegler multirestriction onto H has exponents
  (d₁, d₂).
- If the multirestrictions of A₁ and σ(A₂) are isomorphic, where σ is a field automorphism, they
  have the same exponents, so σ(A₂) is free. Freeness is Galois-invariant, so A₂ is free.
- This is Abe–Yoshinaga, Cor. 5.3, in rank 3. ∎

**Addendum (8 Oct 2026, `TC_FOLIATION.md` Theorem 5.1).** The foliation of P² defined by the
minimal derivation of A₂ has all n lines invariant and its inflection curve (degree 3r) is
divisible by Q; comparing its zeros with the lattice gives 3r ≥ n + 2. With (7) this sharpens (5)
to **d₂ ≤ 2d₁ − 6, d₁ ≥ 7, n ≥ 15**, and sharpens the lower bound in (7) to r ≥ (n + 2)/3; its
Theorem 10.1 then excludes 3r = n + 2 as well, giving **d₂ ≤ 2d₁ − 7 and r ≥ (n + 3)/3**. In
particular the classes (6, 7), (6, 8), (7, 8), (7, 9), (7, 10), (8, 10), (8, 11), (8, 12), … contain
no counterexample for purely theoretical reasons (so TC for 16 lines no longer needs Theorem
10.4), and for n = 17 only (8, 8) with r = 7 is left.

**The smallest admissible exponents** (from (1), (4), (5)):

| n | possible (d₁, d₂) | allowed s_H |
|---|---|---|
| 15 | (6, 8), (7, 7) | {6} and [4, 7] |
| 16 | (7, 8) | [5, 7] |
| 17 | (7, 9), (8, 8) | [6, 7] and [4, 8] |
| 18 | (7, 10), (8, 9) | {7} and [5, 8] |
| 19 | (8, 10), (9, 9) | [6, 8] and [4, 9] |
| 20 | (8, 11), (9, 10) | [7, 8] and [5, 9] |

## 2. Exact proofs of TC for the dangerous lattices

**Method** (as in Barakat–Kühne):
1. Write the complete realisation space over ℚ̄ as an ideal: fix a projective frame, impose the
   incidences, saturate away every degeneration (extra collinearity or concurrency), and decompose
   over ℚ.
2. On each component, decide freeness exactly. By Theorem 1(7), a realisation of L is free iff it
   has no derivation of degree d₁ − 1 apart from multiples of E. This is a full-rank condition on
   a matrix M over the coordinate ring.
3. The non-free locus is the support of coker(Mᵀ). Compare it with the degeneration locus.

Scripts: `work/tc15_exact.m2`; the general checker is `work/exact_tc_points.py`.

**Theorem 2 (new).** TC holds for the 15-line lattice L₁₅: free with exponents (1, 7, 7), not DF,
with 6 quintuple, 6 triple and 27 double points. This is the "database lattice" of Findings 9 and
15 in `NOTES.md`.

*Proof.*
1. Up to PGL(3) the realisations are the 15 lines joining Q₁, …, Q₆ with Q₁…Q₄ the standard
   frame, Q₅ = (d² : d : 2d − 1) and Q₆ = (d(2d − 1) : d² : 2d − 1). Here d ranges over ℂ minus the
   roots of
     B(d) = d²³ (d − 1)²³ (2d − 1)⁷ (d² − 3d + 1)⁴ (d² + d − 1)⁴,
   which are exactly the parameters where the lattice degenerates. The realisation ideal has one
   non-degenerate component; it is a rational curve.
2. With θ(z) = 0, the degree-6 derivations form the kernel of a 98 × 56 matrix over ℚ[d] of
   generic rank 56, so the generic member is free.
3. The annihilator of coker(Mᵀ) is generated by
     d⁷ (d − 1)⁷ (2d − 1)³ (d² − 3d + 1)(d² + d − 1).
4. Every root of it is a root of B. So every realisation of L₁₅ is free. ∎

This lattice has d₁ = m + 2 (ε = 2 in Dimca–Kühne–Pokora's notation), the class they identify
as having the most room for counterexamples. The same computation for the 13-line lattice with
moduli (exponents (1, 6, 6)) also passes; it is within the 14-line range anyway.

**Other candidates** (`work/exact_tc_driver.py`). I ran the same exact check on every distinct
free, non-DF lattice from my connecting-line searches over F₁₁, F₁₃ and F₁₇ (56 lattices,
13–28 lines):
- **13-line (1, 6, 6) lattice with moduli:** passes (one rational curve, non-free locus inside
  the degeneration locus). It is within the 14-line range anyway.
- **15-line lattice:** independently confirms Theorem 2.
- **One 19-line (1, 9, 9) lattice from F₁₁:** its saturated realisation ideal is (1), so it has
  no realisation in characteristic 0.
- **The rest are still running** (slowly; the machine was under memory pressure). Results
  append to `work/exact_tc_driver.out`.

Most of these lattices have d₁ = q (the field size). That is the signature of the Frobenius
derivation, so I expect them to be finite-field artefacts. The exception is the 21-line
(1, 9, 11) lattice on 7 points. It occurs over F₁₁ but not over F₁₃ or F₁₇, which is the
pattern of a realisation over ℚ(√−7). It is the one to watch.

## 3. Fifteen lines

**Proposition 3.** A 15-line counterexample has exponents (6, 8) or (7, 7).

**The (6, 8) case.**
- Every line carries exactly 6 multiple points, and m ≤ 5.
- Counting (Σ_P C(m_P, 2) = 105, Σ_P (m_P − 1) = 62, Σ_H s_H = 90) leaves four point-multiplicity
  profiles (n₂, n₃, n₄, n₅):
    (3, 16, 9, 0), (2, 19, 6, 1), (1, 22, 3, 2), (0, 25, 0, 3).

**Proposition 4.** A line arrangement with profile (0, 25, 0, 3) is projectively equivalent to the
Ceva arrangement (x⁵ − y⁵)(y⁵ − z⁵)(z⁵ − x⁵) = 0. So TC holds for it.

*Proof.*
1. Every line has one quintuple point and five triple points. So the lines split into three
   pencils of 5 lines through P₁, P₂, P₃, and no line contains two of the P_i.
2. A line of pencil 1 meets the 10 lines of pencils 2 and 3 at its 5 triple points. So each
   intersection of lines from different pencils is a triple point: the arrangement is a 3-net of
   order 5.
3. *If P₁, P₂, P₃ are collinear,* send their line to infinity. The pencils become parallel
   classes x = aᵢ, y = bⱼ, x + y = c_k with aᵢ + bⱼ ∈ {c_k}. So |A + B| = 5 for 5-element sets
   A, B ⊂ ℂ, contradicting |A + B| ≥ |A| + |B| − 1 in a torsion-free group.
4. *So the P_i are the coordinate points.* The pencils are x = aᵢy, y = bⱼz, z = c_kx with
   aᵢ, bⱼ, c_k ∈ ℂ*, and the triple points force aᵢbⱼ ∈ {c_k⁻¹}. So |A·B| = 5 = |A| = |B|.
5. By Kneser's theorem, A and B are cosets of the subgroup μ₅ ⊂ ℂ*.
6. Rescaling coordinates turns A, B, C into μ₅. That is the Ceva arrangement, which is free
   (the reflection arrangement of G(5, 5, 3), exponents (1, 6, 8)). ∎

**Still open.** The profiles (3, 16, 9, 0), (2, 19, 6, 1) and (1, 22, 3, 2), and the (7, 7) case,
are the smallest cases these constraints leave open. For the two profiles with m = 5 = d₁ − 1,
Dimca–Kühne–Pokora add one condition: a non-free realisation would be plus-one generated with
exponents (5, 10, 12). Settling 15 lines would need a Barakat–Kühne-type enumeration of these
profiles.

## 4. Finite fields

**Proposition 5.** TC holds for every line arrangement over F_q with q ≤ 7.

*Proof.* Let n be the number of lines.
- *n ≤ 14:* Barakat–Kühne, valid in every characteristic.
- *n ≥ 2q:* Abe 2014, Cor. 6.2, building on Yoshinaga 2006. If χ(A, q) = 0 then A is free, and
  if n ≥ 2q and A is free then χ(A, q) = 0. So freeness is equivalent to χ(A, q) = 0, which is
  combinatorial.
- For q ≤ 7 we have 2q ≤ 14, so the two ranges cover every n. ∎

For q = 8 the open range is n = 15; for q = 9 it is 15 ≤ n ≤ 17. My exhaustive PG(2, 5) search
(Finding 13) agrees with this. As far as I know this combination is not stated anywhere, but it
is immediate from published results.

**Proposition 6 (all ranks).** Over F_q, TC holds for every *covering* lattice. Here covering means
that every codimension-2 subspace lies in some hyperplane, equivalently
|A|·[ℓ−1]_q − b₂ = [ℓ choose 2]_q, which is combinatorial.
- Such arrangements are free with exponents (1, q, …, q^{ℓ−2}, |A| − [ℓ−1]_q), by Lemma 1 of
  `FREE_NOT_DF.md`.
- In rank 3 this is Yoshinaga's theorem.
- Over F₂ and F₃, TC holds trivially, because binary and ternary matroids are uniquely
  representable.

## 5. P³

**Proposition 7 (reduction).** Let (A₁, A₂) be a rank-4 counterexample. Then one of two things
holds:
- **(a)** Some rank-3 localisation of L is itself a TC counterexample, so the problem drops to P².
- **(b)** A₂ is locally free in codimension 3. Then for every plane H the Ziegler
  multirestriction (A₂^H, m^H) is a non-free rank-3 multiarrangement, while (A₁^H, m^H) is free
  [Abe–Yoshinaga, Thm. 5.1(3)]. The two share their simple lattice and multiplicities, and also
  every local exponent, since those come from the free localisations. They are never isomorphic
  [Abe–Yoshinaga, Cor. 5.3].

In addition:
- L is not DF [Abe 2016].
- L has no locally heavy flag [Abe–Kühne].

So TC in P³ follows from TC in P² plus a statement about multirestrictions. That statement is:
two locally free rank-4 realisations whose Ziegler multirestrictions share all combinatorial and
local data have the same multirestriction freeness.

**What my experiments say about that statement.**
- It cannot be proved from the multiarrangement alone. Freeness of rank-3 multiarrangements is
  not combinatorial: in the X3 family it is non-free exactly at t = 1, or at t² − t + 1 = 0
  (Finding 1).
- In every free lift I built (more than 2,300), the rank-4 lattice changed exactly where the
  multirestriction became non-free, and the lift was DF (Findings 2, 7, 8).

**Corollary 8.** If some plane H has a restriction lattice that is projectively unique up to field
automorphisms (with its multiplicities), then TC holds for L.

Known free non-DF rank-4 examples:
- G(r, r, 4): over the finite fields I tried, its realisations were few, Galois-type and all free
  (Finding 14). I have not computed its complex realisation space.
- **The 26-plane arrangement** (Finding 16; exponents (1, 7, 9, 9), not DF). TC holds for it
  (`work/exact26_space.py`), because its complex realisations form one Galois orbit:
  1. Its lattice determines the 8 points that span the planes, and their collinearity and
     coplanarity structure. So every realisation is, up to PGL(4), a member of the 3-parameter
     family of Finding 16.
  2. Imposing all 8 + 47 + 124 dependencies of the lattice and saturating away the 54 forbidden
     coplanarities gives the realisation ideal (a − c, b − c, c² − c + 1).
  3. So the only complex realisations are A(ω, ω, ω) and its complex conjugate.

  Its freeness was checked over F₇, F₁₃ and F₁₉. TC for it does not depend on that.
- The seven F₃ examples are rigid and exist only in characteristic 3 (`FREE_NOT_DF.md`).

## 6. Where the proof stops

**In P².**
- Every constraint in Theorem 1 is numerical: points per line, exponents, multiplicities. They
  rule out most lattices, but they contradict nothing in general.
- A counterexample is a lattice inside the "window" of Theorem 1(3)–(7). On its realisation space
  the logarithmic bundle splits generically but jumps on a nonempty closed set, to an unstable
  bundle with a section of degree r < d₁, while the lattice stays the same.
- In every case I could compute exactly (§2), the jump locus is contained in the degeneration
  locus. The bundle "cannot jump without an extra incidence."
- A proof would need a reason why a jump of the logarithmic bundle forces an extra concurrency.
  For a lattice with irreducible realisation space, that is equivalent to TC for the lattice.
  I see no mechanism that gives it in general.
- Dimca's Conjecture 1.2 (mdr < (n − 2)/2 is combinatorial) would imply TC. Its stronger form
  fails for a 9-line pair (Dimca–Pokora 2026).

**In P³.** The missing piece is the multirestriction statement in Proposition 7. The experiments
show it holds whenever I could test it, through "protection": the lift's lattice records the
special parameter that the restriction's lattice cannot see. But I have no proof of that
mechanism.

## 7. Over ℚ (and over ℝ)

TC over ℚ is weaker than TC over ℂ:
- Freeness is unchanged by extending the field, so a ℚ-counterexample is also a ℂ-counterexample.
- The converse fails: a ℂ-counterexample need not be definable over ℚ. Freeness is
  Galois-invariant, so the non-free locus of a ℚ-defined realisation space is defined over ℚ, but
  it need not contain rational points.

I could not prove TC over ℚ either. But ℚ ⊂ ℝ gives a constraint that is unavailable over ℂ.

**Proposition 9.** If (A₁, A₂) is a counterexample over ℝ (in particular over ℚ), then
  d₂ ≤ 2d₁ − 7 + 18/(d₁ + 3),
which is strictly stronger than Abe's d₂ ≤ 2d₁ − 4 for d₁ ≥ 4.

*Proof.*
1. A real line arrangement that is not a pencil satisfies Melchior's inequality
   t₂ ≥ 3 + Σ_{k≥4} (k − 3) t_k, equivalently 2N − b₂ ≥ 3, where N is the number of points.
2. Summing Theorem 1(3), s_H ≤ d₁, over the n lines gives b₂ + N = Σ_H s_H ≤ n d₁.
3. So (b₂ + 3)/2 ≤ N ≤ n d₁ − b₂. Substitute b₂ = d₁d₂ + d₁ + d₂ and n = d₁ + d₂ + 1. ∎

**Consequences.** Over ℚ there is no counterexample:
- with 15 lines and exponents (6, 8) (all four complex-admissible profiles violate Melchior);
- with exponents (7, 9), (7, 10) or (8, 11) — exactly the cases excluded by the new bound.

The smallest open real/rational cases are 15 lines with exponents (7, 7) and 16 lines with
(7, 8). Counting weak combinatorics that satisfy all the numerical constraints of Theorem 1 plus
Melchior (with m ≤ d₁ − 1):

| n | (d₁, d₂) | admissible profiles over ℂ | over ℝ |
|---|---|---:|---:|
| 15 | (6, 8) | 4 | **0** |
| 15 | (7, 7) | 108 | 85 |
| 16 | (7, 8) | 101 | 62 |
| 17 | (7, 9) | 70 | **0** |
| 17 | (8, 8) | 377 | 300 |
| 18 | (7, 10) | 16 | **0** |
| 18 | (8, 9) | 438 | 323 |
| 19 | (8, 10) | 397 | 172 |
| 19 | (9, 9) | 1257 | 1070 |
| 20 | (8, 11) | 314 | **0** |
| 20 | (9, 10) | 1613 | 1300 |

**Where it stops over ℚ.** The surviving profiles need actual lattices (linear spaces) and their
realisation spaces over ℚ. Each is a finite computation of the §2 type, but the enumeration is
large, and I have not done it. No arithmetic argument I tried — rational points on the non-free
locus, or reduction mod p — forces the non-free locus to lie in the degeneration locus.

## 8. Search over quadratic number fields

**Scripts.** `work/numfield_search.py`, `work/numfield_deep.py`, `work/numfield_screen.py`;
results in `work/numfield/`.

**Method.**
- **Arithmetic.** All arithmetic is exact in ℤ[α], for α ∈ {i, √2, ω, φ, √−2, √3, √−7, √5}.
  A lattice is accepted only if it is identical modulo two large primes that split in K.
- **Generators.**
  (a) Connecting-line arrangements of random point sets, with coordinates in
      {0, ±1, ±α, ±1±α, 2}; about 147,000 tried.
  (b) Greedy incidence-rich line sets.
  (c) Deletions of up to 4 lines from, and additions of up to 3 lines through the multiple points
      of, the special arrangements of each field: B₃ (every field), G(4,4,3) and G(4,1,3) over
      ℚ(i), G(3,3,3), G(3,1,3) and G(6,1,3) over ℚ(ω), and the icosahedral H₃ over ℚ(√5).
      About 13.8 million arrangements; 1.67 million had split χ and 1.50 million were free.
- **Screen.** Every distinct free, non-DF lattice found was screened by enumerating all its
  realisations over two medium primes that split in K, then testing each one's freeness exactly.
  A counterexample over K would show up as mixed freeness for almost every split prime.

**Result.** No counterexample. Free, non-DF lattices are very rare among these arrangements. Only
six distinct ones appeared:

| lines | exponents | points (kᵗᵐ) | moduli | split-prime realisations, free/total |
|---|---|---|---|---|
| 12 | (1, 5, 6) | 3¹⁶ 4³ | 0 | 2/2, 2/2 |
| 13 | (1, 6, 6) | 3⁶ 4⁶ 5¹ | 0 | 2/2, 2/2 |
| 13 | (1, 6, 6) | 3³ 4³ 5³ | 1 | 54/54 … 66/66 (in 7 fields) |
| 15 | (1, 7, 7) | 3⁶ 5⁶ | 1 | 54/54, 64/64 (Theorem 2) |
| 18 | (1, 7, 10) | 3³⁶ 6³ | 0 | 2/2, 2/2 (Ceva(6) = G(6, 6, 3)) |

The table lists five rows; the two 12-line hits, from G(4,1,3) and G(4,4,3), are the same
weak combinatorics, which makes six. All lattices with at most 14 lines are already covered
by Barakat–Kühne. The 15-line one is proved exactly in §2. The 18-line Ceva(6) is rigid, and both
of its split-prime realisations are free.

**Assessment.** The special geometry of these fields — reflection arrangements and their
deletions and additions — overwhelmingly produces divisionally free arrangements, which satisfy
TC automatically. The few non-DF ones are rigid, or they are the two known lattices with moduli.
A counterexample would need a non-DF free lattice with moduli and more than 14 lines, and these
generators essentially never produce one.

## 9. Conjecture F (positive-dimensional components)

**Conjecture F.** Let C be a positive-dimensional component of the realisation space of a free,
non-DF lattice, and Z(C) the set of non-free points on C. Then Z(C) is empty: the incidence theorem
that gives C its excess dimension also forces freeness along all of C.

**Proved in general.**
- **(F1)** Z(C) is a proper closed subset of C (Yuzvinsky's openness of freeness).
- **(F2)** Z(C) is exactly the rank-drop locus of the degree-(d₁ − 1) derivation matrix. It is
  defined over the field of definition of C and is invariant under Aut(L).
- **(F3) Local-to-global certificate.** For every line H, Z(C) ⊆ J_H(C), the set where the Ziegler
  restriction to H changes exponents (Yoshinaga's criterion). J_H(C) is the pull-back of a finite
  jump set of a rank-2 multiarrangement under the map C → M₀,ₛ_H. So if J_H(C) ∩ J_H′(C) = ∅ for
  two lines, then F holds on C. Special cases:
  - some line's points are constant along C (rigidity principle);
  - some line has s_H = 4 and n is even (parity).

  For the 15-line family none of the trivial cases applies: all 15 lines move.

**Proved for every case that occurs in a large class.** By Corollary C, free non-DF lattices with
moduli need excess dimension, i.e. an incidence theorem. In every source I have, they come from
point configurations (lines through pairs of points). The exhaustive enumerations of connecting-line
arrangements found, as the only free non-DF lattices with positive-dimensional realisation space:
- over F₁₁, all configurations of ≤ 9 points;
- over F₁₃ and F₁₇, all configurations of ≤ 8 points (new runs; 33,685 and 258,735 orbits at
  8 points);

only the 13-line (1, 6, 6) lattice and the 15-line (1, 7, 7) lattice. For both, Conjecture F is
proved exactly over ℚ̄ (§2: the non-free locus lies inside the degeneration locus).

Hence F, and TC, hold for every characteristic-0 family of connecting-line arrangements of ≤ 8
points whose generic member keeps its lattice modulo 11, 13 or 17.

**Not proved.** That F3 or a direct computation always applies. A general argument would have to
explain why, in the 15-line family, the rank drop of the derivation matrix lands exactly on the
extra concurrencies. I have no such argument.

## 10. Beyond 14 lines: exhaustive verification by exponent class

The literature stops at 14 lines (Barakat–Kühne). The anatomy of §1 makes larger n tractable: a
counterexample lattice with n lines and exponents (d₁, d₂) must have χ = (t − 1)(t − d₁)(t − d₂),
every line with s_H ∈ [d₂ − d₁ + 4, d₁] points, and all multiplicities ≤ d₁ − 1. For n = 15 the only
exponent classes are (6, 8) and (7, 7).

**Method** (`work/tc15/`).
1. *Enumeration.* Lines are elements, multiple points are blocks. Write w(x) = Σ_{B∋x}(|B| − 2) =
   n − 1 − s_x and W = Σ_B C(|B| − 1, 2) = C(n, 2) − b₂. The constraints become w(x) ∈ [wmin, wmax]
   and W = Wtot. Stage 1 (`bigblocks.py`) enumerates the configurations of blocks of size ≥ 4 up to
   isomorphism (one block at a time, one representative per orbit of the automorphism group, nauty
   certificates). Stage 2 (`fill_triples.py`) adds the triples by an exact search that decides each
   pair once, then removes isomorphic duplicates.
2. *Realisation space* (`exact_tc_lattice.py`). In the dual plane the lines are points; four in
   general position are the frame, the others are determined or parametrised greedily, and the
   blocks give the collinearity equations. The components of the realisation space are the minimal
   primes of this ideal that contain no forbidden collinearity.
3. *Freeness on each component* by Yoshinaga's criterion on the Ziegler restriction to the line
   z = 0: free iff the matrix of the conditions (ax + by)^μ | af + bg, in degree d₁ − 1, has full
   rank 2d₁. On a 0-dimensional component the rank is computed over the residue field, which
   covers all Galois conjugates at once. On a positive-dimensional component, generic rank plus the
   annihilator of the cokernel give the non-free locus, which is compared with the degeneration
   locus.

**Theorem 10.1.** Terao's conjecture holds for arrangements of 15 lines in P²_ℂ with exponents
(1, 6, 8): if a free arrangement with these exponents has lattice L, every realisation of L is free.

*Proof.* A counterexample lattice has s_H = 6 on every line, multiplicities ≤ 5, and χ =
(t − 1)(t − 6)(t − 8), so w(x) = 8 for every point. Writing f(x), q(x) for the numbers of
quintuple and quadruple points on the line x, the number of double points on x is
d(x) = 2f(x) + q(x) − 2. This rules out the profile (n₂, n₃, n₄, n₅) = (1, 22, 3, 2): its five lines
through no quintuple point would need ≥ 10 incidences with three quadruple points that pairwise
share at most one line, which inclusion–exclusion forbids on 5 lines. The remaining profiles have at
most 9 blocks of size ≥ 4. The enumeration gives 12,721 big-block configurations and exactly three
candidate lattices:
- the two 3-nets of order 5 (profile (0, 25, 0, 3); the Latin squares of Z₅ and of the non-group
  quasigroup of order 5 — the search found exactly 161,280 = |Latin squares of order 5| raw
  solutions);
- one lattice with 9 quadruple and 16 triple points (profile (3, 16, 9, 0)).

Exact computation: the non-group net and the 9-quadruple lattice have realisation ideal (1), so no
complex realisation. The Z₅ net has a single 0-dimensional component of degree 4 (the Ceva
arrangement over ℚ(ζ₅)), on which the Yoshinaga matrix has full rank 12/12: all realisations are
free. ∎

**Theorem 10.2.** Terao's conjecture holds for arrangements of 15 lines in P²_ℂ with exponents
(1, 7, 7).

*Proof.* A counterexample lattice has χ = (t − 1)(t − 7)², every line with 4 to 7 points, and
multiplicities ≤ 6; in the enumeration parameters, w(x) ∈ [7, 10] and W = 42.
1. *Enumeration.* Stage 1 gives 99,993 big-block configurations; stage 2 gives 6,091,145 candidate
   lattices (2 GB). The known (1, 7, 7) lattice with moduli (Theorem 2) is among them, as it must be.
2. *Realisability, exactly, in three passes* (`fast_real.py`, `fast_real2.py`, `exact_tc_lattice.py`;
   all over ℚ, with python-flint and Macaulay2):
   - a forbidden collinearity holds identically in the frame-fixed parametrisation, or the
     equations reduce to a nonzero rational number, or (one parameter) the gcd of the equations is
     constant, or every root of it is degenerate, or (two parameters) the gcd of the v-resultants is
     constant: 4,831,300 lattices non-realisable, 1,259,845 deferred;
   - two parameters, with gcds over the number fields ℚ[u]/(φ) for the factors φ of the resultant
     gcd, and curve components checked for forced degeneracy: 1,245,893 more non-realisable,
     13,952 deferred;
   - Macaulay2 (minimal primes of the realisation ideal, degenerate components removed): 13,942
     non-realisable (1,383 with ideal (1), 12,559 with only degenerate components), **10 realisable**.
   The first two passes were validated against Macaulay2 on a 2,000-lattice sample (no
   disagreement), and are one-sided: they only ever assert non-realisability.
3. *Freeness on the 10 realisable lattices*, by Yoshinaga's criterion on each component:
   - 5 lattices with 0-dimensional realisation spaces (one Galois orbit each, of degree 2, 4, 2, 4,
     4) on which every realisation is non-free (rank 13 of 14);
   - 4 lattices with 0-dimensional realisation spaces on which every realisation is free: three
     of degree 2 (conjugate pairs over quadratic fields) and one of degree 1, i.e. a unique
     realisation, defined over ℚ, with 3 quintuple, 6 quadruple and 6 triple points
     (`work/tc15/realisable_n15_7_7.json`, index 13926);
   - 1 lattice with a 1-dimensional realisation space, generically free, whose non-free locus lies
     inside the degeneration locus: the known lattice with 6 quintuple and 6 triple points
     (Theorem 2 again, now found by the enumeration).
   No lattice has both free and non-free realisations. ∎

*Cross-check* (`hunter/realize.py`, `hunter/ffree.py`): realising each of the 10 lattices over
F_q for the ten primes 11 ≤ q ≤ 43 and testing freeness with the independent finite-field engine
agrees with the exact verdicts in every case (the rigid lattices realise exactly at the primes where
their field of definition splits; every realisation of the family is free).

**Corollary 10.3.** Terao's conjecture holds for all arrangements of 15 lines in P²_ℂ.

*Proof.* By §1, a counterexample with 15 lines has exponents (6, 8) or (7, 7) [Abe 2014,
Cor. 5.4 and 5.5], its lattice is not divisionally free [Abe 2016], every line carries between
d₂ − d₁ + 4 and d₁ points [Abe 2014 Cor. 1.2; Abe 2012 Prop. 4.2 and Cor. 0.4], and the largest
multiplicity is at most d₁ − 1 [Dimca–Kühne–Pokora]. Theorems 10.1 and 10.2 cover exactly these
lattices. ∎

This extends the Barakat–Kühne verification (≤ 14 lines) by one. As a by-product, the free
15-line arrangements with exponents (1, 7, 7) that are not divisionally free, have at most 7
points on every line and multiplicities ≤ 6, form exactly 5 lattices: 4 rigid (three conjugate pairs
of realisations and one rational arrangement) and the known one-parameter family, all of whose
members are free.

**Theorem 10.4.** Terao's conjecture holds for all arrangements of 16 lines in P²_ℂ.

*Proof.* With 16 lines, d₁ + d₂ = 15 and the reductions of §1 leave only the exponents (7, 8):
(6, 9) has δ = 3 ≥ d₁ − 3 [Abe 2014, Cor. 5.4] and smaller d₁ is covered by Cor. 5.5. A
counterexample lattice for (7, 8) has χ = (t − 1)(t − 7)(t − 8), between 5 and 7 points on every
line and multiplicities ≤ 6 (w(x) ∈ [8, 10], W = 49, blocks ≤ 6). The enumeration gives 8,884,481
big-block configurations and 16,371,552 candidate lattices. The exact filters decide 16,343,863 of
them (13,748,942 in the first pass, 2,594,921 in the number-field pass) and Macaulay2 the remaining
27,689: 3,039 have realisation ideal (1) and 24,650 have only degenerate components. **No candidate
lattice has a complex realisation**, so none has a free one, and there is no counterexample.
(Soundness check: on a random sample of 3,001 of the candidate lattices, the full Macaulay2 pipeline
agrees with the exact filters, as it did on the 15-line sample, which contained realisable
lattices.) ∎

So the verified range is now 16 lines. Note the contrast with n = 15: the (7, 8) class is more
over-determined (e(L) ≤ d₁(1 − δ) − 6 = −6 by Theorem B, against ≤ 1 for (7, 7)), and indeed it
contains no realisable lattice at all, free or not. The volume was also far below my estimate of
§11: the ratio lattices/skeletons was 1.8 for this class (61 for (7, 7)), because the window of
points per line is narrower, so the whole computation took about 4 hours on 8 cores.

**Theorem 10.5 (17 lines, 9 Oct 2026).** Terao's conjecture holds for arrangements of 17 lines
in P²_ℂ with exponents (7, 9), and for arrangements with exponents (8, 8) whose non-free member
would have mdr ≤ 6 (part [A] of §11: every line with 6 or 7 points, multiplicities ≤ 6).

*Proof.* The candidate lattices have χ = (t − 1)(t − 7)(t − 9) with 6 or 7 points on every line
and multiplicities ≤ 6 (w(x) ∈ [9, 10], W = 57), respectively χ = (t − 1)(t − 8)² with 6 or 7
points on every line and multiplicities ≤ 6 (w(x) ∈ [9, 10], W = 56). Stage 1 (`bigblocks2.py`,
one shared run for both classes, 81,644 s on 10 cores) produced 1,503,001,339 big-block skeleton
states (1,495,909,996 usable for (7, 9), 1,016,814,025 for (8, 8)) in 2,001 chunks. Stage 2
(`pipeline.py`, 220.7 CPU-hours) turned them into 6,581,531 candidate lattices: 4,623,124 for
(7, 9) and 1,958,407 for (8, 8)[A]. The exact filters decided 4,600,181 and 1,943,787 of them as
non-realisable, and Macaulay2 (`exact_tc_lattice.py`, 22 minutes on 10 cores) the remaining
22,943 and 14,620: realisation ideal (1) for 2,443 and 1,301, only degenerate components for
20,500 and 13,319. **No candidate lattice of either class has a complex realisation**, so none
has a free one, and there is no counterexample. (MIXED = 0 and errors = 0 in both classes.) ∎

*Correction (10 Oct 2026).* Stage 1 of this run (`bigblocks2.py`) applied the unjoined-pair
condition of §11 in its too-strong form. For the class (7, 9) it discarded every skeleton with two
disjoint blocks of sizes {4, 6} or {5, 5}, i.e. with (m_P − 1) + (m_Q − 1) = 8 strictly between
d₁ = 7 and d₂ = 9, which the correct condition allows. **So the (7, 9) part of Theorem 10.5 is
not a complete computer proof**; the class (7, 9) is excluded only by `TC_FOLIATION.md`
Theorem 5.1. For (8, 8) the condition used, (m_P − 1) + (m_Q − 1) ≤ 8, is the correct one, and
that part of the theorem stands. The 15- and 16-line runs used `bigblocks.py`, which does not
apply the condition, so Theorems 10.1–10.4 are unaffected.

Both statements are also consequences of `TC_FOLIATION.md`: Theorem 5.1 gives 3·mdr(A₂) ≥ n + 2,
i.e. mdr(A₂) ≥ 7 for 17 lines, which excludes (7, 9) (there mdr(A₂) ≤ d₁ − 1 = 6) and part [A]
of (8, 8); so the computation is an independent check of that theorem on 6.6 million lattices.
What remains for "TC for 17 lines" is part [B] of (8, 8): the non-free member nearly free with
exponents (7, 10), lines with 4 to 8 points, m ≤ 6, see §11 and `TC_FOLIATION.md` §10.

**Larger n.** For n = 18 the classes are (7, 10) (exactly 7 points on every line) and (8, 9);
Theorem 10.1 of `TC_FOLIATION.md` excludes (7, 10), and (8, 9) needs mdr(A₂) = 7. The balanced
classes (8, 8)[B] at 17 and (8, 9) at 18 are the (7, 7) problem one size up and one to two orders
of magnitude larger. See §11.

## 11. Scaling beyond 15 lines: where the cost is, and what would remove it

**Diagnosis from the 15-line run** (`work/tc15/`). The candidate class for exponents (7, 7) had
6,091,145 lattices; 10 are realisable; the other 99.9998% are abstract linear spaces with no
geometry. The cost is therefore intrinsic to "enumerate lattices, then test realisability": the
number of dense linear spaces grows super-exponentially (99,993 big-block skeletons at n = 15,
8,884,481 at n = 16 for the single class (7, 8)), and the ratio lattices/skeletons was 61.

Measurements that rule out the obvious shortcuts:
- *Profile inequalities.* Hirzebruch's and the Bojanowski–Pokora inequality are satisfied by 99.6%
  of the skeletons (n = 15 and 16): the candidates have many double points.
- *Realisability of the skeleton alone.* Skeletons with ≤ 8 big blocks are essentially all
  realisable, with realisation spaces of dimension 4–16; non-realisability appears only for the
  densest skeletons (n = 16 sample: 11 big blocks 23/58 realisable, 12 big blocks 0/14). The
  over-determination comes from the triples, i.e. at the leaves of the search.
- *Realisability pruning inside the triple search* (`fill_pruned_experiment.py`): with the exact
  one-sided test applied at every node where it is cheap, the tree shrank by 28% and the leaves by
  39%, at 20× the cost. The combinatorial search followed by the leaf filter is the right design;
  it just produces too many leaves.
- *Theoretical cuts along the obvious axes do not help.* Of the 6,091,145 candidates, 5,068,388
  have maximal multiplicity 5 (ε = d₁ − m = 2) and 5,209,745 have smallest line size 5 — exactly
  where the five free (1, 7, 7) lattices live (all have ε = 2). No free candidate has ε = 3.

**A new combinatorial necessary condition** (small, but exact). Apply Abe 2014, Cor. 1.2(2), to
the free realisation A₁: every line L of the plane not in A₁ meets A₁ in k_L ∈ {d₁ + 1} ∪
ℤ_{≥ d₂+1} points, i.e. σ_L = Σ_{P ∈ L} (m_P − 1) ∈ {0, …, d₁} ∪ {d₂}. Two multiple points P, Q
not on a common line of A are joined by an external line, so

  **(m_P − 1) + (m_Q − 1) ≤ d₁, or = d₂ with no third multiple point on PQ.**

*Correction (10 Oct 2026).* The bold statement is too strong when d₂ ≥ d₁ + 2. Abe's corollary
constrains σ_L, and σ_L can exceed (m_P − 1) + (m_Q − 1) through further multiple points of A₁
on the line PQ, which the lattice does not record (PQ is not a line of A). The correct lattice
condition is **(m_P − 1) + (m_Q − 1) ≤ d₂**, with σ_L = d₂ forced in the realization when the
sum exceeds d₁. For d₂ ≤ d₁ + 1 the two statements coincide, so everything below about the
(7, 7) lattices stands.

This is a condition on the lattice. It excludes 1.3% of the (7, 7) skeletons and certifies
combinatorially that two of the ten realisable (7, 7) lattices (indices 3143 and 4608: two 6-fold
points not on a common line) have no free realisation — in agreement with the exact computation.

**What does scale.**
1. *Streaming and a compiled leaf filter.* The leaf filter costs 3 ms per lattice in python-flint;
   the (7, 8) class at n = 16 (~5·10⁸ lattices) is then ~400 CPU-hours, i.e. about two days on
   8 cores if the lattices are filtered as they are generated instead of written out. This makes
   16 lines a large but finite computation; 17 lines is ×50 beyond it.
2. *Components only.* Terao can fail for L only if the non-degenerate realisation space has a
   positive-dimensional component or at least two irreducible components over ℚ (§5, Prop. A).
   So no freeness computation is ever needed for the rigid single-orbit lattices, which were 9 of
   the 10 realisable ones here; freeness is computed only on the rare multi-component or
   positive-dimensional lattices.
3. *Geometry-first enumeration.* Enumerate the dual point configurations directly, adding one
   point at a time as the intersection of two existing lines, on one existing line (one parameter)
   or free (two parameters), with the matroid as the isomorphism key and the realisation space
   tracked exactly; prune when it becomes empty or degenerate, and when the density conditions
   (≤ d₁ lines through a point, the fixed total W) cannot be met. The number of nodes is then the
   number of realisable dense partial configurations, not of abstract linear spaces. The
   measurements above are a warning: partial configurations are mostly realisable until they are
   nearly complete, so the gain comes from the last few levels, and the algebra at every node must
   stay in the ≤ 2-parameter range to be affordable.
4. *An induction with a bigger class.* Deleting any line from a counterexample (A₁ free, A₂
   non-free, same lattice) gives A₁ ∖ H plus-one generated with mdr = d₁ and A₂ ∖ H with mdr ≤
   d₁ − 1 (derivations restrict; mdr drops by at most one under deletion). So every deletion of a
   counterexample lattice is a lattice with n − 1 lines whose realisations have different minimal
   degrees of Jacobian relations, with χ = (t − 1)[(t − d₁)(t − d₂) − (t − s_H + 1)]. Terao for n
   lines would follow from the absence of such "mdr-mixed" lattices with n − 1 lines. This is
   Dimca's Conjecture 1.2 territory (mdr < (n − 2)/2 combinatorial), now known to fail in its
   stronger form for 9 lines (Dimca–Pokora 2026), so it is a research question, not a computation.

**Bottom line.** 16 lines turned out to be a four-hour computation (Theorem 10.4), because the
(7, 8) class is narrow. The balanced classes (8, 8) at 17 and (9, 9) at 19 are where lattice
enumeration ends; beyond that, only a structural
theorem about free arrangements with d₁ ≥ m + 2 (the ε ≥ 2 regime of Dimca–Kühne–Pokora, where
all our free candidates sit) or about mdr-mixed lattices would remove the wall.

**The 17-line (8, 8) class, part [B].** For exponents (8, 8) the refinement Theorem 1(7) splits the
candidates by r = mdr(A₂) ∈ {6, 7}. For r = 6 every line has 6 or 7 points and m ≤ 6 (this is what
the running enumeration covers, together with (7, 9)). For r = 7 the non-free member is *nearly
free* with exponents (7, 10) (τ = 192 = 193 − 1 in du Plessis–Wall), its lines carry 4 to 8 points,
and m ≤ 7. Two published results cut this case down:
- Dimca–Ibadula–Măcinic, Prop. 4.7 (citing Abe–Dimca, Cor. 1.7): if A₂ is nearly free with
  exponents (d₁', d₂') and m(A₂) ≥ d₁', every lattice-mate of A₂ is nearly free. A free
  arrangement is not nearly free, so **m ≤ 6** in part [B].
- Abe–Dimca (Thm. 5.3, as quoted in DIM Prop. 4.6): every Ziegler restriction of a nearly free
  arrangement with exponents (7, 10) has exponents (6, 10) or (7, 9); with Abe's gap bound
  e₂ − e₁ ≤ s_H − 2 this forces (7, 9) on every line with s_H ≤ 5, and (7, 9) on lines with 8
  points by s_H ≤ e₁ + 1.
What is left of part [B] is: lattices with χ = (t − 1)(t − 8)², m ≤ 6, every line with 4 to 8 points
and at least one line with 4, 5 or 8 points (lattices with all lines in {6, 7} are in part [A]).
Remark 4.2 of DIM would dispose of the 8-point lines if d₂' ≠ d₁' + 3; here d₂' = d₁' + 3 exactly,
so it does not apply. This residual class is not covered by the current run; it is the only
obstacle to "TC for 17 lines" once the run finishes.

*Later the same day:* `TC_FOLIATION.md` Theorem 5.1 excludes r ≤ (n + 1)/3 = 6 for n = 17, so
the (7, 9) class and part [A] (r = 6) of (8, 8) — everything the current run covers — are now
settled by theory, and the run is an independent check of that theorem. *9 Oct 2026:* the run
finished (Theorem 10.5): no realisable candidate lattice in either class. Part [B] is the only open
17-line class; there r = 7, the residual curve J/Q of the inflection curve is a quartic, and the
excess (d₁ − r)(d₂ − r) is exactly 1.

**General n.** `TC_FOLIATION.md` proves 3·mdr(A₂) ≥ n + 2 for every counterexample (hence
d₂ ≤ 2d₁ − 6, d₁ ≥ 7, n ≥ 15) by the inflection curve of the foliation of the minimal
derivation. An earlier attempt to turn the patterns into a proof for all n is in `TC_GENERAL.md`:
the window for every n (§1), the structure forced in the narrow classes δ = d₁ − 4 (every line with
exactly d₁ points, mdr(A₂) = d₁ − 1, all Ziegler restrictions of A₂ with exponents (d₁ − 1, d₂ + 1),
a section of Ω¹(d₁ + 1) pinned to the multiple points; no real counterexample in these classes for
any n), and the reduction of TC in P² to a single statement about positions, Conjecture J (a jump of
the Ziegler exponents on one line forces an extra incidence), which is equivalent to TC. No proof.

## Sources

- Abe, [Exponents of 2-multiarrangements and freeness of 3-arrangements](https://arxiv.org/abs/1005.5276) (2010/2012).
- Abe, [Roots of characteristic polynomials and intersection points of line arrangements](https://arxiv.org/abs/1302.3822), J. Singularities 8 (2014).
- Abe, [Divisionally free arrangements of hyperplanes](https://arxiv.org/abs/1502.07520), Invent. Math. 204 (2016).
- Abe–Yoshinaga, [Free arrangements and coefficients of characteristic polynomials](https://arxiv.org/abs/1109.0668), Math. Z. (2013).
- Barakat–Kühne, [Computing the nonfree locus of the moduli space of arrangements and Terao's freeness conjecture](https://arxiv.org/abs/2112.13065), Math. Comp. 92 (2023).
- Dimca–Ibadula–Măcinic, [Freeness and near freeness are combinatorial for line arrangements in small degrees](https://arxiv.org/abs/1712.04400).
- Abe–Ibadula–Măcinic, [On some freeness-type properties for line arrangements](https://arxiv.org/abs/2101.02150).
- Dimca–Kühne–Pokora, [Free line arrangements with low maximal multiplicity](https://arxiv.org/abs/2505.01733).
- Dimca–Pokora, [A nine-line counterexample to a conjecture on the minimal degree of Jacobian relations](https://arxiv.org/abs/2607.01985).
- Yoshinaga, On the freeness of 3-arrangements, Bull. LMS 37 (2005); Free arrangements over finite field, Proc. Japan Acad. 82 (2006).
- Pereira, Vector fields, invariant varieties and linear systems, Ann. Inst. Fourier 51 (2001) (extactic curves; used in `TC_FOLIATION.md`).
