# TC17 — Terao's conjecture for 17 lines in ℙ²

Code of the computer-assisted proof that Terao's conjecture holds for arrangements of 17 lines in the
complex projective plane (21 October 2026, audited 21–23 October 2026), together with the code of the
fifteen- and sixteen-line verification that it builds on.

The material was moved here from the research repository `TeraoHunter` (commits `0ac01f5`, the proof, and
`2c21d14`, the audit, plus the corrections of 23 October 2026 recorded in `work/n17/audit/AUDIT.md` §4).
The layout of that repository is kept so that every path quoted in the notes, the manifest and the
manuscripts stays valid. The only edit made to the files is the replacement of the absolute prefix
`/Users/agent/Projects/TeraoHunter` by `/Users/agent/Projects/TC17` in the scripts.

## Layout

| path | contents |
|---|---|
| `work/n17/` | the 17-line computation: enumerators (`heavy/`), core classes (`cores/`, `cores50/`), realisation spaces and extension (`comp/`, `run/`), covering lemma (`cover/`), no 8-point line (`n8zero/`), canonical forms (`validate/`), audit (`audit/`). `work/n17/MANIFEST.md` describes every directory, gives the command line of every step and lists the large regenerable files that are not kept (`manifest_excluded.tsv`). |
| `work/tc15/` | the fifteen- and sixteen-line computation (stages 1–4: `bigblocks.py`, `fill_triples.py`, `fast_real.py`, `fast_real2.py`, `exact_tc_lattice.py`, chain scripts) and its 17-line use (`bigblocks2.py`, `pipeline.py`, part A); `recheck_resultant/` holds the corrected filters (`fast_real_fix.py`, `full_recheck.py`) used for every verdict of the 17-line proof. |
| `work/chains17/` | lattice chains, the 28 cores of the known window lattices (`cores13.jsonl`), checks of the theorems on E₁₇ and R₁₇ᵃ. |
| `work/foliation/` | Macaulay2 checks of the structure predicted for the minimal derivation (Bourbaki ideal, inflection scheme). |
| `work/global/` | `sqf5.m2`, `sqf678.m2`: square-freeness checks used in the proof. |
| `hunter/` | the finite-field and exact realisation routines of the fifteen-line cross-checks (`ffree.py`, `realize.py`). |
| `TC_N17.md` | the proof note (theorems, measurements, covering lemma, extension step, no 8-point line, chain of the proof, result); `TC_CHAINS17.md`, `TC_FOLIATION.md`, `TC_GLOBAL.md`, `TC_CONTRADICTION.md`, `TC_ATTEMPT.md` (§10: fifteen and sixteen lines), `TC_AS17.md`, `TC_BUILD.md`: the notes it refers to. |
| `paper/terao17/` | the manuscript (`terao17.tex`); `paper/short/terao1516.tex`: the fifteen/sixteen-line write-up. |
| `third_party/anghel_stan_anc/` | place for the ancillary files of Anghel–Stan, arXiv:2610.25868 (not included; see its README). |

Code is committed; the result files (logs, verdicts, `jsonl` records, compressed Macaulay2 records), the
notes and the manuscripts are kept in the working tree and added separately.

## Software

macOS on Apple silicon (10 cores). Python 3.12 with python-flint 0.9 and pynauty 2.8 (a virtual
environment at `.venv`, referenced by the scripts as `/Users/agent/Projects/TC17/.venv/bin/python`);
Macaulay2 1.26; nauty 2.9 (`labelg`); GLPK 5.0 (`glpsol`); a C compiler for the enumerators
(`work/n17/heavy/*.c`, built as in `work/n17/MANIFEST.md`). The audit scripts that re-decide verdicts with
the independent code of Anghel–Stan import `realize.py`, `exact.py`, `g6util.py` from
`third_party/anghel_stan_anc/anc`.

## Not included

The regenerable intermediates of the 17-line computation (383 files, 9.3 GB: raw enumerations, core lists,
per-core verdicts, Macaulay2 shards; SHA-256 in `work/n17/manifest_excluded.tsv`) and the raw lattice lists
of the fifteen-, sixteen- and seventeen-line enumerations (`work/tc15/bb_n17/`, `lattices_n1*.jsonl`,
tens of GB). The scripts regenerate them.
