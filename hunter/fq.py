"""
fq.py -- small finite fields F_q (q = p^k, q <= 256) with table arithmetic, and the
rank-3 machinery needed for exhaustive searches over non-prime fields:
lattice of a line arrangement, chi, exponents, rank-3 DF test, EXACT freeness via
the Ziegler-restriction criterion (Yoshinaga; valid in every characteristic), and a
realization enumerator.

Elements are integers 0..q-1; for k > 1 an element is the integer whose base-p
digits are its coefficients in F_p[s]/(f).
"""
from __future__ import annotations

import itertools
from functools import lru_cache

import numpy as np

from .core import integer_roots


def _irreducible_monic(p, k):
    for coeffs in itertools.product(range(p), repeat=k):
        f = list(coeffs) + [1]                     # low -> high, monic degree k
        if f[0] == 0 and k > 1:
            continue
        # brute-force irreducibility: no root & no factor of degree <= k//2
        ok = True
        for d in range(1, k // 2 + 1):
            for g in itertools.product(range(p), repeat=d):
                gg = list(g) + [1]
                # polynomial remainder f mod gg over F_p
                r = f[:]
                while len(r) >= len(gg):
                    c = r[-1]
                    if c:
                        for t in range(len(gg)):
                            r[len(r) - len(gg) + t] = (r[len(r) - len(gg) + t] - c * gg[t]) % p
                    r.pop()
                if not any(r):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return f
    raise ValueError


class GF:
    def __init__(self, q):
        p = next(d for d in range(2, q + 1) if q % d == 0)
        k = 0
        t = q
        while t > 1:
            assert t % p == 0
            t //= p
            k += 1
        self.p, self.k, self.q = p, k, q
        f = _irreducible_monic(p, k) if k > 1 else [0, 1]
        self.f = f

        def to_vec(a):
            return [(a // p ** i) % p for i in range(k)]

        def to_int(v):
            return sum(int(c) * p ** i for i, c in enumerate(v))

        add = np.zeros((q, q), dtype=np.int64)
        mul = np.zeros((q, q), dtype=np.int64)
        for a in range(q):
            va = to_vec(a)
            for b in range(q):
                vb = to_vec(b)
                add[a, b] = to_int([(x + y) % p for x, y in zip(va, vb)])
                prod = [0] * (2 * k - 1)
                for i, x in enumerate(va):
                    for j, y in enumerate(vb):
                        prod[i + j] = (prod[i + j] + x * y) % p
                for d in range(len(prod) - 1, k - 1, -1):
                    c = prod[d]
                    if c:
                        for t2 in range(k + 1):
                            prod[d - k + t2] = (prod[d - k + t2] - c * f[t2]) % p
                mul[a, b] = to_int(prod[:k])
        self.add, self.mul = add, mul
        self.neg = np.array([next(b for b in range(q) if add[a, b] == 0) for a in range(q)], dtype=np.int64)
        self.inv = np.zeros(q, dtype=np.int64)
        for a in range(1, q):
            self.inv[a] = next(b for b in range(1, q) if mul[a, b] == 1)
        self.sub = np.array([[add[a, self.neg[b]] for b in range(q)] for a in range(q)], dtype=np.int64)
        self.one = 1

    # vectors -------------------------------------------------------------
    def dot(self, u, v):
        acc = 0
        for a, b in zip(u, v):
            acc = self.add[acc, self.mul[a, b]]
        return acc

    def cross(self, u, v):
        m, s = self.mul, self.sub
        return (s[m[u[1], v[2]], m[u[2], v[1]]],
                s[m[u[2], v[0]], m[u[0], v[2]]],
                s[m[u[0], v[1]], m[u[1], v[0]]])

    def normalize(self, v):
        for c in v:
            if c:
                ic = self.inv[c]
                return tuple(int(self.mul[ic, x]) for x in v)
        return None

    def points(self, l):
        return [v for v in itertools.product(range(self.q), repeat=l)
                if any(v) and next(c for c in v if c) == 1]

    # linear algebra ------------------------------------------------------
    def rank(self, M):
        M = [list(map(int, r)) for r in M]
        if not M:
            return 0
        rows, cols = len(M), len(M[0])
        r = 0
        for c in range(cols):
            piv = next((i for i in range(r, rows) if M[i][c]), None)
            if piv is None:
                continue
            M[r], M[piv] = M[piv], M[r]
            ic = self.inv[M[r][c]]
            M[r] = [int(self.mul[ic, x]) for x in M[r]]
            for i in range(rows):
                if i != r and M[i][c]:
                    f = M[i][c]
                    M[i] = [int(self.sub[x, self.mul[f, y]]) for x, y in zip(M[i], M[r])]
            r += 1
            if r == rows:
                break
        return r


# ------------------------------------------------------------ rank-3 tools

class LineArr:
    """Line arrangement over F_q: lines = tuples of field elements."""

    def __init__(self, F: GF, lines):
        self.F = F
        self.lines = [tuple(int(x) for x in l) for l in lines]
        self.n = len(self.lines)
        pts = {}
        for i, j in itertools.combinations(range(self.n), 2):
            P = F.normalize(F.cross(self.lines[i], self.lines[j]))
            if P is None:
                raise ValueError("repeated line")
            pts.setdefault(P, set()).update((i, j))
        self.pts = pts
        self.flats = [frozenset(s) for s in pts.values()]

    def char_poly(self):
        b2 = sum(len(S) - 1 for S in self.flats)
        return [1, -self.n, b2, -(b2 - self.n + 1)]

    def exponents(self):
        return integer_roots(self.char_poly())

    def is_df(self):
        ex = self.exponents()
        if ex is None:
            return False
        cnt = [0] * self.n
        for S in self.flats:
            for i in S:
                cnt[i] += 1
        return any((c - 1) in ex[1:] for c in cnt)

    def signature(self):
        return frozenset(self.flats)

    def free(self):
        """Exact over F_q: chi = (t-1)(t-d2)(t-d3), d2 <= d3; free iff the
        Ziegler restriction onto line 0 has no derivation of degree d2-1."""
        ex = self.exponents()
        if ex is None:
            return False
        d2 = ex[1]
        F = self.F
        H = self.lines[0]
        # basis of the line H as a 2-dim subspace: two independent vectors orthogonal to H
        cand = [v for v in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]]
        B = []
        for e in cand:
            # project: vectors x with H.x = 0 -> use cross products of H with unit vectors
            w = F.normalize(F.cross(H, e))
            if w is not None and (not B or F.rank([B[0], w]) == 2):
                B.append(w)
            if len(B) == 2:
                break
        # points on H with Ziegler multiplicities
        forms, mults = [], []
        for P, S in self.pts.items():
            if 0 not in S:
                continue
            j = next(i for i in S if i != 0)
            a = (F.dot(self.lines[j], B[0]), F.dot(self.lines[j], B[1]))
            forms.append(a)
            mults.append(len(S) - 1)
        k = d2 - 1
        if k < 0:
            return True
        return rank2_kernel_dim(F, forms, mults, k) == 0


@lru_cache(maxsize=None)
def _binom_mod(n, r, p):
    from math import comb
    return comb(n, r) % p


def rank2_kernel_dim(F: GF, forms, mults, k):
    """dim of D(A, m)_k for a rank-2 multiarrangement over F_q: theta = f d_u + g d_v,
    f, g binary forms of degree k; condition alpha^m | (a f + b g) for alpha = a u + b v."""
    q = F.q
    unknowns = 2 * (k + 1)                 # coefficients f_0..f_k, g_0..g_k of u^(k-i) v^i
    rows = []
    for (a, b), m in zip(forms, mults):
        # change variables so that alpha becomes y0: choose (u, v) = y0 * n + y1 * w with
        # alpha(n) = 1, alpha(w) = 0.  w = (b, -a) up to sign, n with a n_u + b n_v = 1.
        if a:
            n_vec = (int(F.inv[a]), 0)
        else:
            n_vec = (0, int(F.inv[b]))
        w = (b, int(F.neg[a]))
        # monomial u^(k-i) v^i  ->  polynomial in y0, y1: (n_u y0 + w_u y1)^(k-i) (n_v y0 + w_v y1)^i
        # we need coefficients of y0^j y1^(k-j) for j < m in  a f + b g.
        def expand(i):
            # returns list coef[j] of y0^j y1^(k-j)
            A = _pow_lin(F, n_vec[0], w[0], k - i)
            Bp = _pow_lin(F, n_vec[1], w[1], i)
            out = [0] * (k + 1)
            for j1, c1 in enumerate(A):
                if not c1:
                    continue
                for j2, c2 in enumerate(Bp):
                    if c2:
                        out[j1 + j2] = int(F.add[out[j1 + j2], F.mul[c1, c2]])
            return out
        E = [expand(i) for i in range(k + 1)]
        for j in range(min(m, k + 1)):
            row = []
            for i in range(k + 1):
                row.append(int(F.mul[a, E[i][j]]))
            for i in range(k + 1):
                row.append(int(F.mul[b, E[i][j]]))
            rows.append(row)
    if not rows:
        return unknowns
    return unknowns - F.rank(rows)


def _pow_lin(F, c0, c1, e):
    """(c0 y0 + c1 y1)^e as coefficient list by power of y0."""
    poly = [1]
    for _ in range(e):
        new = [0] * (len(poly) + 1)
        for j, c in enumerate(poly):
            if c:
                new[j + 1] = int(F.add[new[j + 1], F.mul[c, c0]])
                new[j] = int(F.add[new[j], F.mul[c, c1]])
        poly = new
    return poly


def realizations(F: GF, n, flats2, max_solutions=20000):
    """All realizations over F_q (frame-normalised) of the rank-3 lattice given by its
    rank-2 flats on labels 0..n-1."""
    r2 = [frozenset(S) for S in flats2]
    frame = None
    for c in itertools.combinations(range(n), 4):
        if all(len(F_ & set(c)) <= 2 for F_ in r2):
            frame = list(c)
            break
    if frame is None:
        return []
    order = list(frame)
    rest = [i for i in range(n) if i not in order]
    while rest:
        placed = set(order)
        best = max(rest, key=lambda i: sum(1 for S in r2 if i in S and len(S & placed) >= 2))
        order.append(best)
        rest.remove(best)
    pos = {lab: t for t, lab in enumerate(order)}
    sigs = {}

    def ref_sig(d):
        if d not in sigs:
            fl = set()
            for S in r2:
                G = frozenset(pos[i] for i in S if pos[i] < d)
                if len(G) >= 2:
                    fl.add(G)
            sigs[d] = frozenset(fl)
        return sigs[d]

    allpts = F.points(3)
    placed = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    sols = []

    def sig_of(ls):
        try:
            return LineArr(F, ls).signature()
        except ValueError:
            return None

    if sig_of(placed) != ref_sig(4):
        return []

    def rec(d):
        if len(sols) >= max_solutions:
            return
        if d == n:
            sols.append(list(placed))
            return
        lab = order[d]
        req = []
        for S in r2:
            if lab in S:
                pl = [pos[i] for i in S if pos[i] < d]
                if len(pl) >= 2:
                    req.append(F.normalize(F.cross(placed[pl[0]], placed[pl[1]])))
        cands = []
        if not req:
            cands = allpts
        else:
            P0 = req[0]
            for L in allpts:
                if all(F.dot(L, P) == 0 for P in req):
                    cands.append(L)
        for L in cands:
            if L in placed:
                continue
            placed.append(L)
            if sig_of(placed) == ref_sig(d + 1):
                rec(d + 1)
            placed.pop()

    rec(4)
    out = []
    for s in sols:
        arr = [None] * n
        for t, lab in enumerate(order):
            arr[lab] = s[t]
        out.append(arr)
    return out
