"""
moduli.py -- first-order deformations of a line arrangement preserving its
intersection lattice (tangent space to the realization space), mod p.

dim T = 3n - rank(J),  trivial part = n + 8 (GL_3 and rescalings),
moduli dimension (upper bound; exact at smooth points) = 2n - 8 - rank J.
"""
from __future__ import annotations

import numpy as np

from .core import Lattice, _cross3, nullspace_mod, rank_mod


def jacobian_rows(N, points, p):
    n = N.shape[0]
    rows = []
    for S in points:
        S = sorted(S)
        if len(S) < 3:
            continue
        a, b = S[0], S[1]
        for c in S[2:]:
            row = np.zeros(3 * n, dtype=np.int64)
            row[3 * a:3 * a + 3] = _cross3(N[b], N[c], p)
            row[3 * b:3 * b + 3] = _cross3(N[c], N[a], p)
            row[3 * c:3 * c + 3] = _cross3(N[a], N[b], p)
            rows.append(row)
    if not rows:
        return np.zeros((0, 3 * n), dtype=np.int64)
    return np.array(rows, dtype=np.int64) % p


def moduli_dimension(N, p, lattice=None):
    N = np.asarray(N, dtype=np.int64) % p
    L = lattice or Lattice(N, p)
    J = jacobian_rows(N, L.flats[2], p)
    n = N.shape[0]
    return 2 * n - 8 - rank_mod(J, p), J


def tangent_vectors(N, p, lattice=None):
    """Basis of the tangent space (rows, length 3n) modulo nothing (includes
    trivial directions)."""
    dim, J = moduli_dimension(N, p, lattice)
    return nullspace_mod(J, p)
