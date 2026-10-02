"""Read pinned source only; write bounded audit evidence beside this script.
Run Blender --background --disable-autoexec work/open-assets-review/Startup.blend --python data/model-candidates/lower-limb-unbound-source-audit/inspect.py
"""
import bpy
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

START = time.monotonic()
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
EXPECTED = '9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == EXPECTED
seed_path = ROOT / 'data/anatomy/regional-targets-lower-limb-v1.json'
# Fixed task scope: these were the 18 unbound targets at e879fc9.
# Keep the audit reproducible after integration adds representation bindings.
TARGET_TERMS = {6579, 6574, 6586, 6590, 6593, 4727, 1919, 1920, 1921}
targets = [t for t in json.loads(seed_path.read_text())['targets'] if t['terminology']['ta2TableId'] in TARGET_TERMS]
assert len(targets) == 18
TOKENS = ['fibular', 'peroneal', 'peroneus', 'sural', 'plantar', 'talofibular', 'calcaneofibular', 'talofibulare', 'calcaneofibulare']

def match(text):
    return any(k in text.casefold() for k in TOKENS)

matches = []
text_read_errors = []
for obj in bpy.data.objects:
    try:
        text_body = obj.data.body if obj.type == 'FONT' else None
    except UnicodeDecodeError:
        text_body = None
        text_read_errors.append(obj.name)
    fields = dict(name=obj.name, dataBlock=obj.data.name if obj.data else None,
        text=text_body,
        collections=[c.name for c in obj.users_collection])
    direct = match(obj.name) or match(fields['dataBlock'] or '') or match(fields['text'] or '')
    indirect = any(match(c) for c in fields['collections'])
    if direct or indirect:
        matches.append(dict(**fields, type=obj.type, matchKind='object-data-text' if direct else 'collection-only',
            baseVertices=len(obj.data.vertices) if obj.type == 'MESH' else None,
            basePolygons=len(obj.data.polygons) if obj.type == 'MESH' else None))
report = dict(sourceSha256=EXPECTED, sourceObjects=len(bpy.data.objects),
    sourceDate=datetime.now(timezone.utc).isoformat(), tokens=TOKENS, textReadErrors=text_read_errors,
    targetSeedSha256=hashlib.sha256(seed_path.read_bytes()).hexdigest(),
    targets=[dict(id=t['id'],side=t['side'],term=t['terminology']['en'],ta2=t['terminology']['ta2TableId']) for t in targets],
    matchingObjects=matches, matchingCollections=[dict(name=c.name,objects=[o.name for o in c.all_objects]) for c in bpy.data.collections if match(c.name)],
    measuredInspectionSeconds=time.monotonic()-START)
(OUT/'discovery.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps([m for m in matches if m['matchKind']=='object-data-text' and m['type'] in ['CURVE','MESH']], indent=2))

AXIS = np.array([[1.,0.,0.],[0.,0.,-1.],[0.,1.,0.]])
depsgraph = bpy.context.evaluated_depsgraph_get()
geometry = {}


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

candidates=[]
for target in targets:
    name=target['terminology']['en']+'.'+target['side'][0]
    obj=bpy.data.objects.get(name)
    assert obj is not None and obj.type in {'MESH','CURVE'},name
    row=inspect_geometry(obj)
    assert row['observedSide']==target['side'],name
    candidates.append(dict(targetId=target['id'],ta2TableId=target['terminology']['ta2TableId'],term=target['terminology']['en'],
        side=target['side'],identityEvidence='Exact unsided source name + explicit side suffix and source-world side sign; expert identity review pending',
        independentObject=True,compoundScope='Source curve may contain multiple unlabelled splines; do not infer separate named branches' if obj.type=='CURVE' else 'Single named source sheet evaluated with authored modifiers; not attachment-footprint geometry',
        geometry=row,expertReview='pending',productStatus='candidate-not-exported'))

context_tokens=['navicular','cuboid','cuneiform','metatarsal','phalan']
context_matches=[]
for obj in bpy.data.objects:
    if any(t in obj.name.casefold() for t in context_tokens):
        context_matches.append(dict(name=obj.name,type=obj.type,dataBlock=obj.data.name if obj.data else None,
            baseVertices=len(obj.data.vertices) if obj.type=='MESH' else None,
            basePolygons=len(obj.data.polygons) if obj.type=='MESH' else None,
            collections=[c.name for c in obj.users_collection]))
(OUT/'context-discovery.json').write_text(json.dumps(context_matches,indent=2)+'\n')
result=dict(sourceSha256=EXPECTED,targetSeedSha256=report['targetSeedSha256'],blenderVersion=bpy.app.version_string,
    coordinateSystem=dict(source='X left, Y posterior, Z superior; meters',display='X left, Y superior, Z anterior; one common axis rotation only',
        sceneUnitSystem=bpy.context.scene.unit_settings.system,sceneScaleLength=bpy.context.scene.unit_settings.scale_length),
    candidates=candidates,measuredInspectionSeconds=time.monotonic()-START,
    limitations='Private geometry/source audit only. No product export, new registration, full anatomy coverage, self-intersection or expert acceptance.')
(OUT/'evaluated-candidates.json').write_text(json.dumps(result,indent=2)+'\n')
for c in candidates:
    g=c['geometry'];print('CANDIDATE',g['sourceObject'],g['evaluatedVertices'],g['evaluatedTriangles'],g['topology'])

# Additional foot context requested by integration owner; inspection only, no mesh export.
foot_objects=[]
for obj in bpy.data.objects:
    if obj.type!='MESH' or not obj.name.endswith(('.l','.r')):
        continue
    base=obj.name[:-2]
    if base in ['Navicular bone','Cuboid bone','Medial cuneiform bone','Intermediate cuneiform bone','Lateral cuneiform bone'] or base in [ordinal+' metatarsal bone' for ordinal in ['First','Second','Third','Fourth','Fifth']] or ('phalanx of' in base and 'finger of foot' in base):
        foot_objects.append(obj)
assert len(foot_objects)==48
foot_rows=[]
for obj in sorted(foot_objects,key=lambda o:o.name):
    row=inspect_geometry(obj)
    base=obj.name[:-2]
    foot_rows.append(dict(geometry=row,relatedSourceObjects=[dict(name=m['name'],type=m['type'],basePolygons=m['basePolygons'],relationship='opposite-side or annotation companion; not an interchangeable geometry alias') for m in context_matches if m['name'].rsplit('.',1)[0]==base and m['name']!=obj.name],
        proposedEnglishDisplayAlias=('Left ' if obj.name.endswith('.l') else 'Right ')+base.replace('finger of foot','toe').lower(),
        aliasStatus='Project display wording only; source object identity retained; no external ontology crosswalk asserted',
        purpose='Same-source plantar/foot course context; not part of the 18 unbound targets',expertReview='pending'))
(OUT/'foot-context.json').write_text(json.dumps(dict(sourceSha256=EXPECTED,objects=foot_rows,count=len(foot_rows),
    note='48 additional source meshes: 10 tarsal, 10 metatarsal and 28 phalangeal objects. Existing talus/calcaneus context is not re-exported.'),indent=2)+'\n')

# Representative source-candidate renders; never write reusable mesh buffers.
if '--render' in __import__('sys').argv:
    from mathutils import Vector, Matrix
    scene=bpy.data.scenes.new('Unbound lower-limb candidate audit')
    bpy.context.window.scene=scene
    scene.world=bpy.data.worlds.new('Audit world');scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.06,.07,.08,1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
    scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
    scene.cycles.transparent_max_bounces=32
    scene.render.resolution_x=1400;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
    def material(name,color,alpha):
        m=bpy.data.materials.new(name);m.use_nodes=True
        n=m.node_tree.nodes;n.clear()
        out=n.new('ShaderNodeOutputMaterial');mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha
        clear=n.new('ShaderNodeBsdfTransparent');surface=n.new('ShaderNodeBsdfPrincipled')
        surface.inputs['Base Color'].default_value=(*color,1);surface.inputs['Roughness'].default_value=.6
        m.node_tree.links.new(clear.outputs[0],mix.inputs[1]);m.node_tree.links.new(surface.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],out.inputs['Surface'])
        return m
    mats={'bone':material('Bone context',(.8,.86,.9),.12),'nerve':material('Candidate nerve',(1,.7,.08),1),'artery':material('Candidate artery',(.85,.12,.15),1),'ligament':material('Candidate ligament',(.3,.8,.9),1)}
    prior_path=ROOT/'public/models/lower-limb-nerve-reference/atlas.json';prior=json.loads(prior_path.read_text())
    prior_bytes=(ROOT/'public/models/lower-limb-nerve-reference/anatomy.bin').read_bytes()
    assert prior['source']['sha256']==EXPECTED
    for p in prior['parts']:
        if p['sourceObject'].startswith(('Tibia.','Fibula.','Talus.','Calcaneus.','Patella.')):
            v=np.frombuffer(prior_bytes,dtype='<f4',count=p['vertexCount']*3,offset=p['positions']).reshape(-1,3)
            f=np.frombuffer(prior_bytes,dtype='<u4',count=p['indexCount'],offset=p['indices']).reshape(-1,3)
            geometry[p['sourceObject']]=(v,f)
    objects=[]
    for name,(v,f) in geometry.items():
        role='artery' if 'artery' in name else 'nerve' if 'nerve' in name else 'ligament' if 'ligament' in name else 'bone'
        mesh=bpy.data.meshes.new(name+' audit');mesh.from_pydata(v.tolist(),[],f.tolist());mesh.update()
        obj=bpy.data.objects.new(name+' audit',mesh);scene.collection.objects.link(obj);obj.data.materials.append(mats[role])
        for poly in mesh.polygons:poly.use_smooth=True
        objects.append((obj,name,role))
    for pos in [(1,1,1),(-1,.7,-1)]:
        light=bpy.data.lights.new('Audit light','AREA');light.energy=90;light.size=1
        obj=bpy.data.objects.new(light.name,light);scene.collection.objects.link(obj);obj.location=pos
        obj.rotation_euler=(Vector((0,.25,0))-obj.location).to_track_quat('-Z','Y').to_euler()
    camera=bpy.data.cameras.new('Audit camera');camera.type='ORTHO'
    camera_obj=bpy.data.objects.new(camera.name,camera);scene.collection.objects.link(camera_obj);scene.camera=camera_obj
    views=[]
    def view(name,center,direction,scale,roles=None):
        for obj,source,role in objects:
            obj.hide_render=not source.endswith('.l') or (roles is not None and role not in roles)
        center=Vector(center);camera_obj.location=center+Vector(direction);back=(camera_obj.location-center).normalized()
        up=Vector((0,1,0)) if abs(back.y)<.9 else Vector((0,0,1))
        right=up.cross(back).normalized();camera_obj.rotation_euler=Matrix((right,back.cross(right),back)).transposed().to_euler()
        camera.ortho_scale=scale;scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
        views.append(dict(file=name,center=list(center),direction=direction,orthoScaleMeters=scale,side='left',roles=roles or list(mats),
            meaning='Evaluated source candidates in shared rotated frame, with previously packaged same-source lower-leg context and freshly inspected foot context.'))
    view('left-leg-anterior.png',(.09,.28,.03),(.15,.04,1),.61)
    view('left-foot-plantar.png',(.085,.045,.09),(.08,-1,.25),.31,['bone','nerve'])
    view('left-ankle-lateral-ligaments.png',(.09,.105,.00),(1,.03,.12),.18,['bone','ligament'])
    (OUT/'render-evidence.json').write_text(json.dumps(dict(views=views,sourceSha256=EXPECTED,
        reusedContextManifestSha256=hashlib.sha256(prior_path.read_bytes()).hexdigest(),
        renderEngine='Cycles, 16 samples; evaluated viewport geometry snapshots, not render-level reevaluation',
        visualReview='pending-human-or-agent-image-inspection'),indent=2)+'\n')
result['measuredInspectionSeconds']=time.monotonic()-START
result['measuredScope']='Python script execution from source hash check through source/context inspection and optional rendering; excludes Blender startup and conversational review.'
(OUT/'evaluated-candidates.json').write_text(json.dumps(result,indent=2)+'\n')
