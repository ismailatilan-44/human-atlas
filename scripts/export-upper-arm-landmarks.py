"""Export source-derived attachment reference anchors, never whole-bone centers.
Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
  --python scripts/export-upper-arm-landmarks.py [-- --render]
"""
import bpy
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public/models/extensions'
extension = json.loads((OUT / 'upper-arm-nerves.json').read_text())
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == extension['source']['sha256']
transform = np.array(extension['registration']['matrixColumnVector'])
atlas = json.loads((ROOT / 'public/models/atlas.json').read_text())
blobs = [(ROOT / 'public' / c['url'].lstrip('/')).read_bytes() for c in atlas['chunks']]


def mapped(points):
    return np.asarray(points) @ transform[:3, :3].T + transform[:3, 3]


def mesh_data(obj):
    assert obj.type == 'MESH'
    mesh = obj.to_mesh()
    mesh.calc_loop_triangles()
    vertices = np.array([obj.matrix_world @ v.co for v in mesh.vertices])
    faces = np.array([t.vertices[:] for t in mesh.loop_triangles], dtype=int)
    obj.to_mesh_clear()
    return vertices, faces


def bvh(vertices, faces):
    return BVHTree.FromPolygons(vertices.tolist(), faces.tolist(), all_triangles=True)


def nearest(tree, point):
    result = tree.find_nearest(Vector(point))
    assert result[0] is not None
    return np.array(result[0]), float(result[3])


def atlas_mesh(concept_id):
    part = next(p for p in atlas['parts'] if p['conceptId'] == concept_id)
    blob = blobs[part['chunk']]
    vertices = np.frombuffer(blob, dtype='<f4', count=part['vertexCount']*3, offset=part['positions']).reshape(-1, 3).astype(float)
    faces = np.frombuffer(blob, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1, 3)
    return part, vertices, faces


# Anatomical identity comes from the existing curated origin/insertion relations;
# source object names, bone parenting and the dedicated attachment collection
# support selection of an actual source surface rather than an arbitrary bone point.
specs = [
    ('coracoid-process', 'Coracobrachialis muscle.o', 'Scapula', ('FMA13396', 'FMA13395'), 'Coracobrachialis origin surface; representative point for the shared coracoid origin region, not the whole process'),
    ('supraglenoid-tubercle', 'Long head of biceps brachii.o', 'Scapula', ('FMA13396', 'FMA13395'), 'Long-head biceps origin surface; representative attachment-region point, not a segmented tubercle'),
    ('radial-tuberosity', 'Biceps brachii muscle.e', 'Radius', ('FMA23465', 'FMA23464'), 'Biceps distal insertion surface; representative attachment-region point, not the full radial tuberosity'),
]
anchors = []
render_bones = {}
render_patches = []
for index, (side, suffix) in enumerate([('left', 'l'), ('right', 'r')]):
    for slug, stem, bone_name, bone_ids, limitation in specs:
        obj = bpy.data.objects[stem + suffix]
        expected_parent = bone_name + '.' + suffix
        assert obj.parent and obj.parent.name == expected_parent
        assert '2: Muscular insertions' in [c.name for c in obj.users_collection]
        vertices, faces = mesh_data(obj)
        triangles = vertices[faces]
        areas = np.linalg.norm(np.cross(triangles[:, 1]-triangles[:, 0], triangles[:, 2]-triangles[:, 0]), axis=1)/2
        assert np.sum(areas) > 0
        centroid = np.average(triangles.mean(axis=1), axis=0, weights=areas)
        # Restrict the point to the actual source attachment surface.
        source_point, centroid_projection = nearest(bvh(vertices, faces), centroid)
        position = mapped(source_point)
        source_bone_vertices, source_bone_faces = mesh_data(bpy.data.objects[expected_parent])
        _, source_gap = nearest(bvh(source_bone_vertices, source_bone_faces), source_point)
        bone_part, target_vertices, target_faces = atlas_mesh(bone_ids[index])
        target_point, target_gap = nearest(bvh(target_vertices, target_faces), position)
        assert np.isfinite(position).all() and source_gap < .004 and target_gap < .012
        assert (position[0] > 0) == (side == 'left')
        anchors.append(dict(
            conceptId='atlas:' + side + '-' + slug, status='anchored_reference',
            position=position.tolist(), contextPartIds=[bone_part['id']], sourceObject=obj.name, representation='attachment_surface_reference_point',
            source=dict(id='zanatomy', objectName=obj.name, objectType=obj.type,
                        parentObject=expected_parent, collection='2: Muscular insertions',
                        sourceWorldPosition=source_point.tolist(), vertexCount=len(vertices), triangleCount=len(faces),
                        geometryMode='authored_base_attachment_surface',
                        unappliedDisplayModifiers=[dict(name=m.name, type=m.type) for m in obj.modifiers]),
            method='Area-weighted triangle centroid projected to the same source attachment surface, then existing atlas registration transform',
            targetBone=dict(conceptId=bone_ids[index], partId=bone_part['id'], nearestSurfacePosition=target_point.tolist(),
                            distanceMm=target_gap*1000),
            quality=dict(sourceBoneDistanceMm=source_gap*1000, centroidProjectionMm=centroid_projection*1000,
                         registration='shared six-bone similarity fit from upper-arm-nerves.json', expertReview='pending'),
            evidence=[dict(sourceId='zanatomy', locator='Startup.blend / '+obj.name),
                      dict(sourceId='atlas-upper-arm-knowledge', locator='data/anatomy/upper-arm.json / origin or insertion relation targeting atlas:'+side+'-'+slug)],
            limitations=[limitation, 'Not snapped to the target bone: source registration residual is retained and measured.',
                         'Uses the authored base attachment surface before Solidify/Subdivision display modifiers.',
                         'Source authored attachment region and technical registration are not expert anatomical validation.']))
        render_bones[expected_parent] = dict(sourceVertices=mapped(source_bone_vertices), sourceFaces=source_bone_faces,
                                            targetVertices=target_vertices, targetFaces=target_faces)
        render_patches.append((mapped(vertices), faces, position))
    anchors.append(dict(conceptId='atlas:'+side+'-humerus-medial-midshaft', status='unresolved', position=None,
                        representation='unanchored_landmark', source=None,
                        evidence=[dict(sourceId='zanatomy', locator='Startup.blend / Humerus.'+suffix+' children, material slots, vertex groups and coracobrachialis object inventory')],
                        limitations=['No dedicated coracobrachialis insertion patch or matching named midshaft marker was found. Humerus has only Bone/Cartilage material slots and no vertex groups.',
                                     'The source coracobrachialis .o surface is parented to scapula and represents the origin; it cannot stand in for humeral insertion.',
                                     'Neither the whole humerus center nor a guessed muscle endpoint was exported as a landmark.']))

result = dict(version=1, units='meters', coordinateSystem='Human Atlas: X left, Y superior, Z anterior',
              source=extension['source'], registrationManifest='/models/extensions/upper-arm-nerves.json',
              registrationMatrixColumnVector=transform.tolist(),
              anchors=[a for a in anchors if a['position'] is not None],
              unresolved=[a for a in anchors if a['position'] is None],
              limits=['Six anchors represent real source attachment surfaces; two humeral attachment anchors remain unresolved.',
                      'Named two-vertex label connectors were rejected as primary anchors: cached left world transforms are identity; explicit parent composition still leaves coracoid/supraglenoid label offsets inconsistent with the actual left attachment patches.',
                      'The Short head of biceps brachii.ol surface is parented to Scapula.r; its suffix was not trusted for laterality.'])
(OUT/'upper-arm-landmarks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps([dict(id=a['conceptId'], status=a['status'], gapMm=a.get('targetBone', {}).get('distanceMm')) for a in anchors], indent=2))

if '--render' in sys.argv:
    # Pair of reproducible technical QA views: source surfaces, then actual atlas surfaces.
    scene = bpy.data.scenes.new('Landmark registration QA')
    bpy.context.window.scene = scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1300
    scene.render.resolution_percentage = 100
    scene.world = bpy.data.worlds.new('Landmark background')
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
    bone_mat = material('Bone', (.70, .73, .78), .45)
    patch_mat = material('Source attachment surface', (.84, .17, .12))
    point_mat = material('Anchor', (1, .63, .03))
    def add_mesh(name, vertices, faces, mat):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices.tolist(), [], faces.tolist())
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)
        mesh.materials.append(mat)
        return obj
    groups = {'source': [], 'target': []}
    for name, data in render_bones.items():
        for group in groups:
            obj = add_mesh(group+' '+name, data[group+'Vertices'], data[group+'Faces'], bone_mat)
            groups[group].append(obj)
    for vertices, faces, position in render_patches:
        add_mesh('Source attachment patch', vertices, faces, patch_mat)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=.0025, location=position)
        bpy.context.object.data.materials.append(point_mat)
    camera_data = bpy.data.cameras.new('Camera')
    camera = bpy.data.objects.new('Camera', camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = 'ORTHO'
    camera_data.ortho_scale = .72
    camera.location = (.20, 1.20, 2)
    back = (camera.location-Vector((0, 1.19, -.025))).normalized()
    right = Vector((0, 1, 0)).cross(back).normalized()
    up = back.cross(right)
    camera.rotation_euler = Matrix((right, up, back)).transposed().to_euler()
    light_data = bpy.data.lights.new('Key', 'AREA')
    light_data.energy = 220
    light_data.size = 2
    light = bpy.data.objects.new('Key', light_data)
    scene.collection.objects.link(light)
    light.location = (0, 1.4, 1.8)
    light.rotation_euler = (Vector((0, 1.2, 0))-light.location).to_track_quat('-Z', 'Y').to_euler()
    for group in groups:
        for name, objects in groups.items():
            for obj in objects:
                obj.hide_render = name != group
        scene.render.filepath = str(OUT/('landmark-proof-'+group+'.png'))
        bpy.ops.render.render(write_still=True)
