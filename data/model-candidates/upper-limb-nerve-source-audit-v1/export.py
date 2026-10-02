"""Pinned same-source upper-limb candidate. No import-time writes, fit or source saves."""
import bpy,json,gzip,hashlib,sys,time,importlib.util
from pathlib import Path
import numpy as np
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
SHA='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
AXIS=np.array([[1.,0.,0.],[0.,0.,-1.],[0.,1.,0.]])
def build_candidate(output_dir=None):
 start=time.monotonic();dest=Path(output_dir) if output_dir else OUT;dest.mkdir(parents=True,exist_ok=True)
 assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==SHA
 spec=importlib.util.spec_from_file_location('ulgeometry',OUT/'geometry.py');geo=importlib.util.module_from_spec(spec);spec.loader.exec_module(geo)
 specs=json.loads((OUT/'new-object-mapping.json').read_text())+json.loads((OUT/'context-mapping.json').read_text())
 deps=bpy.context.evaluated_depsgraph_get();raw={};parts=[];concepts=[];blob=bytearray();audit=[];checks=[]
 def append(v,dtype):
  while len(blob)%4:blob.append(0)
  offset=len(blob);blob.extend(np.asarray(v,dtype=dtype).tobytes());return offset
 for s in specs:
  obj=bpy.data.objects[s['sourceObject']];g=geo.inspect_geometry(obj,deps,raw);v,f=raw[obj.name];v=v.astype('<f4');f=f.astype('<u4');assert len(v) and len(f)
  if s['role']=='primary':assert obj.type=='CURVE' and not obj.modifiers and g['observedSide']==s['side']
  t=v[f].astype(float);cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);area=np.linalg.norm(cross,axis=1);unit=np.divide(cross,area[:,None],out=np.zeros_like(cross),where=area[:,None]!=0)
  normals=np.zeros_like(v,dtype=float)
  for c in range(3):
   a=t[:,(c+1)%3]-t[:,c];b=t[:,(c+2)%3]-t[:,c];den=np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1)
   angle=np.arccos(np.clip(np.divide(np.sum(a*b,axis=1),den,out=np.ones_like(den),where=den!=0),-1,1));np.add.at(normals,f[:,c],unit*angle[:,None])
  length=np.linalg.norm(normals,axis=1);cancelled=length==0
  for i in np.flatnonzero(cancelled):
   ix=np.flatnonzero(np.any(f==i,axis=1));normals[i]=unit[ix[np.argmax(area[ix])]] if len(ix) and area[ix].max()>0 else [0,1,0];length[i]=1
  normals/=length[:,None];encoded=np.rint(normals*32767).astype('<i2');decoded=encoded.astype(float)/32767
  dot=np.sum(decoded[f].mean(1)*unit,axis=1)
  ck=dict(sourceObject=obj.name,partId=s['partId'],role=s['role'],nonpositiveInterpolatedFaceNormals=int(np.sum(dot<=0)),cancelledOrLooseVertexNormals=int(cancelled.sum()),maxNormalLengthError=float(abs(np.linalg.norm(decoded,axis=1)-1).max()),**g['topology'])
  if s['role']=='primary':assert ck['zeroAreaTriangles']==ck['nonManifoldEdges']==ck['cancelledOrLooseVertexNormals']==0,obj.name
  part=dict(id=s['partId'],datasetId='upper-limb-nerve-reference',conceptId=s['conceptId'],name=(s['side'].title()+' '+obj.name[:-2].lower()) if obj.name.endswith(('.l','.r')) else obj.name,side=s['side'],system=s['system'],componentRole=s['componentRole'],role=s['role'],chunk=0,positions=append(v,'<f4'),normals=append(encoded,'<i2'),indices=append(f,'<u4'),vertexCount=len(v),indexCount=int(f.size),bounds=[v.min(0).tolist(),v.max(0).tolist()],sourceObject=obj.name,sourceObjectType=obj.type,sourceScope=s['scope'],sourceGeometry=g,expertReview='pending',normalMethod='Angle weighted; source bone cancelled/loose normals use largest incident nonzero face or unit Y; no geometry repair')
  parts.append(part);concepts.append(dict(id=part['conceptId'],name=part['name'],elements=[part['id']]));audit.append(dict(**s,geometry=g));checks.append(ck)
 binary=bytes(blob);compressed=gzip.compress(binary,mtime=0,compresslevel=9)
 for p in parts:
  v=np.frombuffer(binary,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3);f=np.frombuffer(binary,'<u4',p['indexCount'],p['indices']).reshape(-1,3)
  assert np.array_equal(v,raw[p['sourceObject']][0].astype('<f4')) and np.array_equal(f,raw[p['sourceObject']][1])
  assert f.max()<len(v) and np.isfinite(v).all() and p['bounds']==[v.min(0).tolist(),v.max(0).tolist()]
 assert len({p['id'] for p in parts})==len(parts) and len({p['conceptId'] for p in parts})==len(parts)
 old=json.loads((OUT/'frozen-source-reference.json').read_text())
 source=dict(old['source']);source.update(sha256=SHA,selectedObjects=[p['sourceObject'] for p in parts],blenderVersion=bpy.app.version_string,attribution='/models/upper-limb-nerve-reference/ATTRIBUTION.md')
 manifest=dict(version='Z-Anatomy upper-limb named nerve source candidate1',datasetId='upper-limb-nerve-reference',sex='male',source=source,parts=parts,concepts=concepts,triangles=sum(p['indexCount']//3 for p in parts),chunks=[dict(url='/models/upper-limb-nerve-reference/anatomy.bin',bytes=len(binary),gzip='/models/upper-limb-nerve-reference/anatomy.bin.gz',gzipBytes=len(compressed),sha256=hashlib.sha256(binary).hexdigest())],coordinateSystem=dict(units='meters',axes='X left; Y superior; Z anterior',sourceWorldToDisplayRowVector=AXIS.tolist()),compatibleWithMainAtlas=False,registration=None,scope='54 new named nerve source curves with whole grouped branches and retained non-rendering point splines;24 existing same-source nerve curves and49 bones for context. Roots and medial/lateral cords remain unresolved; hand/digital branches deferred. No main fit or expert acceptance.',releaseStatus='candidate-root-integration-review-pending',inheritedMeshDefects=[c for c in checks if c['nonpositiveInterpolatedFaceNormals'] or c['cancelledOrLooseVertexNormals'] or c['nonManifoldEdges'] or c['zeroAreaTriangles']])
 (dest/'atlas.json').write_text(json.dumps(manifest,indent=2)+'\n');(dest/'anatomy.bin').write_bytes(binary);(dest/'anatomy.bin.gz').write_bytes(compressed)
 for fn in ['ATTRIBUTION.md','UPSTREAM-LICENSE.txt']:
  if (OUT/fn).exists():(dest/fn).write_bytes((OUT/fn).read_bytes())
 (OUT/'evaluated-candidates.json').write_text(json.dumps(dict(sourceSha256=SHA,objects=audit),indent=2)+'\n')
 report=dict(parts=len(parts),newNerves=54,contextNerves=24,contextBones=len(parts)-78,vertices=sum(p['vertexCount'] for p in parts),triangles=manifest['triangles'],sourceSha256=SHA,binarySha256=hashlib.sha256(binary).hexdigest(),gzipSha256=hashlib.sha256(compressed).hexdigest(),manifestSha256=hashlib.sha256((dest/'atlas.json').read_bytes()).hexdigest(),checks=checks)
 (OUT/'geometry-checks.json').write_text(json.dumps(report,indent=2)+'\n');(OUT/'latest-run-timing.json').write_text(json.dumps(dict(seconds=time.monotonic()-start),indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
 return report
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];build_candidate(args[args.index('--output')+1] if '--output' in args else None)
