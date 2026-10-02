"""Read pinned exact support objects; write evidence only beside this file."""
import bpy,json,hashlib,time
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
SHA='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
AXIS=np.array([[1.,0.,0.],[0.,0.,-1.],[0.,1.,0.]])

def inspect_geometry(obj, depsgraph, geometry):
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

def inspect():
    started=time.monotonic()
    assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==SHA
    specs=json.loads((OUT/'new-object-mapping.json').read_text())
    baseline=json.loads((OUT/'baseline119-atlas.json').read_text())
    assert len(baseline['parts'])==119 and baseline['source']['sha256']==SHA
    depsgraph=bpy.context.evaluated_depsgraph_get();geometry={};rows=[];companions=[]
    for spec in specs:
        obj=bpy.data.objects[spec['sourceObject']]
        assert obj.type=='MESH',obj.name
        g=inspect_geometry(obj,depsgraph,geometry)
        assert g['selectableEvaluatedGeometry'] and g['observedSide']==spec['side'],obj.name
        assert g['topology']['boundaryEdges']==spec['expectedBoundaryEdges'],obj.name
        rows.append(dict(**spec,geometry=g,expertReview='pending'))
    bases={s['sourceObject'][:-2] for s in specs}
    for obj in bpy.data.objects:
        if obj.name.rsplit('.',1)[0] in bases:
            companions.append(dict(name=obj.name,type=obj.type,dataBlock=obj.data.name if obj.data else None,
                baseVertices=len(obj.data.vertices) if obj.type=='MESH' else None,
                basePolygons=len(obj.data.polygons) if obj.type=='MESH' else None,
                collections=[c.name for c in obj.users_collection],selected=obj.name in {s['sourceObject'] for s in specs}))
    report=dict(sourceSha256=SHA,blenderVersion=bpy.app.version_string,
        sourceSceneUnits=dict(system=bpy.context.scene.unit_settings.system,scaleLength=bpy.context.scene.unit_settings.scale_length),
        baselineManifestSha256=hashlib.sha256((OUT/'baseline119-atlas.json').read_bytes()).hexdigest(),
        candidates=rows,relatedSourceObjects=companions,
        coordinates='Source X left/Y posterior/Z superior; shared display (x,z,-y), meters; no fitting or source saving',
        scope='Twenty exact bilateral support objects; source companions distinguish markers/text and anatomy; no completeness claim',
        measuredInspectionSeconds=time.monotonic()-started)
    (OUT/'evaluated-candidates.json').write_text(json.dumps(report,indent=2)+'\n')
    for r in rows:
        g=r['geometry'];print(g['sourceObject'],g['evaluatedVertices'],g['evaluatedTriangles'],g['topology'])

if __name__=='__main__':
    inspect()
