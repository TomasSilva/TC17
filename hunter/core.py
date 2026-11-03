"""
core.py -- hyperplane arrangements in K^l over a prime field F_p (search side).

An arrangement is an (n, l) int64 array of normal covectors, entries in [0, p).
Everything here is modular and probabilistic in the following precise sense:

  * rank_{F_p} M <= rank_{Q} M for the reduction of an integer matrix, so
    dim D(A)_k computed mod p is an UPPER bound for the characteristic-zero
    value (for the reduction of a characteristic-zero arrangement), and is
    exact for p outside a finite set of bad primes;
  * when the arrangement is genuinely defined over F_p (finite-field search)
    the computations are exact over F_p (up to the random choices in the
    Saito determinant test, which can only produce false NEGATIVES).

Claims about characteristic zero are re-proved separately (Macaulay2 over QQ).

Degree convention: theta = sum f_i d_i with deg f_i = k lies in D(A)_k.  The
Euler derivation has degree 1 and a free central arrangement has exponents
(1, d_1, ..., d_{l-1}) with sum n.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import comb
import random

import numpy as np
from flint import nmod_mat

DEFAULT_P = 2147483629          # largest prime below 2^31 - 1 ... (prime)


# --------------------------------------------------------------------------
# monomials and evaluation
# --------------------------------------------------------------------------

@lru_cache(maxsize=None)
def monomials(k: int, l: int) -> np.ndarray:
    """All exponent vectors of degree k in l variables, (M, l) int64."""
    if l == 1:
        return np.array([[k]], dtype=np.int64)
    out = []
    for a in range(k, -1, -1):
        for rest in monomials(k - a, l - 1):
            out.append([a] + list(rest))
    return np.array(out, dtype=np.int64).reshape(-1, l)


def eval_monos(P: np.ndarray, monos: np.ndarray, p: int) -> np.ndarray:
    """(N, M) matrix of monomials evaluated at the rows of P, mod p."""
    N, l = P.shape
    if monos.shape[0] == 0:
        return np.zeros((N, 0), dtype=np.int64)
    k = int(monos.sum(axis=1).max())
    pw = np.ones((N, l, k + 1), dtype=np.int64)
    Pm = P % p
    for e in range(1, k + 1):
        pw[:, :, e] = pw[:, :, e - 1] * Pm % p
    out = np.ones((N, monos.shape[0]), dtype=np.int64)
    for i in range(l):
        out = out * pw[:, i, monos[:, i]] % p
    return out


def hyperplane_basis(a: np.ndarray, p: int) -> np.ndarray:
    """(l-1, l) basis of ker(a) over F_p."""
    l = len(a)
    e = max(i for i in range(l) if a[i] % p)
    inv = pow(int(a[e]), p - 2, p)
    rows = []
    for j in range(l):
        if j == e:
            continue
        v = np.zeros(l, dtype=np.int64)
        v[j] = 1
        v[e] = (-int(a[j]) * inv) % p
        rows.append(v)
    return np.array(rows, dtype=np.int64)


def points_on_hyperplane(a: np.ndarray, k: int, p: int) -> np.ndarray:
    """A unisolvent set for degree-k forms on ker(a): images of the
    principal lattice {b : |b| = k} under a basis of ker(a)."""
    B = hyperplane_basis(a, p)                      # (l-1, l)
    lat = monomials(k, B.shape[0])                  # (N, l-1)
    return lat @ B % p


# --------------------------------------------------------------------------
# rank / nullspace via flint
# --------------------------------------------------------------------------

def _to_nmod(M: np.ndarray, p: int) -> nmod_mat:
    r, c = M.shape
    return nmod_mat(r, c, [int(x) for x in M.ravel()], p)


def rank_mod(M: np.ndarray, p: int) -> int:
    if M.size == 0:
        return 0
    return _to_nmod(M, p).rank()


def nullspace_mod(M: np.ndarray, p: int) -> np.ndarray:
    """(nullity, ncols) basis of the right kernel."""
    r, c = M.shape
    if r == 0:
        return np.eye(c, dtype=np.int64)
    X, nul = _to_nmod(M, p).nullspace()
    if nul == 0:
        return np.zeros((0, c), dtype=np.int64)
    ent = np.array([int(x) for x in X.entries()], dtype=np.int64).reshape(c, c)
    return ent[:, :nul].T.copy()


# --------------------------------------------------------------------------
# intersection lattice (l = 3 or 4) and characteristic polynomial
# --------------------------------------------------------------------------

def _minors3(a, b, c, p):
    """For l=4: the 4-vector v with v . x = det[a; b; c; x] (point of P^3
    common to the three planes).  Overflow-safe for p < 2^31."""
    M = np.stack(np.broadcast_arrays(a, b, c), axis=-2) % p      # (..., 3, 4)
    cols = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]
    out = []
    for m, cs in enumerate(cols):
        s = M[..., :, cs]
        m00 = (s[..., 1, 1] * s[..., 2, 2] - s[..., 1, 2] * s[..., 2, 1]) % p
        m01 = (s[..., 1, 0] * s[..., 2, 2] - s[..., 1, 2] * s[..., 2, 0]) % p
        m02 = (s[..., 1, 0] * s[..., 2, 1] - s[..., 1, 1] * s[..., 2, 0]) % p
        d = (s[..., 0, 0] * m00 % p - s[..., 0, 1] * m01 % p + s[..., 0, 2] * m02 % p) % p
        out.append(d if m % 2 == 0 else (-d) % p)
    return np.stack(out, axis=-1) % p


def _cross3(a, b, p):
    a, b = a % p, b % p
    return np.stack([(a[..., 1] * b[..., 2] % p - a[..., 2] * b[..., 1] % p) % p,
                     (a[..., 2] * b[..., 0] % p - a[..., 0] * b[..., 2] % p) % p,
                     (a[..., 0] * b[..., 1] % p - a[..., 1] * b[..., 0] % p) % p], axis=-1)


def _dot_rows(normals, V, p):
    """(n, m) matrix normals @ V.T mod p, overflow-safe for l <= 5."""
    out = np.zeros((normals.shape[0], V.shape[0]), dtype=np.int64)
    for i in range(normals.shape[1]):
        out = (out + np.outer(normals[:, i], V[:, i]) % p) % p
    return out


class Lattice:
    """Flats of a central arrangement in K^3 or K^4 (as frozensets of
    hyperplane labels), ranks 1..l-1, plus the characteristic polynomial."""

    def __init__(self, normals: np.ndarray, p: int):
        self.p = p
        self.normals = np.asarray(normals, dtype=np.int64) % p
        self.n, self.l = self.normals.shape
        check_simple(self.normals, p)
        if self.l == 3:
            self.flats = {2: self._points_l3()}
        elif self.l == 4:
            self.flats = {2: self._lines_l4(), 3: self._points_l4()}
        else:
            raise NotImplementedError("lattice only for l = 3, 4")

    # rank-2 flats in K^3 (points of P^2)
    def _points_l3(self):
        N, p, n = self.normals, self.p, self.n
        idx = np.array(list(combinations(range(n), 2)), dtype=np.int64)
        V = _cross3(N[idx[:, 0]], N[idx[:, 1]], p)
        if np.any(np.all(V == 0, axis=1)):
            raise ValueError("repeated hyperplane")
        inc = _dot_rows(N, V, p) == 0                 # (n, pairs)
        seen = set()
        flats = []
        for t in range(idx.shape[0]):
            S = frozenset(np.nonzero(inc[:, t])[0].tolist())
            if S not in seen:
                seen.add(S)
                flats.append(S)
        return flats

    def _lines_l4(self):
        N, p, n = self.normals, self.p, self.n
        flats, seen, covered = [], set(), set()
        for i, j in combinations(range(n), 2):
            if (i, j) in covered:
                continue
            # S = {k : rank[a_i; a_j; a_k] = 2}  <=>  all 3x3 minors vanish
            W = _minors3(N[i], N[j], N, p)
            S = frozenset(np.nonzero(np.all(W == 0, axis=1))[0].tolist())
            for a, b in combinations(sorted(S), 2):
                covered.add((a, b))
            if S not in seen:
                seen.add(S)
                flats.append(S)
        return flats

    def _points_l4(self):
        N, p, n = self.normals, self.p, self.n
        idx = np.array(list(combinations(range(n), 3)), dtype=np.int64)
        V = _minors3(N[idx[:, 0]], N[idx[:, 1]], N[idx[:, 2]], p)
        ok = ~np.all(V == 0, axis=1)
        idx, V = idx[ok], V[ok]
        inc = _dot_rows(N, V, p) == 0                 # (n, triples)
        seen, flats = set(), []
        for t in range(idx.shape[0]):
            S = frozenset(np.nonzero(inc[:, t])[0].tolist())
            if S not in seen:
                seen.add(S)
                flats.append(S)
        return flats

    # ---------------------------------------------------------------- chi
    def mobius(self):
        """{rank: [(flat, mu)]}."""
        out = {1: [(frozenset([i]), -1) for i in range(self.n)]}
        out[2] = [(S, len(S) - 1) for S in self.flats[2]]
        if self.l == 4:
            r2 = self.flats[2]
            lst = []
            for S in self.flats[3]:
                s = 1 - len(S) + sum(len(Y) - 1 for Y in r2 if Y <= S)
                lst.append((S, -s))
            out[3] = lst
        return out

    def char_poly(self):
        """Coefficients (descending powers of t) of chi(A, t)."""
        mu = self.mobius()
        b = [1, self.n, sum(m for _, m in mu[2])]
        if self.l == 4:
            b.append(sum(-m for _, m in mu[3]))
        coeffs = [(-1) ** i * b[i] for i in range(self.l)]
        coeffs.append(-sum(coeffs))                  # chi(1) = 0 (central)
        return coeffs

    def exponents(self):
        """Exponents (1, d_1, ..., d_{l-1}) if chi(A,t) splits into linear
        factors (t - d) with integer d >= 0, else None."""
        return integer_roots(self.char_poly())

    def signature(self):
        """Labelled lattice (comparable across a labelled family)."""
        return tuple(frozenset(self.flats[r]) for r in sorted(self.flats))



def check_simple(N, p):
    """Raise if two normals are proportional (repeated hyperplane) or zero."""
    n, l = N.shape
    if np.any(np.all(N % p == 0, axis=1)):
        raise ValueError("zero normal")
    # 2x2 minors of every pair
    for a in range(n):
        D = (N[a][None, :, None] * N[:, None, :] % p - N[:, :, None] * N[a][None, None, :] % p) % p
        same = np.all(D.reshape(n, -1) == 0, axis=1)
        same[a] = False
        if np.any(same):
            raise ValueError(f"repeated hyperplane {a} ~ {int(np.nonzero(same)[0][0])}")


def integer_roots(coeffs):
    """Sorted list of the roots of the integer polynomial (descending
    coefficients) if it splits into linear factors over Z>=0, else None."""
    poly = list(coeffs)
    deg = len(poly) - 1
    roots = []
    r = 0
    bound = sum(abs(c) for c in poly) + 1
    while len(poly) > 1 and r <= bound:
        acc, quo = 0, []
        for a in poly:
            acc = acc * r + a
            quo.append(acc)
        if quo[-1] == 0:
            roots.append(r)
            poly = quo[:-1]
        else:
            r += 1
    if len(roots) != deg:
        return None
    return tuple(sorted(roots))


# --------------------------------------------------------------------------
# logarithmic derivations
# --------------------------------------------------------------------------

def gauge_matrix(normals: np.ndarray, k: int, p: int, h: int = 0) -> np.ndarray:
    """Matrix whose kernel is D_H(A)_k, H = hyperplane h:
    D_H(A) = {theta in D(A) : theta(alpha_h) = 0}; D(A) = S E (+) D_H(A).
    Unknowns: the l-1 components theta_i (i != e) in the monomial basis."""
    N = np.asarray(normals, dtype=np.int64) % p
    n, l = N.shape
    a = N[h]
    e = max(i for i in range(l) if a[i])
    inv = pow(int(a[e]), p - 2, p)
    free = [i for i in range(l) if i != e]
    monos = monomials(k, l)
    blocks = []
    for H in range(n):
        if H == h:
            continue
        b = N[H]
        c = [(int(b[i]) - int(b[e]) * int(a[i]) % p * inv) % p for i in free]
        if not any(c):
            raise ValueError("repeated hyperplane")
        E = eval_monos(points_on_hyperplane(b, k, p), monos, p)
        blocks.append(np.concatenate([ci * E % p for ci in c], axis=1))
    return np.vstack(blocks)


def gauge_to_theta(normals, k, p, h, vec):
    """Full (l, M) coefficient array of theta from a gauge kernel vector."""
    N = np.asarray(normals, dtype=np.int64) % p
    n, l = N.shape
    a = N[h]
    e = max(i for i in range(l) if a[i])
    inv = pow(int(a[e]), p - 2, p)
    free = [i for i in range(l) if i != e]
    M = monomials(k, l).shape[0]
    th = np.zeros((l, M), dtype=np.int64)
    for t, i in enumerate(free):
        th[i] = vec[t * M:(t + 1) * M] % p
    acc = np.zeros(M, dtype=np.int64)
    for i in free:
        acc = (acc + int(a[i]) * th[i]) % p
    th[e] = (-acc * inv) % p
    return th


def hilbert_DH(normals, p, kmax, h=0, kmin=0):
    """[dim D_H(A)_k for k in kmin..kmax] (mod-p upper bounds)."""
    l = normals.shape[1]
    out = []
    for k in range(kmin, kmax + 1):
        M = monomials(k, l).shape[0]
        out.append((l - 1) * M - rank_mod(gauge_matrix(normals, k, p, h), p))
    return out


def free_hilbert(exps, k, l):
    return sum(comb(k - d + l - 1, l - 1) for d in exps if k >= d)


def _det_mod(M, p):
    return int(nmod_mat(M.shape[0], M.shape[1], [int(x) for x in M.ravel()], p).det())


def saito_test(normals, exps, p, h=0, tries=2, rng=None):
    """True if random elements of D_H(A) in degrees exps, together with the
    Euler derivation, have nonzero determinant at a random point (=> free over
    F_p).  False means 'no certificate found' (non-free if the random
    choices were generic)."""
    rng = rng or random.Random(12345)
    N = np.asarray(normals, dtype=np.int64) % p
    l = N.shape[1]
    bases = {}
    for d in set(exps):
        bases[d] = nullspace_mod(gauge_matrix(N, d, p, h), p)
    for _ in range(tries):
        x0 = np.array([rng.randrange(1, p) for _ in range(l)], dtype=np.int64)
        cols = [x0 % p]
        for d in exps:
            B = bases[d]
            if B.shape[0] == 0:
                return False
            coef = np.array([rng.randrange(p) for _ in range(B.shape[0])], dtype=np.int64)
            vec = np.zeros(B.shape[1], dtype=np.int64)
            for c, row in zip(coef, B):
                vec = (vec + int(c) * row) % p
            th = gauge_to_theta(N, d, p, h, vec)
            mv = eval_monos(x0[None, :], monomials(d, l), p)[0]
            cols.append(np.array([int(sum(int(a) * int(b) for a, b in zip(th[i], mv)) % p)
                                  for i in range(l)], dtype=np.int64))
        if _det_mod(np.stack(cols, axis=1), p) != 0:
            return True
    return False


def freeness(normals, p, lattice: Lattice = None, h=None, full=False):
    """Classify freeness over F_p.  Returns dict with keys
    status in {'free', 'nonfree_chi', 'nonfree_hilbert', 'nonfree_saito'},
    exps, hilbert (list of (k, dim, expected))."""
    N = np.asarray(normals, dtype=np.int64) % p
    L = lattice or Lattice(N, p)
    exps = L.exponents()
    res = {"exps": exps, "hilbert": []}
    if exps is None:
        res["status"] = "nonfree_chi"
        return res
    d = exps[1:]                                     # drop the exponent 1
    if h is None:
        # gauge on a hyperplane with the most flats through it (fewest rows)
        h = 0
    l = N.shape[1]
    ks = list(range(min(d) - 1, max(d) + 1)) if not full else list(range(0, max(d) + 1))
    bad = False
    for k in ks:
        if k < 0:
            continue
        dim = (l - 1) * monomials(k, l).shape[0] - rank_mod(gauge_matrix(N, k, p, h), p)
        exp = free_hilbert(d, k, l)
        res["hilbert"].append((k, dim, exp))
        if dim != exp:
            bad = True
            if not full:
                break
    if bad:
        res["status"] = "nonfree_hilbert"
        return res
    res["status"] = "free" if saito_test(N, d, p, h) else "nonfree_saito"
    return res


# --------------------------------------------------------------------------
# localisations
# --------------------------------------------------------------------------

def localization_l4(normals, S, p):
    """Rank-3 essentialisation of A_X for a rank-3 flat X (labels S) in K^4:
    returns (|S|, 3) normals."""
    N = np.asarray(normals, dtype=np.int64)[sorted(S)] % p
    # common kernel vector v: N v = 0
    ns = nullspace_mod(N, p)
    assert ns.shape[0] == 1, "not a rank-3 flat"
    v = ns[0]
    e = max(i for i in range(4) if v[i])
    keep = [i for i in range(4) if i != e]
    return N[:, keep]


def local_freeness_l4(normals, p, lattice: Lattice = None):
    """List of (flat, status) for rank-3 flats with >= 4 hyperplanes whose
    localisation is not free (empty list = locally free)."""
    L = lattice or Lattice(normals, p)
    bad = []
    for S in L.flats[3]:
        if len(S) <= 3:
            continue
        loc = localization_l4(normals, S, p)
        r = freeness(loc, p)
        if r["status"] != "free":
            bad.append((S, r["status"]))
    return bad


# --------------------------------------------------------------------------
# multiarrangements
# --------------------------------------------------------------------------

@lru_cache(maxsize=None)
def compositions(j: int, l: int):
    """All t in Z_{>=0}^l with |t| = j."""
    return [tuple(int(x) for x in row) for row in monomials(j, l)]


def taylor_eval(Q: np.ndarray, nvec: np.ndarray, monos: np.ndarray, j: int,
                p: int) -> np.ndarray:
    """(N, M): coefficient of s^j in (q + s n)^a for q in rows of Q and the
    monomials a (rows of monos), mod p."""
    N, l = Q.shape
    M = monos.shape[0]
    if M == 0:
        return np.zeros((N, 0), dtype=np.int64)
    k = int(monos.sum(axis=1).max())
    pw = np.ones((N, l, k + 1), dtype=np.int64)
    Qm = Q % p
    for e in range(1, k + 1):
        pw[:, :, e] = pw[:, :, e - 1] * Qm % p
    out = np.zeros((N, M), dtype=np.int64)
    binom = np.array([[comb(e, t) % p for t in range(j + 1)] for e in range(k + 1)],
                     dtype=np.int64)
    npw = np.array([[pow(int(nvec[i]), t, p) for t in range(j + 1)] for i in range(l)],
                   dtype=np.int64)
    for t in compositions(j, l):
        term = np.ones((N, M), dtype=np.int64)
        ok = np.ones(M, dtype=bool)
        for i in range(l):
            ti = t[i]
            ai = monos[:, i]
            ok &= ai >= ti
            ex = np.clip(ai - ti, 0, None)
            coef = binom[ai, ti] * npw[i, ti] % p           # (M,)
            term = term * (pw[:, i, ex] * coef[None, :] % p) % p
        term[:, ~ok] = 0
        out = (out + term) % p
    return out


def transversal(a: np.ndarray, p: int) -> np.ndarray:
    """A vector n with a . n = 1."""
    l = len(a)
    e = max(i for i in range(l) if a[i] % p)
    v = np.zeros(l, dtype=np.int64)
    v[e] = pow(int(a[e]), p - 2, p)
    return v


def multi_matrix(normals, mult, k, p):
    """Kernel = D(A, m)_k (full coordinates, l * M_k unknowns)."""
    N = np.asarray(normals, dtype=np.int64) % p
    n, l = N.shape
    monos = monomials(k, l)
    blocks = []
    for H in range(n):
        b = N[H]
        nv = transversal(b, p)
        for j in range(min(int(mult[H]), k + 1)):
            Q = points_on_hyperplane(b, k - j, p)
            E = taylor_eval(Q, nv, monos, j, p)
            blocks.append(np.concatenate([int(b[i]) * E % p for i in range(l)], axis=1))
    if not blocks:
        return np.zeros((0, l * monos.shape[0]), dtype=np.int64)
    return np.vstack(blocks)


@lru_cache(maxsize=None)
def _mult_index(k: int, l: int, v: int) -> np.ndarray:
    """Index map: monomial index in degree k-1 -> index of x_v * monomial."""
    lo = monomials(k - 1, l)
    hi = monomials(k, l)
    pos = {tuple(r): i for i, r in enumerate(hi.tolist())}
    out = []
    for r in lo.tolist():
        r = list(r)
        r[v] += 1
        out.append(pos[tuple(r)])
    return np.array(out, dtype=np.int64)


def shift_up(basis: np.ndarray, k: int, l: int) -> np.ndarray:
    """Images x_v * theta (v = 0..l-1) of degree-(k-1) derivations (rows of
    basis, l blocks of M_{k-1} coefficients) in degree k."""
    if basis.shape[0] == 0:
        return np.zeros((0, l * monomials(k, l).shape[0]), dtype=np.int64)
    Mlo = monomials(k - 1, l).shape[0]
    Mhi = monomials(k, l).shape[0]
    outs = []
    for v in range(l):
        idx = _mult_index(k, l, v)
        img = np.zeros((basis.shape[0], l * Mhi), dtype=np.int64)
        for c in range(l):
            img[:, c * Mhi + idx] = basis[:, c * Mlo:(c + 1) * Mlo]
        outs.append(img)
    return np.vstack(outs)


def module_generators(normals, mult, p, kmax=None, stop_at_rank=True):
    """Degrees of minimal generators of D(A, m) up to kmax (mod p).
    Returns (gens: list of degrees, bases: {k: kernel basis})."""
    N = np.asarray(normals, dtype=np.int64) % p
    l = N.shape[1]
    total = int(sum(mult))
    kmax = total if kmax is None else kmax
    gens, bases = [], {}
    prev = None
    for k in range(0, kmax + 1):
        B = nullspace_mod(multi_matrix(N, mult, k, p), p)
        bases[k] = B
        r = 0
        if prev is not None and prev.shape[0] and B.shape[0]:
            r = rank_mod(shift_up(prev, k, l), p)
        g = B.shape[0] - r
        gens.extend([k] * g)
        prev = B
        if stop_at_rank and len(gens) >= l:
            break
    return gens, bases


def _eval_theta(vec, k, l, x0, p):
    M = monomials(k, l).shape[0]
    mv = eval_monos(x0[None, :], monomials(k, l), p)[0]
    return np.array([int(sum(int(a) * int(b) for a, b in zip(vec[i * M:(i + 1) * M], mv)) % p)
                     for i in range(l)], dtype=np.int64)


def multi_freeness(normals, mult, p, rng=None, tries=8):
    """Freeness of the multiarrangement (A, m) over F_p via minimal
    generators + Saito's criterion.  Returns (status, generator degrees)."""
    rng = rng or random.Random(7)
    N = np.asarray(normals, dtype=np.int64) % p
    l = N.shape[1]
    total = int(sum(mult))
    gens, bases = module_generators(N, mult, p)
    if len(gens) != l or sum(gens) != total:
        return "nonfree", gens
    for _ in range(tries):
        x0 = np.array([rng.randrange(1, p) for _ in range(l)], dtype=np.int64)
        cols = []
        for d in gens:
            B = bases[d]
            coef = [rng.randrange(p) for _ in range(B.shape[0])]
            vec = np.zeros(B.shape[1], dtype=np.int64)
            for c, row in zip(coef, B):
                vec = (vec + c * row) % p
            cols.append(_eval_theta(vec, d, l, x0, p))
        if _det_mod(np.stack(cols, axis=1), p) != 0:
            return "free", gens
    return "nonfree_saito", gens
