"""
multi.py -- combinatorial helpers for rank-3 multiarrangements (lines in P^2
with multiplicities), used to predict freeness before computing it.

* local_exponents(normals, mult, S, p): exponents of the rank-2 localisation
  at the point where the lines S meet (Wakamiko's formula for |S| <= 3,
  computed for |S| >= 4).
* b2(normals, mult, points, p): sum over points of the product of local
  exponents (the second coefficient of chi((A,m),t), Abe-Terao-Wakefield).
* generic_rank2_exponents(mults): (M - max, max) if max >= M/2 else balanced.
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np

from .core import module_generators, nullspace_mod


def wakamiko(ms):
    ms = sorted(ms)
    if len(ms) == 1:
        return (0, ms[0])
    if len(ms) == 2:
        return (ms[0], ms[1])
    a, b, c = ms
    M = a + b + c
    if c >= a + b - 1:
        return tuple(sorted((a + b, c)))
    return (M // 2, M - M // 2)


def generic_rank2_exponents(ms):
    M = sum(ms)
    mx = max(ms)
    if 2 * mx >= M:
        return (M - mx, mx)
    return (M // 2, M - M // 2)


def project_to_point(normals, S, p):
    """Normals of the lines S (all through one point v of P^2), written as
    2-vectors (drop a coordinate where v != 0)."""
    N = np.asarray(normals, dtype=np.int64)[sorted(S)] % p
    v = nullspace_mod(N, p)
    assert v.shape[0] == 1, "lines are not concurrent at a single point"
    v = v[0]
    e = max(i for i in range(3) if v[i])
    keep = [i for i in range(3) if i != e]
    return N[:, keep]


def local_exponents(normals, mult, S, p):
    S = sorted(S)
    ms = [int(mult[i]) for i in S]
    if len(S) <= 3:
        return wakamiko(ms)
    P2 = project_to_point(normals, S, p)
    gens, _ = module_generators(P2, ms, p)
    return tuple(sorted(gens[:2]))


def b2(normals, mult, points, p, skip=()):
    tot = 0
    for S in points:
        if frozenset(S) in skip:
            continue
        e = local_exponents(normals, mult, S, p)
        tot += e[0] * e[1]
    return tot


def points_on_line_P1(normals, i0, p):
    """For the line i0, the intersection points with every other line,
    as P^1 coordinates w.r.t. a fixed basis (b1, b2) of the line; returns
    dict j -> (u, v) (projective, normalised)."""
    N = np.asarray(normals, dtype=np.int64) % p
    from .core import hyperplane_basis
    B = hyperplane_basis(N[i0], p)          # (2, 3) basis of the plane alpha_i0 = 0
    out = {}
    for j in range(N.shape[0]):
        if j == i0:
            continue
        # point = u b1 + v b2 with alpha_j(point) = 0
        a1 = int(N[j] @ B[0] % p)
        a2 = int(N[j] @ B[1] % p)
        u, v = a2 % p, (-a1) % p
        if u:
            inv = pow(u, p - 2, p)
            key = (1, v * inv % p)
        else:
            key = (0, 1)
        out[j] = key
    return out


def euler_restriction_dominant(normals, mult, i0, p):
    """Euler restriction to line i0 assuming i0 is dominant at every point on
    it: point multiplicity = sum of the multiplicities of the other lines
    through that point.  Returns (rank-2 normals, multiplicities)."""
    pts = points_on_line_P1(normals, i0, p)
    groups = {}
    for j, key in pts.items():
        groups.setdefault(key, []).append(j)
    nor, ms = [], []
    for (u, v), js in groups.items():
        # linear form on P^1 vanishing at (u:v): v*X - u*Y
        nor.append([v % p, (-u) % p])
        ms.append(sum(int(mult[j]) for j in js))
    return np.array(nor, dtype=np.int64), ms
