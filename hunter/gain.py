"""
gain.py -- gain-graphic ("bias") arrangements in K^l:
    { x_i = 0 : i in K }  u  { x_i - q^g x_j = 0 : [i, j, g] in E }.
For q not a root of unity the intersection lattice depends only on the gain
graph (a cycle of hyperplanes is dependent iff its signed gain sum is 0).
"""
from __future__ import annotations

import numpy as np


def bias_normals(l, coords, edges, q, p):
    rows = []
    for i in coords:
        v = [0] * l
        v[i] = 1
        rows.append(v)
    for (i, j, g) in edges:
        v = [0] * l
        v[i] = 1
        v[j] = (-pow(q, g % (p - 1), p)) % p if g >= 0 else (-pow(pow(q, p - 2, p), -g, p)) % p
        rows.append(v)
    return np.array(rows, dtype=np.int64) % p
