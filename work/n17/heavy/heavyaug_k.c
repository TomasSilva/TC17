/* Canonical augmentation (McKay) for "heavy configurations": sets of blocks (multiple points of
 * multiplicity in [4, mmax]) on d lines, pairwise meeting in at most one line, with the monotone
 * constraints of the residual Terao cases:
 *     h(v) := sum_{B ∋ v} (|B|-2) <= hi_eff,   W + sum_v max(0, h(v)-lo) <= budget,   X_H <= Xt.
 * Outputs (graph6, points first, then blocks) every configuration that also satisfies (H4) and (H5)
 * of Lemma 4.1 of the paper (W >= Wmin, completion capacity), one per isomorphism class (Section 4.2).
 *
 * Canonical deletion: the block whose vertex has the largest canonical index (blocks are coloured
 * by size, size cells after the point cell).  A child C+B is accepted iff B is in the Aut(C+B)-orbit
 * of the canonical deletion block; siblings are de-duplicated by their canonical graph.
 *
 * usage: heavyaug d mmax lo hi Xt Wmin
 */
#define MAXN 64
#include <nauty/nauty.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

#define MAXD 24
#define MAXB 40

static int d, mmax, lo, hi, Xt, Wmin, budget, hi_eff, Wmax = 1000, quiet = 0;
static long long whist[64];
static int Dmax = 4, split_n = 1, split_r = 0, split_depth = 2;
static long long split_ctr = 0, subtrees_done = 0;
static int probe = 0; static double est_nodes = 0, est_out = 0, cur_w = 1.0; static double est_wout[64];
static unsigned long long rng = 88172645463325252ULL;
static unsigned long long xr(void){ rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static long long nodes = 0, nout = 0;

typedef struct {
    int nb;
    uint32_t b[MAXB];
    int h[MAXD];
    uint32_t cov[MAXD];
    int X, W;
} Cfg;

static int popc(uint32_t x) { return __builtin_popcount(x); }

static void make_graph(const Cfg *c, graph *g, int *lab, int *ptn, int *n_out) {
    int n = d + c->nb;
    int m = SETWORDSNEEDED(n);
    EMPTYGRAPH(g, m, n);
    /* order block vertices by size for the colouring */
    int idx[MAXB], k = 0;
    for (int s = 4; s <= mmax; s++)
        for (int j = 0; j < c->nb; j++) if (popc(c->b[j]) == s) idx[k++] = j;
    for (int j = 0; j < c->nb; j++) {
        int v = d + j;
        for (int x = 0; x < d; x++) if ((c->b[j] >> x) & 1) ADDONEEDGE(g, x, v, m);
    }
    int p = 0;
    for (int x = 0; x < d; x++) { lab[p] = x; ptn[p] = 1; p++; }
    ptn[p - 1] = 0;
    for (int q = 0; q < c->nb; q++) {
        int j = idx[q];
        lab[p] = d + j;
        int s = popc(c->b[j]);
        int nexts = (q + 1 < c->nb) ? popc(c->b[idx[q + 1]]) : -1;
        ptn[p] = (nexts == s) ? 1 : 0;
        p++;
    }
    *n_out = n;
}

/* canonical form + orbits */
static void canon(const Cfg *c, graph *cg, int *orbits, int *lab, int *n_out) {
    DEFAULTOPTIONS_GRAPH(options);
    statsblk stats;
    graph g[MAXN * MAXM];
    int ptn[MAXN];
    int n;
    make_graph(c, g, lab, ptn, &n);
    int m = SETWORDSNEEDED(n);
    options.getcanon = TRUE;
    options.defaultptn = FALSE;
    densenauty(g, lab, ptn, orbits, &options, &stats, m, n, cg);
    *n_out = n;
}

static void emit(const Cfg *c) {
    int n = d + c->nb;
    int nbits = n * (n - 1) / 2;
    static unsigned char bits[8192];
    memset(bits, 0, (size_t)nbits + 6);
    int pos = 0;
    for (int j = 1; j < n; j++)
        for (int i = 0; i < j; i++) {
            int a = 0;
            if (j >= d && i < d) a = (c->b[j - d] >> i) & 1;
            bits[pos++] = (unsigned char)a;
        }
    char buf[8192];
    int k = 0;
    buf[k++] = (char)(63 + n);
    for (int p = 0; p < nbits; p += 6) {
        int v = 0;
        for (int q = 0; q < 6; q++) v = (v << 1) | (p + q < nbits ? bits[p + q] : 0);
        buf[k++] = (char)(63 + v);
    }
    buf[k++] = '\n'; buf[k] = 0;
    fputs(buf, stdout);
}

static int final_ok(const Cfg *c) {
    if (c->W < Wmin || c->W > budget) return 0;
    int t3 = Xt - c->X;
    if (t3 < 0) return 0;
    int need = 0, cap = 0, ex = 0;
    uint32_t all = (1u << d) - 1;
    for (int j = 0; j < d; j++) {
        if (c->h[j] > hi_eff) return 0;
        int u = popc(~c->cov[j] & all & ~(1u << j));
        int cc = u / 2;
        if (cc > hi_eff - c->h[j]) cc = hi_eff - c->h[j];
        int nd = lo - c->h[j]; if (nd < 0) nd = 0;
        if (cc < nd) return 0;
        need += nd; cap += cc;
        if (c->h[j] > lo) ex += c->h[j] - lo;
    }
    if (3 * t3 < need || 3 * t3 > cap) return 0;
    if (c->W + ex > budget) return 0;
    return 1;
}

static int monotone_ok(const Cfg *c) {
    if (c->X > Xt) return 0;
    if (c->W > Wmax) return 0;
    {   /* (W5) and the D-pair bound: only the last block can create new disjoint pairs */
        int nb = c->nb, sl = popc(c->b[nb - 1]), dp = 0;
        for (int i = 0; i < nb; i++) for (int j = i + 1; j < nb; j++) {
            if (c->b[i] & c->b[j]) continue;
            int t = popc(c->b[i]) + popc(c->b[j]) - 2;
            if (t > 8) return 0;
            if (t == 8) dp++;
        }
        if (dp > Dmax) return 0;
        (void)sl;
    }
    int ex = 0;
    for (int j = 0; j < d; j++) {
        if (c->h[j] > hi_eff) return 0;
        if (c->h[j] > lo) ex += c->h[j] - lo;
    }
    if (c->W + ex > budget) return 0;
    if (ex > budget - Wmin) return 0;
    return 1;
}

/* simple open-addressing hash set of canonical graphs for sibling de-duplication */
typedef struct { uint64_t *key; int cap, n; } HSet;
static uint64_t hash_graph(const graph *g, int m, int n) {
    uint64_t h = 1469598103934665603ULL ^ (uint64_t)n;
    for (int i = 0; i < m * n; i++) { h ^= (uint64_t)g[i]; h *= 1099511628211ULL; h ^= h >> 29; }
    return h ? h : 1;
}

static void add_block(Cfg *c, uint32_t B) {
    int s = popc(B);
    c->b[c->nb++] = B;
    for (int x = 0; x < d; x++) if ((B >> x) & 1) { c->h[x] += s - 2; c->cov[x] |= B & ~(1u << x); }
    c->X += (s - 1) * (s - 2) / 2;
    c->W += (s - 2) * (s - 3) / 2;
}

static void extend(const Cfg *c);

#define MAXCAND 300000   /* at most C(16,4)+C(16,5)+C(16,6) = 14196 candidates are needed */

/* enumerate candidate blocks B (size 4..mmax) compatible with c: |B ∩ b| <= 1 for all blocks,
   i.e. no pair inside B already covered. */

static void gen_blocks(const Cfg *c, uint32_t cur, int start, int size, uint32_t *out, int *nout_) {
    int s = popc(cur);
    if (s >= 4) {
        if (*nout_ >= MAXCAND) { fprintf(stderr, "heavyaug: too many candidate blocks\n"); exit(3); }
        out[(*nout_)++] = cur;
    }
    if (s >= mmax) return;
    for (int x = start; x < d; x++) {
        if (c->cov[x] & cur) continue;
        if (c->h[x] + 2 > hi_eff) continue;   /* a heavy block adds >= 2 to h(x) */
        gen_blocks(c, cur | (1u << x), x + 1, size, out, nout_);
    }
    (void)size;
}

static void extend(const Cfg *c) {
    if (c->nb == split_depth) {
        long long k = split_ctr++;
        if (k % split_n != split_r) return;
    }
    nodes++;
    if (probe) { est_nodes += cur_w; if (final_ok(c)) { est_out += cur_w; if (c->W < 64) est_wout[c->W] += cur_w; } }
    if (!probe && (c->nb >= split_depth || split_r == 0) && final_ok(c)) { if (!quiet) emit(c); nout++; if (c->W < 64) whist[c->W]++; }
    /* candidates */
    uint32_t *cands = (uint32_t *)malloc(sizeof(uint32_t) * MAXCAND);
    int nc = 0;
    gen_blocks(c, 0, 0, 0, cands, &nc);
    if (nc < 0 || nc > MAXCAND) { fprintf(stderr, "heavyaug: candidate count out of range\n"); exit(3); }
    /* sibling dedupe */
    int hcap = 1;
    while (hcap < 4 * nc + 16) hcap <<= 1;
    uint64_t *hs = (uint64_t *)calloc((size_t)hcap, sizeof(uint64_t));
    int *hidx = (int *)malloc(sizeof(int) * (size_t)hcap);
    graph *store = (graph *)malloc(sizeof(graph) * (size_t)MAXN * (size_t)(nc + 1));
    int *storen = (int *)malloc(sizeof(int) * (size_t)(nc + 1));
    int nstore = 0;
    Cfg *pchild = probe ? (Cfg *)malloc(sizeof(Cfg) * (size_t)(nc + 1)) : NULL; int npchild = 0;
    for (int q = 0; q < nc; q++) {
        uint32_t B = cands[q];
        Cfg ch = *c;
        add_block(&ch, B);
        /* block-size bound per vertex */
        int okb = 1;
        for (int x = 0; x < d; x++) if (((B >> x) & 1) && ch.h[x] > hi_eff) { okb = 0; break; }
        if (!okb || !monotone_ok(&ch)) continue;
        graph cg[MAXN * MAXM];
        int orbits[MAXN], lab[MAXN], n;
        canon(&ch, cg, orbits, lab, &n);
        int m = SETWORDSNEEDED(n);
        /* canonical deletion: vertex at the last canonical position is a block (blocks after points,
           largest size cell last) */
        int last = lab[n - 1];
        int newv = d + ch.nb - 1;
        if (orbits[last] != orbits[newv]) continue;
        uint64_t hv = hash_graph(cg, m, n);
        int pos = (int)(hv & (uint64_t)(hcap - 1)), dup = 0;
        while (hs[pos]) {
            if (hs[pos] == hv) {
                int k = hidx[pos];
                if (storen[k] == n && memcmp(store + (size_t)k * MAXN, cg, sizeof(graph) * (size_t)(m * n)) == 0) { dup = 1; break; }
            }
            pos = (pos + 1) & (hcap - 1);
        }
        if (dup) continue;
        hs[pos] = hv; hidx[pos] = nstore;
        memcpy(store + (size_t)nstore * MAXN, cg, sizeof(graph) * (size_t)(m * n));
        storen[nstore] = n; nstore++;
        if (probe) { pchild[npchild++] = ch; continue; }
        extend(&ch);
        if (c->nb == split_depth - 1 && 0) {}
    }
    if (probe) { if (npchild > 0) { int k = (int)(xr() % (unsigned long long)npchild); double sv = cur_w; cur_w *= npchild; Cfg cc = pchild[k]; free(pchild); pchild = NULL; extend(&cc); cur_w = sv; } if (pchild) free(pchild); }
    if (c->nb == split_depth && 1) { subtrees_done++; if (subtrees_done % 20 == 0) fprintf(stderr, "progress r=%d: %lld subtrees, %lld nodes, %lld out\n", split_r, subtrees_done, nodes, nout); }
    free(hs); free(hidx); free(store); free(storen);
    free(cands);
}

/* ---- output integrity: a failed write must never look like a successful run ---- */
#include <unistd.h>
static void check_output_at_exit(void) {
    if (fflush(stdout) != 0 || ferror(stdout)) {
        fputs("fatal: error while writing the output\n", stderr);
        _exit(2);
    }
}

int main(int argc, char **argv) {
    atexit(check_output_at_exit);
    if (argc < 7) { fprintf(stderr, "usage: heavyaug d mmax lo hi Xt Wmin\n"); return 1; }
    d = atoi(argv[1]); mmax = atoi(argv[2]); lo = atoi(argv[3]); hi = atoi(argv[4]);
    Xt = atoi(argv[5]); Wmin = atoi(argv[6]);
    if (argc > 7) Wmax = atoi(argv[7]);
    if (argc > 8) quiet = atoi(argv[8]);
    if (argc > 9) split_n = atoi(argv[9]);
    if (argc > 10) split_r = atoi(argv[10]);
    if (argc > 11) Dmax = atoi(argv[11]);
    if (argc > 12) split_depth = atoi(argv[12]);
    if (argc > 13) probe = atoi(argv[13]);
    if (argc > 14) rng ^= (unsigned long long)atoll(argv[14]) * 0x9E3779B97F4A7C15ULL;
    budget = 3 * Xt - d * lo;
    hi_eff = hi;
    if (lo + budget - Wmin < hi_eff) hi_eff = lo + budget - Wmin;
    nauty_check(WORDSIZE, MAXM, MAXN, NAUTYVERSIONID);
    if (probe) {
        int nprobe = probe; Cfg c0; double sn = 0, so = 0, sw[64] = {0}; double so2 = 0;
        for (int t = 0; t < nprobe; t++) {
            est_nodes = est_out = 0; for (int w = 0; w < 64; w++) est_wout[w] = 0; cur_w = 1.0;
            memset(&c0, 0, sizeof c0); extend(&c0);
            sn += est_nodes; so += est_out; so2 += est_out * est_out; for (int w = 0; w < 64; w++) sw[w] += est_wout[w];
        }
        fprintf(stderr, "PROBE n=%d est_nodes=%.4g est_out=%.4g (sd of mean %.3g)\n", nprobe, sn / nprobe, so / nprobe, sqrt((so2 / nprobe - (so / nprobe) * (so / nprobe)) / nprobe));
        for (int w = 0; w < 64; w++) if (sw[w] > 0) fprintf(stderr, "  W=%d: %.4g\n", w, sw[w] / nprobe);
        return 0;
    }
    Cfg c;
    memset(&c, 0, sizeof c);
    extend(&c);
    fprintf(stderr, "heavyaug d=%d mmax=%d lo=%d hi_eff=%d Xt=%d Wmin=%d budget=%d: nodes=%lld output=%lld\n",
            d, mmax, lo, hi_eff, Xt, Wmin, budget, nodes, nout);
    for (int w = 0; w < 64; w++) if (whist[w]) fprintf(stderr, "W=%d: %lld\n", w, whist[w]);
    return 0;
}
