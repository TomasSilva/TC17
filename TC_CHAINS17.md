# Chains of 8-point lines in the 17-line class (8, 8)[B]

Continued in `TC_N17.md` (21 Oct 2026), where the 17-line case is closed (computer-assisted). The open
points listed below are the state of 20 Oct; the covering lemma and the core computation of `TC_N17.md`
go around them.

Added 20 Oct 2026 (evening). Notation as in `TC_AS17.md`, `TC_FOLIATION.md`, `TC_GLOBAL.md` §11:
L is a lattice of 17 lines with χ = (t − 1)(t − 8)², m ≤ 6, every line with 4 to 8 points;
(A₁, A₂) is a counterexample: A₁ free with exponents (8, 8), A₂ nearly free with exponents
(7, 10), minimal derivation θ₀ (degree 7), Bourbaki point P₀. E_A is the sheaf of logarithmic
derivations killing Q (the Jacobian syzygy sheaf), c₁(E_A) = −(n − 1), c₂(E_A) = b₂ − n + 1.
For a set S of lines, L ∖ S is the sub-lattice of the other lines.

**Summary.** Deleting from a counterexample lines that carry exactly 8 points peels both members
down to the same kind of arrangement. After four such deletions both members are *free* with
exponents (6, 6). Since every line of the window is determined by the others, the realisations of
L are determined by those of the 13-line core, so Terao's conjecture holds for every such L whose
core has a rigid realisation space (a single Galois orbit). In every known window lattice with an
8-point line the core is free and rigid. This turns the high-W part of the search, which is what
made it infeasible, into a 13-line problem.

## 1. Statements

Call a set S of k lines of L a **k-chain** if b₂(L ∖ S) = 80 − 8k. Since deleting a line H from
an arrangement lowers b₂ by the number of points of the arrangement on H, which is ≤ 8 in the
window, this holds iff, in every deletion order, each line of S meets the remaining arrangement in
exactly 8 points. A k-chain consists of 8-point lines of L whose pairwise intersections are points
of multiplicity ≥ 3, with no point of multiplicity m lying on more than m − 2 of them.

**Lemma A (small deletions of the non-free member).** For every set S of at most 3 lines,
mdr(A₂ ∖ S) = 7.

**Theorem B (chains).** Let S be a k-chain, k ≤ 4. Then:

| k | A₂ ∖ S | A₁ ∖ S |
|---|---|---|
| 1 | nearly free (7, 9) | nearly free (8, 8), E ≅ T_{P²}(−9) (`TC_BUILD.md` Lemma 1.3) |
| 2 | nearly free (7, 8) | nearly free (7, 8) |
| 3 | nearly free (7, 7), E ≅ T_{P²}(−8) | E ≅ T_{P²}(−8), or nearly free (6, 8) |
| 4 | **free (6, 6)** | **free (6, 6)** |

**Lemma C (lines are determined by the others).** Every line of L passes through at least two
points of multiplicity ≥ 3; more generally, if S is a chain, each line of S, at the moment it is
deleted, passes through at least two multiple points of the remaining arrangement. Hence a
realisation of L is determined by its restriction to L ∖ S, and restriction R(L) → R(L ∖ S) is
injective, with Galois-stable image.

**Corollary D (4-chains).** If L has a 4-chain S, then F = L ∖ S is a lattice of 13 lines with
χ = (t − 1)(t − 6)² all of whose realisations are free, and if R(F) is a single Galois orbit then
all realisations of L are Galois conjugate and Terao's conjecture holds for L. So a counterexample
with a 4-chain needs a free (6, 6) core of 13 lines whose realisation space has positive dimension
or at least two Galois orbits (the flexible 13-line family of Abe–Cuntz–Kawanoue–Nozawa is one
such lattice).

**Corollary E (where W comes from).** W = 32 − Σ_H (8 − s_H). So a lattice with at most three
8-point lines has W ≤ 18; with none, W ≤ 15 (≤ 13 with a 5-point line, ≤ 12 with a 4-point line);
W ≥ 19 forces at least four 8-point lines. Always W ≥ 11, since t₂ = 3W − 32 − t₅ − 3t₆ ≥ 0.

## 2. Proofs

*Lemma A.* θ₀ is a derivation of A₂ ∖ S, so mdr ≤ 7. Let φ be a derivation of A₂ ∖ S of degree
≤ 6, not a multiple of the Euler derivation E, and α_S the product of the forms of S. Then α_S·φ is
a derivation of A₂ of degree ≤ 9. Since D₀(A₂) is generated in degrees 7, 10, 10, α_S·φ = gE + qθ₀
with deg q = deg φ + |S| − 7 ≤ 2. If q = 0, every component of α_S·φ is a multiple of the matching
coordinate, which forces α_S | g and φ ∈ S·E. Otherwise restrict to a line H ∈ S: if α_H ∤ q, then
θ₀|_H is proportional to E|_H, i.e. f_H = det_H(θ₀|_H, E_H) = 0, which is impossible
(`TC_FOLIATION.md` 1.1: f_H ≠ 0 for every line of A₂). So every α_H, H ∈ S, divides q, and
deg q ≥ |S| = 3 > 2, a contradiction. ∎

*Theorem B, the column A₂.* Write E_k for the sheaf of A₂ minus the first k lines of S. Each
deletion step is the Faenzi–Vallès sequence 0 → E_{k−1} → E_k → O_{H_k}(8 − (17 − k)) → 0.
- k = 1, 2: mdr = 7 by Lemma A, so θ₀ is a section of E_k(7) with isolated zeros (a section
  vanishing on a curve would give a derivation of degree < 7). Its zero scheme has length
  c₂(E_k(7)) = 57 − 105 + 49 = 1, resp. 50 − 98 + 49 = 1 (this is the Bourbaki degree χ̄(7)), i.e. it
  is one reduced point, and the arrangement is nearly free with exponents (7, 9), resp. (7, 8).
- k = 3: c₁(E₃(7)) = 1, c₂(E₃(7)) = 43 − 91 + 49 = 1, and h⁰(E₃(6)) = 0 by Lemma A. So E₃(6) is a
  stable bundle with c₁ = −1, c₂ = 1, and the only one is T_{P²}(−2). Hence E₃ ≅ T(−8).
- k = 4: 0 → T(−8) → E₄ → O_{H₄}(−5) → 0. Twisting by 6, H⁰(T(−2)) = H¹(T(−2)) = 0 (Bott), so
  h⁰(E₄(6)) = h⁰(O_{H₄}(1)) = 2. If E₄(5) had a section, multiplying it by x, y, z would give three
  independent sections of E₄(6); so h⁰(E₄(5)) = 0. Now c₁(E₄(6)) = 0 and c₂(E₄(6)) = 36 − 72 + 36
  = 0. A nonzero section of E₄(6) cannot vanish on a curve (that would give a section of E₄(5)), so
  its zero scheme has length c₂ = 0, it vanishes nowhere, and E₄(6) is an extension of O by O,
  hence O ⊕ O. So A₂ ∖ S is free with exponents (6, 6). ∎

*Theorem B, the column A₁.* k = 1 is `TC_BUILD.md` Lemma 1.3. For k = 2:
0 → T(−9) → E₂ → O_{H₂}(−7) → 0 gives h⁰(E₂(6)) = 0 and h⁰(E₂(7)) = 1 (Bott vanishing again), and
c₂(E₂(7)) = 1, so A₁ ∖ S is nearly free (7, 8). For k = 3 the same numbers as on the A₂ side give
c₁(E₃(7)) = c₂(E₃(7)) = 1 and h⁰(E₃(6)) ≤ 1: if it is 0, E₃ ≅ T(−8) by stability; if it is 1, the
section has a zero scheme of length c₂(E₃(6)) = 1 and A₁ ∖ S is nearly free (6, 8). For k = 4,
A₁ ∖ S has the same 13-line lattice as A₂ ∖ S, which is free; Terao's conjecture holds for 13 lines
(Dimca–Ibadula–Măcinic; also our range n ≤ 16), so A₁ ∖ S is free. ∎

*Lemma C.* On a line H the multiplicities satisfy Σ_{P∈H} (m_P − 1) = 16 with at most 8 points and
m_P ≤ 6. If at most one point had m_P ≥ 3, the sum would be at most 5 + 7 = 12. For a chain line
H_i deleted after i − 1 others, the 17 − i remaining lines meet it in 8 points; if at most one of
these points carried two or more of them, that point would carry at least 10 − i ≥ 6 remaining lines,
i.e. m ≥ 7 in L. So each deleted line is the line through two intersection points of remaining
lines. The image of R(L) is cut out from R(L ∖ S) by incidence conditions defined over ℚ, so it is
Galois-stable. ∎

*Corollary D.* Theorem B (k = 4) and Lemma C. If R(F) is one Galois orbit, the image of R(L) is
empty or all of it, so all realisations of L are conjugate and have the same freeness. ∎

*Corollary E.* From X = 56 and b₂ = 80: p = W + 24 points and Σ_H s_H = Σ_P m_P = 80 + p, so
Σ_H (8 − s_H) = 32 − W. ∎

## 3. Computations (`work/chains17/`)

**Theorem B on examples** (Jacobian syzygy degrees in Macaulay2 over F₁₀₀₀₉):

| arrangement | deleted | syzygy degrees | predicted |
|---|---|---|---|
| E₁₇ (nearly free (7, 10)) | none | 7, 10, 10 | |
| E₁₇ | 1-chains (4 tried) | 7, 9, 9 | nearly free (7, 9) |
| E₁₇ | 2-chains (4) | 7, 8, 8 | nearly free (7, 8) |
| E₁₇ | 3-chains (4) | 7, 7, 7 | T(−8) |
| E₁₇ | 4-chains (4) | 6, 6 | free (6, 6) |
| R₁₇ᵃ (rational, nearly free (7, 10)) | 1-, 2-, 3-, 4-chains | 7,9,9 / 7,8,8 / 7,7,7 / 6,6 | same |
| E₁₇, R₁₇ᵃ | 16 random sets of 1–3 lines | minimum always 7 | Lemma A |
| G₁₇ (harmonic grid, free (8, 8)) | 1-chains (5) / 2-chains (5) | 8,8,8 / 7,8,8 | T(−9) / nearly free (7, 8) |

**Chains in every known window lattice** (`latchain.py`, from the lattice data alone):

| classes | 8-point lines | 4-chains |
|---|---|---|
| 12 window deletions of A(G₂₆) (`work/build/del17.jsonl`) | 6 to 9 | 1 to 30 each (E₁₇: 30) |
| the deletion of A(6, 1, 3) (Ceva(6) minus a line; violates (W5)) | 0 | 0 |
| 6 census classes over F₁₁, F₁₃ (`census5_classes.jsonl`; R₁₇ᵃ, R₁₇ᵇ, two A(G₂₆) deletions, two char-11 artefacts) | 6 to 10 | 1 to 12 each |

**The cores.** These lattices have 28 distinct 13-line cores L ∖ S up to isomorphism
(`core13.py`). `work/tc15/exact_tc_lattice.py` (n = 13, d₁ = 6) finds every one of them
realisable, rigid (one non-degenerate component, dimension 0, degree 1, 2 or 4) and free (Yoshinaga
rank 12/12). By Corollary D this re-proves Terao's conjecture for all these 17-line lattices
without computing their own realisation spaces; for the two char-11 artefact classes the rigid core
exists over ℚ̄ but does not carry the four lines.

## 4. What this does to the search

The 17-line class splits into:
1. lattices with a 4-point line: the exact pencil enumeration of `TC_AS17.md` §4 (finite);
2. lattices with a 4-chain: Corollary D reduces them to free 13-line lattices with χ = (t − 1)(t − 6)²
   whose realisation space is not a single Galois orbit, and their four-line extensions. That is a
   13-line enumeration (all free (6, 6) lattices with m ≤ 6 and lines ≤ 7 points, divisionally free
   ones included) followed by a finite extension check on the few non-rigid ones;
3. lattices with neither: at most three 8-point lines gives W ≤ 18 (Corollary E); the only part
   without a bound is four or more 8-point lines with no 4-chain among them.

Part (2) contains every realisable window lattice with an 8-point line found so far, and it is where
the large values of W live. Part (3) is the bottleneck now. Not proved: that four or more 8-point
lines force a 4-chain, or any bound on W in part (3).

Other consequences of Theorem B, not used above:
- After deleting a 2-chain both members are nearly free (7, 8): the whole difference between A₁ and
  A₂ is then whether the unique degree-7 derivation of the 15-line arrangement is tangent to the two
  deleted lines (it is for A₂, it is not for A₁).
- For a 3-chain S and N = A₂ ∖ S ≅ T(−8), each deleted line ℓ determines the unique point w_ℓ with
  θ_{w_ℓ} tangent to ℓ (w_ℓ ∉ ℓ), and A₂ is non-free exactly because the three points w_ℓ coincide
  (with P₀).
