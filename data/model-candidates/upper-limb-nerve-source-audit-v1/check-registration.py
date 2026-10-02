"""Evaluate existing nerve-frame transform only; never fit or publish it."""
import bpy,json,hashlib,time
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
def run():
 start=time.monotonic();refpath=ROOT/'public/models/extensions/upper-arm-nerves.json';ref=json.loads(refpath.read_text());matrix=np.array(ref['registration']['matrixColumnVector']);assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==ref['source']['sha256']
 atlaspath=ROOT/'public/models/atlas.json';atlas=json.loads(atlaspath.read_text());parts={p['name'].lower():p for p in atlas['parts']};buffers={i:(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for i,c in enumerate(atlas['chunks'])};deps=bpy.context.evaluated_depsgraph_get()
 def source(name):
  o=bpy.data.objects[name].evaluated_get(deps);m=o.to_mesh();m.calc_loop_triangles();v=np.array([list(o.matrix_world@x.co) for x in m.vertices]);f=np.array([list(t.vertices) for t in m.loop_triangles]);o.to_mesh_clear();return v@matrix[:3,:3].T+matrix[:3,3],f
 def distance(v,w,f):
  tree=BVHTree.FromPolygons(w.tolist(),f.tolist(),all_triangles=True);return np.array([tree.find_nearest(Vector(x))[3] for x in v])*1000
 verts={'Vertebra C3':'third cervical vertebra','Vertebra C4':'fourth cervical vertebra','Vertebra C5':'fifth cervical vertebra','Vertebra C6':'sixth cervical vertebra','Vertebra C7':'seventh cervical vertebra','Vertebra T1':'first thoracic vertebra','Vertebra T2':'second thoracic vertebra'}
 rows=[]
 for s in json.loads((OUT/'context-mapping.json').read_text()):
  if s['componentRole']!='bone':continue
  name=s['sourceObject'];key=verts.get(name) or (s['side']+' '+name[:-2].lower().removesuffix(' bone')).replace('triquetrum','triquetral');p=parts[key];b=buffers[p['chunk']];tv=np.frombuffer(b,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3).astype(float);tf=np.frombuffer(b,'<u4',p['indexCount'],p['indices']).reshape(-1,3);sv,sf=source(name)
  d=np.concatenate([distance(sv,tv,tf),distance(tv,sv,sf)])
  row=dict(sourceObject=name,targetPartId=p['id'],targetConceptId=p['conceptId'],role='original-fit-reference' if name.startswith(('Humerus.','Radius.','Scapula.')) else 'independent-regional-holdout',rmsMm=float(np.sqrt(np.mean(d*d))),meanMm=float(d.mean()),p95Mm=float(np.percentile(d,95)),maxMm=float(d.max()));rows.append(row);print(name,round(row['rmsMm'],3),round(row['maxMm'],3),flush=True)
 curve=[]
 for s in json.loads((OUT/'new-object-mapping.json').read_text()):
  v,f=source(s['sourceObject']);curve.append(dict(sourceObject=s['sourceObject'],registeredBounds=[v.min(0).tolist(),v.max(0).tolist()],vertices=len(v),triangles=len(f),status='Existing matrix applied only for preview; no target nerve counterpart or course validation asserted'))
 report=dict(sourceSha256=ref['source']['sha256'],sourceRegistrationManifestSha256=hashlib.sha256(refpath.read_bytes()).hexdigest(),mainManifestSha256=hashlib.sha256(atlaspath.read_bytes()).hexdigest(),matrixColumnVector=matrix.tolist(),newFit=False,method='Bidirectional all-vertex to opposite triangle surface distances, vertex-weighted; geometry correspondence by exact bone identity. Source viewport evaluated; old similarity matrix only. Not clinical error bounds or nerve-path validation.',measurements=rows,newCurvePreviewExtents=curve,seconds=time.monotonic()-start)
 (OUT/'registration-checks.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':run()
