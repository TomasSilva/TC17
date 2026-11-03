# Campaign report: rerun of the 17-line proof

Generated 2026-11-03 05:51:26 by `work/n17/campaign/report.py` from `done/*.json`. Log: `campaign.log`.

## Stages

| stage | status | finished | seconds | what |
|---|---|---|---|---|
| prep | done | 2026-11-02 20:14:25 | 0 | tools, compiled enumerators, SHA-256 of the code of record |
| cover | done | 2026-11-02 20:22:27 | 397 | covering lemma (ILP: level 1, Farkas certificates, propagation, glpsol, validation) |
| n8zero | done | 2026-11-02 20:28:44 | 378 | no 8-point line (K4444, five-point vectors, screening, Anghel-Stan) |
| cores | done | 2026-11-02 20:34:37 | 318 | core classes b48, b48w, b49, b50, b51 (heavyaug_p + lsgen3 + labelg), invariants, positive controls |
| indep_cores | done | 2026-11-02 20:39:56 | 319 | second enumerator (bigblocks + fill_triples) and comparison |
| filters | done | 2026-11-02 21:02:15 | 1339 | exact fast filters on every core |
| as_cores | done | 2026-11-02 21:05:56 | 221 | Anghel-Stan's code on every core |
| m2 | done | 2026-11-02 22:41:55 | 5758 | Macaulay2 components of the deferred cores; comparison with Anghel-Stan; filter-only cores confirmed |
| ext_b48 | done | 2026-11-02 22:43:01 | 66 | extension of class b48 |
| ext_b48w | done | 2026-11-02 22:44:37 | 95 | extension of class b48w (8-point lines allowed; the class the manuscript leaves open) |
| ext_b49 | done | 2026-11-02 22:54:59 | 623 | extension of class b49 |
| ext_b50 | done | 2026-11-03 00:57:47 | 7368 | extension of class b50 |
| ext_b51 | done | 2026-11-03 05:31:49 | 16442 | extension of class b51 |
| route_timeouts | done | 2026-11-03 05:35:28 | 13 | the cores/children on which Macaulay2 timed out, routed through the lattice-level step (as in October 2026); their children screened with Anghel-Stan |
| as_children | done | 2026-11-03 05:33:14 | 85 | Anghel-Stan's code on every child of the lattice-level step |
| indep_rigid | done | 2026-11-03 05:49:43 | 989 | independent numeric rigid search on every rigid component |
| final | done | 2026-11-03 05:49:54 | 11 | collection of the lattices found, exact realisation spaces and freeness, syzygy degrees, Anghel-Stan re-certification |
| report | not run |  |  | this report |

## Mismatches against the recorded values of 21-23 October 2026

| stage | check | got | expected |
|---|---|---|---|
| cover | propagation check: infeasible | 2333 | 2435 |
| cover | propagation check: open (settled by Farkas) | 138 | 36 |
| ext_b51 | Macaulay2 timeouts/errors among cores and children | 2 | 0 |

Explanations:

- **cover / propagation check: infeasible:** the figure 2,435 in the manuscripts came from an incomplete run of propcheck.py (its output files stop at system 614 of 2,471); the complete, deterministic run gives 2,333 refuted and 138 open, all 138 settled by the exact Farkas certificates. Both manuscripts corrected on 2 Nov 2026.
- **cover / propagation check: open (settled by Farkas):** same cause as the line above.
- **ext_b51 / Macaulay2 timeouts/errors among cores and children:** the expectation 0 was wrong: the run of October 2026 also had exactly two Macaulay2 timeouts, on the same two 14-line children of b51 (same canonical forms); the stage route_timeouts routes them through the lattice-level step as in October (142 children with 15 lines, none realisable, no 17-line lattice).

## Checks, stage by stage

### prep (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| git_head | "48c3e6bcc7811b4462fe60c72d43d3bef94e9329" | | recorded |
| M2 | "1.26.06" | | recorded |
| python | "3.12.14 python-flint 0.9.0 pynauty 2.8.8.1" | | recorded |
| labelg | "/opt/homebrew/bin/labelg" | | recorded |
| glpsol | "/opt/homebrew/bin/glpsol" | | recorded |
| ncpu | 10 | | recorded |
| sha256 | {"work/n17/heavy/heavyaug_p.c": "63c7eced1a14bb06c004d962f5a1995c94e385cd047af6a122824493c966e51b", "work/n17/heavy/lsgen3.c": "e5a0f87c9a07c87843a6a728e104935d1ae3c8b4ce349d307a69d5438866dac3", "work/n17/heavy/g6blocks.py": "ca394a029a50d79478352ac5d110e4c927dfe7d20247f25ceaec74f029e2f086", "work/t... | | recorded |
| AS_heavyaug_identical | null | | recorded |
| AS_lsgen3_identical | null | | recorded |
| Anghel-Stan code imports | "ok" | "ok" | OK |

### cover (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| level1 surviving delta-assignments | 2471 | 2471 | OK |
| Farkas certificates verified exactly | 2471 | 2471 | OK |
| Farkas certificates missing | 0 | 0 | OK |
| propagation check: infeasible | 2333 | 2435 | **MISMATCH** |
| propagation check: open (settled by Farkas) | 138 | 36 | **MISMATCH** |
| level2 glpsol verdicts | {"INFEASIBLE": 2471} | | recorded |
| level2 feasible or undecided | 0 | 0 | OK |
| validate.py (model evaluated on the 299 lattices with phi_max = 1) | "checked 299 lattices, with violations: 0" | | recorded |
| model violations on real lattices | 0 | 0 | OK |

### n8zero (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| K4444 triangle decompositions (lattices with a 4-point line) | 23 | 23 | OK |
| 5-point vector 55411: heavy configurations | 1 | n/a | OK |
| 5-point vector 55411: lattices | 0 | 0 | OK |
| 5-point vector 55321: heavy configurations | 1 | n/a | OK |
| 5-point vector 55321: lattices | 0 | 0 | OK |
| 5-point vector 55222: heavy configurations | 3 | n/a | OK |
| 5-point vector 55222: lattices | 0 | 0 | OK |
| 5-point vector 54421: heavy configurations | 5 | n/a | OK |
| 5-point vector 54421: lattices | 0 | 0 | OK |
| 5-point vector 54331: heavy configurations | 26 | n/a | OK |
| 5-point vector 54331: lattices | 0 | 0 | OK |
| 5-point vector 54322: heavy configurations | 379 | n/a | OK |
| 5-point vector 54322: lattices | 0 | 0 | OK |
| 5-point vector 53332: heavy configurations | 2303 | 2303 | OK |
| 5-point vector 53332: lattices | 0 | 0 | OK |
| 5-point vector 44431: heavy configurations | 87 | 87 | OK |
| 5-point vector 44431: lattices | 122 | 122 | OK |
| 5-point vector 44422: heavy configurations | 863 | 863 | OK |
| 5-point vector 44422: lattices | 232 | 232 | OK |
| 5-point vector 44332: heavy configurations | 49565 | 49565 | OK |
| 5-point vector 44332: lattices | 3124 | 3124 | OK |
| 5-point vector 43333: heavy configurations | 192133 | 192133 | OK |
| 5-point vector 43333: lattices | 7723 | 7723 | OK |
| lattices without an 8-point line to screen | 11224 | 11224 | OK |
| invariants (b2 = 80, m <= 6, 4-7 points, W5, isomorphism classes) | {"n": 17, "b2": 80, "points_per_line": [4, 7], "mmax": 6, "cut": true, "w4": true, "total": 11224, "distinct": 11224, "violations": {}, "max_points_on_a_line": {"7": 11224}, "line_profiles": 5, "multiplicity_profiles": 7, "commonest_profiles": [["77777777777777775", 9455], ["77777777777777765", 1649... | | recorded |
| invariant violations | 0 | 0 | OK |
| distinct lattices (pynauty) | 11224 | 11224 | OK |
| screening | {"lattices": 11224, "verdict_lines": 11224, "filter_stats": {"NONREAL": 10320, "DEFER": 904}, "deferred": 904, "m2_status": {"NONREAL": 904}, "m2_records": 904} | | recorded |
| verdict lines | 11224 | 11224 | OK |
| realisable lattices (Macaulay2) | 0 | 0 | OK |
| Macaulay2 timeouts/errors | 0 | 0 | OK |
| Macaulay2 records | 904 | 904 | OK |
| no-8-point-line lattices: ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 11224} | | recorded |
| no-8-point-line lattices: disagreements with Anghel-Stan | 0 | 0 | OK |
| no-8-point-line lattices: lattices without a verdict of ours | 0 | 0 | OK |

### cores (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| b48 heavy configurations | 258 | 258 | OK |
| b48 raw completions | 213339 | 213339 | OK |
| b48 lattices up to isomorphism | 21164 | 21164 | OK |
| b48 jsonl records | 21164 | 21164 | OK |
| b48 invariants | {"n": 13, "b2": 48, "points_per_line": [3, 7], "mmax": 6, "cut": true, "w4": false, "total": 21164, "distinct": 21164, "violations": {}, "max_points_on_a_line": {"6": 913, "7": 20251}, "line_profiles": 108, "multiplicity_profiles": 35, "commonest_profiles": [["7766666655554", 2151], ["7766666665554"... | | recorded |
| b48 invariant violations | 0 | 0 | OK |
| b48 distinct certificates (pynauty) = class size | 21164 | 21164 | OK |
| b48w heavy configurations | 260 | n/a | OK |
| b48w raw completions | 250572 | n/a | OK |
| b48w lattices up to isomorphism | 26234 | n/a | OK |
| b48w jsonl records | 26234 | 26234 | OK |
| b48w invariants | {"n": 13, "b2": 48, "points_per_line": [3, 8], "mmax": 6, "cut": true, "w4": false, "total": 26234, "distinct": 26234, "violations": {}, "max_points_on_a_line": {"6": 913, "7": 20251, "8": 5070}, "line_profiles": 203, "multiplicity_profiles": 35, "commonest_profiles": [["7766666655554", 2151], ["776... | | recorded |
| b48w invariant violations | 0 | 0 | OK |
| b48w distinct certificates (pynauty) = class size | 26234 | 26234 | OK |
| b49 heavy configurations | 274 | 274 | OK |
| b49 raw completions | 1820363 | 1820363 | OK |
| b49 lattices up to isomorphism | 154172 | 154172 | OK |
| b49 jsonl records | 154172 | 154172 | OK |
| b49 invariants | {"n": 13, "b2": 49, "points_per_line": [3, 8], "mmax": 6, "cut": true, "w4": false, "total": 154172, "distinct": 154172, "violations": {}, "max_points_on_a_line": {"6": 498, "7": 92180, "8": 61494}, "line_profiles": 301, "multiplicity_profiles": 36, "commonest_profiles": [["7776666655555", 7807], ["... | | recorded |
| b49 invariant violations | 0 | 0 | OK |
| b49 distinct certificates (pynauty) = class size | 154172 | 154172 | OK |
| b50 heavy configurations | 284 | n/a | OK |
| b50 raw completions | 12276119 | 12276119 | OK |
| b50 lattices up to isomorphism | 738023 | 738023 | OK |
| b50 jsonl records | 738023 | 738023 | OK |
| b50 invariants | {"n": 13, "b2": 50, "points_per_line": [3, 8], "mmax": 6, "cut": true, "w4": false, "total": 738023, "distinct": 738023, "violations": {}, "max_points_on_a_line": {"6": 118, "7": 289381, "8": 448524}, "line_profiles": 412, "multiplicity_profiles": 38, "commonest_profiles": [["8777666665555", 40857],... | | recorded |
| b50 invariant violations | 0 | 0 | OK |
| b50 distinct certificates (pynauty) = class size | 738023 | 738023 | OK |
| b51 heavy configurations | 285 | n/a | OK |
| b51 raw completions | 65691853 | 65691853 | OK |
| b51 lattices up to isomorphism | 2916332 | 2916332 | OK |
| b51 jsonl records | 2916332 | 2916332 | OK |
| b51 invariants | {"n": 13, "b2": 51, "points_per_line": [3, 8], "mmax": 6, "cut": true, "w4": false, "total": 2916332, "distinct": 2916332, "violations": {}, "max_points_on_a_line": {"6": 10, "7": 673072, "8": 2243250}, "line_profiles": 439, "multiplicity_profiles": 39, "commonest_profiles": [["8777766666555", 20556... | | recorded |
| b51 invariant violations | 0 | 0 | OK |
| b51 distinct certificates (pynauty) = class size | 2916332 | 2916332 | OK |
| positive controls | {"cores13": 28, "cores13_in_b48": 28, "chains_per_lattice": [30, 12, 11, 12, 13, 1, 1, 1, 1, 1, 5, 8, 7, 9, 6, 1], "chain_cores": 33, "chain_cores_in_b48": 33, "b48_subset_of_b48w": true, "b48w_minus_b48": 5070, "b48": 21164, "b48w": 26234} | | recorded |
| known cores (work/n17/validate/cores13.jsonl) present in b48 | 28 | 28 | OK |
| phi-max cores of the 16 lattices present in b48 | 33 | 33 | OK |
| b48 is a subset of b48w | true | true | OK |
| b48w lattices with an 8-point line | 5070 | | recorded |

### indep_cores (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| b48 comparison | "a48: heavyaug+lsgen3 21164 distinct, ours 21164 distinct, common 21164, only heavyaug 0, only ours 0 (of which with an unjoined heavy pair t > 8: 0)" | | recorded |
| b48: lattices found only by heavyaug+lsgen3 | 0 | 0 | OK |
| b48: lattices found only by the second enumerator and not explained by the cut | 0 | 0 | OK |
| b48: lattices removed by the unjoined-pair cut | 0 | 0 | OK |
| b48w comparison | "a48w: heavyaug+lsgen3 26234 distinct, ours 26234 distinct, common 26234, only heavyaug 0, only ours 0 (of which with an unjoined heavy pair t > 8: 0)" | | recorded |
| b48w: lattices found only by heavyaug+lsgen3 | 0 | 0 | OK |
| b48w: lattices found only by the second enumerator and not explained by the cut | 0 | 0 | OK |
| b48w: lattices removed by the unjoined-pair cut | 0 | n/a | OK |
| b49 comparison | "a49: heavyaug+lsgen3 154172 distinct, ours 154172 distinct, common 154172, only heavyaug 0, only ours 0 (of which with an unjoined heavy pair t > 8: 0)" | | recorded |
| b49: lattices found only by heavyaug+lsgen3 | 0 | 0 | OK |
| b49: lattices found only by the second enumerator and not explained by the cut | 0 | 0 | OK |
| b49: lattices removed by the unjoined-pair cut | 0 | 0 | OK |
| b50 comparison | "a50: heavyaug+lsgen3 738023 distinct, ours 738023 distinct, common 738023, only heavyaug 0, only ours 0 (of which with an unjoined heavy pair t > 8: 0)" | | recorded |
| b50: lattices found only by heavyaug+lsgen3 | 0 | 0 | OK |
| b50: lattices found only by the second enumerator and not explained by the cut | 0 | 0 | OK |
| b50: lattices removed by the unjoined-pair cut | 0 | 0 | OK |
| b51 comparison | "a51: heavyaug+lsgen3 2916332 distinct, ours 2916339 distinct, common 2916332, only heavyaug 0, only ours 7 (of which with an unjoined heavy pair t > 8: 7)" | | recorded |
| b51: lattices found only by heavyaug+lsgen3 | 0 | 0 | OK |
| b51: lattices found only by the second enumerator and not explained by the cut | 0 | 0 | OK |
| b51: lattices removed by the unjoined-pair cut | 7 | 7 | OK |

### filters (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| b48 verdicts | {"NONREAL": 20969, "DEFER": 195} | | recorded |
| b48 verdict lines = class size | 21164 | 21164 | OK |
| b48 deferred to Macaulay2 | 195 | 195 | OK |
| b48w verdicts | {"NONREAL": 25985, "DEFER": 249} | | recorded |
| b48w verdict lines = class size | 26234 | 26234 | OK |
| b48w deferred to Macaulay2 | 249 | n/a | OK |
| b49 verdicts | {"DEFER": 2950, "NONREAL": 151222} | | recorded |
| b49 verdict lines = class size | 154172 | 154172 | OK |
| b49 deferred to Macaulay2 | 2950 | 2950 | OK |
| b50 verdicts | {"DEFER": 26093, "NONREAL": 711930} | | recorded |
| b50 verdict lines = class size | 738023 | 738023 | OK |
| b50 deferred to Macaulay2 | 26093 | 26093 | OK |
| b51 verdicts | {"DEFER": 157533, "NONREAL": 2758799} | | recorded |
| b51 verdict lines = class size | 2916332 | 2916332 | OK |
| b51 deferred to Macaulay2 | 157533 | 157533 | OK |

### as_cores (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| b48 Anghel-Stan statuses | {"empty-family-degenerate": 12, "empty": 20994, "family": 41, "points": 43, "empty-degenerate": 72, "cost>1": 2} | | recorded |
| b48 Anghel-Stan verdict lines = class size | 21164 | 21164 | OK |
| b48w Anghel-Stan statuses | {"empty-family-degenerate": 14, "empty": 26027, "points": 43, "cost>1": 27, "empty-degenerate": 82, "family": 41} | | recorded |
| b48w Anghel-Stan verdict lines = class size | 26234 | 26234 | OK |
| b49 Anghel-Stan statuses | {"family": 542, "empty": 152118, "cost>1": 181, "points": 571, "empty-family-degenerate": 305, "empty-degenerate": 455} | | recorded |
| b49 Anghel-Stan verdict lines = class size | 154172 | 154172 | OK |
| b50 Anghel-Stan statuses | {"cost>1": 1006, "family": 3751, "empty-family-degenerate": 3114, "empty": 723251, "points": 5155, "empty-degenerate": 1746} | | recorded |
| b50 Anghel-Stan verdict lines = class size | 738023 | 738023 | OK |
| b51 Anghel-Stan statuses | {"cost>1": 6528, "family": 18702, "empty-family-degenerate": 16329, "empty": 2830716, "points": 37824, "empty-degenerate": 6233} | | recorded |
| b51 Anghel-Stan verdict lines = class size | 2916332 | 2916332 | OK |

### m2 (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| deferred cores (all classes) | 187020 | | recorded |
| Macaulay2 records = deferred cores | 187020 | 187020 | OK |
| b48 statuses | {"REAL": 85, "NONREAL": 110} | | recorded |
| b48 realisable cores | 85 | 85 | OK |
| b48 Macaulay2 timeouts/errors | 0 | 0 | OK |
| b48 cores with rigid / curve / surface components | [80, 5, 0] | [80, 5, 0] | OK |
| b48: ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 21078, "AS REAL / ours REAL": 84, "AS cost>1 / ours NONREAL": 1, "AS cost>1 / ours REAL": 1} | | recorded |
| b48: disagreements with Anghel-Stan | 0 | 0 | OK |
| b48: lattices without a verdict of ours | 0 | 0 | OK |
| b48w statuses | {"REAL": 85, "NONREAL": 164} | | recorded |
| b48w realisable cores | 85 | n/a | OK |
| b48w Macaulay2 timeouts/errors | 0 | 0 | OK |
| b48w cores with rigid / curve / surface components | [80, 5, 0] | n/a | OK |
| b48w: ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 26123, "AS REAL / ours REAL": 84, "AS cost>1 / ours NONREAL": 26, "AS cost>1 / ours REAL": 1} | | recorded |
| b48w: disagreements with Anghel-Stan | 0 | 0 | OK |
| b48w: lattices without a verdict of ours | 0 | 0 | OK |
| b49 statuses | {"REAL": 1147, "NONREAL": 1803} | | recorded |
| b49 realisable cores | 1147 | 1147 | OK |
| b49 Macaulay2 timeouts/errors | 0 | 0 | OK |
| b49 cores with rigid / curve / surface components | [1050, 83, 14] | [1050, 83, 14] | OK |
| b49: ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 152878, "AS REAL / ours REAL": 1113, "AS cost>1 / ours NONREAL": 147, "AS cost>1 / ours REAL": 34} | | recorded |
| b49: disagreements with Anghel-Stan | 0 | 0 | OK |
| b49: lattices without a verdict of ours | 0 | 0 | OK |
| b50 statuses | {"REAL": 9162, "NONREAL": 16931} | | recorded |
| b50 realisable cores | 9162 | 9162 | OK |
| b50 Macaulay2 timeouts/errors | 0 | 0 | OK |
| b50 cores with rigid / curve / surface components | [7985, 1091, 86] | [7985, 1091, 86] | OK |
| b50: ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 728111, "AS REAL / ours REAL": 8906, "AS cost>1 / ours NONREAL": 750, "AS cost>1 / ours REAL": 256} | | recorded |
| b50: disagreements with Anghel-Stan | 0 | 0 | OK |
| b50: lattices without a verdict of ours | 0 | 0 | OK |
| b51 statuses | {"NONREAL": 98662, "REAL": 58871} | | recorded |
| b51 realisable cores | 58871 | 58871 | OK |
| b51 Macaulay2 timeouts/errors | 0 | 0 | OK |
| b51 cores with rigid / curve / surface components | [49118, 9001, 752] | [49118, 9001, 752] | OK |
| b51: ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 2853278, "AS REAL / ours REAL": 56526, "AS cost>1 / ours NONREAL": 4183, "AS cost>1 / ours REAL": 2345} | | recorded |
| b51: disagreements with Anghel-Stan | 0 | 0 | OK |
| b51: lattices without a verdict of ours | 0 | 0 | OK |
| cores rejected by our filters only and undecided by Anghel-Stan (sent to Macaulay2) | 2944 | | recorded |
| filter-only cores: Macaulay2 statuses | {"NONREAL": 2944} | | recorded |
| filter-only cores confirmed non-realisable by Macaulay2 | 2944 | 2944 | OK |

### ext_b48 (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| runclass log | ["22:41:55 records 195 REAL 85 other (timeout/error) 0", "22:41:55 n=13 rigid 80, dim1 5, dim>=2 0", "22:41:58 n=13 rigid done", "22:41:58 n=13 rigid components: 80 expected, 80 finished", "22:43:01 n=13 family components: 5 expected, 5 finished", "22:43:01 n=13 families done; 0 family records sent ... | | recorded |
| worker failures | 0 | 0 | OK |
| components missing a completion record | 0 | 0 | OK |
| dim2gen failures | 0 | 0 | OK |
| pipeline finished | true | true | OK |
| rigid components finished | 80 | | recorded |
| family component statuses | {"OK": 5} | | recorded |
| 17-line lattice records accepted by the window test | 106 | | recorded |
| 17-line lattices rejected by the window test | 0 | 0 | OK |
| rejection reasons | {} | | recorded |
| Macaulay2 timeouts/errors among cores and children | 0 | 0 | OK |
| children generated at the lattice level | {} | | recorded |

### ext_b48w (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| runclass log | ["22:43:01 records 249 REAL 85 other (timeout/error) 0", "22:43:01 n=13 rigid 80, dim1 5, dim>=2 0", "22:43:05 n=13 rigid done", "22:43:05 n=13 rigid components: 80 expected, 80 finished", "22:44:37 n=13 family components: 5 expected, 5 finished", "22:44:37 n=13 families done; 0 family records sent ... | | recorded |
| worker failures | 0 | 0 | OK |
| components missing a completion record | 0 | 0 | OK |
| dim2gen failures | 0 | 0 | OK |
| pipeline finished | true | true | OK |
| rigid components finished | 80 | | recorded |
| family component statuses | {"OK": 5} | | recorded |
| 17-line lattice records accepted by the window test | 106 | | recorded |
| 17-line lattices rejected by the window test | 0 | 0 | OK |
| rejection reasons | {} | | recorded |
| Macaulay2 timeouts/errors among cores and children | 0 | 0 | OK |
| children generated at the lattice level | {} | | recorded |

### ext_b49 (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| runclass log | ["22:44:37 records 2950 REAL 1147 other (timeout/error) 0", "22:44:37 n=13 rigid 1050, dim1 83, dim>=2 14", "22:45:17 n=13 rigid done", "22:45:17 n=13 rigid components: 1050 expected, 1050 finished", "22:50:09 n=13 family components: 83 expected, 83 finished", "22:50:09 n=13 families done; 1 family ... | | recorded |
| worker failures | 0 | 0 | OK |
| components missing a completion record | 0 | 0 | OK |
| dim2gen failures | 0 | 0 | OK |
| pipeline finished | true | true | OK |
| rigid components finished | 2525 | | recorded |
| family component statuses | {"OK": 267, "SLOW": 2} | | recorded |
| 17-line lattice records accepted by the window test | 0 | | recorded |
| 17-line lattices rejected by the window test | 0 | 0 | OK |
| rejection reasons | {} | | recorded |
| Macaulay2 timeouts/errors among cores and children | 0 | 0 | OK |
| children generated at the lattice level | {"b49_n13_ch.jsonl": 6608, "b49_n14_ch.jsonl": 5314, "b49_n15_ch.jsonl": 153} | | recorded |

### ext_b50 (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| runclass log | ["22:55:00 records 26093 REAL 9162 other (timeout/error) 0", "22:55:00 n=13 rigid 7985, dim1 1091, dim>=2 86", "22:57:28 n=13 rigid done", "22:57:28 n=13 rigid components: 7985 expected, 7985 finished", "23:35:53 n=13 family components: 1091 expected, 1091 finished", "23:35:53 n=13 families done; 26... | | recorded |
| worker failures | 0 | 0 | OK |
| components missing a completion record | 0 | 0 | OK |
| dim2gen failures | 0 | 0 | OK |
| pipeline finished | true | true | OK |
| rigid components finished | 22788 | | recorded |
| family component statuses | {"OK": 3123, "SLOW": 97, "NOMODEL": 4} | | recorded |
| 17-line lattice records accepted by the window test | 0 | | recorded |
| 17-line lattices rejected by the window test | 0 | 0 | OK |
| rejection reasons | {} | | recorded |
| Macaulay2 timeouts/errors among cores and children | 0 | 0 | OK |
| children generated at the lattice level | {"b50_n13_ch.jsonl": 102705, "b50_n14_ch.jsonl": 64180, "b50_n15_ch.jsonl": 55} | | recorded |

### ext_b51 (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| runclass log | ["00:57:49 records 157533 REAL 58871 other (timeout/error) 0", "00:57:49 n=13 rigid 49118, dim1 9001, dim>=2 752", "01:01:07 n=13 rigid done", "01:01:07 n=13 rigid components: 49118 expected, 49118 finished", "03:23:58 n=13 family components: 9001 expected, 9001 finished", "03:23:58 n=13 families do... | | recorded |
| worker failures | 0 | 0 | OK |
| components missing a completion record | 0 | 0 | OK |
| dim2gen failures | 0 | 0 | OK |
| pipeline finished | true | true | OK |
| rigid components finished | 74102 | | recorded |
| family component statuses | {"OK": 11257, "SLOW": 179, "NOMODEL": 8} | | recorded |
| 17-line lattice records accepted by the window test | 0 | | recorded |
| 17-line lattices rejected by the window test | 0 | 0 | OK |
| rejection reasons | {} | | recorded |
| Macaulay2 timeouts/errors among cores and children | 2 | 0 | **MISMATCH** |
| children generated at the lattice level | {"b51_n13_ch.jsonl": 357086, "b51_n14_ch.jsonl": 4093} | | recorded |

### route_timeouts (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| Macaulay2 timeouts/errors to route | {"b51 n=14": 2} | | recorded |
| timeouts/errors outside b51 at 14 lines | 0 | 0 | OK |
| the b51 timeouts are the same two 14-line lattices as in October 2026 | true | true | OK |
| b51to2 runclass log | ["05:35:14 records 2 REAL 2 other (timeout/error) 0", "05:35:14 n=14 rigid 0, dim1 0, dim>=2 2", "05:35:14 n=14 rigid done", "05:35:14 n=14 rigid components: 0 expected, 0 finished", "05:35:15 n=14 family components: 0 expected, 0 finished", "05:35:15 n=14 families done; 0 family records sent to the... | | recorded |
| b51to2 worker failures | 0 | 0 | OK |
| b51to2 components missing a completion record | 0 | 0 | OK |
| b51to2 dim2gen failures | 0 | 0 | OK |
| b51to2 pipeline finished | true | true | OK |
| b51to2 17-line lattice records accepted by the window test | 0 | | recorded |
| b51to2 17-line lattices rejected by the window test | 0 | 0 | OK |
| b51to2 rejection reasons | {} | | recorded |
| b51to2 Macaulay2 timeouts/errors among the routed children | 0 | 0 | OK |
| b51to2 children generated at the lattice level | {"b51to2_n14_ch.jsonl": 142} | | recorded |
| b51to2_n14 (15 lines): ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 142} | | recorded |
| b51to2_n14 (15 lines): disagreements with Anghel-Stan | 0 | 0 | OK |
| b51to2_n14 (15 lines): lattices without a verdict of ours | 0 | 0 | OK |
| children of the routed records screened by Anghel-Stan | 142 | | recorded |

### as_children (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| b49_n13 (14 lines): ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 5168, "AS REAL / ours REAL": 1341, "AS cost>1 / ours NONREAL": 64, "AS cost>1 / ours REAL": 35} | | recorded |
| b49_n13 (14 lines): disagreements with Anghel-Stan | 0 | 0 | OK |
| b49_n13 (14 lines): lattices without a verdict of ours | 0 | 0 | OK |
| b49_n13: filter-only children confirmed non-realisable by Macaulay2 | 51 | 51 | OK |
| b49_n14 (15 lines): ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 5015, "AS REAL / ours REAL": 286, "AS cost>1 / ours NONREAL": 7, "AS cost>1 / ours REAL": 6} | | recorded |
| b49_n14 (15 lines): disagreements with Anghel-Stan | 0 | 0 | OK |
| b49_n14 (15 lines): lattices without a verdict of ours | 0 | 0 | OK |
| b49_n14: filter-only children confirmed non-realisable by Macaulay2 | 4 | 4 | OK |
| b49_n15 (16 lines): ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 152, "AS REAL / ours REAL": 1} | | recorded |
| b49_n15 (16 lines): disagreements with Anghel-Stan | 0 | 0 | OK |
| b49_n15 (16 lines): lattices without a verdict of ours | 0 | 0 | OK |
| b50_n13 (14 lines): ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 85990, "AS REAL / ours REAL": 15851, "AS cost>1 / ours NONREAL": 426, "AS cost>1 / ours REAL": 438} | | recorded |
| b50_n13 (14 lines): disagreements with Anghel-Stan | 0 | 0 | OK |
| b50_n13 (14 lines): lattices without a verdict of ours | 0 | 0 | OK |
| b50_n13: filter-only children confirmed non-realisable by Macaulay2 | 269 | 269 | OK |
| b50_n14 (15 lines): ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 63422, "AS REAL / ours REAL": 735, "AS cost>1 / ours NONREAL": 17, "AS cost>1 / ours REAL": 6} | | recorded |
| b50_n14 (15 lines): disagreements with Anghel-Stan | 0 | 0 | OK |
| b50_n14 (15 lines): lattices without a verdict of ours | 0 | 0 | OK |
| b50_n14: filter-only children confirmed non-realisable by Macaulay2 | 12 | 12 | OK |
| b50_n15 (16 lines): ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 55} | | recorded |
| b50_n15 (16 lines): disagreements with Anghel-Stan | 0 | 0 | OK |
| b50_n15 (16 lines): lattices without a verdict of ours | 0 | 0 | OK |
| b51_n13 (14 lines): ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 329064, "AS EMPTY / ours TIMEOUT": 1, "AS REAL / ours REAL": 26978, "AS REAL / ours TIMEOUT": 1, "AS cost>1 / ours NONREAL": 525, "AS cost>1 / ours REAL": 517} | | recorded |
| b51_n13 (14 lines): disagreements with Anghel-Stan | 0 | 0 | OK |
| b51_n13 (14 lines): lattices without a verdict of ours | 0 | 0 | OK |
| b51_n13: filter-only children confirmed non-realisable by Macaulay2 | 356 | 356 | OK |
| b51_n14 (15 lines): ours vs Anghel-Stan | {"AS EMPTY / ours NONREAL": 4066, "AS REAL / ours REAL": 27} | | recorded |
| b51_n14 (15 lines): disagreements with Anghel-Stan | 0 | 0 | OK |
| b51_n14 (15 lines): lattices without a verdict of ours | 0 | 0 | OK |
| children screened | 540194 | | recorded |

### indep_rigid (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| records with a rigid component | 99573 | | recorded |
| comparison | {"exact_components": 99575, "numeric_components": 99575, "compared": 99575, "differing": 0, "examples": [], "lattice_mismatch": 0, "errors": 0, "ambiguous": 0, "numeric_only_components": 0, "distinct_lattices_exact": 16, "distinct_lattices_numeric": 16} | | recorded |
| rigid components compared | 99575 | 99575 | OK |
| components whose lattice sets differ | 0 | 0 | OK |
| numeric realisation not reproducing the core lattice | 0 | 0 | OK |
| numeric errors | 0 | 0 | OK |
| ambiguous incidences (recomputed in 50 digits) | 0 | | recorded |

### final (done)

| check | value | recorded value (Oct 2026) | |
|---|---|---|---|
| collection | {"accepted_records": 212, "rejected_records": 0, "distinct": 16, "known": 16, "new": 0, "known_missing": 0, "rejected_distinct": 0, "per_class": {"b48": 16, "b48w": 16}} | | recorded |
| distinct 17-line lattices accepted by the window test | 16 | 16 | OK |
| of which among the 16 of work/n17/run/checked_L.jsonl | 16 | 16 | OK |
| new lattices | 0 | 0 | OK |
| lattices rejected by the window test (distinct) | 0 | 0 | OK |
| the 16 known lattices all found | 0 | 0 | OK |
| lattices found per class | {"b48": 16, "b48w": 16} | | recorded |
| window and 4-chain check of the lattices found | {"n": 16, "window_with_4chain": 16, "per": [{"idx": 0, "known": "del17.jsonl:10", "window": true, "conditions": {"W1_b2": true, "W2_mult": true, "W3_lines": true, "W4_double": true, "W5_unjoined": true}, "phi_max": 4, "four_chains": 30, "D_pairs": 0, "profile": "88888888777777774", "multiplicities":... | | recorded |
| lattices found that are window lattices with phi_max = 4 and a 4-chain | 16 | 16 | OK |
| exact_tc_lattice verdicts | {"0": ["LATTICE 0 components 1 good 1 dims {0} zerobad 0", "COMP dim 0 degree 2 rank 15/16 NONFREE"], "10": ["LATTICE 10 components 3 good 1 dims {0} zerobad 0", "COMP dim 0 degree 2 rank 15/16 NONFREE"], "1": ["LATTICE 1 components 1 good 1 dims {0} zerobad 0", "COMP dim 0 degree 1 rank 15/16 NONFR... | | recorded |
| lattices with every component NONFREE (exact_tc_lattice) | 16 | 16 | OK |
| lattices with a FREE or MIXED component | 0 | 0 | OK |
| exact_tc_lattice errors | 0 | 0 | OK |
| freecheck (Macaulay2: realisation over K, lattice reproduced, minimal syzygy degrees) | {"0": {"lattice_ok": true, "degrees": [7, 10, 10], "field": "Q[T]/({75, -15, 1})", "free": false, "error": null}, "5": {"lattice_ok": true, "degrees": [7, 10, 10], "field": "Q[T]/({4, -2, 1})", "free": false, "error": null}, "10": {"lattice_ok": true, "degrees": [7, 10, 10], "field": "Q[T]/({25, -5,... | | recorded |
| freecheck: realisations reproduce their lattice | 16 | 16 | OK |
| freecheck: non-free with minimal syzygy degrees (7, 10, 10) | 16 | 16 | OK |
| freecheck: free realisations | 0 | 0 | OK |
| Anghel-Stan re-certification | {"0": {"status": "points", "comps": [[2, "nonfree"]]}, "1": {"status": "family-point", "comps": [[1, "nonfree"]]}, "2": {"status": "family-point", "comps": [[1, "nonfree"]]}, "3": {"status": "family-point", "comps": [[1, "nonfree"]]}, "4": {"status": "family-point", "comps": [[1, "nonfree"]]}, "5": ... | | recorded |
| Anghel-Stan: lattices realisable with every component certified nonfree | 16 | 16 | OK |

