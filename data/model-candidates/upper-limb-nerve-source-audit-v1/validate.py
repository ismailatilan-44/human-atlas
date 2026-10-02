"""Dependency-free decoded package checks; optional deterministic output comparison."""
from pathlib import Path
import json,hashlib,gzip,struct,math,sys
OUT=Path(__file__).resolve().parent
def validate():
 m=json.loads((OUT/'atlas.json').read_text());b=(OUT/'anatomy.bin').read_bytes();assert gzip.decompress((OUT/'anatomy.bin.gz').read_bytes())==b
 assert len(m['parts'])==len(m['concepts'])==127 and len({x['id'] for x in m['parts']})==len({x['id'] for x in m['concepts']})==127
 normalerror=0
 for p in m['parts']:
  assert all(p[k]%4==0 for k in ['positions','normals','indices'])
  v=list(struct.iter_unpack('<fff',b[p['positions']:p['positions']+12*p['vertexCount']]));n=list(struct.iter_unpack('<hhh',b[p['normals']:p['normals']+6*p['vertexCount']]));f=list(struct.iter_unpack('<I',b[p['indices']:p['indices']+4*p['indexCount']]))
  assert len(v)==len(n)==p['vertexCount'] and len(f)==p['indexCount'] and max(x[0] for x in f)<len(v)
  assert all(math.isfinite(x) for a in v for x in a)
  assert [[min(x[i] for x in v) for i in range(3)],[max(x[i] for x in v) for i in range(3)]]==p['bounds']
  normalerror=max(normalerror,max(abs(math.sqrt(sum((a/32767)**2 for a in x))-1) for x in n))
 assert normalerror<.00003
 specs=json.loads((OUT/'new-object-mapping.json').read_text())+json.loads((OUT/'context-mapping.json').read_text());assert [(s['partId'],s['conceptId'],s['sourceObject']) for s in specs]==[(p['id'],p['conceptId'],p['sourceObject']) for p in m['parts']]
 evidence={x['sourceObject']:x['geometry'] for x in json.loads((OUT/'evaluated-candidates.json').read_text())['objects']};splines=json.loads((OUT/'spline-checks.json').read_text())['objects']
 for x in splines:
  assert sum(s['vertices'] for s in x['splines'])==evidence[x['sourceObject']]['evaluatedVertices']
  assert sum(s['triangles'] for s in x['splines'])==evidence[x['sourceObject']]['evaluatedTriangles']
 files=['atlas.json','anatomy.bin','anatomy.bin.gz','ATTRIBUTION.md','UPSTREAM-LICENSE.txt']
 reproduced=False
 if '--compare' in sys.argv:
  for f in files:assert (OUT/f).read_bytes()==(OUT/'reproduction'/f).read_bytes(),f
  reproduced=True
 report=dict(parts=127,uniquePartConceptIds=True,exactMapping=True,finitePositions=True,indexBounds=True,float32Bounds=True,offsetAlignment=True,gzipRoundTrip=True,maxNormalLengthError=normalerror,all54IsolatedSplineTotalsMatch=True,deterministicPackageFiveFiles=reproduced,fileSha256={f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in files})
 (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return report
if __name__=='__main__':validate()
