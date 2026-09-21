"""Export Z-Anatomy median nerves after measuring forearm/wrist registration.
Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
  --python scripts/export-median-nerves.py [-- --render]
The existing upper-arm extension and main atlas are read-only inputs.
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

def atlas_mesh(name):
    part = next(p for p in atlas['parts'] if p['name'] == name)
    blob = buffers[part['chunk']]
    positions = np.frombuffer(blob, dtype='<f4', count=part['vertexCount']*3, offset=part['positions']).reshape(-1, 3).astype(float)
    faces = np.frombuffer(blob, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1, 3)
    return part, positions, faces

def nearest_distance(vertices, other, faces):
    tree = BVHTree.FromPolygons(other.tolist(), faces.tolist(), all_triangles=True)
    return np.array([tree.find_nearest(Vector(v))[3] for v in vertices])*1000

# Radius participated in the original fit; ulna and the eight carpal pairs did not.
# Every comparison retains source/target identity and laterality.
reference_names = [('Radius', 'radius'), ('Ulna', 'ulna'), ('Scaphoid bone', 'scaphoid'),
                   ('Lunate bone', 'lunate'), ('Capitate bone', 'capitate'), ('Hamate bone', 'hamate'),
                   ('Pisiform bone', 'pisiform'), ('Trapezium bone', 'trapezium'),
                   ('Trapezoid bone', 'trapezoid'), ('Triquetrum bone', 'triquetral')]
measurements = []
context = []
for side, suffix in [('Left', 'l'), ('Right', 'r')]:
    for source_name, target_name in reference_names:
        obj, source_vertices, source_faces = source_mesh(source_name+'.'+suffix)
        part, target_vertices, target_faces = atlas_mesh(side+' '+target_name)
        distances = np.concatenate([nearest_distance(source_vertices, target_vertices, target_faces),
                                    nearest_distance(target_vertices, source_vertices, source_faces)])
        measurements.append(dict(sourceObject=obj.name, targetPartId=part['id'], targetConceptId=part['conceptId'],
                                 role='original_fit_reference' if source_name == 'Radius' else 'independent_holdout',
                                 sourceVertices=len(source_vertices), targetVertices=len(target_vertices),
                                 sourceGeometry='authored base bone surface',
                                 unappliedSourceModifiers=[dict(name=m.name,type=m.type) for m in obj.modifiers],
                                 rmsMm=float(np.sqrt(np.mean(distances**2))), meanMm=float(distances.mean()),
                                 p95Mm=float(np.percentile(distances, 95)), maxMm=float(distances.max())))
        context.append((part['name'], target_vertices, target_faces, source_vertices, source_faces))
print('REGISTRATION_MEASUREMENTS', json.dumps(measurements, indent=2), flush=True)
# A broad export sanity gate, not an anatomical/clinical accuracy claim.
assert max(m['rmsMm'] for m in measurements) < 4, 'Forearm/wrist similarity registration needs review before export'

blob = bytearray()
parts = []
render_nerves = []
def append(values, dtype):
    while len(blob)%4:
        blob.append(0)
    offset = len(blob)
    blob.extend(np.asarray(values, dtype=dtype).tobytes())
    return offset

for side, suffix in [('Left', 'l'), ('Right', 'r')]:
    obj, positions, indices = source_mesh('Median nerve.'+suffix)
    positions = positions.astype('<f4')
    faces = positions[indices].astype(float)
    face_normals = np.cross(faces[:, 1]-faces[:, 0], faces[:, 2]-faces[:, 0])
    assert np.all(np.linalg.norm(face_normals, axis=1) > 1e-14)
    normals = np.zeros_like(positions, dtype=float)
    for corner in range(3):
        np.add.at(normals, indices[:, corner], face_normals)
    lengths = np.linalg.norm(normals, axis=1)
    assert np.all(lengths > 0) and np.isfinite(positions).all()
    normals /= lengths[:, None]
    quantized = np.rint(normals*32767).astype('<i2')
    assert indices.max() < len(positions)
    assert np.all(np.sum(face_normals*normals[indices].mean(axis=1), axis=1) > 0)
    parts.append(dict(id='ZA-MED-'+side[0], conceptId='atlas:'+side.lower()+'-median-nerve',
                      name=side+' median nerve', system='nervous', chunk=0,
                      positions=append(positions, '<f4'), normals=append(quantized, '<i2'), indices=append(indices, '<u4'),
                      vertexCount=len(positions), indexCount=int(indices.size),
                      bounds=[positions.min(axis=0).tolist(), positions.max(axis=0).tolist()],
                      sourceObject=obj.name, sourceObjectType='CURVE',
                      curveSettings={key:getattr(obj.data,key) for key in ['bevel_depth','bevel_resolution','resolution_u','use_fill_caps']},
                      sourceSplineCount=len(obj.data.splines), sourceControlPointCount=sum(len(s.points)+len(s.bezier_points) for s in obj.data.splines),
                      mirroredWindingCorrected=obj.matrix_world.to_3x3().determinant()<0))
    render_nerves.append((obj.name, positions, indices))
binary = bytes(blob)
compressed = gzip.compress(binary, compresslevel=9, mtime=0)
(OUT/'median-nerves.bin').write_bytes(binary)
(OUT/'median-nerves.bin.gz').write_bytes(compressed)
source = dict(reference['source'])
source['selectedObjects'] = ['Median nerve.l', 'Median nerve.r']
source['blenderVersion'] = bpy.app.version_string
manifest = dict(version='Z-Anatomy median nerve extension 1', sex='male',
                scope='Bilateral source median nerve main curves; separate muscular, palmar and digital branches are not included; expert anatomical review pending',
                source=source, parts=parts,
                chunks=[dict(url='/models/extensions/median-nerves.bin', bytes=len(binary),
                             gzip='/models/extensions/median-nerves.bin.gz', gzipBytes=len(compressed),
                             sha256=hashlib.sha256(binary).hexdigest())],
                triangles=sum(p['indexCount']//3 for p in parts),
                concepts=[dict(id=p['conceptId'], name=p['name'], elements=[p['id']]) for p in parts],
                registration=dict(method='Reused upper-arm six-bone similarity fit, measured against bilateral radius/ulna and all eight carpal bones before export',
                                  referenceManifest='/models/extensions/upper-arm-nerves.json',
                                  matrixColumnVector=transform.tolist(), uniformScale=reference['registration']['uniformScale'],
                                  sourceUnits='meters', sourceAxes='X left, Y posterior, Z superior',
                                  targetUnits='meters', targetAxes='X left, Y superior, Z anterior',
                                  measurements=measurements,
                                  limitations='Bidirectional vertex-to-triangle surface discrepancies include source edits and target simplification. Matching bone surfaces do not validate the median nerve path or complete branch coverage. No local nerve warp or refit was performed.'))
(OUT/'median-nerves.json').write_text(json.dumps(manifest, indent=2)+'\n')
print('EXPORT', json.dumps(dict(parts=len(parts), vertices=sum(p['vertexCount'] for p in parts),
                               triangles=manifest['triangles'], bytes=len(binary), gzipBytes=len(compressed))))

if '--render' in sys.argv:
    scene = bpy.data.scenes.new('Median nerve registration QA')
    bpy.context.window.scene = scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1300
    scene.render.resolution_percentage = 100
    scene.world = bpy.data.worlds.new('Median nerve background')
    scene.world.color = (.06, .07, .09)
    def material(name, color, alpha=1):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        surf = nodes.get('Principled BSDF')
        surf.inputs['Base Color'].default_value = (*color, 1)
        surf.inputs['Roughness'].default_value = .6
        if alpha < 1:
            mix = nodes.new('ShaderNodeMixShader')
            mix.inputs[0].default_value = alpha
            transparent = nodes.new('ShaderNodeBsdfTransparent')
            mat.node_tree.links.new(transparent.outputs[0], mix.inputs[1])
            mat.node_tree.links.new(surf.outputs[0], mix.inputs[2])
            mat.node_tree.links.new(mix.outputs[0], nodes.get('Material Output').inputs['Surface'])
        return mat
    bone_mat = material('Actual atlas bone', (.75, .78, .82), .24)
    muscle_mat = material('Actual atlas muscle', (.50, .20, .18), .13)
    nerve_mat = material('Median nerve', (1, .59, .04))
    def add_mesh(name, vertices, faces, mat):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices.tolist(), [], faces.tolist())
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)
        mesh.materials.append(mat)
        for face in mesh.polygons:
            face.use_smooth = True
        return obj
    for name, vertices, faces, _, _ in context:
        add_mesh(name, vertices, faces, bone_mat)
    for side in ['Left', 'Right']:
        for name in ['humerus', 'scapula']:
            _, vertices, faces = atlas_mesh(side+' '+name)
            add_mesh(side+' '+name, vertices, faces, bone_mat)
    # Use actual atlas muscles, selecting only bilateral upper-limb context.
    for part in atlas['parts']:
        if part['system'] != 'muscular' or not any(s in part['name'].lower() for s in ['biceps brachii','pronator teres','flexor digitorum profundus','flexor digitorum superficialis','flexor carpi radialis']):
            continue
        _, vertices, faces = atlas_mesh(part['name'])
        add_mesh(part['name'], vertices, faces, muscle_mat)
    for name, vertices, faces in render_nerves:
        add_mesh(name, vertices, faces, nerve_mat)
    camera_data = bpy.data.cameras.new('Camera')
    camera = bpy.data.objects.new('Camera', camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = 'ORTHO'
    light_data = bpy.data.lights.new('Key', 'AREA')
    light_data.energy = 220
    light_data.size = 2
    light = bpy.data.objects.new('Key', light_data)
    scene.collection.objects.link(light)
    light.location = (0, 1.25, 1.8)
    light.rotation_euler = (Vector((0, 1.1, 0))-light.location).to_track_quat('-Z', 'Y').to_euler()
    views = [('front', (0, 1.14, 2), (0, 1.14, -.02), .86),
             ('left-wrist', (.50, .95, 1.7), (.26, .94, -.02), .31)]
    for name, location, look_at, scale in views:
        camera.location = location
        camera_data.ortho_scale = scale
        back = (camera.location-Vector(look_at)).normalized()
        right = Vector((0, 1, 0)).cross(back).normalized()
        up = back.cross(right)
        camera.rotation_euler = Matrix((right, up, back)).transposed().to_euler()
        scene.render.filepath = str(OUT/('median-nerve-proof-'+name+'.png'))
        bpy.ops.render.render(write_still=True)
