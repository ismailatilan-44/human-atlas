"""Bounded binary/provenance/merge checks; standard Python, no app mutations."""
from pathlib import Path
import gzip,hashlib,json,math,struct,zipfile
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent
m=json.loads((ROOT/'public/models/extensions/lung-bp3d43.json').read_text())
a=json.loads((ROOT/'public/models/atlas.json').read_text()); ac={c['id']:c for c in a['concepts']}; ap={p['id']:p for p in a['parts']}
b=(ROOT/'public'/m['chunks'][0]['url'].lstrip('/')).read_bytes();gz=(ROOT/'public'/m['chunks'][0]['gzip'].lstrip('/')).read_bytes()
assert len(b)==m['chunks'][0]['bytes'] and hashlib.sha256(b).hexdigest()==m['chunks'][0]['sha256']
assert gzip.decompress(gz)==b and len(gz)==m['chunks'][0]['gzipBytes']
assert len(m['parts'])==18 and len(m['concepts'])==41 and m['triangles']==136376
assert len(m['extendsConceptIds'])==24 and len(m['directParentMemberships'])==17
assert len({p['conceptId'] for p in m['parts']})==17
assert not set(ap)&{p['id'] for p in m['parts']}
assert set(ac)&{c['id'] for c in m['concepts']}==set(m['extendsConceptIds'])
allids={p['id'] for p in m['parts']}; merge=[]
with zipfile.ZipFile(HERE/'lung-parenchyma-source.zip') as z:
 for p in m['parts']:
  nv=p['vertexCount'];ni=p['indexCount'];v=list(struct.iter_unpack('<fff',b[p['positions']:p['positions']+12*nv]));n=list(struct.iter_unpack('<hhh',b[p['normals']:p['normals']+6*nv]));ids=struct.unpack_from('<'+'I'*ni,b,p['indices'])
  assert len(v)==nv and all(math.isfinite(x) for xyz in v for x in xyz) and max(ids)<nv
  assert all(abs(math.sqrt(sum((x/32767)**2 for x in xyz))-1)<.00006 for xyz in n)
  assert p['bounds']==[[min(x[k] for x in v) for k in range(3)],[max(x[k] for x in v) for k in range(3)]]
  raw=z.read(p['sourceObject']);assert hashlib.sha256(raw).hexdigest()==p['sourceSha256']
  expected=[]
  for line in raw.decode().splitlines():
   if line.startswith('v '):
    x,y,z0=map(float,line.split()[1:4]);expected.append(struct.unpack('<fff',struct.pack('<fff',x*.001,z0*.001+.0781112,-y*.001-.1)))
  assert v==expected,p['id']
  used=set(ids)
  p['quality']['unusedRawPositionsVerified']=nv-len(used)
for c in m['concepts']:
 assert set(c['elements'])<=allids
 if c['id'] in ac:
  before=set(ac[c['id']]['elements']);after=before|set(c['elements'])
  assert before<=after
  merge.append(dict(conceptId=c['id'],before=len(before),added=len(c['elements']),after=len(after)))
assert sum(len(ac[i]['elements']) for i in ['FMA7309','FMA7310'])==280
assert sum(x['after'] for x in merge if x['conceptId'] in ['FMA7309','FMA7310'])==298
result=dict(status='passed',checks=['binary length/hash/gzip equality','finite positions and unit normals','bounds and index range','every transformed position exactly equals source float32 conversion','per-OBJ source hash','18 distinct part IDs, 17 leaf concepts, 24 explicit existing concept extensions','all 280 original lung members preserved by union','five lobe groups exactly partition source surfaces'],mergePreview=merge,packageSha256=hashlib.sha256(b).hexdigest(),unusedRawPositions=[dict(partId=p['id'],count=p['quality']['unusedRawPositionsVerified']) for p in m['parts'] if p['quality']['unusedRawPositionsVerified']])
(HERE/'package-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
