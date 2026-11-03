# Re-check of the resultant branch of the exact filters (20 Oct 2026)

Flaw: in the two-parameter branch of `fast_real.py` (pass 1) and `fast_real2.py` (pass 2), the
resultant with respect to u1 of two equations that are both free of u1 is 1 (python-flint
convention), so the gcd G became constant and the lattice was declared NONREAL although u0 may be
a common root of the two univariate equations.  Pointed out by an AI review of the manuscript.

Fix (`fast_real_fix.py`, `recheck_pass2.py`): an equation free of u1 enters G directly as a
univariate condition; resultants only for pairs of equations that both involve u1.  Same index
ranges as the original loops.  Everything else unchanged.

Re-classified: every lattice rejected through that branch in the original runs, taken from the
per-lattice verdict files:
- pass 1 `NONREAL res`: 220,259 (15;7,7) [idx_res_n15.txt], 487,244 (16;7,8) [idx_res_n16.txt];
- pass 2 `NONREAL res2`: 65,802 (15;7,7), 148,991 (16;7,8).
Outcome (logs rc15_*.log, rc16_*.log): all remain NONREAL by the corrected exact arguments except
4 lattices of (15;7,7) from pass 2 (`flipped15.jsonl`, original indices 244334, 244335, 244677,
244678).  Macaulay2 (`exact_tc_lattice.py`, output `flipped15_tc_0.out`): each has one component
and it contains a degeneracy polynomial -> no complex realisation.  Anghel-Stan's screening code
(arXiv:2610.25868 ancillary files) also returns `empty` for all four.
So the realisable lists and Theorems 10.1-10.4 of TC_ATTEMPT.md are unaffected.
