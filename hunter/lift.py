"""
lift.py -- lifting a rank-3 multiarrangement (B, m) to a rank-4 simple
arrangement A whose Ziegler restriction onto the plane at infinity H = {w=0}
is (B, m).

A = H  u  { a_L . x = c_{L,i} w : L in B, i = 1..m_L }.

Local freeness of A along H at a multiple point X of B (|B_X| >= 3) holds iff
the affine line arrangement A_X (planes of the classes through X, projected
along the direction X) has  b2(dA_X) = W_X := product of the local exponents of
(B_X, m_X)  (Yoshinaga's criterion for the rank-3 arrangement A_X: its Ziegler
restriction onto H is (B_X, m_X)).  Equivalently the "savings"
    S_X = sum_q C(mult_q - 1, 2)    (q = affine multiple points of A_X)
must equal  R_X = sigma_2(m_X) - W_X.

A concurrency (a set of planes from distinct classes through X sharing a line
in direction X) is a linear condition on the intercepts: if a_j = l1 a_1 + l2 a_2
then c_j = l1 c_1 + l2 c_2.

The solver builds lifts greedily at random and reports the resulting linear
system so that it can be replayed for other members of a family.
"""
from __future__ import annotations

import random
from itertools import combinations

import numpy as np

from .core import Lattice, nullspace_mod, rank_mod
from .multi import local_exponents


def dependency(a1, a2, a3, p):
    """(l1, l2) with a3 = l1 a1 + l2 a2 (a's dependent, a1, a2 independent)."""
    M = np.array([a1, a2], dtype=np.int64).T % p          # 3 x 2
    # solve M [l1, l2]^T = a3 using two independent rows
    for r1, r2 in combinations(range(3), 2):
        det = (M[r1, 0] * M[r2, 1] - M[r1, 1] * M[r2, 0]) % p
        if det:
            inv = pow(int(det), p - 2, p)
            l1 = (a3[r1] * M[r2, 1] - a3[r2] * M[r1, 1]) % p * inv % p
            l2 = (M[r1, 0] * a3[r2] - M[r2, 0] * a3[r1]) % p * inv % p
            return int(l1), int(l2)
    raise ValueError("a1, a2 dependent")


class LiftProblem:
    def __init__(self, B, m, p):
        self.p = p
        self.B = np.asarray(B, dtype=np.int64) % p
        self.m = list(m)
        self.lat = Lattice(self.B, p)
        self.points = [tuple(sorted(S)) for S in self.lat.flats[2] if len(S) >= 3]
        # plane index map
        self.planes = [(L, i) for L in range(len(self.m)) for i in range(self.m[L])]
        self.idx = {pl: k for k, pl in enumerate(self.planes)}
        self.R = {}
        for X in self.points:
            ms = [self.m[L] for L in X]
            s2 = sum(a * b for a, b in combinations(ms, 2))
            e = local_exponents(self.B, self.m, X, p)
            self.R[X] = s2 - e[0] * e[1]

    def condition_rows(self, X, tup):
        """Linear conditions (rows over the intercept vector) expressing that
        the planes in tup (list of (L, i), distinct classes through X) share a
        line."""
        p = self.p
        (L1, i1), (L2, i2) = tup[0], tup[1]
        rows = []
        for (Lj, ij) in tup[2:]:
            l1, l2 = dependency(self.B[L1], self.B[L2], self.B[Lj], p)
            row = np.zeros(len(self.planes), dtype=np.int64)
            row[self.idx[(Lj, ij)]] = 1
            row[self.idx[(L1, i1)]] = (row[self.idx[(L1, i1)]] - l1) % p
            row[self.idx[(L2, i2)]] = (row[self.idx[(L2, i2)]] - l2) % p
            rows.append(row)
        return rows

    def system(self, pattern):
        """pattern: list of (X, tup).  Returns the condition matrix."""
        rows = []
        for X, tup in pattern:
            rows.extend(self.condition_rows(X, tup))
        if not rows:
            return np.zeros((0, len(self.planes)), dtype=np.int64)
        return np.array(rows, dtype=np.int64) % self.p

    def solve(self, pattern, rng):
        """Random intercepts satisfying the pattern (None if only degenerate
        solutions, i.e. two planes of one class coincide)."""
        p = self.p
        M = self.system(pattern)
        K = nullspace_mod(M, p) if M.shape[0] else np.eye(len(self.planes), dtype=np.int64)
        if K.shape[0] == 0:
            return None
        coef = np.array([rng.randrange(p) for _ in range(K.shape[0])], dtype=np.int64)
        c = np.zeros(len(self.planes), dtype=np.int64)
        for a, row in zip(coef, K):
            c = (c + int(a) * row) % p
        return c

    def arrangement(self, c):
        p = self.p
        rows = [[0, 0, 0, 1]]
        for k, (L, i) in enumerate(self.planes):
            rows.append([int(self.B[L][0]), int(self.B[L][1]), int(self.B[L][2]), (-int(c[k])) % p])
        return np.array(rows, dtype=np.int64) % p

    def savings(self, c):
        """Actual savings S_X of the arrangement with intercepts c, at each X
        (vectorised: affine lines of A_X are intersected in a 2D quotient)."""
        p = self.p
        out = {}
        for X in self.points:
            v = self._direction(X)
            # coordinates on K^3/<v>: drop a coordinate e with v_e != 0
            e = max(i for i in range(3) if v[i])
            keep = [i for i in range(3) if i != e]
            pls = [(L, i) for L in X for i in range(self.m[L])]
            A = np.array([[int(self.B[L][keep[0]]) - int(self.B[L][e]) * int(v[keep[0]]) * pow(int(v[e]), p - 2, p),
                           int(self.B[L][keep[1]]) - int(self.B[L][e]) * int(v[keep[1]]) * pow(int(v[e]), p - 2, p)]
                          for (L, i) in pls], dtype=object)
            A = np.array([[int(x) % p for x in row] for row in A], dtype=np.int64)
            C = np.array([int(c[self.idx[pl]]) % p for pl in pls], dtype=np.int64)
            cls = np.array([pl[0] for pl in pls])
            npl = len(pls)
            I, J = np.triu_indices(npl, 1)
            mask = cls[I] != cls[J]
            I, J = I[mask], J[mask]
            a1, b1, c1 = A[I, 0], A[I, 1], C[I]
            a2, b2, c2 = A[J, 0], A[J, 1], C[J]
            det = (a1 * b2 % p - a2 * b1 % p) % p
            inv = np.array([pow(int(d), p - 2, p) for d in det], dtype=np.int64)
            xs = (c1 * b2 % p - c2 * b1 % p) % p * inv % p
            ys = (a1 * c2 % p - a2 * c1 % p) % p * inv % p
            pts = {}
            for k in range(len(I)):
                key = (int(xs[k]), int(ys[k]))
                s = pts.setdefault(key, set())
                s.add(int(I[k])); s.add(int(J[k]))
            out[X] = sum((len(s) - 1) * (len(s) - 2) // 2 for s in pts.values())
        return out

    def _direction(self, X):
        if not hasattr(self, '_dirs'):
            self._dirs = {}
        if X not in self._dirs:
            ns = nullspace_mod(self.B[list(X)], self.p)
            self._dirs[X] = ns[0]
        return self._dirs[X]

    def greedy(self, rng, max_steps=400):
        """Randomly add concurrencies until every X has savings R_X; returns the
        pattern or None."""
        pattern = []
        c = self.solve(pattern, rng)
        for _ in range(max_steps):
            S = self.savings(c)
            if any(S[X] > self.R[X] for X in self.points):
                return None
            deficit = [X for X in self.points if S[X] < self.R[X]]
            if not deficit:
                # re-validate on fresh generic solutions of the same pattern
                for s in range(2):
                    cg = self.solve(pattern, random.Random(rng.randrange(1 << 30)))
                    if cg is None or not self._distinct(cg) or self.savings(cg) != self.R:
                        return None
                return pattern
            X = rng.choice(deficit)
            # candidate: pick 3 or 4 planes from distinct classes through X
            k = rng.choice([3, 3, 3, 4]) if len(X) >= 4 else 3
            classes = rng.sample(list(X), k)
            tup = [(L, rng.randrange(self.m[L])) for L in classes]
            trial = pattern + [(X, tup)]
            c2 = self.solve(trial, rng)
            if c2 is None or not self._distinct(c2):
                continue
            S2 = self.savings(c2)
            if any(S2[Y] > self.R[Y] for Y in self.points):
                continue
            if sum(S2.values()) <= sum(S.values()):
                continue
            pattern, c = trial, c2
        return None

    def _distinct(self, c):
        for L in range(len(self.m)):
            vals = [int(c[self.idx[(L, i)]]) for i in range(self.m[L])]
            if len(set(vals)) != len(vals):
                return False
        return True
