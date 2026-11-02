"""Rebuild the compressed result archives of this directory from the shard files of the runs.

core_components_b48_b49_b50.jsonl.gz  Macaulay2 component records (m2compb.py) of every 13-line core that the
                                      fast filters deferred, classes b2 = 48, 49, 50: comp/dall_comp_*.jsonl and
                                      comp/dallb_comp_*.jsonl (29,238 records, one per core)
core_components_b51.jsonl.gz          the same for b2 = 51: comp/d51_comp_*.jsonl, comp/d51b_comp_*.jsonl
                                      (157,533 records)
children_components.jsonl.gz          Macaulay2 component records of every child (14 to 16 lines) that the fast
                                      filters deferred in the extension runs: run/*_chcomp_*.jsonl,
                                      run/dim2_b4849_ch_comp_*.jsonl, run/d2c2_comp_*.jsonl; each record gets the
                                      name of its shard file in "_source"

Core records are copied byte for byte; children records are re-serialised with the extra key.  The gzip
header has no time stamp, so the archives are reproducible.  usage: make_archives.py   (from work/n17)"""
import glob, gzip, json, os

def write(out, files, tag):
    n = 0
    with open(out, 'wb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', compresslevel=9, mtime=0) as gz:
        for f in files:
            for line in open(f, 'rb'):
                if not line.strip():
                    continue
                if tag:
                    r = json.loads(line)
                    r['_source'] = os.path.basename(f)
                    line = (json.dumps(r) + '\n').encode()
                gz.write(line if line.endswith(b'\n') else line + b'\n')
                n += 1
    print(out, len(files), 'files', n, 'records')

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
write('results/core_components_b48_b49_b50.jsonl.gz',
      sorted(glob.glob('comp/dall_comp_*.jsonl')) + sorted(glob.glob('comp/dallb_comp_*.jsonl')), False)
write('results/core_components_b51.jsonl.gz',
      sorted(glob.glob('comp/d51_comp_*.jsonl')) + sorted(glob.glob('comp/d51b_comp_*.jsonl')), False)
write('results/children_components.jsonl.gz',
      sorted(glob.glob('run/*_chcomp_*.jsonl') + glob.glob('run/dim2_b4849_ch_comp_*.jsonl')
             + glob.glob('run/d2c2_comp_*.jsonl')), True)
