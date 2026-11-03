"""
restrict.py -- Ziegler restriction of a rank-4 arrangement onto one of its
planes, as a rank-3 multiarrangement (lines in the plane P with multiplicity
= number of other planes meeting P in that line).
"""
from __future__ import annotations

import numpy as np

from .core import hyperplane_basis, Lattice


def ziegler_restriction(A, i, p):
    A = np.asarray(A, dtype=np.int64) % p
    Bp = hyperplane_basis(A[i], p)            # (l-1, l): basis of the hyperplane P_i
    groups = {}
    for j in range(A.shape[0]):
        if j == i:
            continue
        v = np.array([int(A[j] @ Bp[k] % p) for k in range(Bp.shape[0])], dtype=np.int64) % p
        # normalise
        e = next(k for k in range(len(v)) if v[k])
        inv = pow(int(v[e]), p - 2, p)
        key = tuple(int(x) * inv % p for x in v)
        groups.setdefault(key, []).append(j)
    normals = np.array(list(groups.keys()), dtype=np.int64)
    mult = [len(v) for v in groups.values()]
    return normals, mult, list(groups.values())


def heavy_lines(normals, mult, p):
    """Locally heavy lines (Abe-Kuhne): m(L0) >= sum of other multiplicities at
    every point of L0 with >= 3 lines.  Returns list of (index, euler_ziegler
    point multiplicities on L0)."""
    L = Lattice(normals, p)
    pts = [S for S in L.flats[2]]
    out = []
    for i0 in range(len(mult)):
        ok = True
        ez = []
        for S in pts:
            if i0 not in S:
                continue
            others = sum(mult[j] for j in S if j != i0)
            if len(S) >= 3 and mult[i0] < others:
                ok = False
                break
            ez.append(others)
        if ok:
            out.append((i0, sorted(ez)))
    return out
