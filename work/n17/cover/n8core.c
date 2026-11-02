#include <stdio.h>
#include <string.h>
#define D 13
int main(void){ char line[4096]; long hist[14]={0}; long tot=0;
 while(fgets(line,sizeof line,stdin)){ int n=line[0]-63; int len=strlen(line); while(len&&(line[len-1]=='\n'))line[--len]=0;
  static unsigned char bits[1<<16]; int nb=0; for(int k=1;k<len;k++){int v=line[k]-63; for(int q=5;q>=0;q--) bits[nb++]=(v>>q)&1;}
  int cov[D][D]; memset(cov,0,sizeof cov); int s[D]; memset(s,0,sizeof s);
  static unsigned int mask[256]; int nblk=n-D; memset(mask,0,sizeof(unsigned)*nblk); int pos=0;
  for(int j=1;j<n;j++) for(int i=0;i<j;i++){ if(bits[pos]&&j>=D&&i<D) mask[j-D]|=1u<<i; pos++; }
  for(int b=0;b<nblk;b++){ int el[D],m=0; for(int i=0;i<D;i++) if(mask[b]>>i&1) el[m++]=i; for(int a=0;a<m;a++){ s[el[a]]++; for(int c=a+1;c<m;c++) cov[el[a]][el[c]]=1; } }
  for(int a=0;a<D;a++) for(int c=a+1;c<D;c++) if(!cov[a][c]){ s[a]++; s[c]++; }
  int n8=0; for(int i=0;i<D;i++) if(s[i]==8) n8++; hist[n8]++; tot++; }
 printf("total %ld\n", tot); for(int k=0;k<14;k++) if(hist[k]) printf("n8=%d: %ld\n",k,hist[k]); return 0; }
