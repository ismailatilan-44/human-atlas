"""Export four source tibial/common fibular curves with independent distal fit audit.

Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
  --python scripts/export-distal-leg-nerves.py -- --render

Preserves authored splines, radii and open ends; audits the sciatic frame against independent lower-leg references.
The main-frame export is diagnostic and is not approved for main-atlas use.
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
WORK = ROOT / 'data/model-candidates/distal-leg-nerves'
OUT = ROOT / 'public/models/extensions'
EXPECTED_BLEND = '9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
EXPECTED_ATLAS = 'c359f4bcd2cba90b7411d66d5e9fc04dc81294d46cd5c1e8b212c824f2e5bbee'
AXIS = np.array([[1., 0., 0.], [0., 0., -1.], [0., 1., 0.]])
REFERENCES = [
    ('Femur.l', 'FJ3259', 'bone'), ('Femur.r', 'FJ3365', 'bone'),
    ('Tibia.l', 'FJ3282', 'bone'), ('Tibia.r', 'FJ3387', 'bone'),
    ('Fibula.l', 'FJ3260', 'bone'), ('Fibula.r', 'FJ3366', 'bone'),
    ('Patella.l', 'FJ3275', 'bone'), ('Patella.r', 'FJ3381', 'bone'),
    ('Talus.l', 'FJ3280', 'bone'), ('Talus.r', 'FJ3385', 'bone'),
    ('Calcaneus.l', 'FJ3256', 'bone'), ('Calcaneus.r', 'FJ3360', 'bone'),
    ('Medial head of gastrocnemius.l', 'FJ1397M', 'muscle'), ('Medial head of gastrocnemius.r', 'FJ1397', 'muscle'),
    ('Soleus muscle.l', 'FJ1437M', 'muscle'), ('Soleus muscle.r', 'FJ1437', 'muscle'),
]
STRUCTURES = [('Tibial nerve', 'tibial-nerve', 'TIB'), ('Common fibular nerve', 'common-fibular-nerve', 'CFIB')]
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
    metadata = dict(name=name, dataBlock=obj.data.name, materials=[m.name for m in obj.data.materials if m], sourceWorldBounds=[vertices.min(0).tolist(), vertices.max(0).tolist()], objectType=obj.type, parent=obj.parent.name if obj.parent else None,
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


def stats(distances):
    mm = np.array(distances) * 1000
    return dict(samples=len(mm), rmsMm=float(np.sqrt(np.mean(mm ** 2))),
                meanMm=float(mm.mean()), p95Mm=float(np.percentile(mm, 95)), maxMm=float(mm.max()))


def control_points(obj, spline):
    points = spline.bezier_points if spline.type == 'BEZIER' else spline.points
    return np.array([list(obj.matrix_world @ p.co.to_3d()) for p in points]), [float(p.radius) for p in points]


raw = [read_source(base + '.' + side) for base, _, _ in STRUCTURES for side in ['l', 'r']]
for row in raw:
    obj = bpy.data.objects[row['name']]
    row['metadata']['curveSettings'] = {key: getattr(obj.data, key) for key in ['bevel_depth', 'bevel_resolution', 'resolution_u', 'use_fill_caps']}
    row['splines'] = []
    for index, spline in enumerate(obj.data.splines):
        points, radii = control_points(obj, spline)
        row['splines'].append(dict(index=index, type=spline.type, cyclic=spline.use_cyclic_u,
            controlPointCount=len(points), sourceWorldControlPoints=points.tolist(), pointRadii=radii,
            sourceWorldHandlesLeft=[list(obj.matrix_world @ p.handle_left) for p in spline.bezier_points],
            sourceWorldHandlesRight=[list(obj.matrix_world @ p.handle_right) for p in spline.bezier_points],
            handleTypes=[[p.handle_left_type, p.handle_right_type] for p in spline.bezier_points]))
    assert row['splines'], 'Empty source curve'

pairs = []
for name, part_id, role in REFERENCES:
    source = read_source(name)
    target, target_faces = read_target(part_by_id[part_id])
    pairs.append(dict(source=source, target=target, targetFaces=target_faces,
                      targetBvh=bvh(target, target_faces), partId=part_id, role=role))
sciatic_path = OUT / 'sciatic-nerves.json'
sciatic = json.loads(sciatic_path.read_text())
assert sciatic['source']['sha256'] == EXPECTED_BLEND
column_matrix = np.array(sciatic['registration']['matrixColumnVector'])
matrix, translation = column_matrix[:3, :3].T, column_matrix[:3, 3]
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
        nerveExtentBidirectional=stats(np.concatenate([d1[sm], d2[tm]])), regionalBands={name: stats(np.concatenate([d1[(s[:,1]>=lo)&(s[:,1]<hi)],d2[(t[:,1]>=lo)&(t[:,1]<hi)]])) for name,lo,hi in [('knee',.38,.58),('calf',.12,.38),('ankleFoot',-.05,.12)] if np.any((s[:,1]>=lo)&(s[:,1]<hi)) or np.any((t[:,1]>=lo)&(t[:,1]<hi))}))
column_matrix = np.eye(4)
column_matrix[:3, :3] = matrix.T
column_matrix[:3, 3] = translation
registration = dict(method='Exact sciatic uniform transform retained for same-source continuity; independently audited on bilateral lower-leg bones and muscles, without refitting',
    transformSource='/models/extensions/sciatic-nerves.json', transformSourceSha256=hashlib.sha256(sciatic_path.read_bytes()).hexdigest(),
    matrixColumnVector=column_matrix.tolist(), uniformScale=float(np.cbrt(np.linalg.det(matrix))),
    sourceUnits='meters', sourceAxes='X left, Y posterior, Z superior', targetUnits='meters', targetAxes='X left, Y superior, Z anterior',
    sourceSceneUnits=dict(system=bpy.context.scene.unit_settings.system, scaleLength=bpy.context.scene.unit_settings.scale_length),
    measurements=measurements,
    metric='All vertices to opposite triangles, bidirectional vertex-weighted distances; no fit performed on these references. Knee Y=.38-.58m, calf=.12-.38m, ankle/foot=-.05-.12m are measurement bands, not anatomical segmentation. Nerve extent uses +/-20mm padding.',
    limitations='Reference agreement is coordinate evidence only. No nerve-path, attachment, branch identity or anatomical approval inferred. No local warping or displacement. Expert review pending.')

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
    base, slug, code = next(x for x in STRUCTURES if row['name'].startswith(x[0] + '.'))
    part = dict(id='ZA-' + code + '-' + side[0].upper(), conceptId='atlas:' + side + '-' + slug,
        name=side.title() + ' ' + base.lower(), system='nervous', chunk=0,
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
    sciatic_extent = next(e for e in sciatic['sourceExtent'] if e['sourceObject'] == 'Sciatic nerve.' + side[0])
    sciatic_end = np.array(sciatic_extent['splines'][0]['atlasEndpoints'][-1])
    endpoints = np.array(row['splines'][0]['atlasEndpoints'])
    distances = np.linalg.norm(endpoints - sciatic_end, axis=1) * 1000
    extents.append(dict(partId=part['id'], sourceObject=row['name'], splines=row['splines'],
        atlasVerticalBoundsMeters=[float(positions[:, 1].min()), float(positions[:, 1].max())],
        sciaticSourceObject='Sciatic nerve.' + side[0], sciaticDistalEndpointDistancesMm=distances.tolist(),
        nearestSciaticDistalEndpointDistanceMm=float(distances.min()),
        limitations='Preserves entire named source object; separate deep/superficial fibular, plantar, sural and muscular/digital branch objects are not exported. A continuous source junction does not prove anatomical accuracy.'))
    edges = np.sort(np.concatenate([indices[:,[0,1]], indices[:,[1,2]], indices[:,[2,0]]]), axis=1)
    _, edge_counts = np.unique(edges, axis=0, return_counts=True)
    assert not np.any(edge_counts > 2), 'Nonmanifold edge'
    checks.append(dict(partId=part['id'], boundaryEdges=int(np.sum(edge_counts == 1)), nonManifoldEdges=int(np.sum(edge_counts > 2)), minDoubleTriangleArea=float(double_areas.min()), minFaceNormalDot=float(dot.min()),
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
manifest = dict(version='Z-Anatomy distal leg nerve extension 1', sex='male',
    scope='Four source curves: bilateral tibial and common fibular nerves; separate distal branches excluded; anatomical expert review pending',
    parts=parts, concepts=[dict(id=p['conceptId'], name=p['name'], elements=[p['id']]) for p in parts],
    chunks=[dict(url='/models/extensions/distal-leg-nerves.bin', bytes=len(binary),
        gzip='/models/extensions/distal-leg-nerves.bin.gz', gzipBytes=len(compressed), sha256=hashlib.sha256(binary).hexdigest())],
    triangles=sum(p['indexCount'] // 3 for p in parts),
    source=dict(id='zanatomy', url='https://github.com/Z-Anatomy/Models-of-human-anatomy',
        archiveUrl='https://raw.githubusercontent.com/Z-Anatomy/Models-of-human-anatomy/master/Z-Anatomy.zip',
        member='Z-Anatomy/Startup.blend', sha256=EXPECTED_BLEND, blenderVersion=bpy.app.version_string,
        license='CC-BY-SA-4.0 (upstream general declaration; preserve upstream exceptions)',
        attribution='/models/extensions/DISTAL-LEG-NERVES-ATTRIBUTION.md',
        limitations='Object-specific author/source provenance is not supplied by upstream; no blanket commercial clearance of the archive is asserted.'),
    compatibleWithMainAtlas=False, releaseStatus='inactive-registration-rejected',
    placementReview='Distal tibia/fibula and ankle mismatch under sciatic transform; use matched-source reference instead. Expert anatomical review pending.',
    targetAtlasSha256=EXPECTED_ATLAS, registration=registration, sourceExtent=extents,
    existingAtlasContext=dict(namedDistalNerveParts=[p['id'] for p in atlas['parts'] if any(n in p['name'].lower() for n in ['tibial nerve', 'fibular nerve'])],
        nervousPartsBelow105cm=[p['id'] for p in atlas['parts'] if p['system'] == 'nervous' and p['bounds'][0][1] < 1.05],
        scope='Name/system and bounds audit of main atlas only; does not assert anatomical absence inside other surfaces.'))
(OUT / 'distal-leg-nerves.bin').write_bytes(binary)
(OUT / 'distal-leg-nerves.bin.gz').write_bytes(compressed)
(OUT / 'distal-leg-nerves.json').write_text(json.dumps(manifest, indent=2) + '\n')
report = dict(parts=len(parts), vertices=sum(p['vertexCount'] for p in parts), triangles=manifest['triangles'],
              bytes=len(binary), gzipBytes=len(compressed), binarySha256=manifest['chunks'][0]['sha256'],
              registration=registration, sourceExtent=extents, checks=checks)
(WORK / 'registration-report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['registration','sourceExtent']}, indent=2), flush=True)

# The failed main-frame registration is retained above as diagnostic evidence.
# Export a separate source reference using only the common display-axis rotation.
source_blob = bytearray()
source_parts = []
source_checks = []
source_rows = [(row, 'nerve', parts[i]['id'], parts[i]['conceptId']) for i, row in enumerate(raw)]
for pair in pairs:
    if pair['role'] != 'bone' or pair['source']['name'].startswith('Femur'):
        continue
    obj_name = pair['source']['name']
    source_id = 'ZA-DLN-' + obj_name.replace('.', '-').upper()
    source_rows.append((pair['source'], 'bone', source_id, 'zanatomy:' + obj_name.replace('.', '-').lower()))


def source_append(array, dtype):
    while len(source_blob) % 4:
        source_blob.append(0)
    offset = len(source_blob)
    source_blob.extend(np.asarray(array, dtype=dtype).tobytes())
    return offset


for row, role, part_id, concept_id in source_rows:
    positions = (row['vertices'] @ AXIS).astype('<f4')
    indices = row['faces'].astype('<u4')
    triangles = positions[indices].astype(float)
    cross = np.cross(triangles[:,1]-triangles[:,0], triangles[:,2]-triangles[:,0])
    area2 = np.linalg.norm(cross, axis=1)
    assert np.all(area2 > 1e-14), row['name']
    unit = cross / area2[:,None]
    normals = np.zeros_like(positions, dtype=float)
    for corner in range(3):
        a = triangles[:,(corner+1)%3]-triangles[:,corner]
        b = triangles[:,(corner+2)%3]-triangles[:,corner]
        angle = np.arccos(np.clip(np.sum(a*b,axis=1)/(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1)), -1, 1))
        np.add.at(normals, indices[:,corner], unit*angle[:,None])
    lengths = np.linalg.norm(normals,axis=1)
    used_vertices = np.unique(indices)
    assert np.all(lengths[used_vertices] > 0), row['name']
    loose_vertices = lengths == 0
    normals[loose_vertices] = [0,1,0]
    lengths[loose_vertices] = 1
    normals /= lengths[:,None]
    quantized = np.rint(normals*32767).astype('<i2')
    reconstructed = quantized.astype(float)/32767
    dots = np.sum(reconstructed[indices].mean(1)*unit,axis=1)
    assert np.all(np.isfinite(positions)) and indices.max()<len(positions)
    if role == 'nerve':
        assert np.all(dots>0), row['name']
    item = dict(id=part_id, conceptId=concept_id, name=row['name'], system='nervous' if role=='nerve' else 'skeletal',
        chunk=0, positions=source_append(positions,'<f4'), normals=source_append(quantized,'<i2'), indices=source_append(indices,'<u4'),
        vertexCount=len(positions), indexCount=int(indices.size), bounds=[positions.min(0).tolist(),positions.max(0).tolist()],
        sourceObject=row['name'], sourceObjectType=row['metadata']['objectType'], sourceGeometry=row['metadata'],
        componentRole=role, looseVertices=int(np.sum(loose_vertices)), looseVertexNormal='Default up normal only for source vertices unused by triangles; positions preserved', expertReview='pending')
    source_parts.append(item)
    source_checks.append(dict(partId=part_id, nonpositiveInterpolatedFaceNormals=int(np.sum(dots<=0)), looseVertices=int(np.sum(loose_vertices)), minDoubleTriangleArea=float(area2.min()), minFaceNormalDot=float(dots.min()),
        maxNormalLengthError=float(np.max(abs(np.linalg.norm(reconstructed,axis=1)-1)))))
source_binary=bytes(source_blob)
source_gzip=gzip.compress(source_binary,compresslevel=9,mtime=0)
assert gzip.decompress(source_gzip)==source_binary
for part in source_parts:
    v=np.frombuffer(source_binary,dtype='<f4',count=part['vertexCount']*3,offset=part['positions']).reshape(-1,3)
    f=np.frombuffer(source_binary,dtype='<u4',count=part['indexCount'],offset=part['indices'])
    assert np.all(np.isfinite(v)) and f.max()<len(v)
    assert [v.min(0).tolist(),v.max(0).tolist()]==part['bounds']
    assert all(part[k]%4==0 for k in ['positions','normals','indices'])
source_manifest=dict(version='Z-Anatomy matched-source distal nerve candidate 1',datasetId='distal-leg-nerves-source-reference',
    sex='male', compatibleWithMainAtlas=False, atlasRegistration=None, releaseStatus='inactive-source-reference-candidate',
    scope='Four authored nerve curves and ten matched-source bone surfaces. Separate distal branches and full lower-limb innervation excluded. Anatomical expert review pending.',
    coordinates=dict(units='meters',axes='X left, Y superior, Z anterior',sourceAxes='X left, Y posterior, Z superior',
        displayRotationColumnVector=[[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]],
        sourceWorldCoordinatesPreservedBy='One shared orthonormal display-axis rotation only; no scaling, translation or fitting'),
    parts=source_parts,concepts=[dict(id=p['conceptId'],name=p['name'],elements=[p['id']]) for p in source_parts],
    chunks=[dict(url='source-reference.bin',bytes=len(source_binary),gzip='source-reference.bin.gz',gzipBytes=len(source_gzip),sha256=hashlib.sha256(source_binary).hexdigest())],
    triangles=sum(p['indexCount']//3 for p in source_parts), source={**manifest['source'],'attribution':'ATTRIBUTION.md'},
    sourceExtent=[dict(partId=e['partId'],sourceObject=e['sourceObject'],limitations=e['limitations'],
        splines=[{**{k:v for k,v in spline.items() if not k.startswith('atlas')},
            'referenceControlPoints':(np.array(spline['sourceWorldControlPoints']) @ AXIS).tolist()}
            for spline in e['splines']]) for e in extents],
    failedAtlasFitReport='registration-report.json')
(WORK/'source-reference.bin').write_bytes(source_binary)
(WORK/'source-reference.bin.gz').write_bytes(source_gzip)
(WORK/'source-reference.json').write_text(json.dumps(source_manifest,indent=2)+'\n')
(WORK/'source-reference-checks.json').write_text(json.dumps(dict(parts=len(source_parts),vertices=sum(p['vertexCount'] for p in source_parts),
    triangles=source_manifest['triangles'],bytes=len(source_binary),gzipBytes=len(source_gzip),binarySha256=source_manifest['chunks'][0]['sha256'],checks=source_checks),indent=2)+'\n')

if '--render' in sys.argv:
    # Independent QA scene avoids source compositor/render settings.
    scene = bpy.data.scenes.new('Distal nerve registration diagnostic QA')
    bpy.context.window.scene = scene
    scene.world = bpy.data.worlds.new('Sciatic QA world')
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes['Background']
    background.inputs['Color'].default_value = (.055, .065, .08, 1)
    background.inputs['Strength'].default_value = .5
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
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
            if pair['source']['name'].startswith('Femur'): continue
            v = pair['source']['vertices'] @ matrix + translation if panel == 'source' else pair['target']
            f = pair['source']['faces'] if panel == 'source' else pair['targetFaces']
            kind = 'bone' if pair['role'] == 'bone' else 'muscle'
            mesh_object(panel + '-' + pair['source']['name'], v, f, kind, offset)
        for row, exported in zip(raw, export_arrays):
            if panel == 'source':
                v, f = row['vertices'] @ matrix + translation, row['faces']
            else:
                part = exported['part']
                v = np.frombuffer(binary, dtype='<f4', count=part['vertexCount'] * 3, offset=part['positions']).reshape(-1, 3)
                f = np.frombuffer(binary, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1, 3)
            mesh_object(panel + '-' + row['name'], v, f, 'nerve', offset)
    center = Vector((0, .29, -.02))
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

    view((0, .05, -1), 'source-target-posterior.png')
    view((.22, .08, -1), 'source-target-oblique.png')
    # A closer view of both encoded nerves and target references only.
    for item in list(scene.objects):
        if item.type == 'MESH':
            item.hide_render = True
    for pair in pairs:
        if pair['source']['name'].startswith('Femur'): continue
        kind = 'bone' if pair['role'] == 'bone' else 'muscle'
        mesh_object('bilateral-' + pair['source']['name'], pair['target'], pair['targetFaces'], kind, np.zeros(3))
    for exported in export_arrays:
        mesh_object('bilateral-' + exported['part']['id'], exported['positions'], exported['indices'], 'nerve', np.zeros(3))
    camera.ortho_scale = .69
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 1500
    view((.15, .03, -1), 'registered-bilateral.png')

    # Decode the independent reference package for its own visual QA.
    for item in list(scene.objects):
        if item.type == 'MESH':
            item.hide_render = True
    for part in source_parts:
        v = np.frombuffer(source_binary, dtype='<f4', count=part['vertexCount']*3, offset=part['positions']).reshape(-1,3)
        f = np.frombuffer(source_binary, dtype='<u4', count=part['indexCount'], offset=part['indices']).reshape(-1,3)
        mesh_object('source-reference-' + part['id'], v, f, part['componentRole'], np.zeros(3))
    view((.15,.03,-1), 'source-reference-bilateral.png')
