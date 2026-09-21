"""Register and export the authored Z-Anatomy thyroid reference mesh.
Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
  --python scripts/export-thyroid.py [-- --render]
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

def source_mesh(name, evaluated=False):
    obj = bpy.data.objects[name]
    source = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()) if evaluated else obj
    mesh = source.to_mesh()
    mesh.calc_loop_triangles()
    vertices = mapped([list(source.matrix_world@v.co) for v in mesh.vertices])
    faces = np.array([list(t.vertices) for t in mesh.loop_triangles], dtype='<u4')
    if source.matrix_world.to_3x3().determinant() < 0:
        faces = faces[:, [0, 2, 1]]
    source.to_mesh_clear()
    return obj, vertices, faces

def atlas_mesh(part_id):
    part = next(p for p in atlas['parts'] if p['id'] == part_id)
    blob = buffers[part['chunk']]
    vertices = np.frombuffer(blob, dtype='<f4', count=part['vertexCount']*3, offset=part['positions']).reshape(-1, 3).astype(float)
    faces = np.frombuffer(blob, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1, 3)
    return part, vertices, faces

def nearest_distances(vertices, other, faces):
    tree = BVHTree.FromPolygons(other.tolist(), faces.tolist(), all_triangles=True)
    return np.array([tree.find_nearest(Vector(v))[3] for v in vertices])*1000

# Explicit element IDs avoid double-counting duplicated hyoid/cricoid concepts.
references = [('Hyoid bone','FJ3201'),('Thyroid cartilage','FJ2808'),('Cricoid cartilage','FJ2440'),
              ('Vertebra C3','FJ3161'),('Vertebra C4','FJ3164'),('Vertebra C5','FJ3167'),
              ('Vertebra C6','FJ3170'),('Vertebra C7','FJ3172'),('Trachea','FJ2541')]
measurements = []
context = []
for name, part_id in references:
    obj, source_vertices, source_faces = source_mesh(name)
    part, target_vertices, target_faces = atlas_mesh(part_id)
    distances = np.concatenate([nearest_distances(source_vertices,target_vertices,target_faces),
                                nearest_distances(target_vertices,source_vertices,source_faces)])
    measurements.append(dict(sourceObject=name,targetPartId=part_id,targetConceptId=part['conceptId'],
        role='independent_neck_holdout',sourceGeometry='authored base surface',
        unappliedSourceModifiers=[dict(name=m.name,type=m.type) for m in obj.modifiers],
        rmsMm=float(np.sqrt(np.mean(distances**2))),meanMm=float(distances.mean()),
        p95Mm=float(np.percentile(distances,95)),maxMm=float(distances.max())))
    context.append((part['name'],target_vertices,target_faces,source_vertices,source_faces))
print('NECK_REFERENCES',json.dumps(measurements,indent=2),flush=True)
# A neck-specific similarity fit is needed; the upper-arm fit has 4-8 mm RMS here.
# Fit only the hyoid and two laryngeal cartilages; retain trachea and C3-C7 as holdouts.
def fit_similarity(a, b):
    ac, bc = a.mean(0), b.mean(0)
    aa, bb = a-ac, b-bc
    u, d, vt = np.linalg.svd(aa.T@bb)
    correction = np.eye(3)
    correction[-1, -1] = np.linalg.det(u@vt)
    rotation = u@correction@vt
    scale = np.sum(d*np.diag(correction))/np.sum(aa**2)
    return scale*rotation, bc-ac@(scale*rotation)

def nearest_points(vertices, other, faces):
    tree = BVHTree.FromPolygons(other.tolist(), faces.tolist(), all_triangles=True)
    return np.array([tree.find_nearest(Vector(v))[0] for v in vertices])

local_matrix = np.eye(3)
local_translation = np.mean([row[1].mean(0)-row[3].mean(0) for row in context[:3]], axis=0)
for step in range(160):
    aa, bb = [], []
    for _, target_vertices, target_faces, source_vertices, source_faces in context[:3]:
        source_samples = source_vertices[np.linspace(0,len(source_vertices)-1,min(800,len(source_vertices)),dtype=int)]
        current = source_samples@local_matrix+local_translation
        aa.append(source_samples)
        bb.append(nearest_points(current,target_vertices,target_faces))
        target_samples = target_vertices[np.linspace(0,len(target_vertices)-1,min(800,len(target_vertices)),dtype=int)]
        source_nearest = nearest_points(target_samples,source_vertices@local_matrix+local_translation,source_faces)
        aa.append((source_nearest-local_translation)@np.linalg.inv(local_matrix))
        bb.append(target_samples)
    new_matrix, new_translation = fit_similarity(np.concatenate(aa),np.concatenate(bb))
    change = float(np.max(abs(new_matrix-local_matrix))+np.max(abs(new_translation-local_translation)))
    local_matrix, local_translation = new_matrix, new_translation
    if change < 1e-7:
        break
local_transform = np.eye(4)
local_transform[:3,:3] = local_matrix.T
local_transform[:3,3] = local_translation
transform = local_transform@transform
for index, (row, original) in enumerate(zip(context,measurements)):
    name, target_vertices, target_faces, source_vertices, source_faces = row
    source_vertices = source_vertices@local_matrix+local_translation
    context[index] = (name,target_vertices,target_faces,source_vertices,source_faces)
    distances = np.concatenate([nearest_distances(source_vertices,target_vertices,target_faces),nearest_distances(target_vertices,source_vertices,source_faces)])
    original['upperArmTransformRmsMm'] = original['rmsMm']
    original.update(role='local_fit_reference' if index < 3 else 'independent_neck_holdout',
                    rmsMm=float(np.sqrt(np.mean(distances**2))),meanMm=float(distances.mean()),
                    p95Mm=float(np.percentile(distances,95)),maxMm=float(distances.max()))
print('LOCAL_NECK_FIT',json.dumps(dict(iterations=step+1,lastDelta=change,localScale=float(np.cbrt(np.linalg.det(local_matrix))),matrix=transform.tolist(),measurements=measurements),indent=2),flush=True)
obj, positions, indices = source_mesh('Thyroid gland', evaluated=True)
print('THYROID_SOURCE',json.dumps(dict(baseVertices=len(obj.data.vertices),basePolygons=len(obj.data.polygons),
    evaluatedVertices=len(positions),evaluatedTriangles=len(indices),bounds=[positions.min(0).tolist(),positions.max(0).tolist()],
    modifiers=[dict(name=m.name,type=m.type,show_viewport=m.show_viewport,show_render=m.show_render,
                    levels=getattr(m,'levels',None),render_levels=getattr(m,'render_levels',None)) for m in obj.modifiers]),indent=2),flush=True)

assert max(m['rmsMm'] for m in measurements[:3]) < 2, 'Local laryngeal registration needs review'
positions = positions.astype('<f4')
triangles = positions[indices].astype(float)
face_normals = np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0])
assert np.all(np.linalg.norm(face_normals,axis=1)>1e-14)
volume = float(np.sum(np.einsum('ij,ij->i',triangles[:,0],np.cross(triangles[:,1],triangles[:,2])))/6)
if volume < 0:
    indices = indices[:,[0,2,1]]
    face_normals = -face_normals
normals = np.zeros_like(positions,dtype=float)
for corner in range(3):
    np.add.at(normals,indices[:,corner],face_normals)
lengths = np.linalg.norm(normals,axis=1)
assert np.all(lengths>0) and np.isfinite(positions).all()
normals /= lengths[:,None]
quantized = np.rint(normals*32767).astype('<i2')
edges = np.sort(np.concatenate([indices[:,[0,1]],indices[:,[1,2]],indices[:,[2,0]]]),axis=1)
_, edge_counts = np.unique(edges,axis=0,return_counts=True)
assert np.all(edge_counts==2), 'Evaluated thyroid is not a closed two-manifold surface'
assert np.all(np.sum(face_normals*normals[indices].mean(1),axis=1)>0)
blob=bytearray()
def append(values,dtype):
    while len(blob)%4:blob.append(0)
    offset=len(blob)
    blob.extend(np.asarray(values,dtype=dtype).tobytes())
    return offset
part=dict(id='ZA-THYROID',conceptId='atlas:thyroid-gland',name='Thyroid gland',system='endocrine',chunk=0,
          positions=append(positions,'<f4'),normals=append(quantized,'<i2'),indices=append(indices,'<u4'),
          vertexCount=len(positions),indexCount=int(indices.size),bounds=[positions.min(0).tolist(),positions.max(0).tolist()],
          sourceObject='Thyroid gland',sourceObjectType='MESH',
          representation='source_authored_low_detail_reference',expertReview='pending',
          sourceBaseGeometry=dict(vertices=len(obj.data.vertices),polygons=len(obj.data.polygons)),
          appliedSourceModifiers=[dict(name=m.name,type=m.type,viewportLevels=getattr(m,'levels',None),renderLevels=getattr(m,'render_levels',None)) for m in obj.modifiers],
          evaluation='Source viewport evaluation: Mirror, Solidify, then Subdivision level 1. No added smoothing or decimation.',
          quality=dict(closedTwoManifold=True,absoluteEnclosedVolumeCubicCm=abs(volume)*1e6),
          limitations='Low-detail authored shape, not a scan or segmented lobes/isthmus. Subdivision adds display triangles, not anatomical detail. Expert review of location and morphology pending.')
binary=bytes(blob)
compressed=gzip.compress(binary,compresslevel=9,mtime=0)
(OUT/'thyroid.bin').write_bytes(binary)
(OUT/'thyroid.bin.gz').write_bytes(compressed)
source=dict(reference['source'])
source.update(selectedObjects=['Thyroid gland'],blenderVersion=bpy.app.version_string,attribution='/models/extensions/THYROID-ATTRIBUTION.md')
manifest=dict(version='Z-Anatomy thyroid reference extension 1',sex='male',source=source,parts=[part],
    chunks=[dict(url='/models/extensions/thyroid.bin',bytes=len(binary),gzip='/models/extensions/thyroid.bin.gz',gzipBytes=len(compressed),sha256=hashlib.sha256(binary).hexdigest())],
    concepts=[dict(id=part['conceptId'],name=part['name'],elements=[part['id']])],triangles=len(indices),
    scope='One source-authored low-detail thyroid gland reference mesh; parathyroids, subdivisions and expert anatomical validation are not included',
    registration=dict(method='Neck-specific bidirectional nearest-surface similarity ICP on hyoid, thyroid cartilage and cricoid cartilage; C3-C7 and trachea held out',
                      initialization='/models/extensions/upper-arm-nerves.json (rejected as final neck registration)',
                      matrixColumnVector=transform.tolist(),uniformScale=float(np.cbrt(np.linalg.det(transform[:3,:3]))),
                      iterations=step+1,lastTransformDelta=change,sourceUnits='meters',sourceAxes='X left, Y posterior, Z superior',
                      targetUnits='meters',targetAxes='X left, Y superior, Z anterior',measurements=measurements,
                      limitations='Local laryngeal fit is substantially better than the arm transform but residual cervical/tracheal shape differences remain. Surface agreement is not thyroid morphology or anatomical validation.'))
(OUT/'thyroid.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('EXPORT',json.dumps(dict(vertices=len(positions),triangles=len(indices),bytes=len(binary),gzipBytes=len(compressed),volumeCc=abs(volume)*1e6)),flush=True)

if '--render' in sys.argv:
    scene=bpy.data.scenes.new('Thyroid registration QA')
    bpy.context.window.scene=scene
    scene.render.engine='CYCLES'
    scene.cycles.samples=32
    scene.cycles.use_denoising=True
    scene.render.resolution_x=1300
    scene.render.resolution_y=1300
    scene.render.resolution_percentage=100
    scene.world=bpy.data.worlds.new('Thyroid background')
    scene.world.color=(.055,.065,.085)
    def material(name,color,alpha=1):
        mat=bpy.data.materials.new(name)
        mat.use_nodes=True
        nodes=mat.node_tree.nodes
        surf=nodes.get('Principled BSDF')
        surf.inputs['Base Color'].default_value=(*color,1)
        surf.inputs['Roughness'].default_value=.6
        if alpha<1:
            mix=nodes.new('ShaderNodeMixShader')
            mix.inputs[0].default_value=alpha
            trans=nodes.new('ShaderNodeBsdfTransparent')
            mat.node_tree.links.new(trans.outputs[0],mix.inputs[1])
            mat.node_tree.links.new(surf.outputs[0],mix.inputs[2])
            mat.node_tree.links.new(mix.outputs[0],nodes.get('Material Output').inputs['Surface'])
        return mat
    bone_mat=material('Actual atlas neck bone',(.73,.79,.84),.18)
    cartilage_mat=material('Actual atlas cartilage',(.41,.69,.75),.45)
    trachea_mat=material('Actual atlas trachea',(.65,.60,.55),.55)
    gland_mat=material('Thyroid reference',(.84,.22,.12),.85)
    def add_mesh(name,v,f,mat):
        mesh=bpy.data.meshes.new(name)
        mesh.from_pydata(v.tolist(),[],f.tolist())
        mesh.update()
        obj=bpy.data.objects.new(name,mesh)
        scene.collection.objects.link(obj)
        mesh.materials.append(mat)
        for face in mesh.polygons:face.use_smooth=True
        return obj
    for name,v,f,_,_ in context:
        mat=trachea_mat if name=='Trachea' else (cartilage_mat if 'cartilage' in name else bone_mat)
        add_mesh(name,v,f,mat)
    add_mesh('Source thyroid gland',positions,indices,gland_mat)
    camera_data=bpy.data.cameras.new('Camera')
    camera=bpy.data.objects.new('Camera',camera_data)
    scene.collection.objects.link(camera)
    scene.camera=camera
    camera_data.type='ORTHO'
    camera_data.ortho_scale=.15
    light_data=bpy.data.lights.new('Key','AREA')
    light_data.energy=80
    light_data.size=.5
    light=bpy.data.objects.new('Key',light_data)
    scene.collection.objects.link(light)
    light.location=(0,1.55,.7)
    light.rotation_euler=(Vector((0,1.47,0))-light.location).to_track_quat('-Z','Y').to_euler()
    for name,location in [('front',(0,1.47,.6)),('oblique',(.45,1.49,.5))]:
        camera.location=location
        back=(camera.location-Vector((0,1.47,-.005))).normalized()
        right=Vector((0,1,0)).cross(back).normalized()
        up=back.cross(right)
        camera.rotation_euler=Matrix((right,up,back)).transposed().to_euler()
        scene.render.filepath=str(OUT/('thyroid-proof-'+name+'.png'))
        bpy.ops.render.render(write_still=True)
