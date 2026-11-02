"""Canonical form of a rank-3 lattice on d lines (blocks of size >= 3) via nauty labelg with the
lines kept as a separate cell."""
import subprocess
def g6(d, blocks):
    n = d + len(blocks)
    adj = [[0] * n for _ in range(n)]
    for j, b in enumerate(blocks):
        for x in b:
            adj[x][d + j] = adj[d + j][x] = 1
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(adj[i][j])
    while len(bits) % 6: bits.append(0)
    s = chr(63 + n)
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k + 6]: v = 2 * v + b
        s += chr(63 + v)
    return s
def canon_many(d, list_of_blocks):
    inp = '\n'.join(g6(d, [sorted(b) for b in bl if len(b) >= 3]) for bl in list_of_blocks) + '\n'
    r = subprocess.run(['labelg', '-q', '-f' + 'a' * d], input=inp, capture_output=True, text=True)
    return r.stdout.split('\n')[:len(list_of_blocks)]
