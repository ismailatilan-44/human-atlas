"""Export two source sciatic nerve curves after an independent hip/thigh registration.

Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
  --python scripts/export-sciatic-nerves.py -- --render

Preserves all three authored splines per nerve, their radii, and open tube ends.
Does not modify source blend, main atlas, shared attribution, app, or graph files.
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
REFERENCES = [
    ('Hip bone.l', 'FJ3288', 'fit'), ('Hip bone.r', 'FJ3152', 'fit'),
    ('Sacrum', 'FJ3393', 'fit'),
    ('Femur.l', 'FJ3259', 'fit'), ('Femur.r', 'FJ3365', 'fit'),
    ('Piriformis muscle.l', 'FJ1428M', 'holdout'), ('Piriformis muscle.r', 'FJ1428', 'holdout'),
    ('Gluteus maximus muscle.l', 'FJ1418M', 'holdout'), ('Gluteus maximus muscle.r', 'FJ1418', 'holdout'),
    ('Long head of biceps femoris.l', 'FJ1395M', 'holdout'), ('Long head of biceps femoris.r', 'FJ1395', 'holdout'),
    ('Semitendinosus muscle.l', 'FJ1436M', 'holdout'), ('Semitendinosus muscle.r', 'FJ1436', 'holdout'),
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
    assert obj.type in {'MESH', 'CURVE'}, name
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
                    baseVertices=len(obj.data.vertices) if obj.type == 'MESH' else None,
                    basePolygons=len(obj.data.polygons) if obj.type == 'MESH' else None,
                    evaluatedVertices=len(vertices), evaluatedTriangles=len(faces),
                    evaluation='evaluated viewport dependency graph; authored visible modifiers preserved',
                    modifiers=modifiers, worldMatrix=[list(row) for row in evaluated.matrix_world],
                    worldDeterminant=determinant, mirroredWindingCorrected=determinant < 0,
                    collections=[collection.name for collection in obj.users_collection])
    evaluated.to_mesh_clear()
    assert len(vertices) and len(faces) and np.all(np.isfinite(vertices)), name
    # Side is corroborated by world position, not inferred from suffix alone.
    if name.endswith(('.l', '.r')):
        expected_sign = 1 if name.endswith('.l') else -1
        assert expected_sign * vertices[:, 0].mean() > 0.015, 'Source laterality mismatch: ' + name
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


def control_points(obj, spline):
    points = spline.bezier_points if spline.type == 'BEZIER' else spline.points
    return np.array([list(obj.matrix_world @ p.co.to_3d()) for p in points]), [float(p.radius) for p in points]


raw = [read_source('Sciatic nerve.' + side) for side in ['l', 'r']]
for row in raw:
    obj = bpy.data.objects[row['name']]
    row['metadata']['curveSettings'] = {key: getattr(obj.data, key) for key in ['bevel_depth', 'bevel_resolution', 'resolution_u', 'use_fill_caps']}
    row['splines'] = []
    for index, spline in enumerate(obj.data.splines):
        points, radii = control_points(obj, spline)
        row['splines'].append(dict(index=index, type=spline.type, cyclic=spline.use_cyclic_u,
            controlPointCount=len(points), sourceWorldControlPoints=points.tolist(), pointRadii=radii))
    assert len(row['splines']) == 3 and sum(s['controlPointCount'] for s in row['splines']) == 20

pairs = []
for name, part_id, role in REFERENCES:
    source = read_source(name)
    target, target_faces = read_target(part_by_id[part_id])
    pairs.append(dict(source=source, target=target, targetFaces=target_faces,
                      targetBvh=bvh(target, target_faces), partId=part_id, role=role))
fit_pairs = [pair for pair in pairs if pair['role'] == 'fit']
# A fresh, full hip/thigh registration. No existing extension transform is read.
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
        source_points.append((nearest(mapped_tree, t) - translation) @ np.linalg.inv(matrix))
        target_points.append(t)
    new_matrix, new_translation = fit_similarity(np.concatenate(source_points), np.concatenate(target_points))
    change = float(np.max(abs(matrix - new_matrix)) + np.max(abs(translation - new_translation)))
    matrix, translation = new_matrix, new_translation
    if iteration % 20 == 0:
        print('SCIATIC FULL COURSE FIT', iteration, change, flush=True)
    if change < 1e-7:
        break
assert np.linalg.det(matrix) > 0, 'Registration unexpectedly mirrors anatomy'
course = np.concatenate([r['vertices'] @ matrix + translation for r in raw])
course_min, course_max = float(course[:, 1].min()), float(course[:, 1].max())
measurements = []
for pair in pairs:
    s = pair['source']['vertices'] @ matrix + translation
    t = pair['target']
    source_tree = bvh(s, pair['source']['faces'])
    d1 = np.linalg.norm(s - nearest(pair['targetBvh'], s), axis=1)
    d2 = np.linalg.norm(t - nearest(source_tree, t), axis=1)
    baseline = pair['source']['vertices'] @ AXIS
    baseline_d = np.linalg.norm(baseline - nearest(pair['targetBvh'], baseline), axis=1)
    sm = (s[:, 1] >= course_min - .02) & (s[:, 1] <= course_max + .02)
    tm = (t[:, 1] >= course_min - .02) & (t[:, 1] <= course_max + .02)
    measurements.append(dict(sourceObject=pair['source']['name'], targetPartId=pair['partId'],
        targetConceptId=part_by_id[pair['partId']]['conceptId'], role=pair['role'],
        axisOnlySourceToTarget=stats(baseline_d), registeredBidirectional=stats(np.concatenate([d1, d2])),
        nerveExtentBidirectional=stats(np.concatenate([d1[sm], d2[tm]]))))
column_matrix = np.eye(4)
column_matrix[:3, :3] = matrix.T
column_matrix[:3, 3] = translation
registration = dict(method='Fresh labeled bidirectional nearest-surface similarity ICP using complete bilateral hip bones/femora and sacrum; eight nearby muscle meshes held out',
    initialization='Matched bone centroids after axis conversion; no upper-arm or knee transform reused',
    matrixColumnVector=column_matrix.tolist(), uniformScale=float(np.cbrt(np.linalg.det(matrix))),
    iterations=iteration + 1, lastTransformDelta=change, converged=change < 1e-7,
    sourceUnits='meters', sourceAxes='X left, Y posterior, Z superior',
    targetUnits='meters', targetAxes='X left, Y superior, Z anterior',
    sourceSceneUnits=dict(system=bpy.context.scene.unit_settings.system, scaleLength=bpy.context.scene.unit_settings.scale_length),
    measurements=measurements,
    metric='All vertices measured against opposite triangles in both directions, vertex-weighted not area-weighted. Additional nerve-extent metric spans the exported nerve vertical bounds +/-20 mm; it does not drive the fit. Axis baseline is one-way, not the symmetric registered statistic.',
    limitations='Reference agreement is coordinate evidence, not validation of sciatic branch identities, root levels or anatomical path. No source path edits, piecewise transform, local warping or per-structure displacement.')

blob = bytearray()
parts, checks, export_arrays, extents = [], [], [], []


def append(values, dtype):
    while len(blob) % 4:
        blob.append(0)
    offset = len(blob)
    blob.extend(np.asarray(values, dtype=dtype).tobytes())
    return offset


for row in raw:
    side = 'left' if row['name'].endswith('.l') else 'right'
    positions = (row['vertices'] @ matrix + translation).astype('<f4')
    indices = row['faces'].astype('<u4')
    vertices = positions[indices].astype(float)
    face_normals = np.cross(vertices[:, 1] - vertices[:, 0], vertices[:, 2] - vertices[:, 0])
    double_areas = np.linalg.norm(face_normals, axis=1)
    assert np.all(double_areas > 1e-14), 'Degenerate source triangle in ' + row['name']
    unit_faces = face_normals / double_areas[:, None]
    normals = np.zeros_like(positions, dtype=float)
    for corner in range(3):
        first = vertices[:, (corner + 1) % 3] - vertices[:, corner]
        second = vertices[:, (corner + 2) % 3] - vertices[:, corner]
        cosine = np.sum(first * second, axis=1) / (np.linalg.norm(first, axis=1) * np.linalg.norm(second, axis=1))
        angles = np.arccos(np.clip(cosine, -1, 1))
        np.add.at(normals, indices[:, corner], unit_faces * angles[:, None])
    lengths = np.linalg.norm(normals, axis=1)
    assert np.all(lengths > 0)
    normals /= lengths[:, None]
    quantized = np.rint(normals * 32767).astype('<i2')
    reconstructed = quantized.astype(float) / 32767
    dot = np.sum(reconstructed[indices].mean(1) * unit_faces, axis=1)
    assert np.all(dot > 0), 'Opposing interpolated face normal in ' + row['name']
    assert np.all(np.isfinite(positions)) and indices.max() < len(positions)
    sign = 1 if side == 'left' else -1
    assert np.all(sign * positions[:, 0] > 0), 'Nerve crosses midline after registration'
    part = dict(id='ZA-SCI-' + side[0].upper(), conceptId='atlas:' + side + '-sciatic-nerve',
        name=side.title() + ' sciatic nerve', system='nervous', chunk=0,
        positions=append(positions, '<f4'), normals=append(quantized, '<i2'), indices=append(indices, '<u4'),
        vertexCount=len(positions), indexCount=int(indices.size),
        bounds=[positions.min(0).tolist(), positions.max(0).tolist()],
        sourceObject=row['name'], sourceObjectType='CURVE', sourceGeometry=row['metadata'],
        normalMethod='angle-weighted face normals quantized to signed 16-bit', expertReview='pending')
    parts.append(part)
    export_arrays.append(dict(part=part, positions=positions, indices=indices))
    for spline in row['splines']:
        mapped = np.array(spline['sourceWorldControlPoints']) @ matrix + translation
        spline['atlasControlPoints'] = mapped.tolist()
        spline['atlasEndpoints'] = [mapped[0].tolist(), mapped[-1].tolist()]
    main_end = np.array(row['splines'][0]['sourceWorldControlPoints'][-1])
    omitted = []
    for base in ['Tibial nerve', 'Common fibular nerve']:
        obj = bpy.data.objects[base + '.' + side[0]]
        points, _ = control_points(obj, obj.data.splines[0])
        endpoint_distances = np.linalg.norm(points[[0, -1]] - main_end, axis=1) * 1000
        omitted.append(dict(sourceObject=obj.name, objectType=obj.type, exported=False,
            sourceEndpointDistancesFromMainSciaticDistalMm=endpoint_distances.tolist(),
            nearestSourceEndpointDistanceMm=float(endpoint_distances.min())))
    extents.append(dict(partId=part['id'], sourceObject=row['name'], splines=row['splines'],
        atlasVerticalBoundsMeters=[float(positions[:, 1].min()), float(positions[:, 1].max())],
        omittedSeparateObjects=omitted,
        limitations='All three splines of this source object are preserved; individual proximal spline root/branch identities are not inferred. Separate tibial/common-fibular nerve objects and their distal branches are not exported. No claim of the complete lumbosacral plexus or nerve arborization.'))
    checks.append(dict(partId=part['id'], minDoubleTriangleArea=float(double_areas.min()), minFaceNormalDot=float(dot.min()),
                       maxNormalLengthError=float(np.max(abs(np.linalg.norm(reconstructed, axis=1) - 1)))))
binary = bytes(blob)
compressed = gzip.compress(binary, compresslevel=9, mtime=0)
assert gzip.decompress(compressed) == binary
for part in parts:
    v = np.frombuffer(binary, dtype='<f4', count=part['vertexCount'] * 3, offset=part['positions']).reshape(-1, 3)
    f = np.frombuffer(binary, dtype='<u4', count=part['indexCount'], offset=part['indices'])
    assert np.all(np.isfinite(v)) and f.max() < len(v)
    assert [v.min(0).tolist(), v.max(0).tolist()] == part['bounds']
    assert all(part[key] % 4 == 0 for key in ['positions', 'normals', 'indices'])
manifest = dict(version='Z-Anatomy sciatic extension 1', sex='male',
    scope='Two sciatic nerve source curves from pelvic region through posterior thigh; all three splines per side preserved, separate tibial/common-fibular continuations omitted; expert anatomical review pending',
    parts=parts, concepts=[dict(id=p['conceptId'], name=p['name'], elements=[p['id']]) for p in parts],
    chunks=[dict(url='/models/extensions/sciatic-nerves.bin', bytes=len(binary),
        gzip='/models/extensions/sciatic-nerves.bin.gz', gzipBytes=len(compressed), sha256=hashlib.sha256(binary).hexdigest())],
    triangles=sum(p['indexCount'] // 3 for p in parts),
    source=dict(id='zanatomy', url='https://github.com/Z-Anatomy/Models-of-human-anatomy',
        archiveUrl='https://raw.githubusercontent.com/Z-Anatomy/Models-of-human-anatomy/master/Z-Anatomy.zip',
        member='Z-Anatomy/Startup.blend', sha256=EXPECTED_BLEND, blenderVersion=bpy.app.version_string,
        license='CC-BY-SA-4.0 (upstream general declaration; preserve upstream exceptions)',
        attribution='/models/extensions/SCIATIC-ATTRIBUTION.md',
        limitations='Object-specific author/source provenance is not supplied by upstream; no blanket commercial clearance of the archive is asserted.'),
    targetAtlasSha256=EXPECTED_ATLAS, registration=registration, sourceExtent=extents,
    existingAtlasContext=dict(namedSciaticParts=[p['id'] for p in atlas['parts'] if 'sciatic' in p['name'].lower()],
        nervousPartsBelow105cm=[p['id'] for p in atlas['parts'] if p['system'] == 'nervous' and p['bounds'][0][1] < 1.05],
        scope='Name/system and bounds audit of main atlas only; does not assert anatomical absence inside other surfaces.'))
(OUT / 'sciatic-nerves.bin').write_bytes(binary)
(OUT / 'sciatic-nerves.bin.gz').write_bytes(compressed)
(OUT / 'sciatic-nerves.json').write_text(json.dumps(manifest, indent=2) + '\n')
report = dict(parts=len(parts), vertices=sum(p['vertexCount'] for p in parts), triangles=manifest['triangles'],
              bytes=len(binary), gzipBytes=len(compressed), binarySha256=manifest['chunks'][0]['sha256'],
              registration=registration, sourceExtent=extents, checks=checks)
(WORK / 'sciatic-registration-report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)

if '--render' in sys.argv:
    # Independent QA scene avoids source compositor/render settings.
    scene = bpy.data.scenes.new('Sciatic technical QA')
    bpy.context.window.scene = scene
    scene.world = bpy.data.worlds.new('Sciatic QA world')
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes['Background']
    background.inputs['Color'].default_value = (.055, .065, .08, 1)
    background.inputs['Strength'].default_value = .5
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.cycles.transparent_max_bounces = 32
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1200
    scene.render.resolution_percentage = 100

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
        surface.inputs['Roughness'].default_value = .55
        m.node_tree.links.new(clear.outputs[0], mix.inputs[1])
        m.node_tree.links.new(surface.outputs[0], mix.inputs[2])
        m.node_tree.links.new(mix.outputs[0], output.inputs['Surface'])
        return m

    materials = {'bone': material('Sciatic reference bones', (.76, .84, .87), .13),
                 'muscle': material('Sciatic nearby muscle', (.5, .23, .22), .075),
                 'nerve': material('Sciatic source nerve', (1, .67, .10), 1)}

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

    # Posterior camera: positive world X is on the left of the rendered frame.
    for panel, shift in [('source', .22), ('target', -.22)]:
        offset = np.array([shift, 0., 0.])
        for pair in pairs:
            v = pair['source']['vertices'] @ matrix + translation if panel == 'source' else pair['target']
            f = pair['source']['faces'] if panel == 'source' else pair['targetFaces']
            kind = 'bone' if pair['role'] == 'fit' else 'muscle'
            mesh_object(panel + '-' + pair['source']['name'], v, f, kind, offset)
        for row, exported in zip(raw, export_arrays):
            if panel == 'source':
                v, f = row['vertices'] @ matrix + translation, row['faces']
            else:
                part = exported['part']
                v = np.frombuffer(binary, dtype='<f4', count=part['vertexCount'] * 3, offset=part['positions']).reshape(-1, 3)
                f = np.frombuffer(binary, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1, 3)
            mesh_object(panel + '-' + row['name'], v, f, 'nerve', offset)
    center = Vector((0, .74, -.04))
    light = bpy.data.lights.new('Sciatic key', 'AREA')
    light.energy, light.size = 180, 1.5
    light_object = bpy.data.objects.new('Sciatic key', light)
    scene.collection.objects.link(light_object)
    light_object.location = center + Vector((.25, .45, -.85))
    light_object.rotation_euler = (center - light_object.location).to_track_quat('-Z', 'Y').to_euler()
    camera = bpy.data.cameras.new('Sciatic comparison')
    camera.type, camera.ortho_scale = 'ORTHO', .95
    camera_object = bpy.data.objects.new('Sciatic comparison', camera)
    scene.collection.objects.link(camera_object)
    scene.camera = camera_object

    def view(direction, filename):
        camera_object.location = center + Vector(direction)
        back = (camera_object.location - center).normalized()
        right = Vector((0, 1, 0)).cross(back).normalized()
        up = back.cross(right)
        camera_object.rotation_euler = Matrix((right, up, back)).transposed().to_euler()
        scene.render.filepath = str(WORK / filename)
        bpy.ops.render.render(write_still=True)

    view((0, .05, -1), 'sciatic-source-target-posterior.png')
    view((.22, .08, -1), 'sciatic-source-target-oblique.png')
    # A closer view of both encoded nerves and target references only.
    for item in list(scene.objects):
        if item.type == 'MESH':
            item.hide_render = True
    for pair in pairs:
        kind = 'bone' if pair['role'] == 'fit' else 'muscle'
        mesh_object('bilateral-' + pair['source']['name'], pair['target'], pair['targetFaces'], kind, np.zeros(3))
    for exported in export_arrays:
        mesh_object('bilateral-' + exported['part']['id'], exported['positions'], exported['indices'], 'nerve', np.zeros(3))
    camera.ortho_scale = .69
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 1500
    view((.15, .03, -1), 'sciatic-registered-bilateral.png')
