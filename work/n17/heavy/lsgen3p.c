/* Stage 2 of the enumeration (Section 4.3 of the paper): completion of heavy configurations by
 * triple points, subject to the constraints (R1)-(R5).
 *
 * Mode `complete` (the mode used by run.sh) reads heavy configurations (graph6, points first, then
 * blocks) from stdin, relabels the points by decreasing h(v), and processes the points i = 0, 1, ...
 * in this order: at step i it adds all triples whose smallest element is i, pruning with (R2), (R5)
 * and the capacity bounds; every completion satisfying (R1)-(R5) is written to stdout (graph6,
 * points first).  Symmetry breaking at step i: the unprocessed points with identical membership in
 * all existing blocks form classes; the smallest undecided point either lies on no new triple
 * through i (and then neither does any later point of its class), or it is paired with the first
 * unused point of a class.  Such transpositions are automorphisms of the current partial structure
 * fixing all processed points and the triples already chosen.  Remaining isomorphic copies are
 * removed with nauty (labelg) afterwards.
 *
 * (Without the argument `complete`, the program generates the heavy configurations itself by a
 * two-pass orderly algorithm; this mode is not used for the results of the paper.)
 *
 * usage: lsgen3 d mmax mmin lo hi Xt Wmin 0 complete < heavy.g6
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <signal.h>
#include <unistd.h>

#define MAXD 24
#define MAXB 64

static int d, mmax, mmin, lo, hi, Xt, budget, Wmin, hi_eff, heavy_only = 0;
static uint32_t cov[MAXD];
static int ecur[MAXD];
static uint64_t memb[MAXD];
static int tcnt[MAXD][MAXD];
static int t0vec[MAXD];
static uint32_t bmask[MAXB];
static int bsize[MAXB];
static int nb = 0, Xg = 0, Wg = 0;
static int pass = 1;
static int no_t0 = 0;
static long long nodes = 0, nsol = 0, nheavy = 0;
static int maxadd[MAXD + 1];
static int prune3 = 0, eight = -1; static long long npruned = 0;
/* 1 if elements a<b<i (all final) together with i form a 3-chain of 8-point lines: e==eight for all three,
   pairwise in a common block (no double point between them), and no block equal to {a,b,i}. */
static int has_new_chain(int i) {
    if (ecur[i] != eight) return 0;
    for (int a = 0; a < i; a++) {
        if (ecur[a] != eight || !((cov[i] >> a) & 1)) continue;
        for (int b = a + 1; b < i; b++) {
            if (ecur[b] != eight || !((cov[i] >> b) & 1) || !((cov[a] >> b) & 1)) continue;
            uint32_t m = (1u << a) | (1u << b) | (1u << i); int full = 0;
            for (int k = 0; k < nb; k++) if (bmask[k] == m) { full = 1; break; }
            if (!full) return 1;
        }
    }
    return 0;
}


/* compare type(j) with type(0); in pass 1 only sizes >= 4 */
static inline int typegt_vec(const int *v) {
    int smin = (pass == 1) ? 4 : 3;
    for (int s = MAXD - 1; s >= smin; s--)
        if (v[s] != t0vec[s]) return v[s] > t0vec[s];
    return 0;
}
static inline int typegt(int j) { if (no_t0) return 0; return typegt_vec(tcnt[j]); }

static void emit(void) {
    int n = d + nb;
    int nbits = n * (n - 1) / 2;
    static unsigned char bits[8192];
    memset(bits, 0, (size_t)nbits + 6);
    int pos = 0;
    for (int j = 1; j < n; j++)
        for (int i = 0; i < j; i++) {
            int a = 0;
            if (j >= d && i < d) a = (bmask[j - d] >> i) & 1;
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
    buf[k++] = '\n';
    buf[k] = 0;
    fputs(buf, stdout);
}

typedef struct {
    int i;
    int nC, C[MAXD];
    uint32_t Cmask;
    int ncls, clsof[MAXD], shared[MAXD], clssz[MAXD], clsmem[MAXD][MAXD];
    int base_excess;
    int newcnt[MAXD];
    int nnew;
    uint32_t newmask[MAXD];
    int newsize[MAXD];
} Step;

static void step(int i);

static inline int newtypegt(Step *st) {
    if (st->i == 0 || no_t0) return 0;
    int v[MAXD];
    for (int s = 0; s < MAXD; s++) v[s] = tcnt[st->i][s] + st->newcnt[s];
    return typegt_vec(v);
}

/* ---------- feasibility checks at the start of a step (elements >= i unprocessed in this pass) ---------- */
static int feasible_start(int i) {
    int smin = (pass == 1) ? 4 : 3;
    (void)smin;
    int excess = 0;
    if (pass == 2)
        for (int h = 0; h < i; h++) excess += ecur[h] - lo;
    for (int j = (pass == 2 ? i : 0); j < d; j++) if (ecur[j] > lo) excess += ecur[j] - lo;
    if (Wg + excess > budget) return 0;
    if (excess > budget - Wmin) return 0;
    if (Xg > Xt) return 0;
    if (pass == 1) {
        /* every element can still reach lo using triples with any uncovered element (pass 2) */
        uint32_t all = (d == 32) ? 0xffffffffu : ((1u << d) - 1);
        for (int j = 0; j < d; j++) {
            if (ecur[j] > hi_eff) return 0;
            int u = __builtin_popcount(~cov[j] & all & ~(1u << j));
            /* heavy blocks may still be added for j >= i; triples later: e gain <= maxadd[u] */
            if (ecur[j] + maxadd[u] < lo) return 0;
        }
        return 1;
    }
    /* pass 2: only triples among elements >= i remain */
    uint32_t later = 0;
    for (int j = i; j < d; j++) later |= 1u << j;
    int need = 0, cap = 0;
    for (int j = i; j < d; j++) {
        int u = __builtin_popcount(~cov[j] & later & ~(1u << j));
        int c = u / 2;
        if (c > hi_eff - ecur[j]) c = hi_eff - ecur[j];
        if (c < 0) return 0;
        int nd = lo - ecur[j];
        if (nd < 0) nd = 0;
        if (c < nd) return 0;
        need += nd; cap += c;
    }
    int rem = Xt - Xg;              /* triples still to be created (each adds 1 to X) */
    if (3 * rem < need || 3 * rem > cap) return 0;
    /* exact budget: final sum(e-lo) = budget - W.  Remaining e gain = 3*rem. */
    int cur = 0;
    for (int h = 0; h < d; h++) cur += ecur[h] - lo;   /* may be negative for elements below lo */
    if (cur + 3 * rem != budget - Wg) {                  /* identity sum_v e(v) = 3X - W: always holds */
        fprintf(stderr, "lsgen3: internal error (budget identity)\n");
        exit(5);
    }
    return 1;
}

static void apply(Step *st) {
    int i = st->i;
    uint32_t scov[MAXD]; int secur[MAXD]; uint64_t smemb[MAXD]; int stc[MAXD][MAXD]; int st0[MAXD];
    memcpy(scov, cov, sizeof cov); memcpy(secur, ecur, sizeof ecur);
    memcpy(smemb, memb, sizeof memb); memcpy(stc, tcnt, sizeof tcnt); memcpy(st0, t0vec, sizeof t0vec);
    int snb = nb;
    for (int k = 0; k < st->nnew; k++) {
        int b = nb++;
        uint32_t m = st->newmask[k];
        int s = st->newsize[k];
        bmask[b] = m; bsize[b] = s;
        for (int x = 0; x < d; x++)
            if ((m >> x) & 1) {
                cov[x] |= m & ~(1u << x);
                ecur[x] += s - 2;
                memb[x] |= 1ULL << b;
                tcnt[x][s]++;
            }
    }
    int ok = 1;
    if (i == 0) memcpy(t0vec, tcnt[0], sizeof t0vec);
    else if (typegt(i)) ok = 0;
    if (ok && ecur[i] > hi_eff) ok = 0;
    if (ok && pass == 2 && ecur[i] < lo) ok = 0;
    if (ok) for (int j = i + 1; j < d; j++) if (typegt(j)) { ok = 0; break; }
    if (ok && prune3 && pass == 2 && has_new_chain(i)) { ok = 0; npruned++; }
    if (ok) step(i + 1);
    memcpy(cov, scov, sizeof cov); memcpy(ecur, secur, sizeof ecur);
    memcpy(memb, smemb, sizeof memb); memcpy(tcnt, stc, sizeof tcnt); memcpy(t0vec, st0, sizeof t0vec);
    nb = snb;
}

static void build(Step *st, uint32_t assigned, uint32_t doubles, int e_i, int X, int W);

typedef struct {
    Step *st;
    uint32_t assigned, doubles;
    int e_i, X, W;
    int norder, order[MAXD];
    int nav[MAXD], av[MAXD][MAXD];
} Pick;

static void pick(Pick *c, int idx, int nmem, int *mem, uint32_t mask) {
    Step *st = c->st;
    int s = nmem + 1;
    int smin = (pass == 1) ? 4 : 3, smax = (pass == 1) ? mmax : 3;
    if (s >= smin) {
        int ex = s - 2, dX = (s - 1) * (s - 2) / 2, dW = (s - 2) * (s - 3) / 2;
        if (c->e_i + ex <= hi_eff && c->X + dX <= Xt && c->W + dW <= budget) {
            st->newmask[st->nnew] = mask | (1u << st->i);
            st->newsize[st->nnew] = s;
            st->nnew++;
            st->newcnt[s]++;
            if (!newtypegt(st))
                build(st, c->assigned | mask, c->doubles, c->e_i + ex, c->X + dX, c->W + dW);
            st->newcnt[s]--;
            st->nnew--;
        }
    }
    if (s >= smax) return;
    for (int t = idx; t < c->norder; t++) {
        int kk = c->order[t];
        int nL = c->nav[kk];
        int maxc = st->shared[kk] ? 1 : nL;
        uint32_t cm = mask;
        int nm = nmem;
        for (int cc = 1; cc <= maxc; cc++) {
            int x = c->av[kk][cc - 1];
            if (cov[x] & cm) break;
            mem[nm++] = x;
            cm |= 1u << x;
            if (nm + 1 > smax) break;
            pick(c, t + 1, nm, mem, cm);
        }
    }
}

static void build(Step *st, uint32_t assigned, uint32_t doubles, int e_i, int X, int W) {
    nodes++;
    if (pass == 2) {
        int navail = __builtin_popcount(st->Cmask & ~(assigned | doubles));
        if (e_i + navail / 2 < lo) return;
        int exi = e_i > lo ? e_i - lo : 0;
        if (W + st->base_excess + exi > budget) return;
    }
    int j = -1;
    for (int k = 0; k < st->nC; k++) {
        int x = st->C[k];
        if (!(((assigned | doubles) >> x) & 1)) { j = x; break; }
    }
    if (j < 0) {
        if (pass == 1 && st->i == 0)
            for (int k = 0; k + 1 < st->nnew; k++)
                if (st->newsize[k] < st->newsize[k + 1]) return;
        int sX = Xg, sW = Wg;
        Xg = X; Wg = W;
        apply(st);
        Xg = sX; Wg = sW;
        return;
    }
    int k = st->clsof[j];
    uint32_t rest = 0;
    for (int q = 0; q < st->clssz[k]; q++) {
        int x = st->clsmem[k][q];
        if (!(((assigned | doubles) >> x) & 1)) rest |= 1u << x;
    }
    build(st, assigned, doubles | rest, e_i, X, W);
    int smin = (pass == 1) ? 4 : 3;
    if (e_i + (smin - 2) > hi_eff) return;
    Pick c;
    c.st = st; c.assigned = assigned; c.doubles = doubles; c.e_i = e_i; c.X = X; c.W = W;
    c.norder = 0;
    int first[MAXD];
    for (int kk = 0; kk < st->ncls; kk++) {
        c.nav[kk] = 0;
        for (int q = 0; q < st->clssz[kk]; q++) {
            int x = st->clsmem[kk][q];
            if (x == j || (((assigned | doubles) >> x) & 1)) continue;
            c.av[kk][c.nav[kk]++] = x;
        }
        if (c.nav[kk]) { first[kk] = c.av[kk][0]; c.order[c.norder++] = kk; }
    }
    for (int a = 1; a < c.norder; a++) {
        int v = c.order[a], b = a - 1;
        while (b >= 0 && first[c.order[b]] > first[v]) { c.order[b + 1] = c.order[b]; b--; }
        c.order[b + 1] = v;
    }
    int mem[MAXD];
    mem[0] = j;
    pick(&c, 0, 1, mem, 1u << j);
}

static int end_of_pass1_ok(void) {
    if (Wg < Wmin || Wg > budget) return 0;
    int mx = 0;
    for (int b = 0; b < nb; b++) if (bsize[b] > mx) mx = bsize[b];
    if (mx < mmin) return 0;
    int t3 = Xt - Xg;
    if (t3 < 0) return 0;
    int need = 0, cap = 0, ex = 0;
    uint32_t all = (1u << d) - 1;
    for (int j = 0; j < d; j++) {
        if (ecur[j] > hi_eff) return 0;
        int u = __builtin_popcount(~cov[j] & all & ~(1u << j));
        int c = u / 2;
        if (c > hi_eff - ecur[j]) c = hi_eff - ecur[j];
        int nd = lo - ecur[j]; if (nd < 0) nd = 0;
        if (c < nd) return 0;
        need += nd; cap += c;
        if (ecur[j] > lo) ex += ecur[j] - lo;
    }
    if (3 * t3 < need || 3 * t3 > cap) return 0;
    if (Wg + ex > budget) return 0;
    return 1;
}

static void step(int i) {
    if (i == d) {
        if (pass == 1) {
            if (!end_of_pass1_ok()) return;
            nheavy++;
            if (heavy_only) { emit(); return; }
            pass = 2;
            int st0[MAXD]; memcpy(st0, t0vec, sizeof t0vec);
            step(0);
            memcpy(t0vec, st0, sizeof t0vec);
            pass = 1;
            return;
        }
        if (Xg != Xt || Wg < Wmin) return;
        nsol++;
        emit();
        return;
    }
    if (!feasible_start(i)) return;
    Step st;
    st.i = i; st.nC = 0; st.ncls = 0; st.nnew = 0; st.Cmask = 0;
    memset(st.newcnt, 0, sizeof st.newcnt);
    uint64_t key[MAXD];
    for (int j = i + 1; j < d; j++) {
        if ((cov[i] >> j) & 1) continue;
        st.C[st.nC++] = j;
        st.Cmask |= 1u << j;
        int k;
        for (k = 0; k < st.ncls; k++) if (key[k] == memb[j]) break;
        if (k == st.ncls) { key[k] = memb[j]; st.clssz[k] = 0; st.shared[k] = memb[j] != 0; st.ncls++; }
        st.clsmem[k][st.clssz[k]++] = j;
        st.clsof[j] = k;
    }
    int be = 0;
    if (pass == 2) {
        for (int h = 0; h < i; h++) be += ecur[h] - lo;
        for (int j = i + 1; j < d; j++) if (ecur[j] > lo) be += ecur[j] - lo;
    }
    st.base_excess = be;
    build(&st, 0, 0, ecur[i], Xg, Wg);
}

static void report(int sig) {
    (void)sig;
    fprintf(stderr, "[progress] nodes=%lld heavy=%lld solutions=%lld\n", nodes, nheavy, nsol);
    signal(SIGUSR1, report);
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
    if (argc < 8) {
        fprintf(stderr, "usage: lsgen3 d mmax mmin lo hi Xt Wmin [heavy_only | 0 complete]\n");
        return 1;
    }
    d = atoi(argv[1]); mmax = atoi(argv[2]); mmin = atoi(argv[3]);
    lo = atoi(argv[4]); hi = atoi(argv[5]); Xt = atoi(argv[6]); Wmin = atoi(argv[7]);
    if (argc > 8) heavy_only = atoi(argv[8]);
    if (argc > 10) { prune3 = 1; eight = atoi(argv[10]); }
    signal(SIGUSR1, report);
    budget = 3 * Xt - d * lo;
    hi_eff = hi;
    if (lo + budget - Wmin < hi_eff) hi_eff = lo + budget - Wmin;
    int m = mmax < 3 ? 3 : mmax;
    for (int u = 0; u <= d; u++) {
        int q = u / (m - 1), r = u % (m - 1);
        maxadd[u] = q * (m - 2) + (r > 1 ? r - 1 : 0);
    }
    if (argc > 9 && strcmp(argv[9], "complete") == 0) {
        /* read heavy configurations (graph6, points first) from stdin and complete each */
        no_t0 = 1;
        char line[8192];
        long long ncfg = 0;
        while (fgets(line, sizeof line, stdin)) {
            int n = line[0] - 63;
            int nbk = n - d;
            int bits_needed = n * (n - 1) / 2;
            static unsigned char bits[8192];
            int pos = 0;
            /* validate the input line: a malformed or truncated heavy configuration must stop the run */
            {
                size_t len = strcspn(line, "\r\n");
                int ok = n > d && n <= 62 && nbk <= MAXB && line[len] == '\n'
                         && (int)len == 1 + (bits_needed + 5) / 6;
                for (size_t k = 1; ok && k < len; k++) ok = line[k] >= 63 && line[k] <= 126;
                if (!ok) {
                    fprintf(stderr, "lsgen3: malformed heavy configuration on input line %lld\n", ncfg + 1);
                    exit(3);
                }
            }
            for (int k = 1; line[k] && line[k] != '\n' && pos < bits_needed; k++) {
                int v = line[k] - 63;
                for (int q = 5; q >= 0 && pos < bits_needed; q--) bits[pos++] = (v >> q) & 1;
            }
            uint32_t blk[MAXB];
            memset(blk, 0, sizeof blk);
            pos = 0;
            for (int j = 1; j < n; j++)
                for (int i = 0; i < j; i++) {
                    if (bits[pos] && j >= d && i < d) blk[j - d] |= 1u << i;
                    pos++;
                }
            /* relabel: heavy e descending */
            int he[MAXD], ord[MAXD], newlab[MAXD];
            for (int x = 0; x < d; x++) { he[x] = 0; ord[x] = x; }
            for (int b = 0; b < nbk; b++) { int sz = __builtin_popcount(blk[b]); for (int x = 0; x < d; x++) if ((blk[b] >> x) & 1) he[x] += sz - 2; }
            for (int a = 1; a < d; a++) { int v = ord[a], b2 = a - 1; while (b2 >= 0 && he[ord[b2]] < he[v]) { ord[b2 + 1] = ord[b2]; b2--; } ord[b2 + 1] = v; }
            for (int k = 0; k < d; k++) newlab[ord[k]] = k;
            memset(cov, 0, sizeof cov); memset(ecur, 0, sizeof ecur); memset(memb, 0, sizeof memb); memset(tcnt, 0, sizeof tcnt);
            nb = 0; Xg = 0; Wg = 0;
            for (int b = 0; b < nbk; b++) {
                uint32_t m = 0;
                for (int x = 0; x < d; x++) if ((blk[b] >> x) & 1) m |= 1u << newlab[x];
                int sz = __builtin_popcount(m);
                bmask[nb] = m; bsize[nb] = sz;
                for (int x = 0; x < d; x++) if ((m >> x) & 1) { cov[x] |= m & ~(1u << x); ecur[x] += sz - 2; memb[x] |= 1ULL << nb; tcnt[x][sz]++; }
                Xg += (sz - 1) * (sz - 2) / 2; Wg += (sz - 2) * (sz - 3) / 2;
                nb++;
            }
            ncfg++;
            if (!end_of_pass1_ok()) continue;
            pass = 2;
            step(0);
        }
        if (ferror(stdin)) {
            fprintf(stderr, "lsgen3: read error on the input\n");
            return 4;
        }
        fprintf(stderr, "completion mode: configs=%lld nodes=%lld solutions=%lld pruned3=%lld\n", ncfg, nodes, nsol, npruned);
        return 0;
    }
    step(0);
    fprintf(stderr, "d=%d mmax=%d mmin=%d e in [%d,%d] (eff hi %d) Xt=%d budget=%d Wmin=%d : nodes=%lld heavy_configs(labelled)=%lld solutions=%lld\n",
            d, mmax, mmin, lo, hi, hi_eff, Xt, budget, Wmin, nodes, nheavy, nsol);
    return 0;
}
