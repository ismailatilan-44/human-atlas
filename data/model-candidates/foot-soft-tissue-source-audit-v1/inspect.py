"""Bounded read-only source inspection; outputs only beside this file."""
import bpy, json, hashlib, time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
START=time.monotonic()
SHA='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==SHA
TOKENS=['halluc','digitorum brevis','digiti minimi','quadratus plantae','lumbrical','interosse','sesamoid','retinacul','plantar','tarsal','talonavicular','calcaneo','foot','ankle']
rows=[]
for obj in bpy.data.objects:
    if any(t in obj.name.casefold() for t in TOKENS):
        rows.append(dict(name=obj.name,type=obj.type,dataBlock=obj.data.name if obj.data else None,
            baseVertices=len(obj.data.vertices) if obj.type=='MESH' else None,
            basePolygons=len(obj.data.polygons) if obj.type=='MESH' else None,
            collections=[c.name for c in obj.users_collection]))
record=dict(sourceSha256=SHA,inspectedAt=datetime.now(timezone.utc).isoformat(),objects=rows,
    collections=[dict(name=c.name,objects=[o.name for o in c.all_objects]) for c in bpy.data.collections if any(t in c.name.casefold() for t in TOKENS)],
    searchScope='Source object and collection name scan; exact evaluated geometry checked separately; no absence in other datasets inferred.')
(OUT/'discovery.json').write_text(json.dumps(record,indent=2)+'\n')
if not (OUT/'timing.json').exists():
    (OUT/'timing.json').write_text(json.dumps(dict(startedAt=record['inspectedAt'],scope='Elapsed wall time from first Blender discovery through task delivery; excludes initial instruction reading.'),indent=2)+'\n')
for r in rows:
    if r['type']=='MESH' and (r['basePolygons'] or 0)>0 and ('muscle' in r['name'].casefold() or 'sesamoid' in r['name'].casefold()):print(r['name'],r['baseVertices'],r['basePolygons'])

AXIS=np.array([[1.,0.,0.],[0.,0.,-1.],[0.,1.,0.]])
depsgraph=bpy.context.evaluated_depsgraph_get()
geometry={}
def inspect_geometry(obj):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    mesh.calc_loop_triangles()
    vertices = np.array([list(evaluated.matrix_world @ v.co) for v in mesh.vertices], dtype=float)
    faces = np.array([list(t.vertices) for t in mesh.loop_triangles], dtype=np.int64).reshape(-1,3)
    world = np.array([list(r) for r in evaluated.matrix_world])
    if np.linalg.det(world[:3,:3]) < 0:
        faces = faces[:,[0,2,1]]
    rotated = vertices @ AXIS
    cross = np.cross(vertices[faces[:,1]]-vertices[faces[:,0]],vertices[faces[:,2]]-vertices[faces[:,0]])
    area2 = np.linalg.norm(cross,axis=1)
    edges=np.sort(np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]]),axis=1)
    _,counts=np.unique(edges,axis=0,return_counts=True)
    parent=list(range(len(vertices)))
    def find(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]]
            v=parent[v]
        return v
    for a,b in edges:
        parent[find(int(a))]=find(int(b))
    components={}
    for v in np.unique(faces):
        key=find(int(v)); components.setdefault(key,[]).append(int(v))
    result=dict(sourceObject=obj.name, sourceIdentity='Blender object name within pinned SHA; no external anatomical ID asserted',
        sourceObjectType=obj.type, dataBlock=obj.data.name, dataBlockUsers=obj.data.users,
        collections=[c.name for c in obj.users_collection], parent=obj.parent.name if obj.parent else None,
        customProperties={k:str(obj[k])[:2000] for k in obj.keys()},
        worldMatrix=world.tolist(), determinant=float(np.linalg.det(world[:3,:3])),
        sourceWorldBounds=[vertices.min(0).tolist(),vertices.max(0).tolist()],
        displayBounds=[rotated.min(0).tolist(),rotated.max(0).tolist()],
        displayDimensionsMeters=np.ptp(rotated,axis=0).tolist(),
        observedSide='left' if vertices[:,0].min()>0 else 'right' if vertices[:,0].max()<0 else 'crosses-midline',
        evaluatedVertices=len(vertices), evaluatedTriangles=len(faces),
        selectableEvaluatedGeometry=bool(len(vertices) and len(faces) and np.isfinite(vertices).all()),
        baseVertices=len(obj.data.vertices) if obj.type=='MESH' else None,
        basePolygons=len(obj.data.polygons) if obj.type=='MESH' else None,
        modifiers=[dict(name=m.name,type=m.type,showViewport=m.show_viewport,showRender=m.show_render,
            levels=getattr(m,'levels',None),renderLevels=getattr(m,'render_levels',None),thickness=getattr(m,'thickness',None)) for m in obj.modifiers],
        topology=dict(boundaryEdges=int(np.sum(counts==1)),nonManifoldEdges=int(np.sum(counts>2)),
            zeroAreaTriangles=int(np.sum(area2==0)),minDoubleArea=float(area2.min()),
            looseVertices=len(vertices)-len(np.unique(faces)),triangleConnectedComponents=len(components),
            componentVertices=sorted([len(v) for v in components.values()],reverse=True)),
        evaluatedWorldGeometrySha256=hashlib.sha256(vertices.astype('<f8').tobytes()+faces.astype('<i8').tobytes()).hexdigest())
    if obj.type=='CURVE':
        result['curveSettings']={k:getattr(obj.data,k) for k in ['bevel_depth','bevel_resolution','resolution_u','use_fill_caps']}
        result['splines']=[]
        for spline in obj.data.splines:
            points=spline.bezier_points if spline.type=='BEZIER' else spline.points
            coords=np.array([list(obj.matrix_world@p.co.to_3d()) for p in points])
            result['splines'].append(dict(type=spline.type,cyclic=spline.use_cyclic_u,controlPoints=len(points),
                pointRadii=[float(p.radius) for p in points],sourceWorldControlPoints=coords.tolist(),
                displayEndpoints=(coords[[0,-1]]@AXIS).tolist(),
                sourceWorldHandlesLeft=[list(obj.matrix_world@p.handle_left) for p in spline.bezier_points],
                sourceWorldHandlesRight=[list(obj.matrix_world@p.handle_right) for p in spline.bezier_points]))
    geometry[obj.name]=(rotated,faces)
    evaluated.to_mesh_clear()
    return result

base_path=OUT/'baseline87-atlas.json'
baseline=json.loads(base_path.read_text())
assert len(baseline['parts'])==87
existing={p['sourceObject'] for p in baseline['parts']}
rows=[]
for spec in json.loads((OUT/'new-object-mapping.json').read_text()):
    obj=bpy.data.objects[spec['sourceObject']]
    data=inspect_geometry(obj)
    assert data['selectableEvaluatedGeometry'] and data['observedSide']==spec['side']
    rows.append(dict(**spec,geometry=data,expertReview='pending'))
support=[]
for obj in bpy.data.objects:
    name=obj.name.casefold()
    if obj.type not in {'MESH','CURVE'} or not obj.name.endswith(('.l','.r')):
        continue
    if not any(k in name for k in ['ligament','retinacul','aponeurosis','articular capsule','tendon sheath']):
        continue
    bounds=np.array([list(obj.matrix_world @ __import__('mathutils').Vector(v)) for v in obj.bound_box])
    if bounds[:,2].max()>.30 or bounds[:,2].min()<-.10:
        continue
    data=inspect_geometry(obj)
    support.append(dict(sourceObject=obj.name,geometry=data,
        currentReferenceRepresentation='already represented' if obj.name in existing else 'unrepresented in reference87',
        candidateStatus='inventory-only; coarse/compound support scope needs a separately bounded delivery',expertReview='pending'))
result=dict(sourceSha256=SHA,blenderVersion=bpy.app.version_string,baselineManifestSha256=hashlib.sha256(base_path.read_bytes()).hexdigest(),
    coordinates='Source X left/Y posterior/Z superior; display X left/Y superior/Z anterior in meters; common (x,z,-y) only',
    candidates=rows,supportInventory=support,measuredInspectionSeconds=time.monotonic()-START,
    scope='32 exact muscle/sesamoid objects; foot/ankle support inventory bounded by names and source-world bounds superior<=0.30m')
(OUT/'evaluated-candidates.json').write_text(json.dumps(result,indent=2)+'\n')
for r in rows:
    g=r['geometry'];print('EVALUATED',g['sourceObject'],g['evaluatedVertices'],g['evaluatedTriangles'],g['topology'])
print('SUPPORT INVENTORY',len(support))
