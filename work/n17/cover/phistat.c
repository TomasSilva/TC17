/* For complete 17-line lattices (graph6 from lsgen3: points = lines first, then blocks of size >= 3):
 * s_H, n8, max over 4-sets S of phi(S) = sum_{H in S}(s_H - 7) - f(S), f(S) = #points P with L_P subset S.
 * Prints a histogram of (n8, phimax) and writes lattices with n8 >= 1 and phimax <= T to stdout. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define D 17
static int dbl[D][D], tri[D][D][D];
int main(int argc, char **argv) {
    int T = argc > 1 ? atoi(argv[1]) : 0;
    char line[4096];
    long hist[D + 1][16]; memset(hist, 0, sizeof hist);
    long nlat = 0;
    while (fgets(line, sizeof line, stdin)) {
        int n = line[0] - 63; if (n < D) continue;
        int len = strlen(line); while (len && (line[len-1] == '\n' || line[len-1] == '\r')) line[--len] = 0;
        /* decode adjacency upper triangle */
        static unsigned char bits[1 << 16]; int nb = 0;
        for (int k = 1; k < len; k++) { int v = line[k] - 63; for (int q = 5; q >= 0; q--) bits[nb++] = (v >> q) & 1; }
        static unsigned int mask[256]; int nblk = n - D;
        memset(mask, 0, sizeof(unsigned int) * nblk);
        int pos = 0;
        for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) { if (bits[pos]) { if (j >= D && i < D) mask[j - D] |= 1u << i; } pos++; }
        memset(dbl, 0, sizeof dbl); memset(tri, 0, sizeof tri);
        int cov[D][D]; memset(cov, 0, sizeof cov);
        unsigned int quad[64]; int nq = 0;
        int s[D]; memset(s, 0, sizeof s);
        for (int b = 0; b < nblk; b++) {
            int el[D], m = 0;
            for (int i = 0; i < D; i++) if (mask[b] >> i & 1) el[m++] = i;
            for (int a = 0; a < m; a++) { s[el[a]]++; for (int c = a + 1; c < m; c++) cov[el[a]][el[c]] = cov[el[c]][el[a]] = 1; }
            if (m == 3) { int a = el[0], bb = el[1], c = el[2]; tri[a][bb][c] = 1; }
            if (m == 4) quad[nq++] = mask[b];
        }
        for (int a = 0; a < D; a++) for (int c = a + 1; c < D; c++) if (!cov[a][c]) { dbl[a][c] = 1; s[a]++; s[c]++; }
        int n8 = 0; for (int i = 0; i < D; i++) if (s[i] == 8) n8++;
        int best = -100;
        for (int a = 0; a < D; a++) for (int b = a + 1; b < D; b++) for (int c = b + 1; c < D; c++) for (int e = c + 1; e < D; e++) {
            int w = s[a] + s[b] + s[c] + s[e] - 28;
            if (w <= best) continue;
            int f = dbl[a][b] + dbl[a][c] + dbl[a][e] + dbl[b][c] + dbl[b][e] + dbl[c][e]
                  + tri[a][b][c] + tri[a][b][e] + tri[a][c][e] + tri[b][c][e];
            unsigned int S = (1u << a) | (1u << b) | (1u << c) | (1u << e);
            for (int q = 0; q < nq; q++) if (quad[q] == S) f++;
            if (w - f > best) best = w - f;
        }
        nlat++;
        int bi = best + 8; if (bi < 0) bi = 0; if (bi > 15) bi = 15;
        hist[n8][bi]++;
        if (n8 >= 1 && best <= T) printf("%s\n", line);
    }
    fprintf(stderr, "lattices %ld\n n8 : count by phimax (-8..7)\n", nlat);
    for (int k = 0; k <= D; k++) {
        long tot = 0; for (int j = 0; j < 16; j++) tot += hist[k][j];
        if (!tot) continue;
        fprintf(stderr, "n8=%2d:", k);
        for (int j = 0; j < 16; j++) if (hist[k][j]) fprintf(stderr, " phi%+d:%ld", j - 8, hist[k][j]);
        fprintf(stderr, "\n");
    }
    return 0;
}
