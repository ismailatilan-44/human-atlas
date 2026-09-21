"""Export eight Z-Anatomy knee meshes into Human Atlas coordinates.

/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend --python scripts/export-knee-structures.py -- --render

Requires Blender's bundled numpy. Reads the pinned source blend and target atlas;
never saves the blend or modifies the main atlas. --render writes knee-only QA PNGs.
"""
import bpy
import gzip
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work/open-assets-review'
OUT = ROOT / 'public/models/extensions'
EXPECTED_BLEND = '9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
EXPECTED_ATLAS = 'c359f4bcd2cba90b7411d66d5e9fc04dc81294d46cd5c1e8b212c824f2e5bbee'
AXIS = np.array([[1., 0., 0.], [0., 0., -1.], [0., 1., 0.]])
BONES = [
    ('Femur.l', 'FJ3259', 'fit'), ('Femur.r', 'FJ3365', 'fit'),
    ('Tibia.l', 'FJ3282', 'fit'), ('Tibia.r', 'FJ3387', 'fit'),
    ('Fibula.l', 'FJ3260', 'fit'), ('Fibula.r', 'FJ3366', 'fit'),
    ('Patella.l', 'FJ3275', 'holdout'), ('Patella.r', 'FJ3381', 'holdout'),
]
STRUCTURES = [
    ('Medial meniscus', 'medial-meniscus', 'MM'),
    ('Lateral meniscus', 'lateral-meniscus', 'LM'),
    ('Anterior cruciate ligament', 'anterior-cruciate-ligament', 'ACL'),
    ('Posterior cruciate ligament', 'posterior-cruciate-ligament', 'PCL'),
]
OUT.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == EXPECTED_BLEND, 'Source blend changed'
assert hashlib.sha256((ROOT / 'public/models/atlas.json').read_bytes()).hexdigest() == EXPECTED_ATLAS, 'Target atlas changed'
atlas = json.loads((ROOT / 'public/models/atlas.json').read_text())
blobs = [(ROOT / 'public' / chunk['url'].lstrip('/')).read_bytes() for chunk in atlas['chunks']]
part_by_id = {part['id']: part for part in atlas['parts']}
depsgraph = bpy.context.evaluated_depsgraph_get()


def read_source(name):
    obj = bpy.data.objects[name]
    assert obj.type == 'MESH', name
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    mesh.calc_loop_triangles()
    vertices = np.array([list(evaluated.matrix_world @ v.co) for v in mesh.vertices], dtype=float)
    faces = np.array([list(t.vertices) for t in mesh.loop_triangles], dtype=np.int64)
    determinant = float(evaluated.matrix_world.to_3x3().determinant())
    if determinant < 0:
        faces = faces[:, [0, 2, 1]]
    modifiers = [dict(name=m.name, type=m.type, showViewport=m.show_viewport,
                      showRender=m.show_render, levels=getattr(m, 'levels', None),
                      renderLevels=getattr(m, 'render_levels', None)) for m in obj.modifiers]
    metadata = dict(name=name, objectType=obj.type, parent=obj.parent.name if obj.parent else None,
                    baseVertices=len(obj.data.vertices), basePolygons=len(obj.data.polygons),
                    evaluatedVertices=len(vertices), evaluatedTriangles=len(faces),
                    evaluation='evaluated viewport dependency graph; authored visible modifiers preserved',
                    modifiers=modifiers, worldMatrix=[list(row) for row in evaluated.matrix_world],
                    worldDeterminant=determinant, mirroredWindingCorrected=determinant < 0,
                    collections=[collection.name for collection in obj.users_collection])
    evaluated.to_mesh_clear()
    assert len(vertices) and len(faces) and np.all(np.isfinite(vertices)), name
    # Side is corroborated by world position, not inferred from suffix alone.
    expected_sign = 1 if name.endswith('.l') else -1
    assert expected_sign * vertices[:, 0].mean() > 0.025, 'Source laterality mismatch: ' + name
    return dict(name=name, vertices=vertices, faces=faces, metadata=metadata)


def read_target(part):
    data = blobs[part['chunk']]
    vertices = np.frombuffer(data, dtype='<f4', count=part['vertexCount'] * 3,
                             offset=part['positions']).reshape(-1, 3).astype(float)
    faces = np.frombuffer(data, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1, 3)
    return vertices, faces


def bvh(vertices, faces):
    return BVHTree.FromPolygons(vertices.tolist(), faces.tolist(), all_triangles=True)


def nearest(tree, points):
    return np.array([list(tree.find_nearest(Vector(point))[0]) for point in points])


def fit_similarity(a, b):
    ac, bc = a.mean(0), b.mean(0)
    aa, bb = a - ac, b - bc
    u, singular, vt = np.linalg.svd(aa.T @ bb)
    proper = np.eye(3)
    proper[-1, -1] = np.linalg.det(u @ vt)
    rotation = u @ proper @ vt
    scale = np.sum(singular * np.diag(proper)) / np.sum(aa ** 2)
    assert scale > 0
    matrix = scale * rotation
    return matrix, bc - ac @ matrix


def sample(vertices, maximum=800):
    return vertices[np.linspace(0, len(vertices) - 1, min(maximum, len(vertices)), dtype=int)]


def stats(distances):
    mm = np.array(distances) * 1000
    return dict(samples=len(mm), rmsMm=float(np.sqrt(np.mean(mm ** 2))),
                meanMm=float(mm.mean()), p95Mm=float(np.percentile(mm, 95)), maxMm=float(mm.max()))


pairs = []
for name, part_id, role in BONES:
    source = read_source(name)
    target, target_faces = read_target(part_by_id[part_id])
    pairs.append(dict(source=source, target=target, targetFaces=target_faces,
                      targetBvh=bvh(target, target_faces), partId=part_id, role=role))
fit_pairs = [pair for pair in pairs if pair['role'] == 'fit']
# Bone centroids initialize a fresh knee/lower-limb fit. No shoulder matrix is read.
a = np.array([pair['source']['vertices'].mean(0) @ AXIS for pair in fit_pairs])
b = np.array([pair['target'].mean(0) for pair in fit_pairs])
delta, translation = fit_similarity(a, b)
matrix = AXIS @ delta
for iteration in range(200):
    source_points, target_points = [], []
    for pair in fit_pairs:
        s = pair['source']['vertices']
        mapped_sample = sample(s) @ matrix + translation
        source_points.append(sample(s))
        target_points.append(nearest(pair['targetBvh'], mapped_sample))
        mapped_tree = bvh(s @ matrix + translation, pair['source']['faces'])
        t = sample(pair['target'])
        inverse_points = (nearest(mapped_tree, t) - translation) @ np.linalg.inv(matrix)
        source_points.append(inverse_points)
        target_points.append(t)
    new_matrix, new_translation = fit_similarity(np.concatenate(source_points), np.concatenate(target_points))
    change = float(np.max(abs(matrix - new_matrix)) + np.max(abs(translation - new_translation)))
    matrix, translation = new_matrix, new_translation
    if iteration % 20 == 0:
        print('KNEE FIT', iteration, change, flush=True)
    if change < 1e-7:
        break
assert np.linalg.det(matrix) > 0, 'Registration unexpectedly mirrors anatomy'

raw = []
for name, slug, code in STRUCTURES:
    for side, side_label in [('l', 'left'), ('r', 'right')]:
        row = read_source(name + '.' + side)
        row.update(slug=slug, code=code, side=side_label)
        raw.append(row)
knee_centers = {side: np.concatenate([r['vertices'] @ matrix + translation for r in raw if r['side'] == side]).mean(0)
                for side in ['left', 'right']}
# Refine specifically around the joint: shaft differences outside the knee must not
# dominate placement of a knee-only extension. The initialization above is retained.
whole_bone_initialization = dict(matrixRowVector=matrix.tolist(), translation=translation.tolist(),
    iterations=iteration + 1, lastTransformDelta=change)
source_centers = {side: np.concatenate([r['vertices'] for r in raw if r['side'] == side]).mean(0)
                  for side in ['left', 'right']}
roi_samples = []
for pair in fit_pairs:
    side = 'left' if pair['source']['name'].endswith('.l') else 'right'
    s, t = pair['source']['vertices'], pair['target']
    source_mask = np.abs(s[:, 2] - source_centers[side][2]) <= .075
    target_mask = np.abs(t[:, 1] - knee_centers[side][1]) <= .075
    assert source_mask.sum() >= 12 and target_mask.sum() >= 12
    roi_samples.append((pair, sample(s[source_mask]), sample(t[target_mask])))
for local_iteration in range(200):
    aa, bb = [], []
    for pair, s, t in roi_samples:
        aa.append(s)
        bb.append(nearest(pair['targetBvh'], s @ matrix + translation))
        mapped_tree = bvh(pair['source']['vertices'] @ matrix + translation, pair['source']['faces'])
        aa.append((nearest(mapped_tree, t) - translation) @ np.linalg.inv(matrix))
        bb.append(t)
    new_matrix, new_translation = fit_similarity(np.concatenate(aa), np.concatenate(bb))
    change = float(np.max(abs(matrix - new_matrix)) + np.max(abs(translation - new_translation)))
    matrix, translation = new_matrix, new_translation
    if local_iteration % 20 == 0:
        print('KNEE LOCAL FIT', local_iteration, change, flush=True)
    if change < 1e-7:
        break
knee_centers = {side: np.concatenate([r['vertices'] @ matrix + translation for r in raw if r['side'] == side]).mean(0)
                for side in ['left', 'right']}
measurements = []
for pair in pairs:
    s = pair['source']['vertices'] @ matrix + translation
    t = pair['target']
    source_tree = bvh(s, pair['source']['faces'])
    d1 = np.linalg.norm(s - nearest(pair['targetBvh'], s), axis=1)
    d2 = np.linalg.norm(t - nearest(source_tree, t), axis=1)
    baseline = pair['source']['vertices'] @ AXIS
    baseline_d = np.linalg.norm(baseline - nearest(pair['targetBvh'], baseline), axis=1)
    # Extra knee-local metric: sampled vertices within 10 cm above/below joint center.
    side = 'left' if pair['source']['name'].endswith('.l') else 'right'
    center_y = knee_centers[side][1]
    sm = np.abs(s[:, 1] - center_y) <= .10
    tm = np.abs(t[:, 1] - center_y) <= .10
    measurements.append(dict(sourceObject=pair['source']['name'], targetPartId=pair['partId'],
        targetConceptId=part_by_id[pair['partId']]['conceptId'], role=pair['role'],
        axisOnlySourceToTarget=stats(baseline_d), registeredBidirectional=stats(np.concatenate([d1, d2])),
        kneeLocalBidirectional=stats(np.concatenate([d1[sm], d2[tm]]))))
column_matrix = np.eye(4)
column_matrix[:3, :3] = matrix.T
column_matrix[:3, 3] = translation
registration = dict(method='Labeled bidirectional nearest-surface similarity ICP; whole-bone initialization followed by knee-local bilateral femur/tibia/fibula fit, bilateral patella held out',
    initialization='Fresh matched bone centroids after axis conversion; no upper-arm transform reused',
    matrixColumnVector=column_matrix.tolist(), uniformScale=float(np.cbrt(np.linalg.det(matrix))),
    iterations=local_iteration + 1, lastTransformDelta=change, converged=change < 1e-7,
    wholeBoneInitialization=whole_bone_initialization,
    fittingRegion='Source and target vertex samples within +/-75 mm vertically of each knee structure center; fixed masks after whole-bone initialization. Nearest points restricted to corresponding labeled bone surfaces.',
    sourceUnits='meters', sourceAxes='X left, Y posterior, Z superior',
    targetUnits='meters', targetAxes='X left, Y superior, Z anterior',
    sourceSceneUnits=dict(system=bpy.context.scene.unit_settings.system, scaleLength=bpy.context.scene.unit_settings.scale_length),
    measurements=measurements,
    metric='All vertices measured against opposite triangles in both directions, vertex-weighted not area-weighted. Knee-local subset is within +/-100 mm vertically of the mean exported knee structure position. Axis baseline is one-way and is not the same symmetric statistic.',
    limitations='Source edits and atlas simplification cause residual shape differences. Bone agreement does not establish ligament insertion or meniscus anatomical accuracy. No deformable fit or structure-specific displacement applied.')

blob = bytearray()
parts, checks, export_arrays = [], [], []


def append(values, dtype):
    while len(blob) % 4:
        blob.append(0)
    offset = len(blob)
    blob.extend(np.asarray(values, dtype=dtype).tobytes())
    return offset


for row in raw:
    positions = (row['vertices'] @ matrix + translation).astype('<f4')
    indices = row['faces'].astype('<u4')
    face_vertices = positions[indices].astype(float)
    face_normals = np.cross(face_vertices[:, 1] - face_vertices[:, 0], face_vertices[:, 2] - face_vertices[:, 0])
    areas = np.linalg.norm(face_normals, axis=1)
    assert np.all(areas > 1e-14), 'Degenerate source triangle in ' + row['name']
    # Angle weights avoid large neighboring faces reversing smooth normals across
    # thin source meniscus/PCL triangles. Positions and topology are unchanged.
    unit_face_normals = face_normals / areas[:, None]
    normals = np.zeros_like(positions, dtype=float)
    for corner in range(3):
        first = face_vertices[:, (corner + 1) % 3] - face_vertices[:, corner]
        second = face_vertices[:, (corner + 2) % 3] - face_vertices[:, corner]
        cosine = np.sum(first * second, axis=1) / (np.linalg.norm(first, axis=1) * np.linalg.norm(second, axis=1))
        angle = np.arccos(np.clip(cosine, -1, 1))
        np.add.at(normals, indices[:, corner], unit_face_normals * angle[:, None])
    lengths = np.linalg.norm(normals, axis=1)
    assert np.all(lengths > 0), 'Unused or zero-normal vertices: ' + row['name']
    normals /= lengths[:, None]
    quantized = np.rint(normals * 32767).astype('<i2')
    assert np.all(np.isfinite(positions)) and indices.max() < len(positions)
    sign = 1 if row['side'] == 'left' else -1
    assert sign * positions[:, 0].mean() > .025
    name = row['side'].title() + ' ' + row['name'].rsplit('.', 1)[0].lower()
    part = dict(id='ZA-KNEE-' + row['code'] + '-' + row['side'][0].upper(),
        conceptId='atlas:' + row['side'] + '-' + row['slug'], name=name, system='connective', chunk=0,
        positions=append(positions, '<f4'), normals=append(quantized, '<i2'), indices=append(indices, '<u4'),
        vertexCount=len(positions), indexCount=int(indices.size),
        bounds=[positions.min(0).tolist(), positions.max(0).tolist()],
        sourceObject=row['name'], sourceObjectType='MESH', sourceGeometry=row['metadata'],
        normalMethod='angle-weighted face normals quantized to signed 16-bit', expertReview='pending')
    parts.append(part)
    export_arrays.append(dict(part=part, positions=positions, indices=indices))
    reconstructed_normals = quantized.astype(float) / 32767
    interpolated = reconstructed_normals[indices].mean(1)
    face_dot = np.sum(interpolated * unit_face_normals, axis=1)
    assert np.all(face_dot > 0), 'Opposing interpolated face normal in ' + row['name']
    checks.append(dict(partId=part['id'], minFaceNormalDot=float(face_dot.min()), minDoubleTriangleArea=float(areas.min()),
                       maxNormalLengthError=float(np.max(abs(np.linalg.norm(reconstructed_normals, axis=1) - 1)))))
binary = bytes(blob)
compressed = gzip.compress(binary, compresslevel=9, mtime=0)
assert gzip.decompress(compressed) == binary
for part in parts:
    v = np.frombuffer(binary, dtype='<f4', count=part['vertexCount'] * 3, offset=part['positions']).reshape(-1, 3)
    idx = np.frombuffer(binary, dtype='<u4', count=part['indexCount'], offset=part['indices'])
    assert idx.max() < len(v) and all(part[key] % 4 == 0 for key in ['positions', 'normals', 'indices'])
    assert [v.min(0).tolist(), v.max(0).tolist()] == part['bounds']
manifest = dict(version='Z-Anatomy knee extension 1', sex='male',
    scope='Bilateral medial/lateral menisci and anterior/posterior cruciate ligaments; regional registration measured, anatomical expert review pending',
    parts=parts, concepts=[dict(id=p['conceptId'], name=p['name'], elements=[p['id']]) for p in parts],
    chunks=[dict(url='/models/extensions/knee-structures.bin', bytes=len(binary),
        gzip='/models/extensions/knee-structures.bin.gz', gzipBytes=len(compressed), sha256=hashlib.sha256(binary).hexdigest())],
    triangles=sum(p['indexCount'] // 3 for p in parts),
    source=dict(id='zanatomy', url='https://github.com/Z-Anatomy/Models-of-human-anatomy',
        archiveUrl='https://raw.githubusercontent.com/Z-Anatomy/Models-of-human-anatomy/master/Z-Anatomy.zip',
        member='Z-Anatomy/Startup.blend', sha256=EXPECTED_BLEND, blenderVersion=bpy.app.version_string,
        license='CC-BY-SA-4.0 (upstream general declaration; preserve upstream exceptions)',
        attribution='/models/extensions/KNEE-ATTRIBUTION.md',
        limitations='Object-specific author/source provenance is not supplied by upstream. No blanket commercial clearance of the archive is asserted.'),
    targetAtlasSha256=EXPECTED_ATLAS, registration=registration)
(OUT / 'knee-structures.bin').write_bytes(binary)
(OUT / 'knee-structures.bin.gz').write_bytes(compressed)
(OUT / 'knee-structures.json').write_text(json.dumps(manifest, indent=2) + '\n')
report = dict(parts=len(parts), vertices=sum(p['vertexCount'] for p in parts), triangles=manifest['triangles'],
              bytes=len(binary), gzipBytes=len(compressed), binarySha256=manifest['chunks'][0]['sha256'],
              registration=registration, sourceInspection=[row['metadata'] for row in raw], checks=checks)
(WORK / 'knee-registration-report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)

if '--render' in sys.argv:
    # Two panels at the same coordinates/scale: source bones + meshes vs target bones + exported binary.
    # Clear the scene only after all source measurements/export. The source file is never saved.
    scene = bpy.data.scenes.new('Knee technical QA')
    bpy.context.window.scene = scene
    scene.world = bpy.data.worlds.new('Knee QA world')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.055, .065, .08, 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .5
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1500
    scene.render.resolution_y = 1100
    scene.render.resolution_percentage = 100
    scene.world.color = (.055, .065, .08)

    def material(name, color, opacity):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nodes = m.node_tree.nodes
        nodes.clear()
        output = nodes.new('ShaderNodeOutputMaterial')
        mix = nodes.new('ShaderNodeMixShader')
        mix.inputs[0].default_value = opacity
        clear = nodes.new('ShaderNodeBsdfTransparent')
        surface = nodes.new('ShaderNodeBsdfPrincipled')
        surface.inputs['Base Color'].default_value = (*color, 1)
        surface.inputs['Roughness'].default_value = .52
        m.node_tree.links.new(clear.outputs[0], mix.inputs[1])
        m.node_tree.links.new(surface.outputs[0], mix.inputs[2])
        m.node_tree.links.new(mix.outputs[0], output.inputs['Surface'])
        return m

    materials = {'bone': material('Knee reference bones', (.78, .84, .88), .13),
                 'MM': material('Medial meniscus', (.1, .75, .85), 1),
                 'LM': material('Lateral meniscus', (.15, .48, .9), 1),
                 'ACL': material('Anterior cruciate ligament', (1, .65, .08), 1),
                 'PCL': material('Posterior cruciate ligament', (.82, .22, .55), 1)}

    def mesh_object(name, positions, indices, material_name, offset):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata((positions + offset).tolist(), [], indices.tolist())
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)
        obj.data.materials.append(materials[material_name])
        for polygon in mesh.polygons:
            polygon.use_smooth = True
        return obj

    # Show the left knee twice. A separate bilateral render below checks both sides.
    for panel, shift in [('source', -.09), ('target', .09)]:
        offset = np.array([shift - knee_centers['left'][0], 0., 0.])
        for pair in pairs:
            if not pair['source']['name'].endswith('.l'):
                continue
            v = pair['source']['vertices'] @ matrix + translation if panel == 'source' else pair['target']
            f = pair['source']['faces'] if panel == 'source' else pair['targetFaces']
            # Crop long bone triangles for an unobstructed, similarly framed knee comparison.
            mask = np.all(np.abs(v[f][:, :, 1] - knee_centers['left'][1]) <= .115, axis=1)
            mesh_object(panel + '-' + pair['source']['name'], v, f[mask], 'bone', offset)
        for row, exported in zip(raw, export_arrays):
            if row['side'] != 'left':
                continue
            if panel == 'source':
                v, f = row['vertices'] @ matrix + translation, row['faces']
            else:
                # Reload the written buffer; the image also checks the encoded geometry.
                part = exported['part']
                v = np.frombuffer(binary, dtype='<f4', count=part['vertexCount'] * 3, offset=part['positions']).reshape(-1, 3)
                f = np.frombuffer(binary, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1, 3)
            mesh_object(panel + '-' + row['name'], v, f, row['code'], offset)
    light = bpy.data.lights.new('Knee key', 'AREA')
    light.energy, light.size = 140, 1.2
    obj = bpy.data.objects.new('Knee key', light)
    scene.collection.objects.link(obj)
    center = Vector((0, float(knee_centers['left'][1]), float(knee_centers['left'][2])))
    obj.location = center + Vector((.3, .45, .75))
    obj.rotation_euler = (center - obj.location).to_track_quat('-Z', 'Y').to_euler()
    camera = bpy.data.cameras.new('Knee comparison')
    camera.type, camera.ortho_scale = 'ORTHO', .39
    obj = bpy.data.objects.new('Knee comparison', camera)
    scene.collection.objects.link(obj)
    scene.camera = obj
    for name, direction in [('front', (0, .09, 1)), ('oblique', (.30, .18, 1))]:
        obj.location = center + Vector(direction)
        back = (obj.location - center).normalized()
        right = Vector((0, 1, 0)).cross(back).normalized()
        up = back.cross(right)
        obj.rotation_euler = Matrix((right, up, back)).transposed().to_euler()
        scene.render.filepath = str(WORK / ('knee-source-target-' + name + '.png'))
        bpy.ops.render.render(write_still=True)

    # Keep the camera and light; replace the comparison panels with both exported knees.
    for item in list(scene.objects):
        if item.type == 'MESH':
            item.hide_render = True
    for pair in pairs:
        side = 'left' if pair['source']['name'].endswith('.l') else 'right'
        v, f = pair['target'], pair['targetFaces']
        mask = np.all(np.abs(v[f][:, :, 1] - knee_centers[side][1]) <= .115, axis=1)
        mesh_object('bilateral-' + pair['source']['name'], v, f[mask], 'bone', np.zeros(3))
    for row, exported in zip(raw, export_arrays):
        mesh_object('bilateral-' + row['name'], exported['positions'], exported['indices'], row['code'], np.zeros(3))
    center = Vector(np.mean(list(knee_centers.values()), axis=0))
    camera.ortho_scale = .34
    obj.location = center + Vector((.05, .16, 1))
    back = (obj.location - center).normalized()
    right = Vector((0, 1, 0)).cross(back).normalized()
    up = back.cross(right)
    obj.rotation_euler = Matrix((right, up, back)).transposed().to_euler()
    scene.render.filepath = str(WORK / 'knee-registered-bilateral.png')
    bpy.ops.render.render(write_still=True)
