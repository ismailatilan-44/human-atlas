"""Export independent Z-Anatomy source-space ear dataset. Run with Blender --disable-autoexec.

Default source: work/open-assets-review/Startup.blend (open it before invoking this script).
Output is confined to data/model-candidates/inner-ear-reference. Add -- --render for QA PNGs.
No main-atlas inputs, alignment, recentering, remeshing or source blend saving.
"""
import bpy
import gzip
import hashlib
import json
import shutil
import sys
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/model-candidates/inner-ear-reference'
PIN = '9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == PIN, 'Source blend mismatch'
OUT.mkdir(parents=True, exist_ok=True)
DEPS = bpy.context.evaluated_depsgraph_get()
DATASET = 'inner-ear-reference'
SPECS = [('Cochlea', 'cochlea', 'primary', 'sensory'),
         ('Vestibule', 'vestibular-complex', 'context', 'sensory'),
         ('Temporal bone', 'temporal-bone', 'context', 'skeletal')]
blob = bytearray()
parts = []
rows = []


def append(array, dtype):
    while len(blob) % 4:
        blob.append(0)
    offset = len(blob)
    blob.extend(np.asarray(array, dtype=dtype).tobytes())
    return offset


def write_obj(path, name, vertices, faces):
    lines = ['# Original Z-Anatomy world coordinates in meters; no atlas registration', 'o ' + name]
    lines += ['v ' + ' '.join(format(float(x), '.10g') for x in v) for v in vertices]
    lines += ['f ' + ' '.join(str(int(i) + 1) for i in face) for face in faces]
    path.write_text('\n'.join(lines) + '\n')


for stem, slug, role, system in SPECS:
    for side, suffix in [('left', 'l'), ('right', 'r')]:
        name = stem + '.' + suffix
        obj = bpy.data.objects[name]
        assert obj.type == 'MESH' and len(obj.data.polygons), name
        evaluated = obj.evaluated_get(DEPS)
        mesh = evaluated.to_mesh()
        mesh.calc_loop_triangles()
        positions = np.array([list(evaluated.matrix_world @ v.co) for v in mesh.vertices])
        faces = np.array([list(t.vertices) for t in mesh.loop_triangles], dtype=np.int64)
        reflected = evaluated.matrix_world.to_3x3().determinant() < 0
        if reflected:
            faces = faces[:, [0, 2, 1]]
        modifiers = [dict(name=m.name, type=m.type, visible=m.show_viewport,
                          viewportLevels=getattr(m, 'levels', None), renderLevels=getattr(m, 'render_levels', None))
                     for m in obj.modifiers]
        provenance = dict(baseVertices=len(obj.data.vertices), basePolygons=len(obj.data.polygons),
                          evaluatedVertices=len(positions), evaluatedTriangles=len(faces),
                          modifiers=modifiers, evaluation='Authored viewport modifiers evaluated; no additional modifiers',
                          sourceWorldMatrix=[list(r) for r in evaluated.matrix_world], mirroredWindingCorrected=reflected,
                          parent=obj.parent.name if obj.parent else None,
                          collections=[c.name for c in obj.users_collection])
        evaluated.to_mesh_clear()
        assert np.isfinite(positions).all() and len(faces)
        assert (1 if side == 'left' else -1) * positions[:, 0].mean() > .025, name
        base_positions = np.array([list(obj.matrix_world @ v.co) for v in obj.data.vertices])
        base_faces = [list(p.vertices)[::-1] if reflected else list(p.vertices) for p in obj.data.polygons]
        write_obj(OUT / (side + '-' + slug + '-base.obj'), name, base_positions, base_faces)
        write_obj(OUT / (side + '-' + slug + '-surface.obj'), name, positions, faces)
        tris = positions[faces]
        cross = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        degenerate = np.linalg.norm(cross, axis=1) <= 1e-15
        normals = np.zeros_like(positions)
        for i in range(3):
            np.add.at(normals, faces[:, i], cross)
        lengths = np.linalg.norm(normals, axis=1)
        normals[lengths > 0] /= lengths[lengths > 0, None]
        edges = np.sort(np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]]), axis=1)
        _, counts = np.unique(edges, axis=0, return_counts=True)
        quantized = positions.astype('<f4')
        error = np.linalg.norm(quantized.astype(float) - positions, axis=1)
        quality = dict(boundaryEdges=int(np.sum(counts == 1)), nonManifoldEdges=int(np.sum(counts > 2)),
                       zeroAreaFacesRetained=int(degenerate.sum()), zeroNormalVertices=int(np.sum(lengths == 0)),
                       maxFloat32PositionErrorMm=float(error.max() * 1000),
                       dimensionsMm=(np.ptp(positions, axis=0) * 1000).tolist())
        ear = stem != 'Temporal bone'
        license_info = dict(license='CC-BY-NC-SA-4.0' if ear else 'CC-BY-SA-4.0',
                            lineageStatus='inferred_from_archive_component_attribution' if ear else 'archive_general_declaration',
                            sourceComponent='University of Dundee Anatomy of the Inner Ear' if ear else 'Z-Anatomy / underlying BodyParts3D',
                            note='Individual object author/license lineage is not encoded in the blend. Component association is an inference.' if ear else 'Retains general Z-Anatomy license and underlying BodyParts3D attribution; no object-specific lineage certificate.')
        label = side.capitalize() + (' vestibule / semicircular-canal complex (source: Vestibule)' if stem == 'Vestibule' else ' ' + stem.lower())
        part = dict(id='IE-' + slug.upper() + '-' + suffix.upper(), datasetId=DATASET,
                    conceptId=DATASET + ':' + side + '-' + slug, name=label, system=system, side=side, role=role,
                    chunk=0, positions=append(positions, '<f4'), normals=append(np.rint(normals * 32767), '<i2'),
                    indices=append(faces, '<u4'), vertexCount=len(positions), indexCount=int(faces.size),
                    bounds=[positions.min(0).tolist(), positions.max(0).tolist()], sourceObject=name,
                    sourceObjectType='MESH', sourceGeometry=provenance, quality=quality, licenseScope=license_info)
        if stem == 'Vestibule':
            part['anatomicalScope'] = 'One authored combined surface. Semicircular loops remain part of Vestibule; no independently segmented canal identity asserted.'
        parts.append(part)
        rows.append(dict(part=part, vertices=positions, faces=faces))

binary = bytes(blob)
compressed = gzip.compress(binary, compresslevel=9, mtime=0)
(OUT / 'inner-ear-reference.bin').write_bytes(binary)
(OUT / 'inner-ear-reference.bin.gz').write_bytes(compressed)
# Preserve evidence that individually named canals are labels/connectors, not additional surfaces.
label_evidence = []
for obj in bpy.data.objects:
    if 'semicircular canal' in obj.name.lower():
        label_evidence.append(dict(name=obj.name, sourceObjectType=obj.type,
                                   parent=obj.parent.name if obj.parent else None,
                                   vertices=len(obj.data.vertices) if obj.type == 'MESH' else None,
                                   polygons=len(obj.data.polygons) if obj.type == 'MESH' else None,
                                   text=obj.data.body if obj.type == 'FONT' else None,
                                   exported=False))
all_positions = np.concatenate([r['vertices'] for r in rows])
manifest = dict(schemaVersion=1, version='Z-Anatomy source-space inner-ear reference 1', datasetId=DATASET,
                status='independent_noncommercial_reference_candidate', sex='unspecified',
                scope='Bilateral cochlea, authored Vestibule complexes, and same-source temporal bones',
                coordinateSystem=dict(unit='meter', x='left', y='posterior', z='superior',
                                      origin='Original Startup.blend world origin; no recentering',
                                      worldTransform=np.eye(4).tolist(), atlasRegistration=None,
                                      compatibleWithMainAtlas=False),
                licensePolicy=dict(packageUse='noncommercial', innerEar='CC-BY-NC-SA-4.0',
                                   temporalBones='CC-BY-SA-4.0',
                                   note='Separate source-license scopes retained; package restriction does not relicense temporal bones.'),
                source=dict(id='zanatomy-inner-ear-reference', url='https://github.com/Z-Anatomy/Models-of-human-anatomy',
                            archiveUrl='https://raw.githubusercontent.com/Z-Anatomy/Models-of-human-anatomy/master/Z-Anatomy.zip',
                            member='Z-Anatomy/Startup.blend', sha256=PIN, attribution='ATTRIBUTION.md',
                            license='Mixed: inner-ear CC-BY-NC-SA-4.0 (component lineage inferred), temporal bones CC-BY-SA-4.0',
                            upstreamLicenseUrl='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/License.txt',
                            componentLicenseUrl='https://www.dundee.ac.uk/tilt/medical-illustration/anatomy-inner-ear'),
                parts=parts,
                chunks=[dict(url='inner-ear-reference.bin', bytes=len(binary), gzip='inner-ear-reference.bin.gz',
                             gzipBytes=len(compressed), sha256=hashlib.sha256(binary).hexdigest(),
                             gzipSha256=hashlib.sha256(compressed).hexdigest())],
                triangles=sum(p['indexCount'] // 3 for p in parts),
                bounds=[all_positions.min(0).tolist(), all_positions.max(0).tolist()],
                concepts=[dict(id=p['conceptId'], datasetId=DATASET, name=p['name'], elements=[p['id']]) for p in parts],
                excludedCanalLabels=label_evidence,
                limitations=['Source world positions are preserved. There is no main-atlas fit or clinical placement claim.',
                             'Authored viewport subdivision evaluated; original base cages also supplied as OBJ.',
                             'Cochlear and vestibular surfaces are illustrative source objects; membranes, sensory cells and organ of Corti are not modeled.',
                             'Semicircular canals are visible portions of combined Vestibule objects; individually named source objects are text/line labels only.',
                             'Bilateral authored objects do not imply independent specimens or independently verified anatomical segmentations.',
                             'Open and nonmanifold source edges are recorded and retained, not repaired. Expert anatomical review pending.'])
(OUT / 'inner-ear-reference.json').write_text(json.dumps(manifest, indent=2) + '\n')
(OUT / 'geometry-proof.json').write_text(json.dumps(dict(sourceSha256=PIN, atlasRead=False, transform='identity after authored source world transforms',
                                                      parts=[dict(id=p['id'], sourceObject=p['sourceObject'], **p['quality']) for p in parts],
                                                      excludedCanalLabels=label_evidence), indent=2) + '\n')
shutil.copyfile(ROOT / 'public/models/extensions/UPSTREAM-LICENSE.txt', OUT / 'UPSTREAM-LICENSE.txt')
print(json.dumps(dict(parts=len(parts), triangles=manifest['triangles'], bytes=len(binary), gzipBytes=len(compressed),
                      quality=[dict(name=p['sourceObject'], **p['quality']) for p in parts]), indent=2), flush=True)

if '--render' in sys.argv:
    scene = bpy.data.scenes.new('Independent inner-ear reference QA')
    bpy.context.window.scene = scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.cycles.transparent_max_bounces = 32
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.world = bpy.data.worlds.new('Reference world')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.07, .09, .13, 1)
    scene.view_settings.view_transform = 'AgX'
    def material(name, color, alpha=1):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        shader = nodes.get('Principled BSDF')
        shader.inputs['Base Color'].default_value = (*color, 1)
        shader.inputs['Roughness'].default_value = .55
        if alpha < 1:
            mix = nodes.new('ShaderNodeMixShader')
            mix.inputs[0].default_value = alpha
            transparent = nodes.new('ShaderNodeBsdfTransparent')
            mat.node_tree.links.new(transparent.outputs[0], mix.inputs[1])
            mat.node_tree.links.new(shader.outputs[0], mix.inputs[2])
            mat.node_tree.links.new(mix.outputs[0], nodes.get('Material Output').inputs['Surface'])
        return mat
    render_objects = []
    for row in rows:
        p = row['part']
        bone = p['system'] == 'skeletal'
        color = (.63, .73, .83) if bone else ((.24, .76, .52) if 'Vestibule' in p['sourceObject'] else (.96, .52, .14))
        mesh = bpy.data.meshes.new(p['sourceObject'])
        mesh.from_pydata(row['vertices'].tolist(), [], row['faces'].tolist())
        mesh.update()
        obj = bpy.data.objects.new(p['sourceObject'], mesh)
        scene.collection.objects.link(obj)
        mesh.materials.append(material(p['sourceObject'], color, .10 if bone else 1))
        for poly in mesh.polygons:
            poly.use_smooth = True
        render_objects.append((obj, p))
    center = Vector(np.concatenate([r['vertices'] for r in rows if r['part']['system'] == 'sensory']).mean(0))
    camera = bpy.data.objects.new('Camera', bpy.data.cameras.new('Camera'))
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera.data.type = 'ORTHO'
    camera.data.clip_start = .001
    for name, delta, power in [('Key', (.13, -.16, .2), 6), ('Fill', (-.14, .10, .13), 4)]:
        light = bpy.data.objects.new(name, bpy.data.lights.new(name, 'AREA'))
        scene.collection.objects.link(light)
        light.data.energy = power
        light.data.size = .12
        light.location = center + Vector(delta)
        light.rotation_euler = (center - light.location).to_track_quat('-Z', 'Y').to_euler()
    views = [('source-temporal-context', None, (0, -.06, .3), .205, True),
             ('bilateral-inner-ear', None, (0, -.05, .3), .13, False),
             ('left-ear-context', 'left', (.06, -.08, .06), .046, True),
             ('right-ear-context', 'right', (-.06, -.08, .06), .046, True)]
    for name, side, delta, scale, bones in views:
        selected = [r['vertices'] for r in rows if r['part']['system'] == 'sensory' and (side is None or r['part']['side'] == side)]
        look = Vector(np.concatenate(selected).mean(0))
        for obj, p in render_objects:
            obj.hide_render = (side is not None and p['side'] != side) or (not bones and p['system'] == 'skeletal')
        camera.location = look + Vector(delta)
        backward = (camera.location - look).normalized()
        upref = Vector((0, -1, 0)) if side is None else Vector((0, 0, 1))
        right = upref.cross(backward).normalized()
        up = backward.cross(right)
        camera.rotation_euler = Matrix((right, up, backward)).transposed().to_euler()
        camera.data.ortho_scale = scale
        scene.render.filepath = str(OUT / (name + '.png'))
        bpy.ops.render.render(write_still=True)
checks = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir())
          if p.is_file() and p.name not in ['checksums.json', 'export.log']}
(OUT / 'checksums.json').write_text(json.dumps(checks, indent=2) + '\n')
