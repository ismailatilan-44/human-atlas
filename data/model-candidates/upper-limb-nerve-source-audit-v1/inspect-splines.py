"""Per-spline geometry accounting without anatomical relabeling or source save."""
import bpy,json,hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent
SHA='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
def run():
 assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==SHA
 rows=[]
 for spec in json.loads((OUT/'new-object-mapping.json').read_text()):
  obj=bpy.data.objects[spec['sourceObject']];splines=[]
  for i,s in enumerate(obj.data.splines):
   d=obj.data.copy()
   for j in reversed(range(len(d.splines))):
    if j!=i:d.splines.remove(d.splines[j])
   o=bpy.data.objects.new('temporary-spline-probe',d);bpy.context.scene.collection.objects.link(o);mesh=o.to_mesh();mesh.calc_loop_triangles();splines.append(dict(index=i,type=s.type,controlPoints=len(s.bezier_points if s.type=='BEZIER' else s.points),vertices=len(mesh.vertices),triangles=len(mesh.loop_triangles),cyclic=s.use_cyclic_u,fillCaps=obj.data.use_fill_caps,anatomicalSubidentity=None));o.to_mesh_clear();bpy.data.objects.remove(o,do_unlink=True);bpy.data.curves.remove(d)
  rows.append(dict(sourceObject=obj.name,splines=splines,generatedTubeSplines=sum(x['vertices']>0 for x in splines),geometryFreeSplines=[x['index'] for x in splines if not x['vertices']]))
 (OUT/'spline-checks.json').write_text(json.dumps(dict(sourceSha256=SHA,method='Each copied source spline converted in isolation with original curve settings; temporary objects discarded; no source save or inferred anatomical spline identity',objects=rows),indent=2)+'\n')
if __name__=='__main__':run()
