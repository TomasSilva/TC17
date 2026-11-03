"""
db.py -- read the FreeLineArrangements certified database (read-only) and
reduce records modulo a prime (quadratic fields via a square root of d mod p).
"""
from __future__ import annotations

import gzip
import json
import re
from fractions import Fraction
from pathlib import Path

DB = Path("/Users/agent/Projects/FreeLineArrangements/certified_free_arrangements.jsonl.gz")
_TOK = re.compile(r"^(?P<a>[+-]?\d+(?:/\d+)?(?=[+-]))?(?P<b>[+-]?(?:\d+(?:/\d+)?)?)s$")


def records(path=DB):
    with gzip.open(path, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            if "_meta" in r:
                continue
            yield r


def sqrt_mod(d, p):
    d %= p
    if d == 0:
        return 0
    if pow(d, (p - 1) // 2, p) != 1:
        return None
    # Tonelli-Shanks
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(d, q, p), pow(d, (q + 1) // 2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1:
            tt = tt * tt % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


def parse_scalar(tok, d):
    """Return (a, b) Fractions with value a + b*sqrt(d)."""
    t = str(tok).strip()
    neg = False
    if t.startswith("-["):
        neg, t = True, t[1:]
    if t.startswith("[") and t.endswith("]"):
        m = _TOK.match(t[1:-1].replace(" ", ""))
        a = Fraction(m.group("a")) if m.group("a") else Fraction(0)
        b = m.group("b")
        b = Fraction(1) if b in ("", "+") else Fraction(-1) if b == "-" else Fraction(b)
        return (-a, -b) if neg else (a, b)
    return (Fraction(t), Fraction(0))


def field_d(rec):
    f = rec.get("field", "QQ")
    if isinstance(f, dict) and f.get("type") == "quadratic":
        return int(f["d"])
    return None


def lines_exact(rec):
    d = field_d(rec)
    return [[parse_scalar(c, d) for c in l] for l in rec["lines"]], d


def lines_mod_p(rec, p, root_choice=0):
    """Integer normals mod p (None if the field does not split at p or a
    denominator vanishes)."""
    L, d = lines_exact(rec)
    s = 0
    if d is not None:
        s = sqrt_mod(d, p)
        if s is None:
            return None
        if root_choice:
            s = (-s) % p
    out = []
    for l in L:
        row = []
        for (a, b) in l:
            val = 0
            for q, mult in ((a, 1), (b, s)):
                if q == 0:
                    continue
                if q.denominator % p == 0:
                    return None
                val = (val + q.numerator % p * pow(q.denominator % p, p - 2, p) % p * mult) % p
            row.append(val)
        out.append(row)
    return out
