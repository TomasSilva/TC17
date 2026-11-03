# TC_BUILD.md — trying to build a counterexample

Started 2026-10-14. The task: construct a pair (A₁, A₂) of line arrangements in P²_ℂ with the
same lattice, A₁ free and A₂ not, using every necessary condition established so far. The smallest
open case is 17 lines with exponents (1, 8, 8), A₂ nearly free with exponents (7, 10)
(TC_ATTEMPT §11, TC_FILTER, TC_CONTRADICTION §5). Notation as there.

## 0. Verdict

**Not built.** The attempt produced the following.

1. Three structural lemmas on the free member A₁ (§1): it has no free sub-arrangement of 14, 15
   or 16 lines; its free 13-line sub-arrangements, if any, have exponents (6, 6) and are obtained
   by deleting four 8-point lines whose six pairwise intersections are existing points; and, when
   A₁ has an 8-point line H, A₁ \ H is nearly free with exponents (8, 8) and logarithmic bundle
   T_{P²}(−9), while conversely every line meeting such a 16-line arrangement in 8 points gives a
   free (8, 8) arrangement.
2. A reformulation (§2): a 17-line counterexample with an 8-point line is the same thing as a
   16-line Ziegler pair with b₂ = 72 whose members are nearly free (8, 8) and nearly free (7, 9)
   (or worse), together with a common external line of weight 8.
3. Two explicit 17-line arrangements with χ̄ = (t − 8)² (§3, §3b). The harmonic four-pencil grid
   G₁₇ is free with exponents (8, 8) but has 9-point lines, so its lattice is divisionally free.
   The equianharmonic four-pencil arrangement E₁₇ over ℚ(√−3) is in the window and nearly free
   with exponents (7, 10): it is the reflection arrangement of G₂₆ (Hesse ∪ dual Hesse) minus the
   four Hesse lines through one flex, its four rich lines are exactly those, and its residual
   inflection quartic splits into them. E₁₇ is the non-free half of a would-be counterexample;
   its lattice is rigid.
4. The 2,655 seventeen-line sub-arrangements of the two reduced convex arrangements of degree 7,
   A(G₂₆) and A(6, 1, 3), with χ̄ = (t − 8)² are all nearly free; they form 13 lattices, all rigid
   with one conjugate pair of realisations, so Terao's conjecture holds for them (§5.4).
5. Every natural extension of the two known flexible free families fails (§4): the 15-line
   family has no external 8-point line at all, the 13-line family admits four 8-point lines with
   pairwise intersections on the arrangement only through one quintuple point, and deleting a
   line from the 15-line family leaves the same curve, with the lost concurrency automatic.
6. Pencil censuses over F₁₁ and F₁₃, lifted exactly (§5).
   - 4-point lines: the only window arrangement is E₁₇.
   - 5-point lines: the window arrangements are two new rational nearly free (7, 10) arrangements,
     R₁₇ᵃ and R₁₇ᵇ, whose residual quartic is two rich lines times a smooth conic, plus two
     deletions of A(G₂₆).
   - All six are rigid and non-free, and no free arrangement of this shape exists over these
     fields.
7. The literature mechanism for Ziegler pairs is a singular realisation space with hidden
   collinearities (§6). No lattice with χ̄ = (t − 8)² and a singular realisation space is known.

**What a counterexample at 17 lines now has to be.** Its non-free member is nearly free (7, 10)
with four or fewer rich lines; when the residual quartic is four lines, it is a reduced convex
arrangement minus four leaves, and all those lattices are rigid. So either the residual quartic
of A₂ is not a product of lines, or the lattice has a 5-point or 8-point line whose pencil
structure has moduli. No example of a free (8, 8) arrangement with all lines ≤ 8 points is known,
and Lemma 1.1 says it cannot be reached from a free arrangement by adding at most three lines.

## 1. What the free member must look like (17 lines, exponents (8, 8))

Throughout, A₁ is free with exponents (1, 8, 8), every line has 4 to 8 points and every
multiplicity is at most 6 (the window).

**Lemma 1.1 (no free sub-arrangement of 14–16 lines).** Deleting k ≤ 3 lines from A₁ never
gives a free arrangement.

*Proof.* TC_CONTRADICTION Lemma 6(b). For k = 1 directly: A₁ \ H is free iff s_H = 9. ∎

**Lemma 1.2 (free 13-line sub-arrangements).** If A₁ \ {ℓ₁, ℓ₂, ℓ₃, ℓ₄} = F is free, then
- F has exponents (1, 6, 6) and b₂(F) = 48;
- each ℓᵢ meets F in exactly 8 points, hence passes through multiple points of F of total weight
  W_F(ℓᵢ) = 5;
- each ℓᵢ has exactly 8 points in A₁, and every intersection ℓᵢ ∩ ℓⱼ lies on a line of F.
Similarly a free 12-line sub-arrangement has exponents (5, 6), b₂ = 41, and the five deleted
lines have 8, 8, 8, 8, 7 points at the time of addition.

*Proof.* Let e₁ + e₂ = 12 be the exponents of F. Then e₁e₂ = b₂(F) − 12 and
b₂(F) = 80 − Σ sᵢ, where sᵢ ≤ 8 is the number of points on ℓᵢ when it is added. So
e₁e₂ ≥ 80 − 32 − 12 = 36, forcing (6, 6) and all sᵢ = 8. Since sᵢ ≤ s_{ℓᵢ}(A₁) ≤ 8, no later line
creates a new point on ℓᵢ, so ℓᵢ ∩ ℓⱼ is already a point of F ∪ (earlier lines). For the
12-line case, e₁ + e₂ = 11 and e₁e₂ ≥ 80 − 40 − 11 = 29 gives (5, 6). ∎

**Lemma 1.3 (8-point lines and T(−9)).** Let A be any 17-line arrangement with b₂ = 80 and H a
line of A with 8 points, N = A \ H. The following are equivalent:
- (i) A is free with exponents (8, 8);
- (ii) mdr(N) = 8;
- (iii) N is nearly free with exponents (8, 8);
- (iv) E_N ≅ T_{P²}(−9).
When they hold, every line ℓ ∉ N with |N ∩ ℓ| = 8 gives a free arrangement N ∪ ℓ, and every line
of the plane meets N in at least 8 points.

*Proof.* b₂(N) = 72, c₁(E_N) = −15, c₂(E_N) = 57, so c₂(E_N(8)) = 1 and c₁(E_N(8)) = 1.
(i) ⇒ (ii): Abe's deletion theorem for a free arrangement with exponents (8, 8) and a line with
8 points gives a plus-one generated N with exponents (8, 8) and level 17 − 8 − 1 = 8, so N is
nearly free and mdr(N) = 8. (ii) ⇒ (iv): E_N(8) has no section of E_N(7), hence is stable with
c₁ = c₂ = 1, and the only such bundle is T(−1). (iv) ⇒ (iii): the Euler sequence twisted.
(iv) ⇒ (i): T(−9) restricts to O(−7) ⊕ O(−8) on every line, so for a line ℓ with
|N ∩ ℓ| = 8 the Faenzi–Vallès map E_N → O_ℓ(−8) kills the O(−7) summand and E_{N∪ℓ}(8) has
c₁ = c₂ = 0 with a two-dimensional space of sections. A section vanishing on a curve would give a
derivation of N of degree < 8. So some section is nowhere zero and E_{N∪ℓ} ≅ O(−8)². The last
sentence is Theorem 1 of TC_CONTRADICTION with (a₁, a₂) = (7, 8). ∎

*Reading.* Free (8, 8) arrangements with an 8-point line come in families N ∪ ℓ indexed by the
weight-8 lines of a T(−9)-arrangement N. Theorem 17(c) says the lattice has a line with 4, 5 or 8
points; the 8-point case is this one.

## 2. Reformulation through Ziegler pairs

**Proposition 2.1.** The following are equivalent.
- (a) A 17-line counterexample (A₁, A₂) whose lattice has an 8-point line H.
- (b) Two 16-line arrangements N₁, N₂ with the same lattice, b₂ = 72, mdr(N₁) = 8 (so
  E_{N₁} ≅ T(−9)) and mdr(N₂) ≤ 7, together with a line through multiple points of the common
  lattice of total weight 8, realised in both.

*Proof.* (a) ⇒ (b): put Nᵢ = Aᵢ \ H and apply Lemma 1.3 to A₁; since mdr(A₂) = 7 and
D(A₂) ⊆ D(N₂), mdr(N₂) ≤ 7. (b) ⇒ (a): N₁ ∪ ℓ is free by Lemma 1.3. If N₂ ∪ ℓ were free, it
would be free with exponents (8, 8) (b₂ = 80), and Lemma 1.3 would give mdr(N₂) = 8. ∎

Pairs as in (b) are Ziegler pairs (same lattice, different mdr) of a specific kind: the
exponents jump from (8, 8, 8) to (7, 9, 9) at the borderline mdr = (n − 2)/2 of Dimca's
conjecture. The known mechanism for Ziegler pairs (§6) is a singular realisation space.

## 3. Pencil lattices and the first free (8, 8) example

If the lattice has a line H with 4 points of multiplicities m₁, …, m₄, Σ(mᵢ − 1) = 16, then the
other 16 lines fall into four pencils through the four points, and (TC_FILTER Lemma F3) the
lattice is a system linear in the pencil offsets with the cross-ratio of the four centres as the
only non-linear parameter. By Proposition jump4 and Corollary F2, a realisation is free iff the
cross-ratio avoids a finite set S(μ): for (4, 4, 4, 4) the eight roots of
(λ² − 5λ + 1)(λ² − λ + 1)(λ² + 3λ − 3)(3λ² − 3λ − 1), none rational.

**Example 3.1.** Put the centres at (1:0:0), (0:1:0), (1:1:0), (−1:1:0) and take
  A₁ = {z = 0} ∪ {y = az : a = 0, 1, 2, 3} ∪ {x = bz : b = 2, …, 5}
       ∪ {x − y = cz : c = 0, …, 3} ∪ {x + y = dz : d = 3, …, 6}.
This is a sub-arrangement of the B₂ Catalan grid. Exact computation (`work/build/grid17.m2`):
b₂ = 80, points 2²⁴ 3⁸ 4⁸ 5⁴, Jacobian syzygies of degrees 8, 8: **free with exponents
(1, 8, 8)**. It is the first explicit free 17-line arrangement with χ̄ = (t − 8)² in these notes.
But three of its lines carry 9 points, so χ̄(A^H) = t − 8 divides χ̄(A) and the lattice is
divisionally free: every realisation is free. Its realisation space is a single rational point
(`pencil_real2.m2`: dim 0, degree 1, t = −1).

The count behind it: for four pencils of four lines the off-H points satisfy
t₃ + 3t₄ = 32, t₂ = 3t₄, and a pencil line has 13 − 2κ − τ points (κ quadruple, τ triple points
on it), so every pencil line must carry 2κ + τ ≥ 5. The example has (t₃, t₄) = (8, 8) and the
C- and D-lines at the ends of the ranges carry only 2κ + τ = 4.

**Why four-pencil lattices tend to be rigid.** Over ℂ a relation b − a ∈ C with |A| = |B| = |C| = 4
has at most 12 solutions, with equality only for arithmetic progressions with one common
difference, and the four relation types must supply 32 + t₄ solutions in all. Each relation is a
linear condition on 13 normalised offsets (for fixed cross-ratio), so 22 to 32 conditions on 13
unknowns; moduli need incidence theorems, and the near-progression structures that reach the
counts are grids.

## 3b. The equianharmonic four-pencil arrangement E₁₇ (non-free, in the window)

The census over F₁₃ (§5.2) found, for the vector (4, 4, 4, 4), exactly one lattice class, only at the
equianharmonic cross-ratio, and it lifts to characteristic zero: the realisation space over ℚ is
one point of degree 2 with t² − t + 1 = 0 (`pencil_real2.m2`). Solving (`equi_solve.m2`) gives,
with w = e^{iπ/3} (w² − w + 1 = 0), the arrangement

  E₁₇ = {z = 0} ∪ {y = az : a ∈ {0, 1, w − 1, w}} ∪ {x = bz : b ∈ {0, 1, w, 1 − w}}
        ∪ {x + y = cz : c ∈ {0, 1, w, w + 1}} ∪ {x + wy = dz : d ∈ {0, 1, w − 1, w}},

a sub-arrangement of the Eisenstein grid. Verified directly over ℚ(w) (`equi_clean.m2`,
`equi_clean2.m2`):
- 17 lines, points 2²⁴ 3⁸ 4⁸ 5⁴, b₂ = 80, so χ̄ = (t − 8)²; lines with 4, 7 or 8 points; every
  multiplicity ≤ 5: it is in the window of a 17-line counterexample;
- Jacobian syzygies of degrees 7, 10, 10: **nearly free with exponents (7, 10)**, the type the
  non-free member of a 17-line counterexample must have (Theorem 17(a));
- every line has Ziegler exponents (7, 9), so the Bourbaki point P₀ = (1/2 : w/2 : 1) lies on no
  line of E₁₇;
- exactly four lines of the plane have weight ≥ 9: all four have weight 10, pass through P₀, are
  leaves of the minimal foliation, and meet the bound 3r − n = 4 of TC_CONTRADICTION Theorem 1.
  So the residual inflection quartic J′ is the product of the four rich lines.

**E₁₇ ∪ {four rich lines} is the reflection arrangement of G₂₆** (Hesse ∪ dual Hesse): 21 lines,
points 2³⁶ 4⁹ 5¹², b₂ = 111, every line with exactly 8 points (Hirzebruch's property for d = 7),
free with exponents (1, 7, 13), every Ziegler restriction (7, 13). Its degree-7 derivation defines
a reduced convex foliation of degree 7 with these 21 invariant lines; the four rich lines are the
four Hesse lines through one flex, and E₁₇ is A(G₂₆) with those four lines removed. This is
Proposition 5 of TC_CONTRADICTION made concrete: the non-free member is a reduced-convex
arrangement minus leaves, exactly as the 18-line seed is A(6, 1, 3) minus three lines.

The lattice of E₁₇ is rigid (one Galois-conjugate pair over ℚ(√−3)), so Terao's conjecture
holds for it: both realisations are non-free. For a counterexample one would need a deletion
lattice of this kind with a second, free realisation. The same weak combinatorics 2²⁴ 3⁸ 4⁸ 5⁴ is
realised by the free harmonic grid of Example 3.1, so freeness is not a function of the weak
combinatorics in this class either.

**Deletions of the reduced convex arrangements.** Removing four lines from A(G₂₆) (b₂ = 111)
gives b₂ = 80 exactly when one pair of removed lines meets at a double point and the other five
pairs at multiple points; all such 17-line arrangements lie in the window (multiplicities ≤ 5,
lines ≤ 8 points). `g26del.m2` enumerates them and tests freeness by Yoshinaga's criterion on one
line; `fermatdel.m2` does the same for A(6, 1, 3) with the multiplicity bound.

- A(6, 1, 3): 18 four-line deletions have b₂ = 80 and multiplicities ≤ 6; all 18 are non-free
  (`fermatdel.out`). They include the three-coordinate-line deletions (Ceva(6) minus a line) and
  the seed-type ones.
- A(G₂₆): 2,637 four-line deletions have b₂ = 80 (all in the window since the multiplicities are
  ≤ 5); all 2,637 are non-free (`g26del.m2`, 12 minutes). So every 17-line sub-arrangement of the
  two reduced convex arrangements of degree 7 with χ̄ = (t − 8)² is nearly free, never free.
  These 2,655 arrangements fall into 13 lattice classes; their realisation spaces are
  computed in §5.4.

## 4. The known flexible families do not extend

Scripts in `work/build/` (`famtools.m2`, `f13plus4.m2`, `f13rich.m2`, `b18.m2`, `real14.m2`).

- **13-line family (6, 6) plus four lines (Lemma 1.2).** The lines through two unjoined multiple
  points with generic weight exactly 5 are 12: each joins a quintuple point to one of the four
  double points not joined to it. Pairs whose intersection lies on the arrangement: 18 of 66;
  4-cliques: exactly 3, each the four lines through one quintuple point, which then has
  multiplicity 9. No window arrangement.
- **13-line family as the base of a free 18-line (7, 10) arrangement.** This needs a line with 7
  points on F₁₃ (weight 6); the generic weights of the 233 lines through two unjoined multiple
  points are 2 (126), 3 (65), 4 (30), 5 (12). None has weight 6.
- **15-line family (7, 7) plus lines.** Adding two lines is excluded by Lemma 1.1. A free 18-line
  (7, 10) arrangement containing F₁₅ needs an external line with 8 points on F₁₅ (weight 7); there
  is none (`b18.m2`: 0 candidate lines of weight 7 or 8). So A₂ = B \ ℓ cannot come from F₁₅.
- **Deleting a line from F₁₅.** The realisation space of L(F₁₅ \ ℓ) is still a curve (dim 1,
  degree 2) for ℓ with 7 points (5 concurrency conditions) and for ℓ with 6 points (4 conditions),
  and the lost concurrencies hold identically on it. So the deleted line's points stay collinear
  in every realisation: the hidden collinearity is forced, and no Ziegler phenomenon arises.
- **Dual torsion arrangements.** The duals of n-torsion subsets of a plane cubic form families
  over the j-line with constant lattice, but they have only double and triple points, and
  b₂ ≥ n(n − 1)/3 > 80 for 17 lines. A (8, 8) arrangement needs Σ_P C(m_P − 1, 2) = 56.

## 5. Searches

### 5.1 Four-pencil arrangements with integer offsets
`work/build/pencils.c`: pencils A, B, C with integer offsets in [−6, 6] (A, B normalised to
start at 0), the fourth pencil derived from the lines of its direction through at least three
intersection points of the others (necessary for at most 8 points on it); all five 4-point
multiplicity vectors, all orderings of the sizes, and the cross-ratios −1, 2, 1/2, 3, 1/3, −2,
4, 5, 5/2, 7/2, 7/3, 6. Output: configurations with b₂ = 80 and 4 to 8 points on every line.
Validated on Example 3.1 with the point bound relaxed to 9.

**Result.** 420 runs, 12.2 million derived-pencil choices for (4, 4, 4, 4) alone: **no configuration**
with b₂ = 80 and every line carrying 4 to 8 points (`pencil_runs/log.txt`). With the bound relaxed to
9 points the harmonic grids of Example 3.1 appear, as they must.

### 5.2 Complete census over F₁₁ and F₁₃
`work/build/pencils_fp.c`: the same with offsets in F_p, normalised a₀ = 0, a₁ = 1, b₀ = 0, so
every configuration over F_p is found once per affine class, for every cross-ratio class
(representatives of the anharmonic orbits: for p = 13 the harmonic orbit, the equianharmonic
orbit and one orbit of size 6). Over F₇ the field is too small (83,832 hits for (4, 4, 4, 4),
all forced coincidences).

**Result.** For (4, 4, 4, 4) over F₁₁: nothing in any cross-ratio class. Over F₁₃: nothing in the
harmonic class and nothing in the generic class of size 6, and **24 configurations in the
equianharmonic class**, forming a single lattice (§3b). For the other four vectors ((5, 5, 5, 1), (5, 5, 3, 3), (5, 4, 4, 3), (5, 5, 4, 2)), in every
ordering and every cross-ratio class, over F₁₁ and F₁₃: nothing. All 175 runs are complete
(`fp_runs/log.txt`). **So over F₁₁ and F₁₃ the only 17-line window arrangements with a 4-point line
are E₁₇ and its conjugate.**

### 5.3 Exact lifting
`work/build/pencil_post_fp.py` groups the hits by lattice isomorphism class (nauty on the
line–point graph) and `pencil_real2.m2` computes, for each class, the realisation space over ℚ
of the four-pencil lattice: unknown offsets and cross-ratio t, the concurrency equations,
saturation by the degeneracies, minimal primes, and on each component whether t is constant and
whether extra incidences hold identically (coarser lattice).

**Result.** The 236 lattice classes found over F₇ are all non-realisable over ℚ̄ (`fp7_lift.txt`):
pure characteristic-7 artefacts. The single F₁₃ class lifts to E₁₇, rigid, with t² − t + 1 = 0.

### 5.4 Sub-arrangements of the reduced convex arrangements
`delclasses.py` groups the 2,655 window deletions of §3b into **13 lattice classes** (12 from
A(G₂₆), 1 from A(6, 1, 3), the latter being Ceva(6) minus a line; E₁₇'s class has 9 members, the
nine flexes). `work/tc15/exact_tc_lattice.py` (the pipeline of the 15- and 16-line proofs:
frame, greedy parametrisation, minimal primes, Yoshinaga's matrix on each component) gives for
every one of the 13 classes: exactly one non-degenerate component, of dimension 0 and degree 2,
on which the Yoshinaga matrix has rank 15 of 16 (`del17_tc_0.out`, `del17_tc_1.out`). So all 13
lattices are rigid, realised only by a conjugate pair over ℚ(√−3), both members nearly free.
**Terao's conjecture holds for every 17-line sub-arrangement of A(G₂₆) and A(6, 1, 3) with
χ̄ = (t − 8)².**

### 5.5 Five-point lines (five pencils, two cross-ratios)

`work/build/pencils5x.c` enumerates every 17-line arrangement over F_p made of a line H = {z = 0}
with five points and the five pencils through them, for each of the eleven multiplicity vectors of
a 5-point line (partitions of 16 into five parts ≤ 5):
- the points of H are put at (1:0:0), (0:1:0), (1:1:0), (λ₁:1:0), (λ₂:1:0), with (λ₁, λ₂) running
  over all ordered pairs of distinct elements of F_p ∖ {0, 1}, so every configuration of five
  points on H is covered;
- four pencils are enumerated over all of F_p, normalised by the affine group fixing H pointwise
  (two offsets of the first pencil set to 0 and 1, one of the second to 0); the largest pencil is
  derived, its lines being those whose excess Σ(m_R − 2) over the other pencils' points lies in the
  window;
- b₂ is checked arithmetically before any line check: adding a derived line d changes b₂ by
  (number of enumerated lines) − ex(d), so the derived lines must have excesses summing to a known
  target;
- every line must carry 5 to 8 points (lattices with a 4-point line were covered by §5.2 at the
  same primes), multiplicities are at most 6 automatically, and b₂ = 80.

**Validation.** Two window deletions of A(G₂₆) have a 5-point line with every other line carrying
7 or 8 points, with H-vectors (4, 4, 3, 3, 2) and (4, 4, 4, 3, 1). Reduced mod 13
(w = 4), their census coordinates are λ = (4, 6) or (10, 8), and λ = (4, 10), …
(`mk_test5.py`). The enumerator finds them with exactly 36 = 4·3·3 and 48 = 4·3·4 hits, the number
of normalisations of each, at 0.33 µs per configuration.

**Run.** All eleven vectors, p = 11 and p = 13, 220 jobs, 4.4 · 10¹⁰ configurations.

**Two rational nearly free arrangements (found at p = 11, lifted exactly).** In the line
coordinates dq·x − dp·y = v·z for the pencil of direction (dp : dq : 0):
- R₁₇ᵃ: H = {z = 0}; y = −a (a = 0, 1, 2, 3); x = 0, 2, 4; x − y = 2, 3, 5; 3x − 4y = 12;
  x − 2y = 2, 4, 5, 6, 8. H-vector (5, 4, 3, 3, 1), cross-ratios (4/3, 2).
  Points 2²³ 3¹⁰ 4⁸ 5² 6¹.
- R₁₇ᵇ: H = {z = 0}; y = −a (a = 0, …, 4); x = 0, 1, 2, 4; x − y = 4; 2x + y = 2;
  x + y = −2, −1, 0, 1, 2. H-vector (5, 5, 4, 1, 1), cross-ratios (−1/2, −1).
  Points 2²⁰ 3¹⁸ 4² 5² 6².

Both have b₂ = 80, lines with 5 to 8 points and multiplicities ≤ 6, so both are in the window. Both
are **nearly free with exponents (7, 10)** (syzygies 7, 10, 10) with one Bourbaki point
(`c5rational.m2`). Each realisation space is one rational point (`exact_tc_lattice.py`: dim 0,
degree 1, Yoshinaga rank 15/16), so Terao's conjecture holds for both lattices.

Unlike E₁₇ they have only **two** rich lines, crossing at the Bourbaki point. The residual
inflection quartic is J′ = (rich line)·(rich line)·(smooth conic over ℚ) (`c5jprime.m2`):
- R₁₇ᵃ: (x − 4y − 8z)(x − y − 4z)(2x² − 2xy + 2y² − 11xz + 10yz + 20z²);
- R₁₇ᵇ: (x − 3z)(x + 2y + 2z)(x² + xy + y² − 2xz + 2yz + 2z²).

Sing J′ has length 5 and contains the Bourbaki point, as the scheme lemma requires. The conic
passes through no intersection point and is tangent to no line of the arrangement (`c5conic.m2`).
So the extremal case of TC_CONTRADICTION Proposition 5 (J′ a product of rich lines) is not forced:
non-free window arrangements with a conic in J′ exist. They are rigid here.

**Result (complete, 220 jobs, 2,222 cross-ratio pairs, 4.36 · 10¹⁰ configurations, 1,304 hits).**
`census5_post.py` groups the hits into **6 lattice classes**. `exact_tc_lattice.py` decides each one
over ℚ̄ (`census5_lift.txt`):

| class | H-vector | primes | points | realisation space over ℚ̄ | freeness |
|---|---|---|---|---|---|
| 0 = R₁₇ᵃ | (5, 4, 3, 3, 1) | 11, 13 | 2²³ 3¹⁰ 4⁸ 5² 6¹ | one rational point | nearly free (7, 10) |
| 1 | (4, 4, 3, 3, 2) | 13 | 2²³ 3⁵ 4¹³ 5² | conjugate pair over ℚ(√−3) | nearly free (7, 10) |
| 2 | (4, 4, 4, 3, 1) | 13 | 2²⁴ 3⁸ 4⁸ 5⁴ | conjugate pair over ℚ(√−3) | nearly free (7, 10) |
| 3 | (5, 5, 4, 1, 1) | 11 | 2³⁰ 3⁶ 4⁸ 5¹ 6² | none (ideal (1)) | – |
| 4 = R₁₇ᵇ | (5, 5, 4, 1, 1) | 11, 13 | 2²⁰ 3¹⁸ 4² 5² 6² | one rational point | nearly free (7, 10) |
| 5 | (5, 5, 4, 1, 1) | 11 | 2³⁰ 3⁶ 4⁸ 5¹ 6² | none (ideal (1)) | – |

Classes 1 and 2 are the two validation lattices (window deletions of A(G₂₆)). They appear at
p = 13 ≡ 1 (mod 3) and not at p = 11, as a ℚ(√−3)-lattice must. Classes 3 and 5 are
characteristic-11 artefacts. Every realisable class is rigid and non-free, and nothing free was
found.

**Positive characteristic** (TC_CHARP.md §4, `work/charp17/`). The lifting above decides freeness
over ℚ̄. Freeness was then decided directly in characteristic p as well:
- all 1,328 F_p-hits of §5.2 and §5.5 are nearly free (7, 10) over their own field, including the
  hits of the characteristic-11 classes 3 and 5;
- the realisation spaces of the seven census lattices over F̄₁₁ and F̄₁₃ are finite, and every point
  is nearly free (7, 10);
- each of the 236 F₇ lattices of §5.3 is realised over F̄₇ by its F₇-point alone, which is nearly
  free.

So no census lattice is a counterexample in characteristic 7, 11 or 13 either.

**Conclusion of §5.2 and §5.5 together.** Over F₁₁ and F₁₃, every 17-line arrangement in the
window of class (8, 8)[B] whose smallest line has 4 or 5 points is one of six arrangements, up to
conjugation:
- E₁₇;
- R₁₇ᵃ and R₁₇ᵇ;
- the two 5-point-line deletions of A(G₂₆).

All six are nearly free with exponents (7, 10) and rigid. So a 17-line counterexample whose lattice
has a 4- or 5-point line can only exist if that lattice has no realisation over any field with a
degree-1 prime above 11 or 13 (or degenerates there). Moreover, no free (8, 8) window arrangement
of this shape exists over these two fields at all. This is a search, not a proof: number fields in
which neither 11 nor 13 splits are not covered. Q(√2) is the smallest example. Covering it would
need p = 17, which costs about 90 CPU-hours (estimate in §5.5).

The remaining part of class (8, 8)[B] is lattices whose smallest line has 8 points. By Lemma 1.3 a
free member then comes from a T(−9)-arrangement N of 16 lines plus a weight-8 line, so the
natural next search is over 16-line arrangements with logarithmic bundle T(−9).

## 6. The mechanism in the literature

Barakat–Kühne–Pokora (arXiv:2407.07070) construct Ziegler pairs from (3, 12)-matroids with
singular realisation spaces: for their matroid M₁ the realisation space is the union of two
surfaces meeting along a conic, mdr = 8 on both surfaces and 7 on the conic, where a hidden
collinearity holds. Their second example has three curves through a point. Abe–Kühne–Pokora
(arXiv:2509.19011) show that adding generic lines preserves Ziegler pairs. Their 13-line
"numerical Terao" pair has different lattices and is not relevant here.

So the structure to look for is a lattice L with χ̄ = (t − 8)² whose realisation space is
singular, free away from the singular locus and non-free on it. By TC_RIGIDITY Lemma 3 the jump
function of every line vanishes to order ≥ 2 along each branch there, which is consistent with a
crossing of branches. None of the lattices examined here has a singular realisation space.

## 7. Files

`work/build/`: `famtools.m2`, `f13plus4.m2`, `f13rich.m2`, `b18.m2`, `real14.m2`, `grid17.m2`,
`pencils.c`, `pencils_fp.c`, `pencil_post.py`, `pencil_post_fp.py`, `pencil_real2.m2`,
`mkclass_z.py`, run outputs in `pencil_runs/` and `fp_runs/`, class files in `fp_classes/`.
