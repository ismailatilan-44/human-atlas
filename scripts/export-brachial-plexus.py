"""Export only verified Z-Anatomy brachial plexus source curves.
Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
  --python scripts/export-brachial-plexus.py [-- --render]
"""
import bpy
import gzip
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'public/models/extensions'
reference = json.loads((OUT/'upper-arm-nerves.json').read_text())
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == reference['source']['sha256']
transform = np.array(reference['registration']['matrixColumnVector'])
atlas = json.loads((ROOT/'public/models/atlas.json').read_text())
buffers = [(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for c in atlas['chunks']]

def mapped(points):
    return np.asarray(points)@transform[:3, :3].T + transform[:3, 3]

def source_mesh(name):
    obj = bpy.data.objects[name]
    assert obj.type in ('MESH', 'CURVE')
    assert obj.type != 'CURVE' or not obj.modifiers
    mesh = obj.to_mesh()
    mesh.calc_loop_triangles()
    positions = mapped([list(obj.matrix_world@v.co) for v in mesh.vertices])
    faces = np.array([list(t.vertices) for t in mesh.loop_triangles], dtype='<u4')
    if obj.matrix_world.to_3x3().determinant() < 0:
        faces = faces[:, [0, 2, 1]]
    obj.to_mesh_clear()
    return obj, positions, faces

def atlas_mesh(part_id):
    part = next(p for p in atlas['parts'] if p['id'] == part_id)
    blob = buffers[part['chunk']]
    positions = np.frombuffer(blob, dtype='<f4', count=part['vertexCount']*3, offset=part['positions']).reshape(-1, 3).astype(float)
    faces = np.frombuffer(blob, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1, 3)
    return part, positions, faces

def nearest_distance(vertices, other, faces):
    tree = BVHTree.FromPolygons(other.tolist(), faces.tolist(), all_triangles=True)
    return np.array([tree.find_nearest(Vector(v))[3] for v in vertices])*1000


references = [('Vertebra C5','FJ3167'),('Vertebra C6','FJ3170'),('Vertebra C7','FJ3172'),('Vertebra T1','FJ3158'),
              ('Clavicle.l','FJ3237'),('Clavicle.r','FJ3362'),('First rib.l','FJ3228'),('First rib.r','FJ3334'),
              ('Scapula.l','FJ3279'),('Scapula.r','FJ3384'),('Humerus.l','FJ3262'),('Humerus.r','FJ3368')]
measurements=[]
context=[]
for name,part_id in references:
    obj,sv,sf=source_mesh(name)
    part,tv,tf=atlas_mesh(part_id)
    distances=np.concatenate([nearest_distance(sv,tv,tf),nearest_distance(tv,sv,sf)])
    measurements.append(dict(sourceObject=name,targetPartId=part_id,targetConceptId=part['conceptId'],
        role='original_fit_reference' if name.startswith(('Scapula','Humerus')) else 'independent_regional_holdout',
        rmsMm=float(np.sqrt(np.mean(distances**2))),meanMm=float(distances.mean()),
        p95Mm=float(np.percentile(distances,95)),maxMm=float(distances.max())))
    context.append((part['name'],tv,tf,sv,sf))
print('REGIONAL_REFERENCES',json.dumps(measurements,indent=2),flush=True)

# Assess a local rigid-similarity fit instead of silently extending the arm fit
# into a neck/thoracic-inlet region where independent residuals are larger.
def fit_similarity(a,b):
    ac,bc=a.mean(0),b.mean(0)
    aa,bb=a-ac,b-bc
    u,d,vt=np.linalg.svd(aa.T@bb)
    q=np.eye(3)
    q[-1,-1]=np.linalg.det(u@vt)
    rot=u@q@vt
    scale=np.sum(d*np.diag(q))/np.sum(aa**2)
    return scale*rot,bc-ac@(scale*rot)
def nearest_points(vertices,other,faces):
    tree=BVHTree.FromPolygons(other.tolist(),faces.tolist(),all_triangles=True)
    return np.array([tree.find_nearest(Vector(v))[0] for v in vertices])
local_matrix=np.eye(3)
local_translation=np.mean([row[1].mean(0)-row[3].mean(0) for row in context[:8]],axis=0)
for step in range(160):
    aa,bb=[],[]
    for _,tv,tf,sv,sf in context[:8]:
        samples=sv[np.linspace(0,len(sv)-1,min(500,len(sv)),dtype=int)]
        aa.append(samples)
        bb.append(nearest_points(samples@local_matrix+local_translation,tv,tf))
        targets=tv[np.linspace(0,len(tv)-1,min(500,len(tv)),dtype=int)]
        sources=nearest_points(targets,sv@local_matrix+local_translation,sf)
        aa.append((sources-local_translation)@np.linalg.inv(local_matrix))
        bb.append(targets)
    new_matrix,new_translation=fit_similarity(np.concatenate(aa),np.concatenate(bb))
    change=float(np.max(abs(new_matrix-local_matrix))+np.max(abs(new_translation-local_translation)))
    local_matrix,local_translation=new_matrix,new_translation
    if change<1e-7:break
candidate=[]
for name,tv,tf,sv,sf in context:
    adjusted=sv@local_matrix+local_translation
    d=np.concatenate([nearest_distance(adjusted,tv,tf),nearest_distance(tv,adjusted,sf)])
    candidate.append(dict(name=name,rmsMm=float(np.sqrt(np.mean(d*d))),p95Mm=float(np.percentile(d,95)),maxMm=float(d.max())))
print('REGIONAL_FIT_CANDIDATE',json.dumps(dict(matrix=local_matrix.tolist(),translation=local_translation.tolist(),iterations=step+1,measurements=candidate),indent=2),flush=True)

# Keep the same source frame as the already exported arm nerves: the trial local
# fit reduces inlet residuals but substantially worsens shoulder agreement.
# No deformation, fabricated cord, or inferred per-level root segmentation.
specs=[('SUP-TRUNK','superior-trunk','Superior trunk of brachial plexus','trunk'),
       ('MID-TRUNK','middle-trunk','Middle trunk of brachial plexus','trunk'),
       ('INF-TRUNK','inferior-trunk','Inferior trunk of brachial plexus','trunk'),
       ('SUP-ANT-DIV','superior-anterior-division','Anterior division of superior trunk of brachial plexus','division'),
       ('MID-ANT-DIV','middle-anterior-division','Anterior division of middle trunk of brachial plexus','division'),
       ('INF-ANT-DIV','inferior-anterior-division','Anterior division of inferior trunk of brachial plexus','division'),
       ('SUP-POST-DIV','superior-posterior-division','Posterior division of superior trunk of brachial plexus','division'),
       ('MID-POST-DIV','middle-posterior-division','Posterior division of middle trunk of brachial plexus','division'),
       ('INF-POST-DIV','inferior-posterior-division','Posterior division of inferior trunk of brachial plexus','division'),
       ('POST-CORD','posterior-cord','Posterior cord of brachial plexus','cord')]
selected_names={stem+'.'+suffix for _,_,stem,_ in specs for suffix in ['l','r']}
assert len(selected_names)==20
existing_names=set()
for filename in ['upper-arm-nerves.json','median-nerves.json']:
    existing=json.loads((OUT/filename).read_text())
    assert np.allclose(existing['registration']['matrixColumnVector'],transform,atol=1e-12,rtol=0)
    existing_names.update(p['sourceObject'] for p in existing['parts'])
assert not selected_names & existing_names
parts=[]
concepts=[]
blob=bytearray()
render_plexus=[]
refit_displacements=[]
def append(values,dtype):
    while len(blob)%4:blob.append(0)
    offset=len(blob)
    blob.extend(np.asarray(values,dtype=dtype).tobytes())
    return offset
for side,suffix in [('Left','l'),('Right','r')]:
    side_parts=[]
    for code,slug,stem,component in specs:
        obj,positions,indices=source_mesh(stem+'.'+suffix)
        assert obj.type=='CURVE'
        displacement=np.linalg.norm(positions@local_matrix+local_translation-positions,axis=1)*1000
        refit_displacements.append(dict(sourceObject=obj.name,rmsMm=float(np.sqrt(np.mean(displacement**2))),maxMm=float(displacement.max())))
        positions=positions.astype('<f4')
        faces=positions[indices].astype(float)
        face_normals=np.cross(faces[:,1]-faces[:,0],faces[:,2]-faces[:,0])
        assert np.all(np.linalg.norm(face_normals,axis=1)>1e-14)
        normals=np.zeros_like(positions,dtype=float)
        for corner in range(3):np.add.at(normals,indices[:,corner],face_normals)
        lengths=np.linalg.norm(normals,axis=1)
        assert np.all(lengths>0) and np.isfinite(positions).all()
        normals/=lengths[:,None]
        quantized=np.rint(normals*32767).astype('<i2')
        assert np.all(np.sum(face_normals*normals[indices].mean(1),axis=1)>0)
        part_id='ZA-BP-'+code+'-'+side[0]
        concept_id='atlas:'+side.lower()+'-brachial-plexus-'+slug
        name=side+' '+stem[0].lower()+stem[1:]
        parts.append(dict(id=part_id,conceptId=concept_id,name=name,system='nervous',chunk=0,
            positions=append(positions,'<f4'),normals=append(quantized,'<i2'),indices=append(indices,'<u4'),
            vertexCount=len(positions),indexCount=int(indices.size),bounds=[positions.min(0).tolist(),positions.max(0).tolist()],
            sourceObject=obj.name,sourceObjectType='CURVE',componentType=component,
            sourceSplineCount=len(obj.data.splines),sourceControlPointCount=sum(len(s.points)+len(s.bezier_points) for s in obj.data.splines),
            curveSettings={key:getattr(obj.data,key) for key in ['bevel_depth','bevel_resolution','resolution_u','use_fill_caps']},
            mirroredWindingCorrected=obj.matrix_world.to_3x3().determinant()<0,
            representation='partial_source_reference',expertReview='pending',
            registrationStatus='limited_neck_shoulder_alignment'))
        concepts.append(dict(id=concept_id,name=name,elements=[part_id]))
        side_parts.append(part_id)
        render_plexus.append((name,positions,indices))
    concepts.append(dict(id='atlas:'+side.lower()+'-brachial-plexus',name=side+' brachial plexus',elements=side_parts,
        representation='partial_source_reference',scope='3 trunks, 6 divisions and posterior cord; root bundle, separate medial/lateral cords and terminal branches not included'))
concepts.append(dict(id='atlas:brachial-plexus',name='Brachial plexus',elements=[p['id'] for p in parts],representation='partial_source_reference'))
binary=bytes(blob)
compressed=gzip.compress(binary,compresslevel=9,mtime=0)
(OUT/'brachial-plexus.bin').write_bytes(binary)
(OUT/'brachial-plexus.bin.gz').write_bytes(compressed)
source=dict(reference['source'])
source.update(selectedObjects=sorted(selected_names),blenderVersion=bpy.app.version_string,attribution='/models/extensions/BRACHIAL-PLEXUS-ATTRIBUTION.md')
local_transform=np.eye(4)
local_transform[:3,:3]=local_matrix.T
local_transform[:3,3]=local_translation
manifest=dict(version='Z-Anatomy partial brachial plexus reference extension 1',sex='male',source=source,parts=parts,concepts=concepts,
    chunks=[dict(url='/models/extensions/brachial-plexus.bin',bytes=len(binary),gzip='/models/extensions/brachial-plexus.bin.gz',gzipBytes=len(compressed),sha256=hashlib.sha256(binary).hexdigest())],
    triangles=sum(p['indexCount']//3 for p in parts),
    scope='Bilateral 3 trunks, 6 divisions and posterior cord only; roots excluded for unresolved source identity; incomplete plexus, limited neck/shoulder registration, expert anatomical review pending',
    coverage=dict(status='partial_source_reference',bilateralObjects=20,perSide=dict(rootBundles=0,trunks=3,divisions=6,cords=1),
        unresolved=['No separate Medial cord or Lateral cord source curve found; neither is inferred from terminal nerve proximal segments.',
                    'Roots objects are excluded: each contains 5 main source branches, an additional superior branch and communicating spline of unverified anatomical identity, plus 3 single-point remnants. No C5-T1 labels are inferred from endpoint topology.',
                    'Terminal and collateral branches outside these 20 named objects are not exported.'],
        excludedSourceObjects=['Roots of brachial plexus.l','Roots of brachial plexus.r'],
        excludedRootSplineReview=dict(mainBranches=[0,1,2,3,4],unverifiedSuperiorBranch=5,communicatingSpline=6,
            geometryFreeSinglePointRemnants=[7,8,9],
            superiorMedialSourcePosition=[0.013460719957947731, 0.015698183327913284, 1.5043705701828003],
            superiorSourceNeighborhood='C3/C4 surface neighborhood; geometric proximity is not a per-root anatomical identity'),
        excludedRootReview='docs/model/asset-registration-brachial-plexus.md#root-spline-review',
        notDuplicated=sorted(existing_names),sourceConnectivity='Source endpoints and intersections preserved, not welded or anatomically reconnected'),
    registration=dict(method='Existing six-bone upper-arm similarity retained for source-frame consistency with median/musculocutaneous packages; independently measured neck, clavicle and first-rib residuals limit regional accuracy',
        status='limited_neck_shoulder_alignment',referenceManifest='/models/extensions/upper-arm-nerves.json',
        matrixColumnVector=transform.tolist(),uniformScale=reference['registration']['uniformScale'],
        sourceUnits='meters',sourceAxes='X left, Y posterior, Z superior',targetUnits='meters',targetAxes='X left, Y superior, Z anterior',measurements=measurements,
        alternativeRegionalFit=dict(applied=False,method='C5-T1, bilateral clavicles and first ribs bidirectional similarity ICP',iterations=step+1,
            matrixColumnVector=(local_transform@transform).tolist(),measurements=candidate,sourceCurveDisplacements=refit_displacements,
            rejectedBecause='Reduces neck/first-rib error but worsens humerus/scapula fit and shifts the source curves away from the frame used by existing arm nerves; the tested local similarity is not a general improvement across the whole region.'),
        limitations='C5-T1/clavicle RMS 4.3-4.8 mm and first-rib RMS 8.3-8.4 mm remain. Not a validated root-foramen placement or complete connected plexus. No warp or fabricated bridging geometry.'))
(OUT/'brachial-plexus.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('EXPORT',json.dumps(dict(parts=len(parts),concepts=len(concepts),vertices=sum(p['vertexCount'] for p in parts),triangles=manifest['triangles'],bytes=len(binary),gzipBytes=len(compressed))),flush=True)

if '--render' in sys.argv:
    scene=bpy.data.scenes.new('Brachial plexus registration QA')
    bpy.context.window.scene=scene
    scene.render.engine='CYCLES'
    scene.cycles.samples=28
    scene.cycles.use_denoising=True
    scene.render.resolution_x=1500
    scene.render.resolution_y=1100
    scene.render.resolution_percentage=100
    scene.world=bpy.data.worlds.new('Plexus background')
    scene.world.color=(.055,.065,.085)
    def material(name,color,alpha=1):
        mat=bpy.data.materials.new(name)
        mat.use_nodes=True
        nodes=mat.node_tree.nodes
        surf=nodes.get('Principled BSDF')
        surf.inputs['Base Color'].default_value=(*color,1)
        surf.inputs['Roughness'].default_value=.55
        if alpha<1:
            mix=nodes.new('ShaderNodeMixShader')
            mix.inputs[0].default_value=alpha
            trans=nodes.new('ShaderNodeBsdfTransparent')
            mat.node_tree.links.new(trans.outputs[0],mix.inputs[1])
            mat.node_tree.links.new(surf.outputs[0],mix.inputs[2])
            mat.node_tree.links.new(mix.outputs[0],nodes.get('Material Output').inputs['Surface'])
        return mat
    bone_mat=material('Actual atlas skeleton',(.72,.76,.81),.15)
    muscle_mat=material('Actual atlas scalene muscle',(.52,.25,.23),.15)
    plexus_mat=material('New source plexus components',(1,.63,.05))
    existing_mat=material('Existing median and musculocutaneous nerves',(.07,.62,.85))
    artery_mat=material('Actual atlas artery',(.68,.12,.14),.65)
    def add_mesh(name,v,f,mat):
        mesh=bpy.data.meshes.new(name)
        mesh.from_pydata(v.tolist(),[],f.tolist())
        mesh.update()
        obj=bpy.data.objects.new(name,mesh)
        scene.collection.objects.link(obj)
        mesh.materials.append(mat)
        for face in mesh.polygons:face.use_smooth=True
        return obj
    for name,v,f,_,_ in context:add_mesh(name,v,f,bone_mat)
    for part in atlas['parts']:
        if any(key in part['name'].lower() for key in ['anterior scalene','middle scalene','subclavian artery','axillary artery']):
            _,v,f=atlas_mesh(part['id'])
            add_mesh(part['name'],v,f,artery_mat if part['system']=='arterial' else muscle_mat)
    for name,v,f in render_plexus:add_mesh(name,v,f,plexus_mat)
    for filename in ['upper-arm-nerves.json','median-nerves.json']:
        old=json.loads((OUT/filename).read_text())
        blobs=[(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for c in old['chunks']]
        for part in old['parts']:
            b=blobs[part['chunk']]
            v=np.frombuffer(b,dtype='<f4',count=part['vertexCount']*3,offset=part['positions']).reshape(-1,3)
            f=np.frombuffer(b,dtype='<u4',count=part['indexCount'],offset=part['indices']).reshape(-1,3)
            add_mesh(part['name'],v,f,existing_mat)
    camera_data=bpy.data.cameras.new('Camera')
    camera=bpy.data.objects.new('Camera',camera_data)
    scene.collection.objects.link(camera)
    scene.camera=camera
    camera_data.type='ORTHO'
    light_data=bpy.data.lights.new('Key','AREA')
    light_data.energy=180
    light_data.size=1.5
    light=bpy.data.objects.new('Key',light_data)
    scene.collection.objects.link(light)
    light.location=(0,1.5,1.6)
    light.rotation_euler=(Vector((0,1.38,0))-light.location).to_track_quat('-Z','Y').to_euler()
    views=[('front',(0,1.42,1.5),(0,1.39,-.015),.52),('left-oblique',(.48,1.42,1.1),(.07,1.415,-.015),.30)]
    for name,location,look_at,scale in views:
        camera.location=location
        camera_data.ortho_scale=scale
        back=(camera.location-Vector(look_at)).normalized()
        right=Vector((0,1,0)).cross(back).normalized()
        up=back.cross(right)
        camera.rotation_euler=Matrix((right,up,back)).transposed().to_euler()
        scene.render.filepath=str(OUT/('brachial-plexus-proof-'+name+'.png'))
        bpy.ops.render.render(write_still=True)
