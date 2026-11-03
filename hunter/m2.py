"""
m2.py -- exact verification with Macaulay2 over QQ (or a number field).

`m2_free(normals)` runs Macaulay2's HyperplaneArrangements package:
D(A) = der A, and reports whether the module is free, its generator
degrees and Betti table.  Normals are integer (or rational string) vectors.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
import textwrap

M2 = "/opt/homebrew/bin/M2"
VARS = "abcdefghij"


def _forms(normals, var_names):
    out = []
    for v in normals:
        terms = []
        for c, x in zip(v, var_names):
            c = str(c)
            if c in ("0", "0/1"):
                continue
            terms.append(f"({c})*{x}")
        out.append("+".join(terms) if terms else "0")
    return out


def m2_script(normals, field="QQ", extra_ring="", hilbert_upto=None):
    l = len(normals[0])
    names = [f"x{i}" for i in range(l)]
    forms = _forms(normals, names)
    hf = ""
    if hilbert_upto is not None:
        hf = f'print("HF " | toString apply(0..{hilbert_upto}, k -> hilbertFunction(k, M)));'
    return textwrap.dedent(f"""
    needsPackage "HyperplaneArrangements";
    {extra_ring}
    R = {field}[{",".join(names)}];
    A = arrangement {{{",".join(forms)}}};
    D = der A;
    M = prune image D;
    print("FREE " | toString isFreeModule M);
    print("GENS " | toString flatten degrees source mingens image D);
    print("BETTI " | toString betti res M);
    {hf}
    """)


def run_m2(script: str, timeout=3600):
    with tempfile.NamedTemporaryFile("w", suffix=".m2", delete=False) as fh:
        fh.write(script)
        path = fh.name
    try:
        out = subprocess.run([M2, "--script", path], capture_output=True,
                             text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-3000:])
    return out.stdout


def m2_free(normals, field="QQ", extra_ring="", hilbert_upto=None, timeout=3600):
    txt = run_m2(m2_script(normals, field, extra_ring, hilbert_upto), timeout)
    res = {"raw": txt}
    for line in txt.splitlines():
        if line.startswith("FREE "):
            res["free"] = line[5:].strip() == "true"
        elif line.startswith("GENS "):
            res["gens"] = line[5:].strip()
        elif line.startswith("BETTI "):
            res["betti"] = line[6:].strip()
        elif line.startswith("HF "):
            res["hf"] = [int(x) for x in line[3:].strip(" {}()").split(",")]
    return res
