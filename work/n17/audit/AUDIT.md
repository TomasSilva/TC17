# Audit of the 17-line proof (21–23 Oct 2026)

Rerun and audit of the computer-assisted proof of `TC_N17.md`, on all 10 cores. Everything is in
`work/n17/audit/`; nothing in the original run directories was modified. **Status: complete.**

**Conclusion.** The result stands: exactly 16 window lattices are realisable over ℂ, all rigid, one Galois
orbit each, non-free; Terao's conjecture holds for 17 lines. Six defects were found (F1–F6) and one cause
of non-reproducible running times (F7); none changes a verdict. Every verdict of the proof is now
established twice, mostly by independent code, and the final step no longer depends on the window rules
W4–W6 (in particular not on the new D-pair lemma).

## 1. Findings

| # | where | finding | effect |
|---|---|---|---|
| F1 | `n8zero/pencil5b.py` | heavy configurations deduplicated with canonical forms in which H₀ is not distinguished (for 43333: 192,113 classes instead of 192,133 with H₀ fixed) | none: `audit/n8zero/pencil5c.py` (H₀ fixed) gives identical lattice sets for all five vectors (merges, no loss) |
| F2 | `n8zero/p5excl.py` | cited as the exhaustive check excluding six vectors of a 5-point line; it only lists the vectors | none: `pencil5c.py` run on all six: zero quota systems, zero lattices |
| F3 | `comp/extend.py` | memoisation keyed by mod-p images of the added lines, never confirmed exactly | none: exact rerun (`ext/extaudit.py`) and an independent numeric search give identical results |
| F4 | `run/runclass.py` | worker output discarded and return codes ignored; a rigid component without extensions leaves no record, so a crashed worker would have gone unnoticed; window rejections not recorded | rerun writes one record per component and every rejection; all components accounted for |
| F5 | part [A] (9 Oct) | used the uncorrected resultant filter (64,997 verdicts from the affected branch) | none: corrected re-screen of the 812 affected chunks regenerates the same 1,951,336 lattices chunk by chunk; 110 verdicts move to other exact arguments; the set sent to Macaulay2 is identical (14,590, all non-realisable on 9 Oct) |
| F6 | `heavy/heavyaug_p.c` | the cut (m_P−1)+(m_Q−1) > 8 on unjoined heavy points is applied to the 13-line cores | valid (a 6-fold point of a core gains no deleted line, so the pair stays unjoined in L and violates W5), but must be stated; it removes exactly 7 lattices of b₂ = 51 |
| F7 | `comp/planemodel.py` | plane models use random linear forms; an unlucky coordinate T makes Macaulay2's decomposition of the special fibres take minutes instead of seconds (b50:12/637: 21 s originally, > 600 s in the rerun) | timing only; components that time out are settled by fresh random models or by the lattice-level step |

## 2. Independent checks

- **Core classes, second enumerator** (`bigblocks.py` + `fill_triples.py` of the 15/16-line work, no
  unjoined-pair cut): b₂ = 48, 49, 50 identical lattice sets (21,164; 154,172; 738,023); b₂ = 51
  2,916,339 against 2,916,332, the 7 extra all with an unjoined {6,5} or {6,6} pair (F6).
- **Core verdicts.** Anghel–Stan's `exact.realization_space` on all 3,829,691 cores: 0 disagreements
  with our filters and Macaulay2 on the 3,821,974 it decides; Macaulay2 confirms the 2,925 undecided
  cores that only our filter had rejected.
- **Children** (541,254 lattices of 14–16 lines): the same, 0 disagreements; Macaulay2 confirms the 694
  undecided ones our filter had rejected; `dim2gen.py` regenerates all 16 child sets identically.
- **No 8-point line**: the 23 lattices of K₄,₄,₄,₄ and the 11,201 of the five vectors are non-realisable
  by both methods.
- **Covering lemma**: every constraint of `gamma_ilp.py` and every pruning rule of `level1.py` re-derived;
  level 1 and the Farkas certificates recomputed: 2,471 of 2,471 certified.
- **The 16 lattices**: re-certified with Anghel–Stan's code (one realisation or one conjugate pair,
  Ziegler multirestriction rank 15 of 16 on two lines, non-free).
- **New theory, numerically**: on the 16 lattices (mod 10009) syzygy degrees 7, 10, 10, Bourbaki scheme
  of degree 1, P₀ on no line; all 4,782 lines through two points of the arrangement satisfy the
  external-line corollary (weight ≤ 7 or 9 off P₀, ≤ 6 or 10 through P₀); at most four of weight ≥ 8.
- **Code review** of the fast filters (`fast_real`, `fast_real2`, `fast_real_fix`), the Macaulay2 driver,
  `extend.py`, `famext.py`, `famrun.py`, `famspecial2.py`, `planemodel.py`, `dim2gen.py`, `phicap.py`,
  `runclass.py`: no soundness error beyond F1–F6. The special-point logic of the family search was checked
  case by case (candidate admissible, too poor, too rich at the generic point).

## 3. Rerun of the extension step (`ext/extaudit.py`: exact memoisation, every lattice and every window verdict recorded, one record per component)

- **Rigid components**: all 99,449 completed. Accepted lattices: exactly the 16. **No window rejection.**
  The independent numeric search (`indep/indep_rigid.py`, written from the definitions) finds identical
  lattice sets on all 99,449 components (no ambiguous incidence). Against the original runs, 204
  components differ, all b₂ = 49 components of the pre-φ-cap run `run/ext_b4849_rigid.jsonl`; the 918
  lattice records found there all have a 4-chain and are among the 16.
- **Family components** (14,983): pass 1 (180 s) and pass 2 (1,800 s) settle 14,873; retries with fresh
  random plane models (400 s each, up to 10 attempts) settle 54 more. Identical results wherever a
  component was settled twice; stored parametrisation consistent with `points_over` everywhere; special
  points never degenerate and never without shape lemma; **no window rejection**. 205 components routed
  to the lattice level by the original run are now settled by the family method: both methods find
  nothing. The remaining 56: 49 were routed to the lattice-level step by the original runs (children
  regenerated identically and re-extended here); 7 had been settled by the family method originally and
  were now forced through the lattice-level step (`lat/`: 4,949 children, 0 disagreements with the
  independent screen, 106 realisable, all re-extended exactly; no lattice).
- **Overall**: across every output of the rerun, the accepted lattices are exactly the 16 of
  `run/checked_L.jsonl`, and the window test rejected no lattice anywhere.

## 4. Changes made (23 Oct 2026)

- **Code** (`work/n17`, working tree; not part of the commit of this directory):
  - `comp/extend.py`: memoisation hits confirmed exactly (the stored lines are compared with the current
    ones); one `done` record per searched component; every lattice rejected by the window test written
    with its reason (`L_rejected`, `why`).
  - `comp/famrun.py`: rejected lattices recorded; uses the exact memoisation of `extend.search`.
  - `run/runclass.py`: worker stderr kept in `TAG_workers.err` and non-zero return codes logged; after the
    rigid and the family step the number of components finished is checked against the input; the return
    code of `dim2gen.py` is checked.
  - `n8zero/pencil5c.py` (new, code of record: heavy configurations up to isomorphisms fixing H₀),
    `n8zero/p5excl.py` (now runs `pencil5c.py` on all eleven vectors and reports heavy sets, quota systems
    and lattices), `n8zero/pencil5b.py` (marked superseded).
  - Tests: `extend.py` on the 80 rigid components of b₂ = 48 (80 completion records, the same 16
    lattices, no collision); `runclass.py` end to end on the two forced groups of `lat/` (identical counts;
    completion checks "89 expected, 89 finished" and "9 expected, 9 finished" for the rigid step and
    "8 expected, 8 finished" for the family step; no worker failure; no lattice).
- **`TC_N17.md`** (working tree): §4 states the unjoined-pair cut of the core enumeration; §6 cites
  `pencil5c.py` and the exclusion run; §8 step 1 notes the part-[A] re-screen; §9 summarises the audit and
  the independence from (W4)–(W6).
- **Paper, version 0.2** (`paper/terao17/`, not under version control; v0.1 kept as `*.tex.v01` and
  `terao17_v0.1.pdf`): notice and date; abstract and introduction mention the audit; Proposition on the
  core classes states the cut and its justification; Theorem (no 8-point line) cites `pencil5c.py` and the
  exhaustive exclusion; Theorem (part [A]) records the re-screen; the extension paragraph states that
  memoisation is confirmed exactly and that no lattice is rejected by (W4)–(W6); timeline entry for
  21–23 Oct; new §11.3 on the audit; the limitations reduced to what is not duplicated by independent code.

## 5. Files

| path | contents |
|---|---|
| `cores/` | second enumeration of the core classes (`bigblocks.py`, `fill_triples.py`, `run_ours.sh`) and the comparison (`compare.py`, `compare_a*.out`) |
| `asscreen/` | independent screening of the cores (`as_screen.py`, `compare_as.py`); the verdicts are in `results/as_status.txt.gz` |
| `costgt1/` | Macaulay2 on the cores that only our filter decided |
| `children/` | independent screening of all children (`children_check.py`), Macaulay2 on the filter-only ones |
| `dim2gen/` | regeneration of the children (`regen.sh`, `regen.out`) |
| `n8zero/` | `pencil5c.py` and its runs on all eleven vectors; `n8_check.py` (two-method check of the no-8-point-line lattices) |
| `cover/` | recomputation of level 1 and of the Farkas certificates |
| `final16/`, `theory/` | the 16 lattices re-certified; external-line test (`extlines.py`) |
| `partA/` | corrected re-screen of part [A] (`pipeline_fix.py`, `sched.py`, `jobs.txt`); per-chunk results in `results/partA_done.jsonl` |
| `ext/` | exact rerun of the extension (`extaudit.py`, schedulers, `retry_all.py`); all records in `results/ext_rerun.jsonl.gz` |
| `indep/` | independent numeric rigid search (`indep_rigid.py`); records in `results/indep_rigid.jsonl.gz` |
| `lat/` | lattice-level step for the 7 components the family method did not settle in the rerun |
| `diag/` | diagnosis of the random plane models (F7) |
| `compare_rigid.py`, `compare_fam.py`, `reconcile_fam.py` | the comparisons of §3 |
| `manifest_excluded.tsv` | the 5,252 files not in git (1.2 GB): size, line count, SHA-256 |
