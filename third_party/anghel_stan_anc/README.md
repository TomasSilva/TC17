# Ancillary files of Anghel–Stan (arXiv:2610.25868)

Not included in this repository. The audit scripts `work/n17/audit/asscreen/as_screen.py`,
`work/n17/audit/children/children_check.py`, `work/n17/audit/lat/children_check_lat.py`,
`work/n17/audit/n8zero/n8_check.py` and `work/n17/audit/final16/recertify.py` import `realize.py`,
`exact.py` and `g6util.py` from the directory `anc/` of those ancillary files: download them from
https://arxiv.org/abs/2610.25868 (ancillary files) and unpack them so that `anc/` sits in this directory,
i.e. `third_party/anghel_stan_anc/anc/realize.py` etc.

The two C enumerators `heavyaug.c` and `lsgen3.c` of the same ancillary files are kept, unmodified, as
`work/n17/heavy/heavyaug_orig.c` and `work/n17/heavy/lsgen3.c`; our modifications of them are the other
`.c` files of that directory (see `work/n17/MANIFEST.md`).
