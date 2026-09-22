from pathlib import Path
import json,gzip,hashlib,struct,math,zipfile
D=Path(__file__).resolve().parent;m=json.loads((D/'right-anterior-pulmonary-43.json').read_text());b=(D/m['chunks'][0]['url']).read_bytes();assert gzip.decompress((D/m['chunks'][0]['gzip']).read_bytes())==b;assert hashlib.sha256(b).hexdigest()==m['chunks'][0]['sha256']
mapping={}
for line in (D.parent/'lung-surfaces/FMA2Obj.txt').read_text().splitlines():
 if not line.startswith('#'):i,t,e=line.split('\t');mapping[i,t]=e.split('+')
assert set(mapping['FMA8620','is_a'])=={p['sourceId'] for p in m['parts']}
assert len({p['bestExistingCorrespondence']['basePartId'] for p in m['overlapReview']})==7
assert m['extendsConceptIds']==[] and m['integrationMode'].endswith('not_additive_merge')
with zipfile.ZipFile(D/'pulmonary-43-source.zip') as z:
 for p in m['parts']:
  raw=z.read(p['sourceObject']);assert hashlib.sha256(raw).hexdigest()==p['sourceSha256'];v=list(struct.iter_unpack('<fff',b[p['positions']:p['positions']+p['vertexCount']*12]));n=list(struct.iter_unpack('<hhh',b[p['normals']:p['normals']+p['vertexCount']*6]));idx=struct.unpack_from('<'+'I'*p['indexCount'],b,p['indices']);assert max(idx)<len(v)
  assert all(math.isfinite(x) for xyz in v for x in xyz);assert all(abs(math.sqrt(sum((x/32767)**2 for x in xyz))-1)<.00006 for xyz in n)
  expected=[]
  for l in raw.decode().splitlines():
   if l.startswith('v '):x,y,z0=map(float,l.split()[1:4]);expected.append(struct.unpack('<fff',struct.pack('<fff',x*.001,z0*.001+.0781112,-y*.001-.1)))
  assert v==expected
result=dict(status='passed',parts=7,triangles=m['triangles'],checks=['official4.3FMA8620 IS-A object set exact match','seven distinct nearest existing branch correspondences','per-OBJ hashes and exact source coordinate conversion','finite positions, valid indices, unit normals','gzip equals binary; binary checksum','withheld non-additive status'],binarySha256=hashlib.sha256(b).hexdigest())
(D/'pulmonary43-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
