"""
ffree.py -- EXACT freeness over a prime field F_p for any prime p (small p
included), for arrangements and multiarrangements in K^l (l = 3, 4, 5).

Why a separate module: core.py imposes the conditions  alpha_H | theta(alpha_H)
by evaluating at a principal lattice of points of H; that is only valid when p
is larger than the degree.  Here every condition is imposed on COEFFICIENTS
after a linear substitution  x = sum_j y_j P[j],  which is exact over any field.

Saito determinants are evaluated at random points over an extension field
GF(p^r) with p^r > 2^40, so a nonzero determinant (degree <= n) is detected with
probability >= 1 - n / p^r.  Rank computations use python-flint nmod_mat.
"""
from __future__ import annotations

import random
from functools import lru_cache
from math import comb

import numpy as np
from flint import nmod_mat

from .core import monomials, rank_mod, nullspace_mod, shift_up, Lattice


# ---------------------------------------------------------------- helpers

@lru_cache(maxsize=None)
def mono_pos(k: int, m: int):
    return {tuple(int(x) for x in r): i for i, r in enumerate(monomials(k, m).tolist())}


@lru_cache(maxsize=None)
def _first_var_split(k: int, l: int):
    """For each degree-k monomial a in l vars: (i, index of a - e_i in degree
    k-1) where i is the first variable with a_i > 0."""
    lo = mono_pos(k - 1, l)
    out = []
    for a in monomials(k, l).tolist():
        i = next(t for t in range(l) if a[t] > 0)
        b = list(a)
        b[i] -= 1
        out.append((i, lo[tuple(b)]))
    return out


@lru_cache(maxsize=None)
def _shift_index(k: int, m: int, j: int):
    """index map degree k-1 -> degree k for multiplication by y_j."""
    hi = mono_pos(k, m)
    out = []
    for b in monomials(k - 1, m).tolist():
        b = list(b)
        b[j] += 1
        out.append(hi[tuple(b)])
    return np.array(out, dtype=np.int64)


def lin_mult(c, k, m, p):
    """Matrix (dim S_k(m) x dim S_{k-1}(m)) of multiplication by sum_j c_j y_j."""
    lo = comb(k - 1 + m - 1, m - 1)
    hi = comb(k + m - 1, m - 1)
    L = np.zeros((hi, lo), dtype=np.int64)
    cols = np.arange(lo)
    for j in range(m):
        if c[j] % p:
            L[_shift_index(k, m, j), cols] = (L[_shift_index(k, m, j), cols] + int(c[j])) % p
    return L


def _matmul_mod(A, B, p):
    if p < (1 << 20):
        return (A @ B) % p
    out = np.zeros((A.shape[0], B.shape[1]), dtype=np.int64)
    for t in range(A.shape[1]):
        out = (out + np.outer(A[:, t], B[t]) % p) % p
    return out


def subst_matrices(P, K, p):
    """x = sum_j y_j P[j]  (P: m x l).  Returns [R_0..R_K], R_k of shape
    (dim S_k(m), dim S_k(l)): column a = coefficients of x^a in the y's."""
    P = np.asarray(P, dtype=np.int64) % p
    m, l = P.shape
    R = [np.ones((1, 1), dtype=np.int64)]
    for k in range(1, K + 1):
        split = _first_var_split(k, l)
        cols = comb(k + l - 1, l - 1)
        Rk = np.zeros((comb(k + m - 1, m - 1), cols), dtype=np.int64)
        by_var = {}
        for col, (i, src) in enumerate(split):
            by_var.setdefault(i, ([], []))
            by_var[i][0].append(col)
            by_var[i][1].append(src)
        for i, (dst, src) in by_var.items():
            L = lin_mult(P[:, i], k, m, p)
            Rk[:, dst] = _matmul_mod(L, R[k - 1][:, src], p)
        R.append(Rk)
    return R


def hyperplane_frame(a, p):
    """(n, B): n with a.n = 1 and B ((l-1) x l) a basis of ker(a)."""
    a = np.asarray(a, dtype=np.int64) % p
    l = len(a)
    e = max(i for i in range(l) if a[i])
    inv = pow(int(a[e]), p - 2, p)
    n = np.zeros(l, dtype=np.int64)
    n[e] = inv
    B = []
    for j in range(l):
        if j == e:
            continue
        v = np.zeros(l, dtype=np.int64)
        v[j] = 1
        v[e] = (-int(a[j]) * inv) % p
        B.append(v)
    return n, np.array(B, dtype=np.int64)


# ---------------------------------------------------------------- GF(p^r)

class GFpr:
    """Arithmetic in GF(p^r) = F_p[s]/(f), elements as int64 arrays (len r)."""

    def __init__(self, p, r=None, seed=1):
        self.p = p
        if r is None:
            r = 1
            while p ** r < (1 << 40):
                r += 1
        self.r = r
        rng = random.Random(seed)
        while True:
            f = [rng.randrange(p) for _ in range(r)] + [1]
            if self._irreducible(f):
                break
        self.f = np.array(f, dtype=np.int64)

    def _irreducible(self, f):
        # Rabin-style: no roots / no factors of degree <= r/2 via gcd(x^(p^i) - x, f)
        p, r = self.p, len(f) - 1
        def mulmod(a, b):
            res = np.convolve(a, b) % p
            for k in range(len(res) - 1, r - 1, -1):
                c = res[k]
                if c:
                    res[k - r:k + 1] = (res[k - r:k + 1] - c * np.array(f)) % p
            return res[:r]
        def powmod(a, e):
            out = np.zeros(r, dtype=np.int64); out[0] = 1
            base = np.array(a, dtype=np.int64)
            while e:
                if e & 1:
                    out = mulmod(out, base)
                base = mulmod(base, base)
                e >>= 1
            return out
        def gcd_nonconst(a):
            # gcd(a, f) over F_p; return True if degree > 0
            A = [int(x) % p for x in a]
            B = [int(x) % p for x in f]
            def trim(v):
                while v and v[-1] == 0:
                    v.pop()
                return v
            A, B = trim(A), trim(B)
            while A:
                inv = pow(A[-1], p - 2, p)
                while len(B) >= len(A) and B:
                    c = B[-1] * inv % p
                    sh = len(B) - len(A)
                    for t in range(len(A)):
                        B[sh + t] = (B[sh + t] - c * A[t]) % p
                    B = trim(B)
                A, B = B, A
            return len(B) > 1
        x = np.zeros(r, dtype=np.int64)
        if r >= 2:
            x[1] = 1
        else:
            return True
        for i in range(1, r // 2 + 1):
            xp = powmod(x, p ** i)
            d = xp.copy()
            d[1] = (d[1] - 1) % p
            if gcd_nonconst(d):
                return False
        return True

    def mul(self, a, b):
        p, r, f = self.p, self.r, self.f
        res = np.convolve(a, b) % p
        for k in range(len(res) - 1, r - 1, -1):
            c = res[k]
            if c:
                res[k - r:k + 1] = (res[k - r:k + 1] - c * f) % p
        out = np.zeros(r, dtype=np.int64)
        out[:min(r, len(res))] = res[:r]
        return out

    def random(self, rng):
        return np.array([rng.randrange(self.p) for _ in range(self.r)], dtype=np.int64)

    def scalar(self, c):
        v = np.zeros(self.r, dtype=np.int64)
        v[0] = c % self.p
        return v

    def eval_monos(self, x, k, l):
        """values of all degree-k monomials at the point x (list of l elements)."""
        pw = [[self.scalar(1)] for _ in range(l)]
        for i in range(l):
            for e in range(1, k + 1):
                pw[i].append(self.mul(pw[i][-1], x[i]))
        out = []
        for a in monomials(k, l).tolist():
            v = self.scalar(1)
            for i in range(l):
                if a[i]:
                    v = self.mul(v, pw[i][a[i]])
            out.append(v)
        return out

    def det(self, M):
        """Determinant of a small square matrix of elements (Laplace)."""
        n = len(M)
        if n == 1:
            return M[0][0]
        acc = np.zeros(self.r, dtype=np.int64)
        for j in range(n):
            minor = [row[:j] + row[j + 1:] for row in M[1:]]
            term = self.mul(M[0][j], self.det(minor))
            acc = (acc + term) % self.p if j % 2 == 0 else (acc - term) % self.p
        return acc


# ------------------------------------------------------- derivation modules

class ExactModule:
    """D(A, m) over F_p via substitution conditions; theta = sum_i f_i d_i,
    unknowns ordered (f_0 | f_1 | ... | f_{l-1}) in the degree-k monomial basis."""

    def __init__(self, normals, mult, p):
        self.p = p
        self.N = np.asarray(normals, dtype=np.int64) % p
        self.n, self.l = self.N.shape
        self.mult = [int(x) for x in mult]
        self.frames = [hyperplane_frame(a, p) for a in self.N]
        self._R = {}

    def _subst(self, H, K):
        if H not in self._R or len(self._R[H]) <= K:
            nvec, B = self.frames[H]
            P = np.vstack([nvec[None, :], B])           # y_0 along n, y_1.. on H
            self._R[H] = subst_matrices(P, K, self.p)
        return self._R[H]

    def matrix(self, k):
        p, l = self.p, self.l
        Mk = comb(k + l - 1, l - 1)
        blocks = []
        for H in range(self.n):
            mH = self.mult[H]
            R = self._subst(H, k)[k]                    # rows: y-monomials of degree k
            ypos = monomials(k, l)
            rows = np.nonzero(ypos[:, 0] < mH)[0]
            if rows.size == 0:
                continue
            RH = R[rows]
            b = self.N[H]
            blocks.append(np.concatenate([int(b[i]) * RH % p for i in range(l)], axis=1))
        if not blocks:
            return np.zeros((0, l * Mk), dtype=np.int64)
        return np.vstack(blocks) % p

    def basis(self, k):
        return nullspace_mod(self.matrix(k), self.p)

    def dim(self, k):
        Mk = comb(k + self.l - 1, self.l - 1)
        M = self.matrix(k)
        return self.l * Mk - rank_mod(M, self.p)

    def generators(self, kmax=None, stop_at=None):
        """Degrees of minimal generators up to kmax (rank-based, exact)."""
        p, l = self.p, self.l
        kmax = sum(self.mult) if kmax is None else kmax
        gens, bases, prev = [], {}, None
        for k in range(0, kmax + 1):
            Bk = self.basis(k)
            bases[k] = Bk
            r = 0
            if prev is not None and prev.shape[0] and Bk.shape[0]:
                r = rank_mod(shift_up(prev, k, l), p)
            gens.extend([k] * (Bk.shape[0] - r))
            prev = Bk
            if stop_at is not None and len(gens) >= stop_at:
                break
        return gens, bases

    def saito(self, degs, bases, tries=3, rng=None):
        """Nonzero determinant of random elements of the given degrees at a
        random point of GF(p^r)^l  =>  basis (Saito).  Both the point and the
        combination coefficients are taken in GF(p^r) (over a small F_p a
        random F_p-combination misses a new generator with probability 1/p)."""
        rng = rng or random.Random(11)
        F = GFpr(self.p)
        l, p, r = self.l, self.p, F.r
        for _ in range(tries):
            x = [F.random(rng) for _ in range(l)]
            cols = []
            used = {}
            for d in degs:
                Bd = bases[d]
                if d not in used:
                    mv = np.array(F.eval_monos(x, d, l), dtype=np.int64)     # (Md, r)
                    Md = mv.shape[0]
                    # E[j][i] = (b_j)_i(x)  as GF elements: (dim, l, r)
                    E = np.stack([(Bd[:, i * Md:(i + 1) * Md] @ mv) % p for i in range(l)], axis=1)
                    used[d] = E
                E = used[d]
                col = []
                coef = [F.random(rng) for _ in range(E.shape[0])]
                for i in range(l):
                    acc = np.zeros(r, dtype=np.int64)
                    for j in range(E.shape[0]):
                        acc = (acc + F.mul(coef[j], E[j, i])) % p
                    col.append(acc)
                cols.append(col)
            M = [[cols[j][i] for j in range(l)] for i in range(l)]
            if np.any(F.det(M) % p):
                return True
        return False

    def freeness(self):
        """('free', degs) / ('nonfree', degs) -- exact up to the Saito test's
        one-sided error (false 'nonfree' with probability <= n/p^r per try)."""
        l = self.l
        gens, bases = self.generators(stop_at=l)
        if len(gens) != l or sum(gens) != sum(self.mult):
            return 'nonfree', gens
        return ('free' if self.saito(gens, bases) else 'nonfree_saito'), gens


def free_simple(normals, p, lattice=None):
    """Freeness of a simple arrangement over F_p, with chi pre-filter."""
    N = np.asarray(normals, dtype=np.int64) % p
    L = lattice or Lattice(N, p)
    ex = L.exponents()
    if ex is None:
        return 'nonfree_chi', None
    st, g = ExactModule(N, [1] * N.shape[0], p).freeness()
    return st, g


def free_rank3_ziegler(normals, p, lattice=None):
    """Rank-3 shortcut (Yoshinaga / Barakat-Kuhne Cor. 4.5, any field):
    chi = (t-1)(t-d2)(t-d3), d2 <= d3: free iff the Ziegler restriction onto a
    line H has no nonzero derivation of degree d2 - 1."""
    N = np.asarray(normals, dtype=np.int64) % p
    L = lattice or Lattice(N, p)
    ex = L.exponents()
    if ex is None:
        return 'nonfree_chi'
    d2 = ex[1]
    # restriction onto line 0: points with multiplicities
    H = 0
    pts = [S for S in L.flats[2] if H in S]
    nvec, B = hyperplane_frame(N[H], p)                  # B: 2 x 3 basis of H
    nor, mul = [], []
    for S in pts:
        j = next(i for i in S if i != H)
        a = np.array([int(N[j] @ B[0] % p), int(N[j] @ B[1] % p)], dtype=np.int64)
        nor.append(a)
        mul.append(len(S) - 1)
    M2 = ExactModule(np.array(nor), mul, p)
    if d2 - 1 < 0:
        return 'free'
    return 'free' if M2.dim(d2 - 1) == 0 else 'nonfree'
