"""Read retained26 official OBJ files; preserve geometry and authored normals. No fit/import writes."""
import bpy,json,hashlib,gzip,time,sys
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
MATRIX=np.array([[.001,0,0,0],[0,0,.001,.0781112],[0,-.001,0,-.1],[0,0,0,1]])
ROT=MATRIX[:3,:3]/.001

def read_obj(path):
 v=[];n=[];f=[]
 for line in path.read_text().splitlines():
  col=line.split()
  if not col:continue
  if col[0]=='v':v.append(list(map(float,col[1:4])))
  elif col[0]=='vn':n.append(list(map(float,col[1:4])))
  elif col[0]=='f':
   assert len(col)==4,'Source triangle preservation requires triangular face'
   ids=[int(x.split('/')[0])-1 for x in col[1:]];ni=[int(x.split('/')[-1])-1 for x in col[1:]];assert ids==ni
   f.append(ids)
 v=np.array(v,dtype=float);n=np.array(n,dtype=float);f=np.array(f,dtype=np.int64)
 assert len(v)==len(n) and np.isfinite(v).all() and np.isfinite(n).all() and f.min()>=0 and f.max()<len(v)
 return v,n,f

def topology(v,f):
 edges=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);_,counts=np.unique(edges,axis=0,return_counts=True)
 par=list(range(len(v)))
 def root(x):
  while par[x]!=x:par[x]=par[par[x]];x=par[x]
  return x
 for a,b in edges:par[root(int(a))]=root(int(b))
 groups={}
 for i,tri in enumerate(f):groups.setdefault(root(int(tri[0])),[]).append(i)
 cross=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]);areas=np.linalg.norm(cross,axis=1)/2
 components=[]
 for ix in groups.values():
  ids=np.unique(f[ix]);vv=v[ids];components.append(dict(vertexIndices=ids.tolist(),faceIndices=ix,vertices=len(ids),triangles=len(ix),surfaceAreaMm2=float(areas[ix].sum()),boundsMm=[vv.min(0).tolist(),vv.max(0).tolist()]))
 components.sort(key=lambda x:(-x['surfaceAreaMm2'],-x['triangles']))
 return dict(boundaryEdges=int(np.sum(counts==1)),nonManifoldEdges=int(np.sum(counts>2)),zeroAreaTriangles=int(np.sum(areas==0)),looseVertices=len(v)-len(np.unique(f)),components=len(components),componentRecords=components,totalSurfaceAreaMm2=float(areas.sum()))

def nearest(a,b,f):
 tree=BVHTree.FromPolygons(b.tolist(),f.tolist(),all_triangles=True);return np.array([tree.find_nearest(Vector(p))[3] for p in a])

def build_candidate(output_dir=None):
 start=time.monotonic();dest=Path(output_dir) if output_dir else OUT;dest.mkdir(parents=True,exist_ok=True)
 intake=json.loads((OUT/'frozen-intake.json').read_text());allrows=intake['objects']+intake['contextObjects'];assert len(allrows)==26
 atlas_path=ROOT/'public/models/atlas.json';atlas=json.loads(atlas_path.read_text());ap={p['id']:p for p in atlas['parts']};chunks={i:(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for i,c in enumerate(atlas['chunks'])}
 blob=bytearray();parts=[];concepts={};audit=[];geometry={};checks=[];holdouts=[]
 def append(a,dtype):
  while len(blob)%4:blob.append(0)
  offset=len(blob);blob.extend(np.asarray(a,dtype=dtype).tobytes());return offset
 for row in allrows:
  path=ROOT/row['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],str(path)
  v,n,f=read_obj(path);raw=topology(v,f);unique,inverse=np.unique(v,axis=0,return_inverse=True);weld=topology(unique,inverse[f]);largest=weld['componentRecords'][0];main_faces=inverse[f][largest['faceIndices']]
  for comp in weld['componentRecords']:
   comp['minimumSampledDistanceToLargestComponentMm']=0.0 if comp is largest else float(nearest(unique[comp['vertexIndices']],unique,main_faces).min())
   comp['surfaceAreaFraction']=comp['surfaceAreaMm2']/weld['totalSurfaceAreaMm2']
  for top in [raw,weld]:
   for c in top['componentRecords']:c.pop('vertexIndices');c.pop('faceIndices')
  pv=(v@MATRIX[:3,:3].T+MATRIX[:3,3]).astype('<f4');norm=n@ROT.T;length=np.linalg.norm(norm,axis=1);assert np.all(length>0);norm/=length[:,None];encoded=np.rint(norm*32767).astype('<i2');decoded=encoded.astype(float)/32767
  t=pv[f].astype(float);cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);area=np.linalg.norm(cross,axis=1);dot=np.sum(cross*decoded[f].mean(1),axis=1)
  fid=row['sourcePartId'];bone=row in intake['contextObjects'];spinal=fid in ['FJ4264','FJ4265','FJ4266','FJ4267','FJ4245'];cord=fid in ['FJ4274','FJ4275'];role='context' if bone or spinal else 'primary'
  quality=dict(rawTopology=raw,exactPositionWeldDiagnostic=weld,rawVertices=len(v),uniquePositions=len(unique),normalLengthSourceMaxError=float(abs(length-1).max()),nonpositiveSourceNormalFaceAgreement=int(np.sum(dot<=0)),maxQuantizedNormalLengthError=float(abs(np.linalg.norm(decoded,axis=1)-1).max()),maxFloat32PositionErrorMeters=float(abs(pv-(v@MATRIX[:3,:3].T+MATRIX[:3,3])).max()))
  part=dict(id='BP43-'+fid,sourceId=fid,sourceRepresentationId=row['returnedRepresentationId'],sourceConceptId=row['returnedConceptId'],conceptId=row['returnedConceptId'],datasetId='upper-limb-bp3d43-reference-candidate',name=row['sourceName'],side='left' if 'left' in row['sourceName'].lower() else 'midline',system='skeletal' if bone else 'nervous',componentRole='bone' if bone else 'spinal-nerve-trunk' if spinal else 'cord' if cord else 'nerve',role=role,chunk=0,positions=append(pv,'<f4'),normals=append(encoded,'<i2'),indices=append(f,'<u4'),vertexCount=len(pv),indexCount=int(f.size),bounds=[pv.min(0).tolist(),pv.max(0).tolist()],sourceObject=path.name,sourceObjectType='OBJ',sourcePath=row['path'],sourceSha256=row['sha256'],sourceHeader=row['header'],sourceScope='Whole retained source OBJ component; not complete nerve/root/cord anatomy acceptance',normalMethod='Authored source vertex normals, common proper rotation, unit normalization and Int16 quantization; no vertex welding or face edits',expertReview='pending',quality=quality)
  parts.append(part);c=concepts.setdefault(part['conceptId'],dict(id=part['conceptId'],name=part['name'],elements=[]));c['elements'].append(part['id']);geometry[fid]=(v,n,f,pv)
  audit.append(dict(sourceId=fid,sourceName=row['sourceName'],sourceSha256=row['sha256'],sourceBoundsMm=[v.min(0).tolist(),v.max(0).tolist()],transformedBounds=part['bounds'],quality=quality,sourceHeader=row['header']))
  checks.append(dict(partId=part['id'],sourceId=fid,finite=True,indexRange=True,sourceFacesPreserved=True,**{k:v for k,v in quality.items() if k not in ['rawTopology','exactPositionWeldDiagnostic']}))
  if bone:
   p=ap[fid];b=chunks[p['chunk']];tv=np.frombuffer(b,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3).astype(float);tf=np.frombuffer(b,'<u4',p['indexCount'],p['indices']).reshape(-1,3)
   mapped=v@MATRIX[:3,:3].T+MATRIX[:3,3];d=np.concatenate([nearest(mapped,tv,tf),nearest(tv,mapped,f)])*1000
   holdouts.append(dict(sourceId=fid,name=row['sourceName'],targetId=p['id'],targetConceptId=p['conceptId'],rmsMm=float(np.sqrt(np.mean(d*d))),p95Mm=float(np.percentile(d,95)),maxMm=float(d.max()),vertices43=len(v),vertices40=len(tv)))
 binary=bytes(blob);compressed=gzip.compress(binary,mtime=0,compresslevel=9)
 for p in parts:
  v=np.frombuffer(binary,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3);f=np.frombuffer(binary,'<u4',p['indexCount'],p['indices']).reshape(-1,3);assert np.array_equal(v,geometry[p['sourceId']][3]) and np.array_equal(f,geometry[p['sourceId']][2])
 manifest=dict(version='BodyParts3D4.3 bounded left upper-limb candidate1',datasetId='upper-limb-bp3d43-reference-candidate',sex='unknown',parts=parts,concepts=list(concepts.values()),triangles=sum(p['indexCount']//3 for p in parts),chunks=[dict(url='/models/upper-limb-bp3d43-reference-candidate/anatomy.bin',bytes=len(binary),gzip='/models/upper-limb-bp3d43-reference-candidate/anatomy.bin.gz',gzipBytes=len(compressed),sha256=hashlib.sha256(binary).hexdigest())],source=dict(intake['sources'][0],intakeSha256=hashlib.sha256((OUT/'frozen-intake.json').read_bytes()).hexdigest(),attribution='/models/upper-limb-bp3d43-reference-candidate/ATTRIBUTION.md'),registration=dict(method='Existing native4.3 thyroid mm-to-m axis/translation hypothesis; nine independent bones tested; no fit',matrixColumnVector=MATRIX.tolist(),targetManifestSha256=hashlib.sha256(atlas_path.read_bytes()).hexdigest(),measurements=holdouts),compatibleWithMainAtlas=False,status='candidate-geometry-and-anatomical-acceptance-pending',scope='17 exact left neural source files, including5 contextual spinal nerve trunks, plus9 bones; duplicate axillary/radial files remain separate parts sharing returned concept. No right mirroring, isolated plexus-root contribution, complete extent or anatomical continuity asserted.')
 for fn,data in [('atlas.json',json.dumps(manifest,indent=2)+'\n'),('geometry-audit.json',json.dumps(dict(objects=audit),indent=2)+'\n'),('registration-checks.json',json.dumps(manifest['registration'],indent=2)+'\n')]:
  (dest/fn if fn=='atlas.json' else OUT/fn).write_text(data)
 (dest/'anatomy.bin').write_bytes(binary);(dest/'anatomy.bin.gz').write_bytes(compressed)
 for fn in ['ATTRIBUTION.md','UPSTREAM-LICENSE.html']:
  if (OUT/fn).exists():(dest/fn).write_bytes((OUT/fn).read_bytes())
 pairs=[]
 for a,b in [('FJ4274','FJ4275'),('FJ4275','FJ4258'),('FJ4274','FJ4240'),('FJ4274','FJ4172'),('FJ4172','FJ4240'),('FJ4171','FJ4243')]:
  av,_,af,_=geometry[a];bv,_,bf,_=geometry[b];da=nearest(av,bv,bf);db=nearest(bv,av,af);pairs.append(dict(sourceA=a,sourceB=b,minVertexAToSurfaceBMm=float(da.min()),minVertexBToSurfaceAMm=float(db.min()),meaning='Geometric sampled proximity only; not proof of anatomical continuity or a branch relationship'))
 (OUT/'source-proximity.json').write_text(json.dumps(dict(pairs=pairs),indent=2)+'\n')
 report=dict(parts=len(parts),concepts=len(concepts),vertices=sum(p['vertexCount'] for p in parts),triangles=manifest['triangles'],bytes=len(binary),gzipBytes=len(compressed),binarySha256=hashlib.sha256(binary).hexdigest(),gzipSha256=hashlib.sha256(compressed).hexdigest(),manifestSha256=hashlib.sha256((dest/'atlas.json').read_bytes()).hexdigest(),checks=checks)
 (OUT/'geometry-checks.json').write_text(json.dumps(report,indent=2)+'\n');(OUT/'latest-run-timing.json').write_text(json.dumps(dict(seconds=time.monotonic()-start),indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2));print('HOLDOUTS',json.dumps(holdouts))
 return report
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];build_candidate(args[args.index('--output')+1] if '--output' in args else None)
