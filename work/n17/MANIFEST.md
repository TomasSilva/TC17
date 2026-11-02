# work/n17: code and data of the 17-line proof

Computer-assisted proof that Terao's conjecture holds for 17 lines in ℙ²_ℂ (`TC_N17.md` §8–§9,
21 Oct 2026). This file says what each directory holds, how each step was run, and what is not in git.

Environment: macOS (Apple M-series, 10 cores), Python 3.12.14 with python-flint 0.9.0 and pynauty
2.8.8.1 (`.venv`), Macaulay2 1.26.06, nauty 2.9.3 (`labelg`, Homebrew), GLPK 5.0 (`glpsol`), Apple
clang 17. Paths in the scripts are absolute (`/Users/agent/Projects/TC17/...`).

## Layout

| directory | contents |
|---|---|
| `heavy/` | Enumerators. `heavyaug_orig.c` and `lsgen3.c` are unmodified copies of `heavyaug.c` and `lsgen3.c` from the ancillary files of Anghel–Stan, [arXiv:2610.25868](https://arxiv.org/abs/2610.25868); `heavyaug_p.c`, `heavyaug_w.c`, `heavyaug_k.c` and `lsgen3p.c` are our modifications of them (window constraints, residue splitting). `g6blocks.py` decodes their graph6 output; `corefilter.py`, `leafclass.py`, `best4.py` produced the measurements of `TC_N17.md` §2. `*_heavy.g6`, `core_X2[678].g6`: the heavy configurations from which the core classes were completed. |
| `cores/`, `cores50/` | The 13-line core classes b₂ = 48, 49 (`cores/`) and 50, 51 (`cores50/`): fast-filter logs `c4[89]_p*.log`, `c5[01]_p*.log`; for b₂ = 48, 49 also the earlier exact runs on the deferred cores (`*_tc_*.out`, `*_m2_*.log`, `stuck_*`). |
| `comp/` | Realisation spaces and extension: `m2compb.py` (Macaulay2 components, batched), `extend.py` (rigid search), `famext.py`, `famrun.py`, `famspecial2.py`, `planemodel.py` (curves), `dim2gen.py` (lattice-level step), `phicap.py` (φ pruning); small test files. |
| `run/` | Orchestration and all extension outputs: `runclass.py`, `slowroute.sh`, `launch_b51.sh`, `retag.py`; logs `runclass_*.log`; rigid and family outputs (`*_ext*.jsonl`, `*_fam*.jsonl`, `famall_*`, `famrun_*`); final collection `finalcheck.sh`, `collectL.py`, `checkL.py`, `final_files.txt`, `final_collect.txt`, `checked_L.jsonl`; `audit.py` → `audit.out`; `rerun/`: rigid reruns after the memoisation change, `compare.out`. |
| `results/` | Compressed Macaulay2 component records (below) and `make_archives.py`, which rebuilds them. |
| `cover/` | Covering lemma (`TC_N17.md` §4): `ilp/` (`gamma_ilp.py`, `level1.py`, `level2.py` with outputs `l2_*.out`, `farkas.py` with outputs `farkas_*.out`, `propcheck.py` → `prop_*.out`, validation `validate.py`, `validate1.py`, `e2e.py`, the LP files `k_*.lp`); `phistat.c`, `phicore.c`, `n8core.c`, `anal.py`; `phi1_all.g6` (299 lattices with φ_max = 1, used for validation), `s20k_part*` (20,011 random heavy configurations). |
| `n8zero/` | No 8-point line (`TC_N17.md` §6): `k4444.py` → `k4444.jsonl` (23 lattices); `p5excl.py`; `pencil5b.py` → `p5b_*`; fast-filter outputs, deferred lists and Macaulay2 records of these lattices. |
| `validate/` | `canon.py` (canonical form with nauty), the 28 cores of the known window lattices and their extension (`cores13*.jsonl`), the two new lattices (`newL.jsonl`, exact check `newL_tc_0.out`). |
| `ext/`, `gamma/` | Prototypes (combinatorial extension, counting test), kept for the record. |

The fast filters are those of the 15/16-line work with the corrected two-parameter branch:
`work/tc15/recheck_resultant/full_recheck.py` (driver) and `fast_real_fix.py`, which load
`work/tc15/fast_real.py` and `fast_real2.py`. Exact checks of lattices use `work/tc15/exact_tc_lattice.py`.

## How each step was run (in `heavy/`, `cores*/`, `comp/`, `run/`; `PY` = `.venv/bin/python`)

1. *Core classes* (13 lines, m ≤ 6; X = 78 − b₂; for b₂ = 48 the lines have 3–7 points, since these cores
   are free with exponents (6, 6) by Theorem 2; otherwise 3–8):
   ```
   cc -O3 -march=native -DWORDSIZE=64 -I/opt/homebrew/include -o heavyaug_p heavyaug_p.c -L/opt/homebrew/lib -lnautyL1
   cc -O3 -march=native -o lsgen3 lsgen3.c
   ./heavyaug_p 13 6 5 9 30 0 100 0 1 0 1000 2 > core48_heavy.g6
   ./lsgen3 13 6 4 5 9 30 0 0 complete < core48_heavy.g6 > core48_raw.g6
   ./heavyaug_p 13 6 4 9 X 0 100 0 1 0 1000 2 > core_XX.g6               # X = 29 (core49_heavy.g6), 28, 27
   ./lsgen3 13 6 4 4 9 X 0 0 complete < core_XX.g6 > core_XX_raw.g6
   labelg -q -f"aaaaaaaaaaaaa" < RAW | sort -u > coreB.g6                  # lines kept as one cell
   PY ../cores/g6tojsonl.py 13 < coreB.g6 > coreB.jsonl
   ```
   Sizes (raw → classes): 213,339 → 21,164; 1,820,363 → 154,172; 12,276,119 → 738,023;
   65,691,853 → 2,916,332.
2. *Fast filters*: `PY .../recheck_resultant/full_recheck.py 13 coreB.jsonl p P cB_pp` for p < P
   (P = 10 for b₂ = 48, 49; 6 for 50, 51); one verdict line per core in `cB_pp.out`, deferred cores in
   `cB_pp_defer.jsonl`, tallies in `cB_pp.log`. The deferred cores, with the class in the index
   (`b48:30`), are `comp/dall_tagged.jsonl` (b₂ = 48–50) and `comp/d51_tagged.jsonl`.
3. *Components*: first `PY m2comp.py 13 dall_tagged.jsonl p 3 300 dall_comp_p.jsonl` and
   `PY m2comp2.py 13 d51_tagged.jsonl p 5 300 d51_comp_p.jsonl` (one Macaulay2 session per lattice), then
   the batched `PY m2compb.py 13 dall_tagged.jsonl p 2 300 dallb_comp_p.jsonl 25 dall_comp_*.jsonl` (and
   `... d51_tagged.jsonl p 6 ... d51b_comp_p.jsonl 25 d51_comp_*.jsonl`), which skips the lattices already
   done, so the shards of each class partition it. No timeout or error among the 186,771 deferred cores.
4. *Extension*: `PY runclass.py TAG P comp_TAG.jsonl` (b₂ = 50, 51; `launch_b51.sh`); for b₂ = 48, 49
   the same steps were run one by one (`extend.py comp_b4849.jsonl` → `ext_b4849_rigid.jsonl`, `famrun.py`
   → `famall_b4849_v*`, `dim2gen.py` → `dim2_b4849_ch*`, `d2c_*`, `runclass.py b49d2n15 2 --n=15 ...`).
   Family components that were slow or failed went through the lattice-level step:
   `slowroute.sh TAG N records family_outputs...` (logs `runclass_*slow*.log`), and the two child-level
   Macaulay2 timeouts of b₂ = 51 through `runclass.py b51to2 2 --n=14 b51_to2_forced.jsonl`.
5. *Collection and check*: `finalcheck.sh`: every rigid and family output (161 files, `final_files.txt`)
   → `collectL.py` → 16 distinct lattices up to isomorphism, 14 known and 2 new (`final_collect.txt`);
   `checkL.py` → `checked_L.jsonl`: each lattice one Galois orbit, rigid, non-free. `PY audit.py > audit.out`: no unrouted family failure, no rigid component
   without exact realisation, no special point without shape lemma, only the two settled timeouts.
   `PY rerun/compare_rerun.py > rerun/compare.out`: the rigid reruns give the same lattices.
6. *Covering lemma* (in `cover/ilp/`): `PY level1.py` (2,471 survivors), `PY level2.py p 4 120`,
   `PY farkas.py p 4 4` (exact certificates, 2,471 of 2,471), `PY propcheck.py p 4`, `PY validate.py
   ../phi1_all.g6 60`.
7. *No 8-point line* (in `n8zero/`): `PY k4444.py > k4444.jsonl`, `PY p5excl.py`,
   `PY pencil5b.py V > p5b_V.jsonl` for the five vectors V; then `full_recheck.py 17`, `m2compb.py 17`
   and `exact_tc_lattice.py 17 8` on what is deferred.

## results/

| archive | records | what |
|---|---|---|
| `core_components_b48_b49_b50.jsonl.gz` | 29,238 | Macaulay2 record of every deferred core of b₂ = 48, 49, 50: status REAL/NONREAL, the parametrisation (frame, statements), and for REAL the good minimal primes with dimension, degree, generators (shape lemma for dimension 0) |
| `core_components_b51.jsonl.gz` | 157,533 | the same for b₂ = 51 |
| `children_components.jsonl.gz` | 146,345 | the same for every child (14–16 lines) deferred by the fast filters in the extension runs; `_source` = shard file |

Built by `PY results/make_archives.py` (verbatim records; checked record by record against the shards).

## Not in git

`.gitignore` of this directory; every ignored file is listed in `manifest_excluded.tsv` (383 files,
9.3 GB: path, bytes, newline count, SHA-256). They are:

- compiled programs (built as in step 1), Macaulay2 scripts written by the Python drivers, `__pycache__`,
  debugging leftovers;
- raw enumerations and the core lists (`heavy/*_raw.g6` up to 4.7 GB, `cores*/core4[89]-5[01].{g6,jsonl}`,
  samples): step 1;
- the per-core and per-child fast-filter verdicts, the deferred lists, the children lists and the record
  files handed to the workers: steps 2–4 (`full_recheck.py`, `runclass.py`, `dim2gen.py`);
- the Macaulay2 component shards of cores and children: their records are in `results/`;
- `n8zero/p5b_43333.jsonl`, `p5b_44332.jsonl` (the lattice lists of the two largest vectors): step 7.
