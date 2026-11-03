# Closing n = 17: the Riemann–Roch obstruction, the covering lemma and the cores (21 Oct 2026)

Continues `TC_CHAINS17.md`. Setting: a 17-line counterexample (A₁ free (8, 8), A₂ nearly free
(7, 10)) has a lattice L in the window (m ≤ 6, 4 to 8 points per line, (W5), at most four unjoined
pairs with σ = 8). E = E_{A₂∖S}; for a set S of k lines deleted one at a time,
Σc(S) = Σ_{H∈S} s_H − f(S), where f(S) is the number of points all of whose lines lie in S, and
b₂(L ∖ S) = 80 − Σc(S). For S ⊂ L put φ(S) = Σ_{H∈S}(s_H − 7) − f(S), so Σc(S) = 7k + φ(S).

## 1. Theorems (proved)

**Lemma A′.** mdr(A₂ ∖ S) ≥ min(7, 10 − |S|). (As Lemma A of `TC_CHAINS17.md`: α_S·φ ∈ D(A₂)
of degree ≤ 9 is gE + qθ₀ with α_H | q for every H ∈ S, and deg q = deg φ + |S| − 7.)

**Theorem 1 (Riemann–Roch obstruction).** For every set S of 4 ≤ k ≤ 9 lines,
Σc(S) ≤ 7k + 4, i.e. φ(S) ≤ 4.

*Proof.* e₀ = 10 − k ≤ mdr(A₂ ∖ S). c₁(E(e₀)) = 4 − k, c₂(E(e₀)) = 4 + 7k − Σc(S) =: δ, and
χ(E(e₀)) = ½(4 − k)(7 − k) + 2 − δ. If δ < 0: for k ≤ 6, h² = h⁰(E(3)) = 0 and h⁰(E(e₀)) ≥ χ ≥ 1;
for k = 7, h² = h⁰ and 2h⁰ − h¹ = χ ≥ 3; for k = 8, 9 a would-be vanishing of h⁰(E(e₀)) forces
≥ 4 (resp. 7) pairwise dependent sections of E(3), hence a section of E(e₀ − 1), against Lemma A′.
So E(e₀) has a section; it cannot vanish on a curve (Lemma A′), so its zero scheme has length
δ < 0, which is impossible. ∎

**Theorem 2 (free cores).** If φ(S) = 4 (4 ≤ k ≤ 9) then A₂ ∖ S is free with exponents (10 − k, 6)
(same computation with δ = 0: the section vanishes nowhere and E(e₀) ≅ O ⊕ O(4 − k)), hence
A₁ ∖ S is free too (TC for ≤ 13 lines) and L ∖ S is a free lattice.

**Corollary 3 (minimal free cores are 4-chains).** If φ(S) = 4 with |S| ≥ 5, some line of S carries a
full point of S; removing a line carrying exactly one keeps φ = 4, removing one carrying ≥ 2 would give
φ ≥ 5 (Theorem 1), and removing a line with s ≤ 6, or a 7-line with a full point, also gives φ ≥ 5.
Descending, one reaches |S| = 4: a 4-chain. So **L has a set with φ = 4 iff L has a 4-chain**, and
by Theorem 1 no set of ≤ 9 lines has φ ≥ 5 (in particular no 5-chain).

**Theorem 4 (nearly free cores).** If |S| = 4 and φ(S) = 3, A₂ ∖ S is nearly free with exponents
(6, 7) (δ = 1, χ = 1, h² = 0). (Also |S| = 7, 8, 9 with φ = 3: nearly free (3,7), (2,7), (1,7).)

**Lemma 5 (cores determine realisations).** If every deleted line of S passes, at its deletion,
through two multiple points of the remaining arrangement (true whenever its deletion count c and
position i satisfy i + c ≤ 12, by m ≤ 6; in particular for chains and for 4-sets of lines with ≥ 7
points), then restriction R(L) → R(L ∖ S) is injective with Galois-stable image. Hence **if R(L ∖ S)
is a single Galois orbit, all realisations of L are conjugate and Terao's conjecture holds for L.**

Checks: Theorem 1 holds in all 19 known window classes (max φ = 4 for every subset size;
`work/chains17/phimax.py`); Theorems 2 and 4 were checked on E₁₇, R₁₇ᵃ (`TC_CHAINS17.md` §3).

## 2. Measurements (`work/n17/`)

- **Brute force is out of reach.** Heavy configurations of the (17; 8, 8) window with (W5) and the
  D-pair bound: about 1.7·10⁹ (3 of 1000 residues at depth 8: 1.2–2.1·10⁶ each, 70–100 s each).
  Their completion by triple points (`lsgen3`) is cheap in some subtrees (0.7 ms per configuration)
  but in an unbiased residue gives ~130 complete lattices *without a 3-chain* per heavy configuration
  and ~0.4 s per configuration: of the order of 10¹¹ lattices and years of CPU.
- **Core classes are small.** All 13-line lattices with m ≤ 6, 3–8 points per line (3–7 for b₂ = 48:
  these cores are free with exponents (6, 6) by Theorem 2, so no line has more than 7 points):
  b₂ = 48: 21,164 classes (213,339 raw), screened: 195 to Macaulay2;
  b₂ = 49: 154,172 classes (1.82 M raw), 2,950 to Macaulay2;
  b₂ = 50: 12.3 M raw; b₂ = 51: 65.7 M raw (40 s and 200 s to generate).
  14-line lattices with b₂ = 56 (cores of 3-chains): 18.9 M raw, 80 s.
- **Coverage in samples.** In 1,109 complete lattices from one subtree: 849 have a 4-chain,
  120 violate Theorem 1, 140 have no 4-chain but a 4-set with φ = 3. In 2,000 lattices without a
  3-chain from an unbiased residue, every one has 4 lines whose deletion leaves a 13-line core with
  b₂ = 50 (1,963) or 51 (37).

## 3. The plan (carried out in §4–§9)

1. Screen the 13-line classes b₂ = 48, …, 51 (≈ 7 M distinct lattices) with the exact filters and
   Macaulay2; keep the realisable ones and the structure of their realisation spaces.
2. For every realisable core whose realisation space is not one Galois orbit, enumerate its
   extensions by four lines into the 17-line window and decide freeness (Lemma 5 disposes of the
   others).
3. **Covering lemma — proved 21 Oct 2026 (computer-assisted, §4).** Every window lattice with an
   8-point line has four lines S with φ(S) ≥ 1, i.e. Σc(S) ≥ 29 (core b₂ ≤ 51).

## 4. The covering lemma

**Lemma 6 (covering).** Let L be a lattice of the window (17 lines, m ≤ 6, 4 ≤ s_H ≤ 8, X = 56) in which
every 8-point line has a double point (Lemma A2 of `TC_GLOBAL.md`). If L has an 8-point line, some set S
of four lines has φ(S) ≥ 1.

*Proof.* Put δ_H = 8 − s_H and Δ = Σ δ_H = 32 − W, so φ(S) = 4 − Σ_S δ − f(S). From t₂ = 3W − 32 − t₅ − 3t₆
≥ 0 we get W ≥ 11, Δ ≤ 21 and t₂ ≤ 64 − 3Δ − t₅ − 3t₆. Suppose every S has φ(S) ≤ 0 and fix an
8-point line H₀ with points P₁, …, P₈, k_i = m_{P_i} − 1, and G_i the k_i other lines through P_i. Every
other line lies in exactly one G_i. For S = {H₀, A, B, C} the full points are: P_i if G_i ⊆ {A, B, C};
a point off H₀ carrying exactly two or exactly three of A, B, C. So the hypothesis gives, for every
three lines A, B, C ≠ H₀,

  δ_A + δ_B + δ_C + Σ_i [G_i ⊆ {A,B,C}] + e_AB + e_AC + e_BC + τ_ABC ≥ 4,

where e_XY = 1 if X ∩ Y is a double point and τ_ABC = 1 if A, B, C meet in a point carrying only them.
Each line X with s = 8 − δ points through P_i has b′ double points off H₀ with
2s − 18 + k_i ≤ b′ ≤ ⌊(5s − 21 + k_i)/4⌋ (from Σ_{P∈X}(m_P − 1) = 16, m ≤ 6), b′ ≤ s − 3 + [k_i ≥ 2] (two
points of multiplicity ≥ 3, Lemma C), and b′ ≥ 1 if s = 8 and k_i ≥ 2; globally Δ ≤ 32 − max(11, W(H₀))
and t₂ = b₀ + Σ e ≤ 64 − 3Δ − t₅(H₀) − 3t₆(H₀). These are linear conditions in 0/1 variables
(`work/n17/cover/ilp/gamma_ilp.py`). For each of the 14 vectors k of H₀:
1. *δ-assignments* (`level1.py`): up to the symmetries (lines inside a G_i, the G_i of equal size),
   the assignments of δ satisfying the conditions that involve δ alone and two aggregated consequences
   (summing the displayed inequality over C for the two shortest lines A, B of a heavy G_i, and over C
   for the two lines of a triple point) — 2,471 assignments survive, all with Δ ≥ 16;
2. *double and triple points* (`farkas.py`): for each surviving assignment the remaining problem in e, τ
   has an infeasible LP relaxation. The Farkas multipliers y are read from the phase-1 duals of GLPK and
   the certificate Σ_j max(0, Σ_i y_i c_ij) < Σ_i y_i b_i is **verified in exact rational arithmetic**:
   2,471 of 2,471 certified. ∎

**Validation.** The model was evaluated on real lattices: for 609 eight-point lines of 299 lattices with
φ_max = 1, at their own threshold (φ ≤ 1 instead of ≤ 0) every constraint holds, every assignment is a
level-1 survivor, and the level-2 problem is reported feasible (40 of 40 tested); in 1.3 M complete
lattices from 20,011 random heavy configurations (and 290,618 more from one residue), every lattice with
an 8-point line has φ_max ≥ 1, and φ_max = 1 occurs only for 1 ≤ n₈ ≤ 3 (W between 13 and 17).

So a counterexample lattice either has **no 8-point line** (then W ≤ 15, and W ≤ 13 if it is not in the
finished part [A]), or has a 4-set S with φ(S) = φ_max(L) ∈ {1, 2, 3, 4} and its core L ∖ S lies in one of
the 13-line classes b₂ = 52 − φ_max: 21,164 (b₂ = 48, lines with at most 7 points, Theorem 2), 154,172 (49),
738,023 (50), 2,916,332 (51) lattices up to isomorphism (`work/n17/cores*/`). The enumeration (`heavyaug_p`)
also discards cores with two points of multiplicities {6, 5} or {6, 6} not joined by a line: a 6-fold point
of a core lies on no deleted line (it would become 7-fold), so such a pair is not joined in L either and
violates (W5) there. Without this cut, an independent enumeration (`bigblocks.py` + `fill_triples.py`)
gives the same four classes plus exactly 7 such lattices of b₂ = 51 (audit, 22 Oct).

## 5. The extension step (exact), and its validation

For a core B = L ∖ S, every realisation of L restricts to a realisation of B, and every line of S is,
at its turn, a line through two multiple points of the arrangement built so far (Lemma 5: c_i + i ≤ 12
for every order). So all window lattices L over B are found by adding four such lines to the
realisations of B. Combinatorial extension is hopeless (more than 2·10⁵ window lattices over one core),
so the extension is geometric:

- **Components** (`work/n17/comp/m2comp.py`, Macaulay2): the realisation space of each deferred core
  (minimal primes, degenerate ones removed), with a shape-lemma representation of every
  0-dimensional component (u_i = g_i(T), f(T) = 0). Median 0.5 s per core.
- **Rigid search** (`extend.py`): the realisation rebuilt exactly over ℚ[T]/(f); every incidence is
  decided exactly (a value is nonzero if its image at a simple root of f mod a 30-bit prime is nonzero,
  and is otherwise checked exactly; no division is ever made). All ways of adding four lines through two
  multiple points each, with the right total point count, every line ending with 4–8 points and every
  point with multiplicity ≤ 6; then the window conditions on L. About 60 ms per component.
- **Families** (`famext.py`, `famrun.py`, `famspecial2.py`): for a 1-dimensional component C, a plane
  model F(T, Y) = 0 (Macaulay2); the same search run symbolically on C, with "g vanishes on C" decided
  by Res_Y(F, g) = 0; every test that is not identically true can change the search only at the roots of
  its resultant, and only roots at which the extra incidences bring a candidate line into the admissible
  range are kept (or any root, for lines already admissible); Macaulay2 computes the points of C over
  these factors, and the rigid search is run at each of them. 3–30 s per component.
- **Verification of every L found**: `work/tc15/exact_tc_lattice.py` (n = 17, d₁ = 8) on the lattice L
  itself — its full realisation space over ℚ and freeness on every component.

**Validation.** (1) From the 28 cores of the known window lattices (`work/chains17/cores13.jsonl`) the
rigid search rediscovers every realisable source lattice (24 of 24; the 4 cores of the characteristic-11
artefact class 3, which is not realisable over ℂ, correctly give nothing) and finds two more window
lattices, both rigid, rational and non-free (TC holds for them). (2) On five 1-parameter families the
family search with the relevance filter switched off (4–10 times more special points) finds exactly the
same lattices.

**Generic behaviour of families.** At a random point of each of the 53 family components of the b₂ = 48
and 49 classes there is no extension at all; most of them do have generic search nodes at depth 1–3,
which is why the special points of every node are needed.

## 6. No 8-point line

If L has no 8-point line, Σ_H (7 − s_H) = 15 − W ≤ 4. Lattices with all lines of 6 or 7 points are the
finished part [A]. Otherwise:

- **A 4-point line H₀** forces W ≤ 12, and the vector of H₀ must have Σ C(k − 1, 2) ≤ 12, which leaves
  only (4, 4, 4, 4): then W = 12, there is no other heavy point, t₂ = 0 and the other 16 lines all have
  7 points, so the lines off H₀ meet in 32 triple points forming a triangle decomposition of K_{4,4,4,4}.
  There are 23 such lattices up to isomorphism (`work/n17/n8zero/k4444.py`, exact cover); none is
  realisable over ℂ (9 by the fast filters, 14 by Macaulay2). **So no counterexample lattice without an
  8-point line has a 4-point line.**
- **A 5-point line H₀ and no 4-point line.** A line X through the point of H₀ with k other lines satisfies
  Σ_{off-H₀ points P on X}(m_P − 3) = 18 − k − 2 s_X ≥ 4 − k, and only heavy points off H₀ contribute
  positively; with W_off = W − W(H₀) ≤ 13 − W(H₀) this excludes the vectors 55411, 55321, 55222, 54421,
  54331 and 54322 of H₀ outright; the exhaustive run of `pencil5c.py` on all eleven vectors (`p5excl.py`,
  23 Oct) confirms that these six have no quota system at all. For the other five vectors the lattices are
  enumerated exactly (`pencil5c.py`): heavy points off H₀ up to isomorphisms fixing H₀ (level-wise nauty
  rejection with H₀ in a cell of its own), line lengths with Σ(7 − s) = 13 − W, and
  for every line the number of triple and double points it carries is then determined
  (tr = 16 − k − h − Σ(m − 3) − (s − 1), db = (s − 1) − h − tr), so the remaining pairs are an exact cover
  with per-line quotas. (The first version, `pencil5b.py`, deduplicated the heavy configurations with
  canonical forms in which H₀ was not distinguished; for 43333 this merged 20 classes, with no lattice lost:
  the lattice sets of the two versions are identical. Audit F1, `work/n17/audit/AUDIT.md`.)

  | vector of H₀ | heavy classes | lattices | deferred by fast filters | realisable over ℂ |
  |---|---|---|---|---|
  | 53332 | 2,303 | 0 | – | – |
  | 44431 | 87 | 122 | 71 (with 44422) | 0 |
  | 44422 | 863 | 232 | | 0 |
  | 44332 | 49,565 | 3,124 | 464 | 0 |
  | 43333 | 192,133 | 7,723 | 355 | 0 |

**So every counterexample lattice has an 8-point line** (with part [A], 1.96 M lattices, and the
23 + 11,201 lattices above, none realisable).

## 7. The core computation (final state, 21 Oct 2026)

| class (b₂ of core) | cores | deferred by fast filters | realisable (Macaulay2) | rigid / curve / surface+ components | extension |
|---|---|---|---|---|---|
| 48 (4-chain) | 21,164 | 195 | 85 | 80 / 5 / 0 | **done**: the 16 lattices of §9 |
| 49 (φ = 3) | 154,172 | 2,950 | 1,147 | 1,050 / 83 / 14 | **done**: no window lattice beyond those of b₂ = 48 (surfaces and one slow family via the lattice-level step) |
| 50 (φ = 2) | 738,023 | 26,093 | 9,162 | 7,985 / 1,091 / 86 cores | **done: no window lattice** (all levels to 16 lines; 102 slow families via the lattice-level step) |
| 51 (φ = 1) | 2,916,332 | 157,533 | 58,871 | 49,118 / 9,001 / 752 cores | **done: no window lattice** (all levels to 15 lines; 2 Macaulay2 timeouts settled by their children) |

(No Macaulay2 timeout or error among the 186,771 deferred cores.) Positive checks of the filters and
the class enumeration: the 28 cores of the known lattices and all 33 φ-max cores of the 16 lattices
found lie in the b₂ = 48 class and survive the fast filters. All 16 lattices found have a 4-chain.

Distinct 17-line window lattices found: 16 (14 known: ten deletions of A(G₂₆), four census
classes; 2 new). All 16 are rigid, a single Galois orbit, and **non-free**; no free realisation of any
window lattice has appeared. Surfaces of realisations (dim ≥ 2) are handled by a lattice-level step:
all 14-line lattices B + N are generated (N through ≥ 2 multiple points, budget and line lengths
respected), screened by the fast filters and Macaulay2, and their components passed back to the
rigid / curve / surface machinery (`dim2gen.py`, `runclass.py`). The pruning by φ is monotone (point
counts only grow and full points only disappear when lines are added), so a partial arrangement with
a 4-set of φ above the class value is dropped: the lattice is reached from a lower class (checked on one
example: the lattice dropped from the b₂ = 49 family b49:9241 is found from the b₂ = 48 class).

**Corrections made during the run (21 Oct, 11:25).**
1. *Family realisation.* The symbolic realisation on a curve (`famext.realise_sym`) rescaled intermediate
   vectors, but the parametrisation statements P_e = P_a + u_i·P_b are not projectively invariant. Six
   14-line families were flagged by the built-in check that the realisation reproduces the lattice
   (`LATTICE-MISMATCH`); the error could also have gone undetected for other families. Fixed by carrying
   every vector as N/D exactly (only the final normals are used projectively, with the zeros of D added to
   the special points). **All family runs are redone with the fixed code**; the rigid search
   (`extend.py`) was never affected (it rebuilds Macaulay2's vectors exactly).
2. *Plane models* of curves that are irreducible over ℚ but split over ℚ(ω) were not found when the lex
   basis element for u_i still involves later variables; fallback: eliminate the other parameters first.
   Also, the coefficient of u_i is now taken as ∂g/∂u_i (it may depend on T, Y); the earlier version
   failed loudly in that case (an exception, never a silent result).
3. *Memoisation of visited line sets* in the rigid search used mod-p hashes; now a hash collision between
   distinct lines (probability ~10⁻¹⁸ per pair, none observed) disables memoisation for that line. The
   rigid runs made before this change were repeated at the end (`work/n17/run/rerun/`): no collision, and
   the same lattices (`rerun/compare.out`).

## 8. The theorem being proved, and the chain of the proof

**Theorem (computer-assisted, 21 Oct 2026).** Terao's conjecture holds for every arrangement of 17
lines in ℙ²_ℂ; hence (with n ≤ 16) for every arrangement of at most 17 lines.

1. *Reduction* (earlier work). Only the class (17; 8, 8)[B] can contain a counterexample: A₁ free with
   exponents (8, 8), A₂ nearly free with exponents (7, 10), on a lattice with m ≤ 6, every line with 4
   to 8 points, X = 56, the unjoined-pair rule (W5), at most four D-pairs, and every 8-point line with a
   double point (Anghel–Stan's numerical reduction; `TC_FOLIATION.md` Thm 5.1 for (7, 9) and mdr 6;
   du Plessis–Wall; Dimca–Ibadula–Măcinic Prop 4.7; Abe 2014 Cor 1.2(2); `TC_CONTRADICTION.md` §5;
   `TC_GLOBAL.md` Lemma A2). Lattices with all lines of 6 or 7 points: none realisable (Thm 10.5 of
   `TC_ATTEMPT.md`; re-screened on 22 Oct with the corrected resultant filter: same lattices, same set sent
   to Macaulay2).
2. *No 8-point line* (§6): no realisable lattice.
3. *Riemann–Roch bound* (§1, Thm 1 with k = 4, Lemma A′): every 4-set has φ ≤ 4.
4. *Covering* (§4, Lemma 6): with an 8-point line, φ_max ∈ {1, 2, 3, 4}; the core L ∖ S of a 4-set with
   φ(S) = φ_max lies in the 13-line class b₂ = 52 − φ_max (enumerated completely).
5. *Cores* (§7): fast filters, then Macaulay2 components of every surviving core.
6. *Extension* (§5): every realisation of L restricts to a point of a component of the core; rigid
   components (exact search), curves (exact search on the curve plus its special points), surfaces and
   higher (one line added at the lattice level, children screened exactly, recursively). Monotone φ
   pruning: a lattice is pursued only in its own class.
7. *Check*: every window lattice found is decided exactly (realisation space over ℚ, freeness on each
   component).

## 9. Result (21 Oct 2026, 20:00)

All runs finished. Over the four core classes, every realisable core, every component (rigid, curve,
surface and higher, through 13 → 14 → 15 → 16 → 17 lines) and every slow or failed case (297 family
components and 2 Macaulay2 timeouts, all routed through the lattice-level step) was processed; the audit
(`work/n17/run/audit.py`) finds no unrouted failure, no rigid component without exact realisation and no
special point skipped. Collecting the window lattices produced by all 161 output files
(`work/n17/run/final_files.txt`, `final_collect.txt`) gives **exactly 16 lattices up to isomorphism**:
the 14 previously known realisable window lattices (deletions of A(G₂₆) and the rational arrangements
R₁₇ᵃ, R₁₇ᵇ of the finite-field census) and two new ones. Each was decided
exactly (`checked_L.jsonl`): one Galois orbit of realisations, rigid, **non-free**. So no window lattice
has a free realisation, and no 17-line lattice carries a free and a non-free realisation.

| class | realisable window lattices found in the class |
|---|---|
| b₂ = 48 (4-chain) | 16 (all of them) |
| b₂ = 49 | 0 beyond those (every lattice reached there has a 4-chain) |
| b₂ = 50 | 0 |
| b₂ = 51 | 0 |
| no 8-point line | 0 |

Every realisable lattice in the window has a 4-chain. In particular there is **no free arrangement of
17 lines with exponents (8, 8), m ≤ 6 and 4 to 8 points on every line**.

**What the proof rests on.** (i) The earlier reduction to the class (8, 8)[B] (§8 step 1) and the
part-[A] enumeration; (ii) the theorems of §1 and the covering lemma of §4 (exact Farkas certificates);
(iii) the enumerators (`heavyaug`/`lsgen3` of Anghel–Stan with our window constraints, `pencil5c.py`,
`k4444.py`); (iv) the corrected fast filters of the 15/16-line work for every NONREAL verdict;
(v) Macaulay2 (minimal primes over ℚ) for every realisation space; (vi) the exact extension code of §5.
Validation: the known window lattices and their cores are rediscovered and pass every filter; the family
method agrees with its unfiltered version; the pruned lattices of a class are found in the lower class.
**Audit (21–23 Oct 2026, `work/n17/audit/AUDIT.md`).** The proof was rerun and checked on all cores. The
core classes were re-enumerated by an independent enumerator (identical); every core and child verdict
was re-decided by the independent exact code of Anghel–Stan, with Macaulay2 where that code is undecided
(no disagreement among 4.37 M lattices); the rigid extension was rerun with exact memoisation and checked
component by component against an independent numeric re-implementation (identical on 99,449
components); every family component was settled again (directly, or through the lattice-level step);
part [A] was re-screened with the corrected filter (identical). Every 17-line lattice found is one of the
16, and **no lattice found is ever rejected by the window conditions (W4)–(W6)**, so the computation does
not depend on them (in particular not on the D-pair bound). Defects found: `pencil5b.py` (H₀ not fixed,
no lattice lost), `p5excl.py` (the cited check had not been run; it has now), inexact memoisation in
`extend.py` and unrecorded worker failures in `runclass.py` (both fixed; no effect).

What is still not duplicated by independent code: the family search over function fields and the
Macaulay2 computations themselves. The code, the logs, the extension outputs and
the Macaulay2 records of every deferred core and child (`work/n17/results/`) are committed; the large
regenerable intermediates (9.3 GB) are not, and `work/n17/MANIFEST.md` lists them with their SHA-256 and
says how each step was run.

