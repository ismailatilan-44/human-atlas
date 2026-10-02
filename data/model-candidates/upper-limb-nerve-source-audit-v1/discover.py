import bpy,json,hashlib,time
from pathlib import Path
OUT=Path(__file__).resolve().parent
SHA='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
def discover():
 start=time.monotonic();assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==SHA
 rows=[]
 for o in bpy.data.objects:
  n=o.name.lower()
  if any(x in n for x in ['nerve','brachial plexus','medial cord','lateral cord']):
   row=dict(name=o.name,type=o.type,collections=[c.name for c in o.users_collection])
   if o.type=='CURVE':
    pts=[o.matrix_world@p.co.to_3d() for s in o.data.splines for p in (s.bezier_points if s.type=='BEZIER' else s.points)]
    row.update(splines=len(o.data.splines),pointsPerSpline=[len(s.bezier_points if s.type=='BEZIER' else s.points) for s in o.data.splines],bounds=[[min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]] if pts else None,modifiers=[m.type for m in o.modifiers])
   if o.type=='MESH':row.update(vertices=len(o.data.vertices),polygons=len(o.data.polygons))
   rows.append(row)
 report=dict(sourceSha256=SHA,blender=bpy.app.version_string,objects=rows,cordCollections=[c.name for c in bpy.data.collections if 'cord' in c.name.lower()],seconds=time.monotonic()-start)
 (OUT/'discovery.json').write_text(json.dumps(report,indent=2)+'\n')
 for r in rows:
  if r['type']=='CURVE' and r.get('bounds') and r['bounds'][1][2]>.7:print(r['name'],r['pointsPerSpline'],r['bounds'])
if __name__=='__main__':discover()
