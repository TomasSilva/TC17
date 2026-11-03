"""
divisional.py -- Abe's divisional freeness (Invent. Math. 2016) in rank 4:
A is divisionally free if some restriction A^P is divisionally free (rank 3)
and chi(A^P) divides chi(A).  In rank 3, A^P is DF iff chi(A^P) splits and
some line of A^P carries exactly e + 1 intersection points for an exponent e
(then the rank-2 restriction's chi divides).  DF is combinatorial, and Terao's
conjecture holds on it, so a counterexample must be free and NOT DF.
"""
from __future__ import annotations

from .core import Lattice
from .restrict import ziegler_restriction


def poly_div(a, b):
    a = list(a)
    out = []
    while len(a) >= len(b):
        if a[0] % b[0]:
            return None
        q = a[0] // b[0]
        out.append(q)
        for i in range(len(b)):
            a[i] -= q * b[i]
        a.pop(0)
    return out if all(x == 0 for x in a) else None


def rank3_df(normals, p, lattice=None):
    L = lattice or Lattice(normals, p)
    ex = L.exponents()
    if ex is None:
        return False
    cnt = [0] * len(normals)
    for S in L.flats[2]:
        for i in S:
            cnt[i] += 1
    return any((c - 1) in ex[1:] for c in cnt)


def df_witnesses(A, p, LA=None):
    """Planes P of the rank-4 arrangement A with A^P DF and chi(A^P) | chi(A)."""
    LA = LA or Lattice(A, p)
    chiA = LA.char_poly()
    out = []
    for i in range(A.shape[0]):
        N, mu, groups = ziegler_restriction(A, i, p)
        LR = Lattice(N, p)
        if poly_div(chiA, LR.char_poly()) is None:
            continue
        if rank3_df(N, p, LR):
            out.append(i)
    return out
