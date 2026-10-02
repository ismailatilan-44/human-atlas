"""Read-only package/source checks; historical recorded validation stays unchanged."""
import json,math,struct,gzip,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
def validate():
 m=json.loads((OUT/'atlas.json').read_text());b=(OUT/'anatomy.bin').read_bytes();assert gzip.decompress((OUT/'anatomy.bin.gz').read_bytes())==b
 files=['atlas.json','anatomy.bin','anatomy.bin.gz','ATTRIBUTION.md','UPSTREAM-LICENSE.html']
 if '--compare' in sys.argv:
  for f in files:assert (OUT/f).read_bytes()==(OUT/'reproduction'/f).read_bytes(),f
 maxerr=0
 for x in m['parts']:
  assert all(x[k]%4==0 for k in ['positions','normals','indices'])
  v=list(struct.iter_unpack('<fff',b[x['positions']:x['positions']+x['vertexCount']*12]));n=list(struct.iter_unpack('<hhh',b[x['normals']:x['normals']+x['vertexCount']*6]));f=list(struct.iter_unpack('<I',b[x['indices']:x['indices']+x['indexCount']*4]));assert len(v)==len(n)==x['vertexCount'] and len(f)==x['indexCount'] and max(z[0] for z in f)<len(v)
  assert all(math.isfinite(y) for z in v for y in z) and x['bounds']==[[min(z[i] for z in v) for i in range(3)],[max(z[i] for z in v) for i in range(3)]]
  maxerr=max(maxerr,max(abs(math.sqrt(sum((a/32767)**2 for a in z))-1) for z in n))
  assert hashlib.sha256((ROOT/x['sourcePath']).read_bytes()).hexdigest()==x['sourceSha256']
 assert maxerr<.00003 and len({x['id'] for x in m['parts']})==26 and len({x['id'] for x in m['concepts']})==24
 assert all(x['conceptId']==x['sourceConceptId'] for x in m['parts'])
 report=dict(parts=26,concepts=24,all26SourceFilesUnchanged=True,finiteDecodedPositions=True,indexAndBoundsChecks=True,offsetAlignment=True,normalizedAuthoredNormals=True,uniqueIds=True,returnedConceptParity=True,gzipRoundTrip=True,twoNumericalExportsFiveFilesIdentical=True if '--compare' in sys.argv else None,maxDecodedNormalLengthError=maxerr,fileSha256={f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in files})
 print(json.dumps(report,indent=2));return report
if __name__=='__main__':validate()
