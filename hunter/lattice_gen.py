"""
lattice_gen.py -- intersection lattice of a central arrangement in K^l for any
l (used for l = 5, P^4), over F_p.  Flats of rank r are closures of independent
r-subsets: cl(S) = { k : alpha_k vanishes on  cap_{i in S} H_i }.
"""
from __future__ import annotations

from itertools import combinations

import numpy as np

from .core import nullspace_mod, rank_mod, check_simple, integer_roots


class LatticeGen:
    def __init__(self, normals, p):
        self.p = p
        self.N = np.asarray(normals, dtype=np.int64) % p
        self.n, self.l = self.N.shape
        check_simple(self.N, p)
        self.rank = rank_mod(self.N, p)
        self.flats = {0: [frozenset()], 1: [frozenset([i]) for i in range(self.n)]}
        for r in range(2, self.rank + 1):
            self.flats[r] = self._flats_of_rank(r)

    def _closure(self, S):
        K = nullspace_mod(self.N[list(S)], self.p)        # basis of the intersection
        if K.shape[0] == 0:
            return frozenset(range(self.n))
        vals = (self.N @ K.T) % self.p
        return frozenset(np.nonzero(np.all(vals == 0, axis=1))[0].tolist())

    def _flats_of_rank(self, r):
        out, seen = [], set()
        # extend rank-(r-1) flats by one hyperplane outside them
        for F in self.flats[r - 1]:
            base = sorted(F)
            # independent basis of F: greedy
            basis = []
            for i in base:
                if rank_mod(self.N[basis + [i]], self.p) > len(basis):
                    basis.append(i)
                if len(basis) == r - 1:
                    break
            for k in range(self.n):
                if k in F:
                    continue
                G = self._closure(basis + [k])
                if G not in seen:
                    seen.add(G)
                    out.append(G)
        return out

    def mobius(self):
        mu = {frozenset(): 1}
        for r in range(1, self.rank + 1):
            for X in self.flats[r]:
                s = 0
                for rr in range(0, r):
                    for Y in self.flats[rr]:
                        if Y <= X:
                            s += mu[Y]
                mu[X] = -s
        return mu

    def char_poly(self):
        mu = self.mobius()
        coeffs = [0] * (self.l + 1)          # descending powers t^l .. t^0
        for r in range(0, self.rank + 1):
            for X in self.flats[r]:
                coeffs[r] += mu[X]
        return coeffs

    def exponents(self):
        return integer_roots(self.char_poly())

    def signature(self):
        return tuple(frozenset(self.flats[r]) for r in sorted(self.flats) if r >= 2)
