# After Anghel–Stan: what their 15/16-line reduction gives at 17 lines, combined with our results

Started 20 Oct 2026. Anghel–Stan, *Terao's freeness conjecture for arrangements of 15 and 16
lines*, [arXiv:2610.25868](https://arxiv.org/abs/2610.25868) (19 Oct 2026), prove TC for 15 and
16 lines over ℂ by (i) a numerical reduction and (ii) an enumeration of the residual matroids with
exact realisation spaces. Their result coincides with our Theorems 10.1–10.4 of `TC_ATTEMPT.md`
(also by enumeration); their reduction is cleaner than ours and their code is published as
ancillary files (`heavyaug.c`, `lsgen3.c`, exact screening in python-flint). This file records
what their method gives at 17 lines once it is combined with the structure we have established
for the open class, and what was computed.

## 1. Their reduction, stated once

For a Terao counterexample L of d lines of type (d; d₁, d₂) (χ₀ = (t − d₁)(t − d₂), d₁ ≤ d₂):

- (R1) m ≤ d₁ − 1 [Dimca; Dimca–Kühne–Pokora];
- (R2) 4 ≤ r_H ≤ d₁ for every line, i.e. d₂ ≤ e(H) ≤ d − 5 where e(H) = d − 1 − r_H
  [Abe's bound on points per line + division theorem; 3-transitivity of PGL₂];
- (R3) X := Σ_P C(m_P − 1, 2) = C(d − 1, 2) − d₁d₂;
- (R4) W := Σ_P C(m_P − 2, 2) ≥ ⌈(5X − 4d₁d₂ + 4)/3⌉ (Bojanowski's Hirzebruch-type inequality);
- (R5) W + Σ_H (e(H) − d₂) = β := 3X − d·d₂ (the budget identity).

Table for 17 and 18 lines (the only types their numbers do not exclude):

| type | X | β | W_min | status |
|---|---|---|---|---|
| (17; 7, 9) | 57 | 18 | 13 | remains (our `TC_FOLIATION.md` Thm 5.1 excludes it: mdr(A₂) ≥ 7) |
| (17; 8, 8) | 56 | 32 | 10 | remains: our class (8, 8)[B] |
| (18; 7, 10) | 66 | 18 | 18 | remains numerically, with W = 18 and r_H = 7 on every line (our Thm 10.1 excludes it) |
| (18; 8, 9) | 64 | 30 | 12 | remains |

Everything else at 17 and 18 lines is excluded by (R4)/(R5) alone.

## 2. What we add for (17; 8, 8)

All of the following are necessary conditions on a counterexample (A₁ free (8, 8), A₂ not free,
same lattice) and were established earlier in this project from published results:

- mdr(A₂) = 7 and A₂ is **nearly free with exponents (7, 10)** (`TC_ATTEMPT.md` §11: r ≤ 6 is
  excluded by `TC_FOLIATION.md` Theorem 5.1 and, independently, by the finished part-[A]
  enumeration; r = 8 would make A₂ free by du Plessis–Wall/Dimca).
- **m ≤ 6** (Dimca–Ibadula–Măcinic Prop. 4.7: a nearly free arrangement with m ≥ d₁' = 7 has only
  nearly free lattice-mates). This sharpens (R1).
- A₂ has one Bourbaki point P₀; its Ziegler exponents are (7, 9) on lines missing P₀ and (6, 10)
  on lines through P₀ (Abe–Dimca), so lines through P₀ have 6 or 7 points and no line has eight
  triple points (`TC_FILTER.md` Lemma F1).
- The free member satisfies Abe's Cor. 1.2(2) (checked against the paper, arXiv:1302.3822): every
  line of the plane **not** in A₁ meets it in at least 9 points, i.e. σ_L = Σ_{P ∈ L}(m_P − 1) ≤ 8
  for every external line. In the lattice: unjoined multiple points P, Q have
  (m_P − 1) + (m_Q − 1) ≤ 8 (our rule (W5)); in the realisation A₁ has no rich line at all.
- Lattices with every line carrying 6 or 7 points are done (part [A], 1.96 M lattices, none
  realisable; this used exactly (W5) for (8, 8), which is correct).

So the residual class at 17 lines is: lattices with X = 56, m ≤ 6, 4 ≤ r_H ≤ 8 for every line,
W ≥ 10, (W5), and at least one line with 4, 5 or 8 points. It splits as in `TC_FILTER.md` §3:
(I) a 4-point line; (II) a 5-point line and no 4-point line; (III) all lines with 6–8 points and
at least one with 8.

## 3. Sizes, measured with their enumerator (`work/as17/`, scratch builds of `heavyaug`/`lsgen3`)

Their stage 1 (`heavyaug d mmax lo hi X Wmin`) was validated here on (15; 6, 8): 1,952 heavy
classes and 3 lattices in one second, as published. At 17 lines (one core each, 20 Oct 2026):

| run | parameters | heavy configurations (raw, before the final labelg deduplication) |
|---|---|---|
| (17; 7, 9) | m ≤ 6, 4 ≤ r_H ≤ 7, X = 57, W ≥ 13 | > 160 M after 85 CPU-min, still running |
| (17; 8, 8), window [6, 8] (sub-case III ∪ part [A]) | m ≤ 6, 6 ≤ r_H ≤ 8, X = 56, W ≥ 10 | > 186 M after 85 CPU-min, still running |
| (17; 8, 8), full window [4, 8] | m ≤ 6, 4 ≤ r_H ≤ 8 | > 59 M after 25 min, identical to the [6, 8] run so far; stopped |

For comparison (16; 7, 8) has 8.3 M heavy classes and 16.5 M lattices, and the ratio
lattices/heavy grew from 63 at (15; 7, 7) to 2 at (16; 7, 8) because the window narrowed; at
(17; 8, 8) the window is wide again. So the brute-force route of their paper, applied to our
residual class, is far beyond this machine for sub-cases (II) and (III); this confirms the
measurement of `TC_FILTER.md` §4 by an independent enumerator.

## 4. Sub-case (I) exactly over ℂ: enumeration at the jump cross-ratios

By Yoshinaga's criterion read on the 4-point line H (`TC_FILTER.md` Lemma F2), a realisation of
a lattice of sub-case (I) is non-free iff the cross-ratio λ of the four points of H is a root of
the jump polynomial J_k of the multiplicity vector k of H. So the non-free member of a
counterexample is a configuration of four pencils with collinear centres at a fixed algebraic
cross-ratio λ₀, and at fixed λ₀ all concurrency conditions are linear in the pencil offsets
(Lemma F3). `work/as17/pencil4_exact.py` enumerates, for each vector k and each irreducible
factor f of J_k (one root per factor; Galois conjugates give the same lattices), every 4-partite
linear space on the 16 pencil lines that is the lattice of the generic point of its solution
space over ℚ(λ₀) (exact linear algebra by restriction of scalars, python-flint), with the window
constraints. Jump polynomials recomputed (`jump4.py`, `jumps4.txt`; they agree with Lemma F1):

| k (pencils A, B, C, D at ∞, 0, 1, λ) | irreducible jump factors (λ ≠ 0, 1) |
|---|---|
| (5,5,5,1) | λ + 1, λ − 2, 2λ − 1 (one S₃-orbit), λ² − λ + 1 |
| (5,5,3,3) | λ + 1, λ⁴ − 8λ³ + 7λ² − 8λ + 1, λ⁴ + 10λ³ − 23λ² + 10λ + 1 |
| (5,4,4,3) | 2λ − 1, 2λ⁸ − 8λ⁷ + 93λ⁶ − 251λ⁵ + 266λ⁴ − 123λ³ + 76λ² − 55λ + 1 |
| (5,5,4,2) | 2λ⁸ − 4λ⁷ − 3λ⁶ + 48λ⁵ − 85λ⁴ + 48λ³ − 3λ² − 4λ + 2 |
| (4,4,4,4) | λ² − 5λ + 1, λ² + 3λ − 3, 3λ² − 3λ − 1 (one anharmonic orbit), λ² − λ + 1 |

**Validation.** (a) E₁₇ (`TC_BUILD.md` §3b), rebuilt exactly over ℚ(ω) in the enumerator's
convention (`e17_lattice.py`: points 2²⁴3⁸4⁸ off H, X = 56, lines with 7 or 8 points), is
reported by the post-processing (`pencil_real2.m2`) as one rigid component with λ² − λ + 1 = 0,
i.e. non-free. (b) `guided_test.py` runs the orderly search restricted to E₁₇'s own blocks for
every labelling of the lines inside the pencils: the search emits E₁₇ (first at the second
labelling tried, 3 of 3,608 labellings tried before stopping), so the symmetry breaking, the
closure at dimension ≤ 2 and the window checks do reach a genuine window lattice.

Each lattice found has a non-free realisation (at λ₀); `pencil4_post.py` then computes its
realisation space with λ free (`work/build/pencil_real2.m2`) and decides whether a free
realisation exists (a genuine component with λ non-constant, or constant outside the jump set).
A lattice with both would be a counterexample.

**Results (20 Oct 2026, `work/as17/out_*.jsonl`, `log_*.txt`).** With the smallest pencil
processed first (its lines need the most concurrencies, so the solution space collapses early)
and closure of the finitely many special configurations as soon as the solution space is
two-dimensional, the harmonic case of (5, 5, 5, 1) takes 90 seconds: 184 root branches,
11,146 + 11,312 nodes on two workers, **no window lattice**. This agrees with the finite-field
census of `TC_BUILD.md` §5.2 (nothing for (5, 5, 5, 1) over F₁₁ and F₁₃), but is now a statement
over ℂ: *no 17-line arrangement of class (8, 8) with m ≤ 6 and 4 to 8 points on every line has a
4-point line of multiplicities (5, 5, 5, 1) at a harmonic cross-ratio.* The other cases are
running (table completed below as they finish).

| k | λ₀ | field degree | result |
|---|---|---|---|
| (5,5,5,1) | −1 (harmonic orbit) | 1 | none (90 s) |
| (5,5,5,1) | ω, ω² − ω + 1 = 0 | 2 | none (21,132 nodes, 400 s) |
| (5,5,3,3) | −1 | 1 | none (30,471 + 40,313 nodes on two workers, 23 min) |
| (5,5,3,3) | root of λ⁴ − 8λ³ + 7λ² − 8λ + 1 | 4 | **stopped** at root branch 1 of 48 (9 min, two workers) |
| (5,5,3,3) | root of λ⁴ + 10λ³ − 23λ² + 10λ + 1 | 4 | **stopped** at root branch 1 of 48 |
| (5,4,4,3) | 1/2 | 1 | half done: worker 0 (even root branches) complete, 70,394 nodes, none, 73 min; worker 1 **stopped** at root branch 98 of 131 (84 min) |
| (5,4,4,3) | root of the degree-8 factor | 8 | **stopped** in root branch 0 of 131 (9 min) |
| (5,5,4,2) | root of the degree-8 factor | 8 | **stopped** in root branch 0 of 99 (4 min) |
| (4,4,4,4) | ω | 2 | **stopped** at root branch 1 of 168 (10 min, three workers); E₁₇ not yet reached |
| (4,4,4,4) | root of λ² − 5λ + 1 | 2 | **stopped** in root branch 0 of 168 (9 min) |

All computations were stopped at the user's request at 16:02 on 20 Oct 2026. The three
completed vectors ((5,5,5,1) both fields, (5,5,3,3) harmonic) are theorems over ℂ. To resume
a case: `work/as17/launchN.sh k1 k2 k3 k4 minpoly tag N` runs N workers that split the root
branches (`i/N`); a finished worker prints `time=`; then `pencil4_post.py jumps4.txt outdir
out_*.jsonl` decides every lattice found. The (7, 9) heavy-configuration count was stopped at
247.3 M raw configurations after 110 CPU-minutes (not finished; the raw file is in the session
scratch directory and not kept).

## 5. The type (17; 7, 9) by their method

Our 17-line run excluded (7, 9) only with a too-strong form of (W5) (`TC_ATTEMPT.md`, correction
of 10 Oct 2026), so computationally it rests on `TC_FOLIATION.md` Theorem 5.1. Their reduction
leaves (17; 7, 9) numerically open (β = 18 ≥ W_min = 13), and their enumerator handles it
directly: m ≤ 6, 4 ≤ r_H ≤ 7, X = 57, W ≥ 13.

**Result.** Not completed: stopped at 247.3 M raw heavy configurations (110 CPU-min), already
30 times the count of (16; 7, 8); the completion and screening stages were never started.
So (17; 7, 9) still rests on `TC_FOLIATION.md` Theorem 5.1.

## 6. What the combination does and does not give (status 20 Oct 2026, evening)

**Theory.** Their numerical reduction and ours agree at 17 lines: only (7, 9) and (8, 8) survive
the counting, (7, 9) dies by `TC_FOLIATION.md` Theorem 5.1 (3·mdr(A₂) ≥ n + 2), and the (8, 8)
class is our part [B]. Nothing in their paper bears on part [B] beyond Bojanowski's inequality
(W ≥ 10), which we had not used and which is weak here (the budget is 32). Conversely, their
Theorem 1.3 (the free 15- and 16-line arrangements in the window are the six lattices
L₀, F₁–F₅ at 15 lines and none at 16) is the kind of statement that would finish 17 lines: a
free (8, 8) arrangement of 17 lines with m ≤ 6 and 4 ≤ r_H ≤ 8 for every line. No such
arrangement is known (`TC_BUILD.md`), and `TC_BUILD.md` Lemma 1.3 shows that one with an 8-point
line H is the same thing as a nearly free (8, 8) arrangement N of 16 lines (logarithmic bundle
T_{P²}(−9), b₂(N) = 72) plus an external line meeting N in 8 points. By Abe's Cor. 1.2(2) the free
member has no external line with ≤ 8 points at all, while the non-free member typically has
rich lines (E₁₇ has four, R₁₇ two); so the forced special incidences of `TC_CONTRADICTION.md`
are exactly the collinearities of A₂ that the free member must break.

**Computation.** The exact linear enumeration settles sub-case (I) case by case; the sub-cases
(II) (a 5-point line, two moduli, jump *curve*) and (III) (6- to 8-point lines only) have no
finite jump set to pin the non-free member to, and their enumerator confirms that brute force
over the lattices is far beyond this machine (> 2·10⁸ heavy configurations in the [6, 8] window
alone, before the completion by triple points). What would make (II) exact is the same method
over the function field of the jump curve C_μ for lattices realisable at its generic point,
plus a separate argument for lattices that force the two cross-ratios of the 5-point line into
finitely many special points of C_μ. What would make (III) exact is a classification of the
nearly free (8, 8) arrangements of 16 lines with 5 to 8 points on every line, or of the
nearly free (7, 10) arrangements of 17 lines with 6 to 8 points on every line.
