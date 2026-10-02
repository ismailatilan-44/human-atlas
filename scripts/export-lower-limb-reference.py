"""Package 21 same-source lower-limb objects, with no atlas fitting.

Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
  --python scripts/export-lower-limb-reference.py -- --render

Writes only this package and its evidence. Never imports/runs legacy exporters.
"""
import bpy
import gzip
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'data/model-candidates/lower-limb-nerve-reference'
OUT = ROOT / 'public/models/lower-limb-nerve-reference'
EXPECTED_BLEND = '9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
AXIS = np.array([[1., 0., 0.], [0., 0., -1.], [0., 1., 0.]])
DATASET = 'lower-limb-nerve-reference'
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == EXPECTED_BLEND
assert np.array_equal(AXIS.T @ AXIS, np.eye(3)) and np.linalg.det(AXIS) == 1
OUT.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)
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
    metadata = dict(name=name, dataBlock=obj.data.name, materials=[m.name for m in obj.data.materials if m],
        sourceWorldBounds=[vertices.min(0).tolist(), vertices.max(0).tolist()], objectType=obj.type,
        parent=obj.parent.name if obj.parent else None,
        baseVertices=len(obj.data.vertices) if obj.type == 'MESH' else None,
        basePolygons=len(obj.data.polygons) if obj.type == 'MESH' else None,
        evaluatedVertices=len(vertices), evaluatedTriangles=len(faces),
        evaluation='evaluated viewport dependency graph; authored visible modifiers preserved',
        modifiers=[dict(name=m.name, type=m.type, showViewport=m.show_viewport, showRender=m.show_render,
            levels=getattr(m, 'levels', None), renderLevels=getattr(m, 'render_levels', None)) for m in obj.modifiers],
        worldMatrix=[list(row) for row in evaluated.matrix_world], worldDeterminant=determinant,
        mirroredWindingCorrected=determinant < 0, collections=[c.name for c in obj.users_collection])
    evaluated.to_mesh_clear()
    assert len(vertices) and len(faces) and np.all(np.isfinite(vertices)), name
    if name.endswith(('.l', '.r')):
        assert (1 if name.endswith('.l') else -1) * vertices[:, 0].mean() > .015, name
    splines = []
    if obj.type == 'CURVE':
        metadata['curveSettings'] = {k: getattr(obj.data, k) for k in ['bevel_depth', 'bevel_resolution', 'resolution_u', 'use_fill_caps']}
        for index, spline in enumerate(obj.data.splines):
            points = spline.bezier_points if spline.type == 'BEZIER' else spline.points
            world = np.array([list(obj.matrix_world @ p.co.to_3d()) for p in points])
            reference = world @ AXIS
            splines.append(dict(index=index, type=spline.type, cyclic=spline.use_cyclic_u,
                controlPointCount=len(points), sourceWorldControlPoints=world.tolist(),
                referenceControlPoints=reference.tolist(), referenceEndpoints=[reference[0].tolist(), reference[-1].tolist()],
                pointRadii=[float(p.radius) for p in points],
                sourceWorldHandlesLeft=[list(obj.matrix_world @ p.handle_left) for p in spline.bezier_points],
                sourceWorldHandlesRight=[list(obj.matrix_world @ p.handle_right) for p in spline.bezier_points],
                handleTypes=[[p.handle_left_type, p.handle_right_type] for p in spline.bezier_points]))
        assert splines and not obj.data.use_fill_caps
    return dict(name=name, vertices=vertices, faces=faces, metadata=metadata, splines=splines)


specs = []
for name, slug, code in [('Tibial nerve', 'tibial-nerve', 'TIB'), ('Common fibular nerve', 'common-fibular-nerve', 'CFIB'), ('Sciatic nerve', 'sciatic-nerve', 'SCI')]:
    for suffix, side in [('l', 'left'), ('r', 'right')]:
        specs.append((name + '.' + suffix, 'ZA-' + code + '-' + suffix.upper(), 'atlas:' + side + '-' + slug, 'nerve', side, side.title() + ' ' + name.lower()))
for name in ['Tibia', 'Fibula', 'Patella', 'Talus', 'Calcaneus', 'Femur', 'Hip bone']:
    for suffix, side in [('l', 'left'), ('r', 'right')]:
        code = 'ZA-LLR-' + ('HIP' if name == 'Hip bone' else name.upper()) if name in ['Femur', 'Hip bone'] else 'ZA-DLN-' + name.upper()
        specs.append((name + '.' + suffix, code + '-' + suffix.upper(), 'zanatomy:' + name.lower().replace(' ', '-') + '-' + suffix, 'bone', side, side.title() + ' ' + name.lower()))
specs.append(('Sacrum', 'ZA-LLR-SACRUM', 'zanatomy:sacrum', 'bone', 'midline', 'Sacrum'))
assert len(specs) == 21
raw = [read_source(spec[0]) for spec in specs]
blob = bytearray()
parts, checks, extents = [], [], []


def append(values, dtype):
    while len(blob) % 4:
        blob.append(0)
    offset = len(blob)
    blob.extend(np.asarray(values, dtype=dtype).tobytes())
    return offset


for row, (_, part_id, concept_id, role, side, name) in zip(raw, specs):
    reference = row['vertices'] @ AXIS
    positions = reference.astype('<f4')
    indices = row['faces'].astype('<u4')
    triangles = positions[indices].astype(float)
    cross = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    area2 = np.linalg.norm(cross, axis=1)
    assert np.all(area2 > 1e-14), row['name']
    unit = cross / area2[:, None]
    normals = np.zeros_like(positions, dtype=float)
    for corner in range(3):
        a = triangles[:, (corner + 1) % 3] - triangles[:, corner]
        b = triangles[:, (corner + 2) % 3] - triangles[:, corner]
        angle = np.arccos(np.clip(np.sum(a*b, axis=1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1)), -1, 1))
        np.add.at(normals, indices[:, corner], unit * angle[:, None])
    lengths = np.linalg.norm(normals, axis=1)
    used = np.zeros(len(positions), dtype=bool)
    used[np.unique(indices)] = True
    loose = ~used
    cancelled = used & (lengths == 0)
    if role == 'nerve':
        assert not np.any(cancelled), row['name']
    # Preserve inherited bone faces; cancellation is recorded, not silently repaired.
    for vertex in np.flatnonzero(cancelled):
        incident = np.flatnonzero(np.any(indices == vertex, axis=1))
        normals[vertex] = unit[incident[np.argmax(area2[incident])]]
        lengths[vertex] = 1
    normals[loose] = [0, 1, 0]
    lengths[loose] = 1
    normals /= lengths[:, None]
    quantized = np.rint(normals * 32767).astype('<i2')
    reconstructed = quantized.astype(float) / 32767
    dots = np.sum(reconstructed[indices].mean(1) * unit, axis=1)
    edges = np.sort(np.concatenate([indices[:, [0, 1]], indices[:, [1, 2]], indices[:, [2, 0]]]), axis=1)
    _, edge_counts = np.unique(edges, axis=0, return_counts=True)
    if role == 'nerve':
        assert np.all(dots > 0) and not np.any(edge_counts > 2), row['name']
        assert int(np.sum(edge_counts == 1)) == 24 * len(row['splines']), row['name']
    part = dict(id=part_id, datasetId=DATASET, conceptId=concept_id, name=name, side=side,
        system='nervous' if role == 'nerve' else 'skeletal', componentRole=role,
        role='primary' if role == 'nerve' else 'context', chunk=0,
        positions=append(positions, '<f4'), normals=append(quantized, '<i2'), indices=append(indices, '<u4'),
        vertexCount=len(positions), indexCount=int(indices.size), bounds=[positions.min(0).tolist(), positions.max(0).tolist()],
        sourceObject=row['name'], sourceObjectType=row['metadata']['objectType'], sourceGeometry=row['metadata'],
        normalMethod='angle-weighted face normals quantized to signed 16-bit', looseVertices=int(np.sum(loose)), cancelledVertexNormals=int(np.sum(cancelled)),
        cancelledVertexNormalFallback='Largest incident face normal for source bone vertices whose angle-weighted normals cancel; faces and positions unchanged',
        looseVertexNormal='Default up normal only for source vertices unused by triangles; positions preserved', expertReview='pending')
    parts.append(part)
    checks.append(dict(partId=part_id, nonpositiveInterpolatedFaceNormals=int(np.sum(dots <= 0)), looseVertices=int(np.sum(loose)), cancelledVertexNormals=int(np.sum(cancelled)),
        boundaryEdges=int(np.sum(edge_counts == 1)), nonManifoldEdges=int(np.sum(edge_counts > 2)),
        minDoubleTriangleArea=float(area2.min()), minFaceNormalDot=float(dots.min()),
        maxFloat32PositionErrorMeters=float(np.max(np.abs(reference - positions))),
        maxNormalLengthError=float(np.max(abs(np.linalg.norm(reconstructed, axis=1) - 1)))))
    if role == 'nerve':
        extents.append(dict(partId=part_id, sourceObject=row['name'], splines=row['splines'],
            referenceVerticalBoundsMeters=[float(positions[:, 1].min()), float(positions[:, 1].max())],
            limitations='Complete named source curve, not complete regional innervation. Sciatic short splines have no independently verified root/branch identities; separate distal branch objects excluded.'))

binary = bytes(blob)
compressed = gzip.compress(binary, compresslevel=9, mtime=0)
assert gzip.decompress(compressed) == binary
for part, row in zip(parts, raw):
    v = np.frombuffer(binary, dtype='<f4', count=part['vertexCount']*3, offset=part['positions']).reshape(-1, 3)
    n = np.frombuffer(binary, dtype='<i2', count=part['vertexCount']*3, offset=part['normals']).reshape(-1, 3)
    f = np.frombuffer(binary, dtype='<u4', count=part['indexCount'], offset=part['indices'])
    assert np.all(np.isfinite(v)) and f.max() < len(v)
    assert np.array_equal(v, (row['vertices'] @ AXIS).astype('<f4'))
    assert np.array_equal(f.reshape(-1, 3), row['faces'])
    assert np.max(abs(np.linalg.norm(n.astype(float)/32767, axis=1) - 1)) < .00003
    assert [v.min(0).tolist(), v.max(0).tolist()] == part['bounds']
    assert all(part[k] % 4 == 0 for k in ['positions', 'normals', 'indices'])

# Retain precise same-source junction evidence without manufacturing connecting faces.
junctions = []
for side in ['left', 'right']:
    sciatic = next(e for e in extents if e['partId'] == 'ZA-SCI-' + side[0].upper())
    endpoint = np.array(sciatic['splines'][0]['referenceEndpoints'][-1])
    for code in ['TIB', 'CFIB']:
        distal = next(e for e in extents if e['partId'] == 'ZA-' + code + '-' + side[0].upper())
        distances = np.linalg.norm(np.array(distal['splines'][0]['referenceEndpoints']) - endpoint, axis=1)
        junctions.append(dict(sciaticPartId=sciatic['partId'], distalPartId=distal['partId'],
            endpointDistancesMeters=distances.tolist(), nearestEndpointDistanceMeters=float(distances.min()),
            meaning='Authored source endpoint proximity only; no anatomical precision or branch identity approval.'))

manifest = dict(schemaVersion=1, version='Z-Anatomy independent lower-limb nerve reference 1', datasetId=DATASET,
    status='independent_source_reference', releaseStatus='packaged-reference-expert-review-pending', sex='male',
    compatibleWithMainAtlas=False, atlasRegistration=None,
    scope='Six authored sciatic, tibial and common fibular nerve curves with fifteen same-source bone surfaces. Separate distal branches, roots and full lower-limb innervation excluded. Anatomical expert review pending.',
    coordinates=dict(units='meters', axes='X left, Y superior, Z anterior', sourceAxes='X left, Y posterior, Z superior',
        displayRotationColumnVector=[[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]],
        sourceSceneUnits=dict(system=bpy.context.scene.unit_settings.system, scaleLength=bpy.context.scene.unit_settings.scale_length),
        sourceWorldCoordinatesPreservedBy='One common orthonormal display-axis rotation only; no scaling, translation or fitting'),
    parts=parts, concepts=[dict(id=p['conceptId'], name=p['name'], elements=[p['id']]) for p in parts],
    chunks=[dict(url='/models/' + DATASET + '/anatomy.bin', bytes=len(binary),
        gzip='/models/' + DATASET + '/anatomy.bin.gz', gzipBytes=len(compressed), sha256=hashlib.sha256(binary).hexdigest())],
    triangles=sum(p['indexCount']//3 for p in parts),
    source=dict(id='zanatomy', url='https://github.com/Z-Anatomy/Models-of-human-anatomy',
        archiveUrl='https://raw.githubusercontent.com/Z-Anatomy/Models-of-human-anatomy/master/Z-Anatomy.zip',
        member='Z-Anatomy/Startup.blend', sha256=EXPECTED_BLEND, blenderVersion=bpy.app.version_string,
        license='CC-BY-SA-4.0 (upstream general declaration; preserve underlying-model notices and upstream exceptions)',
        attribution='/models/' + DATASET + '/ATTRIBUTION.md',
        limitations='Object-specific author/source lineage is not supplied by upstream; no blanket commercial clearance of the archive is asserted.'),
    sourceExtent=extents, sourceJunctions=junctions,
    inheritedMeshDefects=[c for c in checks if c['nonpositiveInterpolatedFaceNormals'] or c['looseVertices'] or c['nonManifoldEdges'] or c['cancelledVertexNormals']],
    anatomicalExpertReview='pending', priorRejectedMainFrameAudit='docs/model/asset-registration-distal-leg-nerves.md')
(OUT / 'anatomy.bin').write_bytes(binary)
(OUT / 'anatomy.bin.gz').write_bytes(compressed)
(OUT / 'atlas.json').write_text(json.dumps(manifest, indent=2) + '\n')
report = dict(parts=len(parts), nerves=6, bones=15, vertices=sum(p['vertexCount'] for p in parts), triangles=manifest['triangles'],
    bytes=len(binary), gzipBytes=len(compressed), binarySha256=hashlib.sha256(binary).hexdigest(),
    gzipSha256=hashlib.sha256(compressed).hexdigest(), sourceSha256=EXPECTED_BLEND,
    manifestSha256=hashlib.sha256((OUT / 'atlas.json').read_bytes()).hexdigest(),
    checks=checks, sourceJunctions=junctions,
    validation='Finite decoded coordinates, bounds, index ranges, normal lengths, aligned offsets, gzip roundtrip; original evaluated source indices and world coordinates retained under one rotation.')
(WORK / 'geometry-checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['checks', 'sourceJunctions']}, indent=2), flush=True)

if '--render' in sys.argv:
    scene = bpy.data.scenes.new('Lower-limb independent reference QA')
    bpy.context.window.scene = scene
    scene.world = bpy.data.worlds.new('Lower-limb QA world')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.055, .065, .08, 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .5
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 16
    scene.cycles.use_denoising = True
    scene.cycles.transparent_max_bounces = 32
    scene.render.resolution_x, scene.render.resolution_y = 1600, 1600
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

    materials = {'bone': material('Reference bones', (.76, .84, .87), .16),
                 'nerve': material('Source nerve', (1, .67, .10), 1)}
    render_objects = []
    for panel, shift in [('source', -.29), ('decoded', .29)]:
        for row, part in zip(raw, parts):
            if panel == 'source':
                v, f = row['vertices'] @ AXIS, row['faces']
            else:
                v = np.frombuffer(binary, dtype='<f4', count=part['vertexCount']*3, offset=part['positions']).reshape(-1, 3)
                f = np.frombuffer(binary, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1, 3)
            mesh = bpy.data.meshes.new(panel + '-' + part['id'])
            mesh.from_pydata((v + np.array([shift, 0, 0])).tolist(), [], f.tolist())
            mesh.update()
            obj = bpy.data.objects.new(mesh.name, mesh)
            scene.collection.objects.link(obj)
            obj.data.materials.append(materials[part['componentRole']])
            for polygon in mesh.polygons:
                polygon.use_smooth = True
            if panel == 'decoded':
                encoded_normals = np.frombuffer(binary, dtype='<i2', count=part['vertexCount']*3, offset=part['normals']).reshape(-1, 3).astype(float) / 32767
                mesh.normals_split_custom_set_from_vertices(encoded_normals.tolist())
            render_objects.append((obj, panel, shift))
    center = Vector((0, .55, 0))
    for location, energy in [((.4, 1.2, -1), 210), ((-.5, .6, 1), 140)]:
        light = bpy.data.lights.new('Reference QA area', 'AREA')
        light.energy, light.size = energy, 1.5
        light_obj = bpy.data.objects.new(light.name, light)
        scene.collection.objects.link(light_obj)
        light_obj.location = location
        light_obj.rotation_euler = (center - light_obj.location).to_track_quat('-Z', 'Y').to_euler()
    camera = bpy.data.cameras.new('Reference QA camera')
    camera.type = 'ORTHO'
    camera_obj = bpy.data.objects.new(camera.name, camera)
    scene.collection.objects.link(camera_obj)
    scene.camera = camera_obj

    def view(center, direction, scale, filename):
        center = Vector(center)
        camera.ortho_scale = scale
        camera_obj.location = center + Vector(direction)
        back = (camera_obj.location - center).normalized()
        right = Vector((0, 1, 0)).cross(back).normalized()
        camera_obj.rotation_euler = Matrix((right, back.cross(right), back)).transposed().to_euler()
        scene.render.filepath = str(WORK / filename)
        bpy.ops.render.render(write_still=True)

    view((0, .55, 0), (0, .04, -1), 1.22, 'source-decoded-posterior.png')
    view((0, .55, 0), (.18, .04, -1), 1.22, 'source-decoded-oblique.png')
    # Display offsets above are QA panel layout only, never package coordinates.
    for obj, panel, shift in render_objects:
        if panel == 'source':
            obj.hide_render = True
        else:
            obj.location.x = -shift
    scene.render.resolution_x, scene.render.resolution_y = 1200, 1200
    view((0, .54, 0), (.14, .02, -1), .44, 'decoded-knee-close.png')
    view((0, .11, 0), (.18, .04, -1), .36, 'decoded-ankle-close.png')
