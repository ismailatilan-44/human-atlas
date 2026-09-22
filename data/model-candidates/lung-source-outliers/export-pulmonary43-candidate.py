"""Blender --background --disable-autoexec --python this.py
Candidate-only 4.3 pulmonary representation. DO NOT add atop existing overlapping surfaces.
"""
import json,gzip,hashlib,zipfile
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(__file__).resolve().parent;ROOT=D.parents[2];a=json.loads((ROOT/'public/models/atlas.json').read_text());ps={p['id']:p for p in a['parts']};chunks=[(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for c in a['chunks']]
def mesh(i):
 p=ps[i];b=chunks[p['chunk']];return np.frombuffer(b,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3),np.frombuffer(b,'<u4',p['indexCount'],p['indices']).reshape(-1,3)
src={}
with zipfile.ZipFile(D/'pulmonary-43-source.zip') as z:
 for member in z.namelist():
  if not member.endswith('.obj'):continue
  raw=z.read(member);h={};v=[];f=[]
  for line in raw.decode().splitlines():
   if line.startswith('# ') and ' : ' in line:k,val=line[2:].split(' : ',1);h[k]=val
   cs=line.split()
   if cs and cs[0]=='v':x,y,z0=map(float,cs[1:4]);v.append([x*.001,z0*.001+.0781112,-y*.001-.1])
   elif cs and cs[0]=='f':
    ids=[int(x.split('/')[0])-1 for x in cs[1:]]
    for i in range(1,len(ids)-1):f.append([ids[0],ids[i],ids[i+1]])
  assert h['Compatibility version']=='4.3' and h['Concept ID']=='FMA8620'
  src[h['File ID']]=dict(header=h,member=member,v=np.array(v,dtype='<f4'),f=np.array(f,dtype='<u4'),sha256=hashlib.sha256(raw).hexdigest())
assert sorted(src)==['FJ6044','FJ6045','FJ6046','FJ6047','FJ6049','FJ6050','FJ6051']
oldIds=['FJ2974','FJ2975','FJ2976','FJ2977','FJ2979','FJ2980','FJ2981'];old={i:mesh(i) for i in oldIds}
def ds(v,w,f):
 t=BVHTree.FromPolygons(w.tolist(),f.tolist(),all_triangles=True);return np.array([t.find_nearest(Vector(p))[3] for p in v])*1000
pairs=[];blob=bytearray();parts=[]
def append(a,dt):
 while len(blob)%4:blob.append(0)
 off=len(blob);blob.extend(np.asarray(a,dtype=dt).tobytes());return off
for i,s in sorted(src.items()):
 v,f=s['v'],s['f'];candidates=[]
 for target,(w,wf) in old.items():
  d=np.concatenate([ds(v,w,wf),ds(w,v,f)])
  candidates.append(dict(basePartId=target,baseConceptId=ps[target]['conceptId'],baseName=ps[target]['name'],rmsMm=float(np.sqrt(np.mean(d*d))),p95Mm=float(np.percentile(d,95)),maxMm=float(d.max())))
 pairs.append(dict(sourceId=i,sourceConceptId=s['header']['Concept ID'],bestExistingCorrespondence=min(candidates,key=lambda d:d['rmsMm']),allComparisons=sorted(candidates,key=lambda d:d['rmsMm'])))
 tri=v[f].astype(float);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);assert np.all(np.linalg.norm(cross,axis=1)>1e-15)
 unique,inv=np.unique(v,axis=0,return_inverse=True);norm=np.zeros_like(unique,dtype=float)
 for k in range(3):np.add.at(norm,inv[f[:,k]],cross)
 length=np.linalg.norm(norm,axis=1);zero=length<1e-20;norm[~zero]/=length[~zero,None];norm[zero]=[0,1,0];norm=norm[inv]
 wf=inv[f];edges=np.sort(np.concatenate([wf[:,[0,1]],wf[:,[1,2]],wf[:,[2,0]]]),axis=1);_,counts=np.unique(edges,axis=0,return_counts=True)
 parts.append(dict(id='BP43-'+i,conceptId='FMA8620',name=s['header']['English name'],system='arterial',chunk=0,positions=append(v,'<f4'),normals=append(np.rint(norm*32767),'<i2'),indices=append(f,'<u4'),vertexCount=len(v),indexCount=int(f.size),bounds=[v.min(0).tolist(),v.max(0).tolist()],sourceId=i,sourceConceptId='FMA8620',sourceObject=s['member'],sourceObjectType='OBJ',sourceHeader=s['header'],sourceSha256=s['sha256'],representation='alternative_source_parent_representation',quality=dict(zeroAveragedNormals=int(zero.sum()),boundaryEdgesAfterExactPositionWeld=int(sum(counts==1)),nonManifoldEdgesAfterExactPositionWeld=int(sum(counts>2))),expertReview='pending'))
raw=bytes(blob);gz=gzip.compress(raw,compresslevel=9,mtime=0);(D/'right-anterior-pulmonary-43.bin').write_bytes(raw);(D/'right-anterior-pulmonary-43.bin.gz').write_bytes(gz)
man=dict(version='BodyParts3D4.3 FMA8620 alternative representation candidate1',status='candidate_withheld_overlaps_existing_surfaces',sex='male',parts=parts,concepts=[dict(id='FMA8620',name='Right anterior segmental artery',elements=[p['id'] for p in parts])],extendsConceptIds=[],existingConceptIdCollision='FMA8620',integrationMode='explicit_reviewed_replacement_or_source_only_view; not_additive_merge',chunks=[dict(url='right-anterior-pulmonary-43.bin',gzip='right-anterior-pulmonary-43.bin.gz',bytes=len(raw),gzipBytes=len(gz),sha256=hashlib.sha256(raw).hexdigest())],triangles=sum(p['indexCount']//3 for p in parts),source=dict(url='https://lifesciencedb.jp/bp3d/?lng=en',downloadUrl='https://lifesciencedb.jp/bp3d/download.cgi',license='CC-BY-SA-2.1-JP',attribution='PULMONARY43-ATTRIBUTION.md',archiveSha256=hashlib.sha256((D/'pulmonary-43-source.zip').read_bytes()).hexdigest()),registration=dict(method='Unmodified established main BP3D mm/Z-up to m/Y-up transform, no fitting',matrixColumnVector=[[.001,0,0,0],[0,0,.001,.0781112],[0,-.001,0,-.1],[0,0,0,1]]),overlapReview=pairs,limitations=['Alternative parent-concept geometry overlaps seven existing named branch surfaces. Do not add over the existing seven: this produces duplicate pulmonary surfaces.','Old FJ2041/FJ2044 are absent from4.3 object set; this package does not relocate or relabel those old objects.','Raw4.0 memberships and geometry remain unchanged; reviewed selection overrides require explicit integration and explanation.','This is a selected pulmonary artery representation, not complete pulmonary vasculature or clinical anatomy certification.'])
(D/'right-anterior-pulmonary-43.json').write_text(json.dumps(man,indent=2)+'\n');(D/'pulmonary43-overlap-review.json').write_text(json.dumps(dict(measure='Bidirectional sampled vertex-to-nearest-triangle distance, existing base binary versus actual4.3source; no fitting.',pairs=pairs),indent=2)+'\n')
print('PAIRS',json.dumps([dict(sourceId=p['sourceId'],**p['bestExistingCorrespondence']) for p in pairs]));print('PACKAGE',len(parts),man['triangles'],len(raw),len(gz))
