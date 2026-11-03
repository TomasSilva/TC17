"""
realize.py -- enumerate ALL realizations over F_q (q prime) of the intersection
lattice of a reference arrangement (rank 3 or 4), up to projective equivalence.

Method: fix a projective frame (l+1 hyperplanes in general position mapped to
e_1..e_l, (1,..,1)), then place the remaining hyperplanes depth-first in a
constraint-greedy order.  Candidates for the next hyperplane are all hyperplanes
of PG(l-1, q) containing the points/lines forced by already placed ones; each
partial arrangement must have exactly the labelled lattice of the reference
arrangement restricted to the placed labels.
"""
from __future__ import annotations

import itertools

import numpy as np

from .core import Lattice, nullspace_mod, _minors3, _cross3


def _norm(v, q):
    v = [int(x) % q for x in v]
    for c in v:
        if c:
            inv = pow(c, q - 2, q)
            return tuple(x * inv % q for x in v)
    return None


def proj_points_of_subspace(K, q):
    """All projective points of the row space of K (k x l)."""
    k = K.shape[0]
    out = set()
    for coef in itertools.product(range(q), repeat=k):
        if not any(coef):
            continue
        v = np.zeros(K.shape[1], dtype=np.int64)
        for c, row in zip(coef, K):
            v = (v + c * row) % q
        nv = _norm(v, q)
        if nv is not None:
            out.add(nv)
    return sorted(out)


class Realizer:
    def __init__(self, ref, q, max_solutions=10 ** 6):
        self.q = q
        self.ref = np.asarray(ref, dtype=np.int64) % q
        self.n, self.l = self.ref.shape
        if self.l not in (3, 4):
            raise NotImplementedError
        L = Lattice(self.ref, q)
        self.r2 = [frozenset(S) for S in L.flats[2]]
        self.r3 = [frozenset(S) for S in L.flats[3]] if self.l == 4 else []
        self.max_solutions = max_solutions
        self._choose_order()
        self._sigs = {}

    # ---------------------------------------------------------- ordering
    def _general_position(self, labels):
        for F in self.r2:
            if len(F & set(labels)) >= 3:
                return False
        for G in self.r3:
            if len(G & set(labels)) >= 4:
                return False
        return True

    def _choose_order(self):
        l = self.l
        frame = None
        for c in itertools.combinations(range(self.n), l + 1):
            if self._general_position(c):
                frame = list(c)
                break
        if frame is None:
            raise ValueError("no frame in general position")
        order = list(frame)
        rest = [i for i in range(self.n) if i not in order]
        while rest:
            def score(i):
                placed = set(order)
                s = 0
                for F in self.r2:
                    if i in F and len(F & placed) >= 2:
                        s += 2 if l == 3 else 2
                for G in self.r3:
                    if i in G and len(G & placed) >= 3:
                        s += 1
                return s
            best = max(rest, key=score)
            order.append(best)
            rest.remove(best)
        self.order = order
        self.frame = frame

    def _ref_sig(self, d):
        if d not in self._sigs:
            sub = self.ref[self.order[:d]]
            self._sigs[d] = Lattice(sub, self.q).signature() if d >= 2 else None
        return self._sigs[d]

    # ---------------------------------------------------------- candidates
    def _candidates(self, placed_vecs, d):
        """Hyperplanes (normalised) satisfying the forced incidences for label
        order[d] given the placed ones."""
        q, l = self.q, self.l
        lab = self.order[d]
        pos = {self.order[t]: t for t in range(d)}
        req_pts = []
        if l == 3:
            for F in self.r2:
                if lab in F:
                    pl = [pos[i] for i in F if i in pos]
                    if len(pl) >= 2:
                        P = _cross3(np.array(placed_vecs[pl[0]]), np.array(placed_vecs[pl[1]]), q)
                        req_pts.append(P)
        else:
            for F in self.r2:
                if lab in F:
                    pl = [pos[i] for i in F if i in pos]
                    if len(pl) >= 2:
                        K = nullspace_mod(np.array([placed_vecs[pl[0]], placed_vecs[pl[1]]]) % q, q)
                        req_pts.extend(list(K))
            for G in self.r3:
                if lab in G:
                    pl = [pos[i] for i in G if i in pos]
                    if len(pl) >= 3:
                        M = np.array([placed_vecs[t] for t in pl]) % q
                        K = nullspace_mod(M, q)
                        if K.shape[0] == 1:
                            req_pts.append(K[0])
        if req_pts:
            K = nullspace_mod(np.array(req_pts, dtype=np.int64) % q, q)
        else:
            K = np.eye(l, dtype=np.int64)
        if K.shape[0] == 0:
            return []
        return proj_points_of_subspace(K, q)

    # ---------------------------------------------------------- search
    def solutions(self):
        q, l = self.q, self.l
        frame_vecs = [tuple(int(i == j) for j in range(l)) for i in range(l)] + [tuple([1] * l)]
        sols = []
        placed = list(frame_vecs)
        if Lattice(np.array(placed), q).signature() != self._ref_sig(l + 1):
            raise ValueError("frame inconsistent")

        def rec(d):
            if len(sols) >= self.max_solutions:
                return
            if d == self.n:
                sols.append(list(placed))
                return
            used = set(placed)
            for v in self._candidates(placed, d):
                if v in used:
                    continue
                placed.append(v)
                ok = True
                try:
                    sig = Lattice(np.array(placed), q).signature()
                    ok = sig == self._ref_sig(d + 1)
                except ValueError:
                    ok = False
                if ok:
                    rec(d + 1)
                placed.pop()

        rec(l + 1)
        # return arrangements in the ORIGINAL label order
        out = []
        for s in sols:
            arr = [None] * self.n
            for t, lab in enumerate(self.order):
                arr[lab] = s[t]
            out.append(np.array(arr, dtype=np.int64))
        return out


class AbstractRealizer(Realizer):
    """Realizer for a rank-3 lattice given abstractly by its rank-2 flats (sets of
    line labels with >= 2 elements, covering every pair exactly once)."""

    def __init__(self, n, flats2, q, max_solutions=10 ** 6):
        self.q = q
        self.n, self.l = n, 3
        self.r2 = [frozenset(S) for S in flats2]
        self.r3 = []
        self.max_solutions = max_solutions
        self._choose_order()
        self._sigs = {}

    def _ref_sig(self, d):
        if d not in self._sigs:
            sub = self.order[:d]
            pos = {lab: t for t, lab in enumerate(sub)}
            fl = set()
            for F in self.r2:
                G = frozenset(pos[i] for i in F if i in pos)
                if len(G) >= 2:
                    fl.add(G)
            self._sigs[d] = (frozenset(fl),)
        return self._sigs[d]
