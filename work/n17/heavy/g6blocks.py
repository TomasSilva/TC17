"""Decode heavyaug/lsgen3 graph6 lines (points first, then blocks) into block lists on d points."""
import sys
def decode(line, d):
    line = line.strip()
    n = ord(line[0]) - 63
    bits = []
    for ch in line[1:]:
        v = ord(ch) - 63
        for q in range(5, -1, -1): bits.append((v >> q) & 1)
    adj = {}
    pos = 0
    for j in range(1, n):
        for i in range(j):
            if bits[pos]:
                adj.setdefault(j, []).append(i)
            pos += 1
    blocks = []
    for j in range(d, n):
        blocks.append(sorted(i for i in adj.get(j, []) if i < d))
    return blocks
if __name__ == '__main__':
    d = int(sys.argv[1])
    import collections
    W = collections.Counter(); nb = collections.Counter()
    for k, line in enumerate(sys.stdin):
        B = decode(line, d)
        w = sum((len(b) - 2) * (len(b) - 3) // 2 for b in B)
        W[w] += 1; nb[len(B)] += 1
    print('W:', sorted(W.items())); print('blocks:', sorted(nb.items()))
