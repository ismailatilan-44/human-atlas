"""Bounded source-space proximity evidence; distances do not establish attachments."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np
OUT=Path(__file__).resolve().parent
SHA='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
def run():
 assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==SHA
 deps=bpy.context.evaluated_depsgraph_get()
 def mesh(name):
  ev=bpy.data.objects[name].evaluated_get(deps);m=ev.to_mesh();m.calc_loop_triangles()
  v=np.array([list(ev.matrix_world@p.co) for p in m.vertices]);f=np.array([list(t.vertices) for t in m.loop_triangles]);ev.to_mesh_clear();return v,f
 rows=[]
 for side in ['l','r']:
  lv,lf=mesh('Intersesamoid ligament.'+side);sv,sf=mesh('Sesamoid bones of foot.'+side)
  groups=[{int(x) for x in f} for f in sf]
  while True:
   merged=[]
   for group in groups:
    for other in merged:
     if group&other:other.update(group);break
    else:merged.append(group.copy())
   if len(merged)==len(groups):break
   groups=merged
  lt=BVHTree.FromPolygons([Vector(v) for v in lv],lf.tolist(),all_triangles=True)
  comps=[]
  for ids in sorted(groups,key=lambda g:min(g)):
   cv=sv[sorted(ids)];cf=[f.tolist() for f in sf if int(f[0]) in ids]
   tree=BVHTree.FromPolygons([Vector(v) for v in sv],cf,all_triangles=True)
   d1=[tree.find_nearest(Vector(v))[3] for v in lv];d2=[lt.find_nearest(Vector(v))[3] for v in cv]
   comps.append(dict(componentIndex=len(comps),vertices=len(ids),triangles=len(cf),sourceWorldBounds=[cv.min(0).tolist(),cv.max(0).tolist()],centroid=cv.mean(0).tolist(),ligamentVerticesToSurfaceMeters=dict(min=min(d1),max=max(d1)),componentVerticesToLigamentSurfaceMeters=dict(min=min(d2),max=max(d2)),aabbOverlapAxes=(np.minimum(lv.max(0),cv.max(0))>=np.maximum(lv.min(0),cv.min(0))).tolist()))
  rows.append(dict(side=side,ligamentSourceObject='Intersesamoid ligament.'+side,ligamentSourceWorldBounds=[lv.min(0).tolist(),lv.max(0).tolist()],ligamentCentroid=lv.mean(0).tolist(),sesamoidSourceObject='Sesamoid bones of foot.'+side,components=comps))
 report=dict(sourceSha256=SHA,coordinateFrame='Original source world metres; no rotation needed for Euclidean proximity',method='Connected triangles of source sesamoid mesh, source viewport-evaluated surfaces; BVH nearest-surface distances sampled at vertices in both directions. No medial/lateral component labels inferred; distances are not contact or attachment acceptance.',rows=rows)
 (OUT/'intersesamoid-placement.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':run()
