# work/n17/campaign — rerun of the 17-line proof (2–3 November 2026)

Complete rerun, from scratch, of the computational chain of `TC_N17.md` §8 (the proof of Terao's conjecture
for 17 lines), with independent checks at every step, on all 10 cores. Nothing in the original directories
(`work/n17/{heavy,cores,cores50,comp,run,cover,n8zero,audit}`) is touched.

* `campaign.py` — the driver (stages, expected values of 21–23 October 2026, logs). `campaign.py [stage ...]`
  runs the given stages (default: all, in order); a finished stage (`done/<stage>.json`) is skipped on a
  restart, a failed one is recorded in `done/<stage>.FAILED` and the stages that depend on it are skipped.
* `run.sh` — launches the driver detached (`nohup`); `status.sh [n]` — stages done, last n log lines, number of
  running processes; `STOP` — create this file to stop the campaign between stages.
* `campaign.log` — the log (every command, every check, every mismatch); `campaign.out` — raw stdout/stderr.
* `REPORT.md` — written by `report.py` at the end (or `python report.py` at any time): every check with the
  recorded value and OK / MISMATCH.

Stages and directories:

| stage | directory | what |
|---|---|---|
| prep | `bin/` | enumerators compiled from `work/n17/heavy/heavyaug_p.c`, `lsgen3.c`; SHA-256 of the code of record; Anghel–Stan ancillary code (`third_party/anghel_stan_anc/anc`, downloaded from arXiv:2610.25868 on 2 Nov 2026; its `heavyaug.c` and `lsgen3.c` are byte-identical to `work/n17/heavy/heavyaug_orig.c` and `lsgen3.c`) |
| cover | `cover/` | covering lemma: `level1.py` (2,471 δ-assignments), `farkas.py` (exact certificates), `propcheck.py`, `level2.py` (glpsol), `validate.py` on the 299 lattices with φ_max = 1 |
| n8zero | `n8zero/` | `k4444.py` (23 lattices), `pencil5c.py` on all eleven 5-point vectors, invariants, fast filters + Macaulay2 on the 11,224 lattices, Anghel–Stan screening and comparison |
| cores | `cores/` | the 13-line classes b48 (3–7 points per line), **b48w (3–8 points: the class the manuscript's Remark on free window lattices leaves open)**, b49, b50, b51: `heavyaug_p` → `lsgen3` (10 parts) → `labelg` → `sort -u`; `invariants.py` (b₂, m ≤ 6, points per line, unjoined-pair cut, pynauty certificates); `chains.py cores`: the 28 known cores and every φ-max core of the 16 lattices lie in b48 |
| indep_cores | `indep/` | second enumerator (`bigblocks.py` + `fill_triples.py`, no cut) and `compare.py` per class |
| filters | `cores/*_ff_*` | `full_recheck.py 13` (corrected exact filters), 10 parts per class; `*_defer.jsonl` with the class tag |
| as_cores | `as/` | `as_screen.py` (Anghel–Stan `exact.realization_space`) on every core |
| m2 | `comp/` | `m2compb.py 13` on every deferred core (10 parts); per-class records `comp_<class>.jsonl`; `compare_as.py` per class; Macaulay2 on the cores only our filters rejected and Anghel–Stan left undecided |
| ext_b48 … ext_b51 | `ext/` | `work/n17/run/runclass.py <class> 10 comp_<class>.jsonl` (rigid search, families, lattice-level step, children screening) |
| route_timeouts | `ext/` | the cores/children on which Macaulay2 timed out (`ext/*_other*.jsonl`) are routed through the lattice-level step as in October 2026 (`runclass.py <class>to2 … --n=14 <class>to2_forced.jsonl`); their children screened with Anghel–Stan |
| as_children | `as/` | `as_jsonl.py` on every `ext/*_ch.jsonl`, comparison, Macaulay2 on the filter-only undecided children |
| indep_rigid | `indep_rigid/` | `indep_rigid.py` (numeric, written from the definitions) on every rigid component of every level; `compare_indep.py` |
| final | `final/` | `collect.py` (every accepted and rejected 17-line lattice → canonical forms, comparison with `work/n17/run/checked_L.jsonl`), `chains.py window`, `exact_tc_lattice.py 17 8`, `freecheck.py` (Macaulay2: realisation over the field of definition, lattice recomputed, minimal syzygy degrees of D₀), `as_recertify.py` |

Not rerun: part [A] (the 1,958,407 lattices with six or seven points on every line, `TC_ATTEMPT.md` Thm 10.5):
its stage 1 alone (`bigblocks2.py`) took 81,644 s on 10 cores and its chunk files (tens of GB) are no longer
on disk; the heavy-configuration enumerator of Anghel–Stan on that window produces > 7 million heavy
configurations in four minutes without finishing. It was re-screened with the corrected filters on 22 Oct 2026
(`work/n17/audit/partA/`).

## Outcome (3 November 2026, 05:50)

Run 2 Nov 20:15 → 3 Nov 05:50 (9 h 35 min wall, 10 cores). Every stage done; `REPORT.md` lists every check.
All counts recorded on 21–23 October 2026 were reproduced, with two explained exceptions:

* `cover`: the propagation check refutes 2,333 of the 2,471 level-2 systems and leaves 138 open (the
  manuscripts said 2,435 / 36, from an incomplete run); the exact Farkas certificates refute all 2,471 and
  GLPK reports all 2,471 infeasible. Both manuscripts were corrected.
* `ext_b51`: two Macaulay2 timeouts among the 14-line children (the driver expected 0, but the October run had
  exactly these two: same canonical forms). Routed through the lattice-level step by `route_timeouts`:
  142 children with 15 lines, all non-realisable (ours and Anghel–Stan agree), no 17-line lattice.

Main results: cores 21,164 / 26,234 / 154,172 / 738,023 / 2,916,332 (b48 / b48w / b49 / b50 / b51), identical
to the second enumerator; realisable cores 85 / 85 / 1,147 / 9,162 / 58,871 with rigid/curve/surface counts as
recorded; no Macaulay2 timeout among the deferred cores; 0 disagreements with Anghel–Stan on all 3.86 million
cores and all 540,336 children. **The 5,070 lattices of b48w with an 8-point line are all non-realisable**
(5,016 by the filters, 54 by Macaulay2), so the extension from b48w gives exactly the extension from b48:
the manuscript's Theorem "sixteen" now holds for every realisable window lattice (Remark on free window
lattices rewritten). Extension: 0 window rejections (W4, W5, D-pairs never trigger), 99,575 rigid components
with identical lattice sets in the numeric re-implementation, 16 distinct 17-line lattices found (all from
b₂ = 48; b49–b51 give none), equal to the 16 of `work/n17/run/checked_L.jsonl`, all window lattices with
φ_max = 4; each has a realisation space of one component of dimension 0 and degree 1 or 2, Yoshinaga rank
15/16 (non-free), minimal syzygy degrees (7, 10, 10) over its field of definition (Macaulay2), and is
certified non-free by Anghel–Stan's code.
