# TC_CONTRADICTION.md — a proof attempt by contradiction

Started 2026-10-14. Assume a counterexample to Terao's conjecture in P²_ℂ and try to derive a
contradiction. Notation as in TC_ATTEMPT.md and TC_FOLIATION.md:
- A₁ is free with exponents (1, d₁, d₂), d₁ ≤ d₂, δ = d₂ − d₁, n = d₁ + d₂ + 1.
- A₂ is non-free with the same lattice L, r = mdr(A₂), and θ₀ its minimal derivation.
- Z is the Bourbaki scheme of θ₀, of length B = (d₁ − r)(d₂ − r) ≥ 1, and j = 3r − n.
- For a line ℓ, W(ℓ) = n − |A ∩ ℓ| = Σ_{P ∈ ℓ} (m_P − 1) is its weight, and z(ℓ) = length(Z ∩ ℓ).

## 0. Verdict

**No contradiction in general.** TC is not proved.

What is new in this round:
1. **The weight dichotomy (Theorem 1).** It holds for every line of the plane, not only the lines of
   the arrangement. For A₂, every line ℓ ∉ A₂ has W(ℓ) ≤ r − z(ℓ) or W(ℓ) = n − 1 − r + z(ℓ). The
   lines of the second kind ("rich lines") are leaves of the minimal foliation, so there are at
   most j = 3r − n of them.
2. **Forced special incidences (Corollary 2).** Take two multiple points P, Q joined by no line of
   the arrangement, with σ := (m_P − 1) + (m_Q − 1) > r. In A₂ the line PQ must pass through
   further multiple points, of total weight at least d₁ + d₂ − r − σ ≥ d₁ − r. In A₁ the same line
   carries extra weight exactly d₂ − σ when σ > d₁, and none when δ = 0 and σ = d₁. This is a
   precise form of the "special incidence" a non-free member must carry.
3. **Absorption (Proposition 4).** Adding a rich line through the Bourbaki scheme lowers the
   Bourbaki degree by z(ℓ). Once the scheme is used up, A₂ plus those lines is free with exponents
   (r, n + k − 1 − r).
4. **The extremal case (Proposition 5).** If the residual inflection curve J′ splits into rich
   lines, A₂ together with its rich lines is 3r lines invariant by a degree-r foliation. Such a
   foliation is "reduced convex" (Pereira; Marín–Pereira). Reduced convex foliations are classified
   only in degrees ≤ 5, where they are Fermat or Hilbert modular. Every counterexample has r ≥ 7.
5. **Seventeen lines (§5).** New necessary conditions for the last open class:
   - no line outside A₂ has weight 8;
   - at most four non-adjacent pairs of multiplicities {5, 5} or {6, 4};
   - the jumping point avoids every line outside A₂ of weight 7, 8 or 9.
6. **Verification (§6).** Theorem 1 and Proposition 4 hold in 9 test arrangements, over 1,225
   lines outside the arrangement, with no violation.

**Where it stops.**
- Corollary 2 only bites when the lattice has heavy non-adjacent pairs. Free lattices in the window
  can have every heavy pair adjacent: the 15-line family of [ACKN] is an example. There the forced
  incidences are absent, and the only remaining interaction between A₁ and A₂ is Yoshinaga's, line
  by line, which is satisfiable.
- To go further one would need either that J′ always splits into rich lines, plus the classification
  of reduced convex foliations of degree ≥ 6 (an open question of Marín–Pereira), plus TC for
  subarrangements of the Fermat arrangements, or a new argument for non-linear J′. I have none of
  these.

## 1. The minimal counterexample: what is already known

From TC_ATTEMPT.md, TC_FOLIATION.md and TC_RIGIDITY.md:
- **Window.** 3r ≥ n + 3, hence d₁ ≥ 7, d₂ ≤ 2d₁ − 7 and n ≥ 17. Every line of L has between δ + 4
  and d₁ points, the multiplicities are at most d₁ − 1, and L is not divisionally free.
- **Foliation.** θ₀ defines a degree-r foliation with all n lines invariant. Its inflection curve
  is J = Q·J′ with deg J′ = j. The Bourbaki scheme Z lies in Sing J′ as a scheme. On every line H of
  A₂, e₁(H) = r − z(H).
- **Rigidity.** Non-freeness is read off any single line (TC_RIGIDITY Lemma 1). Lattice
  degenerations force jumps (Lemma 2). Interior non-free points are tangential (Lemma 3).

## 2. The weight dichotomy

**Theorem 1.** Let A be any arrangement of n lines and ℓ ∉ A a line. Let E_A|_ℓ ≅ O(−a₁) ⊕ O(−a₂),
with a₁ ≤ a₂ and a₁ + a₂ = n − 1, be the splitting type of the logarithmic bundle on ℓ. Then
  |A ∩ ℓ| = a₁ + 1 or |A ∩ ℓ| ≥ a₂ + 1,  equivalently  W(ℓ) = a₂ or W(ℓ) ≤ a₁.

Now let A = A₂ in a counterexample. Then:
- (i) a₁(ℓ) = r − z(ℓ) for every line ℓ, so W(ℓ) ≤ r − z(ℓ) or W(ℓ) = n − 1 − r + z(ℓ). Call ℓ
  *rich* in the second case.
- (ii) Every rich line is invariant under θ₀.
- (iii) There are at most j = 3r − n rich lines.

For A = A₁ the theorem gives Abe's statement: |A₁ ∩ ℓ| = d₁ + 1 or ≥ d₂ + 1. When δ > 0, the
lines with |A₁ ∩ ℓ| = d₁ + 1 are leaves of the minimal foliation of A₁, so there are at most
3d₁ − n of them.

*Proof.*
1. *Elementary modification.* Let B = A ∪ ℓ and k = |A ∩ ℓ|. Derivations of B are the derivations
   of A tangent to ℓ, so E_B ⊂ E_A with quotient a line bundle O_ℓ(a) on ℓ.
   - Chern classes: c₂(E_B) = c₂(E_A) − c₁(E_A) + a. Here c₂ = b₂ − |A| + 1, c₁ = −(|A| − 1), and
     b₂(B) = b₂(A) + k.
   - Solving gives a = k − n, so 0 → E_B → E_A → O_ℓ(k − n) → 0. This is the Faenzi–Vallès
     sequence.
2. *Restriction to ℓ.* We get a surjection O(−a₁) ⊕ O(−a₂) → O(k − n) on P¹. Its components have
   degrees k − n + a₁ and k − n + a₂.
   - If k − n < −a₁, the first component vanishes. The second is then nowhere zero only if
     k − n = −a₂, that is k = a₁ + 1.
   - Otherwise k − n ≥ −a₁, that is k ≥ a₂ + 1.
3. *(i).* θ₀|_ℓ is a nonzero section of E₂(r)|_ℓ whose zero scheme is Z ∩ ℓ. Since a₁ ≤ r < (n−1)/2,
   we have a₂ ≥ n − 1 − r > r. So the O(r − a₂) component of θ₀|_ℓ vanishes, and the other component
   is a form of degree r − a₁ with zero scheme Z ∩ ℓ. Hence r − a₁ = z(ℓ).
4. *(ii).* If ℓ is rich, k = a₁ + 1. The image of θ₀ in H⁰(O_ℓ(r + k − n)) = H⁰(O_ℓ(r − a₂)) is
   zero, because r − a₂ < 0. So θ₀ is a derivation of A₂ ∪ ℓ.
5. *(iii).* A degree-r foliation with finitely many invariant lines has at most 3r of them: they
   are components of the inflection curve, of degree 3r [Per01]. The n lines of A₂ are invariant, so
   at most 3r − n further lines are. ∎

*Remark.* Half of (i) is also a tangency count. A line that is not invariant has exactly r
tangencies with the foliation, and a multiple point P contributes at least m_P − 1 (the jets of θ₀
of order ≤ m_P − 2 at P are radial). So W(ℓ) ≤ r for every non-invariant line [Bru, Prop. 2.2].

## 3. Consequences

**Corollary 2 (forced special incidences).** Let P, Q be multiple points joined by no line of L,
and σ = (m_P − 1) + (m_Q − 1).
- (a) In A₁: σ + κ₁ ≤ d₁ or σ + κ₁ = d₂, where κ₁ is the weight of the other multiple points of A₁
  on PQ. In particular σ ≤ d₂, which is the unjoined-pair lemma.
- (b) In A₂: if σ > r, the line PQ is rich, hence a leaf of θ₀. Its other multiple points have
  weight κ₂ = n − 1 − r + z(PQ) − σ ≥ d₁ + d₂ − r − σ ≥ d₁ − r ≥ 1.
- (c) If δ = 0 and σ = d, then κ₁ = 0, while κ₂ ≥ 1 + (d − 1 − r) + z(PQ).

So on every heavy diagonal the two realisations differ by collinearities of intersection points
that the lattice does not record.

**Corollary 3 (capacity).** Each rich line carries pairwise non-adjacent points whose
multiplicities sum to at most n. At most t ≤ 1 + 2(n − 2)/(r + 3) of them can pairwise satisfy
σ > r. Hence the number of non-adjacent pairs with σ > r is at most j·C(t, 2), a lattice-level
necessary condition.

**Proposition 4 (absorption).** Add rich lines ℓ₁, …, ℓ_k to A₂. Then θ₀ stays a derivation, and
its Bourbaki length becomes B − Σ z(ℓᵢ) + ε. Here ε = Σ_R (number of added lines through R − 1),
summed over the points R outside A₂ where added lines meet. When this is 0, A₂ ∪ {ℓᵢ} is free with
exponents (r, n + k − 1 − r).

*Proof.*
1. Adding a line with k′ points to an arrangement changes c₂(E(r)) by (k′ − 1) − r. A rich line has
   k′ = r − z + 1 points on A₂, plus the new points where it meets earlier added lines.
2. The zeros of θ₀ in the smaller bundle stay inside Z. The quotient by θ₀ embeds in E₂/⟨θ₀⟩, which
   is torsion-free off Z.
3. A section with no zeros splits the bundle. ∎

So, whenever enough rich lines pass through Z, A₂ is a free arrangement with a few leaves removed.

**Proposition 5 (extremal case).** If J′ is a product of j rich lines, then A₂ ∪ {rich lines} is 3r
lines invariant by the degree-r foliation. That foliation is then reduced convex [Per01; MP13], and
its 3r lines have Hirzebruch's property: each meets the others in exactly r + 1 points.
- The known reduced convex foliations are the Fermat foliations (invariant lines = the full monomial
  arrangement A(r−1, 1, 3)), the Hesse pencil (r = 4), and the Hilbert modular foliations (r = 5, 7).
- It is proved that there are no others for r ≤ 5 [BM21 and references]. Marín–Pereira [MP13,
  Problem 9.1] ask whether there are others in any degree.
- If the answer is no, a counterexample with linear J′ has A₂ inside A(r−1, 1, 3) or inside the
  21-line Hilbert modular arrangement (r = 7).
- The user's 18-line seed is A(6, 1, 3) minus three lines. Its three rich lines are exactly the
  missing ones (§6).

**Lemma 6 (sub-arrangements, minimal counterexample).**
- (a) If TC holds below n lines, every proper sub-arrangement of A₁ that is free has smaller exponent
  at most r. Reason: it is free in A₂ too, and θ₀ restricts to it.
- (b) In the window, no deletion of k ≤ 3 lines from A₁ is free.
  - Delete k lines that carry σ_k ≤ k·d₁ points in turn, since s_H ≤ d₁. If the result were free
    with exponents (d₁ − i, d₂ − k + i), then c₂ gives (d₁ − i)(d₂ − k + i) = d₁d₂ + k − σ_k, that
    is i² + (δ − k)i + k ≤ 0.
  - The smaller exponent is at most mdr(A₁) = d₁, so i ≥ 0 or i ≤ k − δ. For i ≤ min(0, k − δ) the
    left side is i(i + δ − k) + k ≥ k > 0. For i ≥ 0 a solution needs δ < k and (k − δ)² ≥ 4k,
    which fails for k ≤ 3.
- (c) For δ = 0 the first possible free deletion removes four lines, with exponents (d − 2, d − 2),
  which then forces r ≥ d − 2.

## 4. The attempted contradiction, and where it breaks

1. A counterexample needs A₂ to carry a degree-r foliation with n invariant lines, Bourbaki length
   B = (d₁ − r)(d₂ − r) ≥ 1, and Z ⊂ Sing J′, with deg J′ = 3r − n ≥ 3.
2. Every heavy non-adjacent pair of L creates a rich leaf in A₂ (Corollary 2). There is room for at
   most 3r − n of them (Corollary 3).
3. If the lattice has more heavy non-adjacent pairs than this capacity, the counterexample is
   impossible. **This is a contradiction, but only for such lattices.**
4. Otherwise, the rich leaves either absorb Z (Proposition 4: A₂ is a free arrangement minus leaves)
   or they do not, and Z sits on non-linear components of J′.
   - In the extremal sub-case (J′ = rich lines), the foliation is reduced convex.
   - Classifying reduced convex foliations of degree r ≥ 7 is an open problem. Even granting it, one
     still needs TC for the lattices of subarrangements of A(r−1, 1, 3).
5. When the heavy points of L are pairwise adjacent, as in all known flexible free lattices, steps
   2–3 say nothing. A₁ then constrains A₂ only through Yoshinaga's criterion on each line, and each
   line's jump condition can be met.

## 5. Seventeen lines

The class (8, 8)[B] of TC_FILTER.md: n = 17, r = 7, B = 1, Z = {P₀} reduced, j = 4.
- A₁: every line outside A₁ has W ≤ 8 (|A₁ ∩ ℓ| ≥ 9).
- A₂: a line outside A₂ missing P₀ has W ≤ 7 or W = 9; one through P₀ has W ≤ 6 or W = 10. So no line
  outside A₂ has weight 8, and P₀ lies on no line outside A₂ of weight 7, 8 or 9.
- The lines of weight 9 or 10 are leaves of θ₀, at most 4, and components of the quartic J′, which is
  singular at P₀.
- Non-adjacent pairs with σ = 8, i.e. multiplicities {5, 5} or {6, 4}: in A₁ their line carries no
  further multiple point; in A₂ it carries extra weight 1 (missing P₀) or 2 (through P₀).
- A rich line has room for only one such pair. So **L has at most four non-adjacent pairs of
  multiplicities {5, 5} or {6, 4}**. Non-adjacent pairs with σ ≥ 9 do not exist.
- A rich line through P₀ (W = 10) would make A₂ ∪ ℓ free with exponents (7, 10) (Proposition 4).

These are new filters for the residual enumeration, which was cancelled and has not been rerun.

## 6. Verification

`work/contradiction/richlines.m2` checks Theorem 1 on every line through two multiple points.
`absorb.m2` checks Proposition 4. All exact, over number fields.

| arrangement | n | r | B | lines checked | violations | rich lines (bound 3r − n) | all leaves |
|---|---:|---:|---:|---:|---:|---|---|
| 18-line seed | 18 | 7 | 2 | 435 | 0 | 3 (3) | yes |
| Ceva(5), free (6,8) | 15 | 6 | 0 | 153 | 0 | 3 (3) | yes |
| Ceva(5) minus a line, nearly free | 14 | 6 | 1 | 154 | 0 | 4 (4) | yes |
| Ceva(5) minus two lines | 13 | 6 | 2 | 143 | 0 | (2r ≥ n − 1: only the dichotomy applies) | – |
| A(4,1,3), free (5,9) | 15 | 5 | 0 | 112 | 0 | 0 (0) | – |
| A(4,1,3) minus x | 14 | 5 | 0 | 97 | 0 | 1 (1) | yes |
| A(4,1,3) minus two lines | 13 | 5 | 0 | 102 | 0 | 2 (2) | yes |
| B₃, free (3,5) | 9 | 3 | 0 | 16 | 0 | 0 (0) | – |
| B₃ minus a line | 8 | 3 | 0 | 13 | 0 | 1 (1) | yes |

Absorption, with syzygy degrees of the Jacobian ideal:

| arrangement | degrees | prediction |
|---|---|---|
| seed | 7, 11, 12 | not free, B = 2 |
| seed + x (z = 2) | 7, 11 | free (7, 11) |
| seed + (y − z) (z = 1) | 7, 12, 12 | B = 1, nearly free |
| seed + its 3 rich lines | 7, 13 | free (7, 13) = A(6, 1, 3) |
| Ceva(5) minus a line + z (z = 1) | 6, 8 | free (6, 8) |
| Ceva(5) minus a line + x (z = 0) | 6, 9, 9 | B stays 1 |

*Caveat.* The rich-line count meets the bound 3r − n in every case. That is because every test
arrangement is a sub-arrangement of a Fermat arrangement: adding back the rich lines gives
A(r−1, 1, 3), whose minimal foliation is the Fermat field. This is selection bias, not evidence
that J′ always splits into lines.

## 7. Files and references

- `work/contradiction/richlines.m2`, `test_rich.m2`, `test_rich2.m2` (outputs `test_rich.out`,
  `test_rich2.out`) and `absorb.m2`.

References:
- [ACKN] Abe, Cuntz, Kawanoue, Nozawa, *Non-recursive freeness and non-rigidity*, arXiv:1411.3351.
- [BM21] Bedrouni, Marín, *Convex foliations of degree 5 on the complex projective plane*,
  arXiv:1901.03174.
- [Bru] Brunella, *Birational geometry of foliations*, Prop. 2.2 (tangency count along a line).
- [FV14] Faenzi, Vallès, *Logarithmic bundles and line arrangements, an approach via the standard
  construction*, J. London Math. Soc. (2014).
- [MP13] Marín, Pereira, *Rigid flat webs on the projective plane*, arXiv:1008.3690 (Problem 9.1).
- [Per01] Pereira, *Vector fields, invariant varieties and linear systems*, Ann. Inst. Fourier 51
  (2001).
