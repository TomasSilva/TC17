/* max over 4-sets of phi(S) = sum (s-7) - f(S) for 13-line lattices (graph6, lines first) */
#include <stdio.h>
#include <string.h>
#define D 13
static int dbl[D][D], tri[D][D][D];
int main(void){ char line[4096]; long hist[20]={0}; long tot=0;
 while(fgets(line,sizeof line,stdin)){ int n=line[0]-63; int len=strlen(line); while(len&&(line[len-1]=='\n'))line[--len]=0;
  static unsigned char bits[1<<16]; int nb=0; for(int k=1;k<len;k++){int v=line[k]-63; for(int q=5;q>=0;q--) bits[nb++]=(v>>q)&1;}
  static unsigned int mask[256]; int nblk=n-D; memset(mask,0,sizeof(unsigned)*nblk); int pos=0;
  for(int j=1;j<n;j++) for(int i=0;i<j;i++){ if(bits[pos]&&j>=D&&i<D) mask[j-D]|=1u<<i; pos++; }
  int cov[D][D]; memset(cov,0,sizeof cov); int s[D]; memset(s,0,sizeof s); memset(dbl,0,sizeof dbl); memset(tri,0,sizeof tri);
  unsigned quad[64]; int nq=0;
  for(int b=0;b<nblk;b++){ int el[D],m=0; for(int i=0;i<D;i++) if(mask[b]>>i&1) el[m++]=i; for(int a=0;a<m;a++){ s[el[a]]++; for(int c=a+1;c<m;c++) cov[el[a]][el[c]]=1; }
     if(m==3) tri[el[0]][el[1]][el[2]]=1; if(m==4) quad[nq++]=mask[b]; }
  for(int a=0;a<D;a++) for(int c=a+1;c<D;c++) if(!cov[a][c]){ s[a]++; s[c]++; dbl[a][c]=1; }
  int best=-100;
  for(int a=0;a<D;a++) for(int b=a+1;b<D;b++) for(int c=b+1;c<D;c++) for(int e=c+1;e<D;e++){
    int w=s[a]+s[b]+s[c]+s[e]-28; if(w<=best) continue;
    int f=dbl[a][b]+dbl[a][c]+dbl[a][e]+dbl[b][c]+dbl[b][e]+dbl[c][e]+tri[a][b][c]+tri[a][b][e]+tri[a][c][e]+tri[b][c][e];
    unsigned S=(1u<<a)|(1u<<b)|(1u<<c)|(1u<<e); for(int q=0;q<nq;q++) if(quad[q]==S) f++;
    if(w-f>best) best=w-f; }
  hist[best+10]++; tot++; }
 printf("total %ld\n",tot); for(int k=0;k<20;k++) if(hist[k]) printf("phimax_core=%d: %ld\n",k-10,hist[k]); return 0; }
