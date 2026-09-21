"""Register Z-Anatomy musculocutaneous nerves to the existing Human Atlas.

Run from any directory (source download is deliberately not automatic):
  Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
    --python scripts/export-upper-arm-nerves.py

Requires Blender's bundled numpy; does not modify atlas.json or the .blend file.
"""
import bpy
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

root = Path(__file__).resolve().parents[1]
work = root / 'work/open-assets-review'
out = root / 'public/models/extensions'
out.mkdir(parents=True, exist_ok=True)
source_path = Path(bpy.data.filepath)
expected_hash = '9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
assert hashlib.sha256(source_path.read_bytes()).hexdigest() == expected_hash, 'Source blend changed; review provenance before exporting'
bindings = json.loads((root/'data/anatomy/upper-arm.json').read_text())['assetBindings']
raw = []
for binding in bindings:
    obj = bpy.data.objects[binding['objectName']]
    mesh = obj.to_mesh()
    mesh.calc_loop_triangles()
    raw.append(dict(id=binding['entityId'], name=obj.name, type=obj.type,
                    vertices=[list(obj.matrix_world @ vertex.co) for vertex in mesh.vertices],
                    triangles=[list(triangle.vertices) for triangle in mesh.loop_triangles],
                    matrix=[list(row) for row in obj.matrix_world],
                    curveSettings=({key: getattr(obj.data, key) for key in
                        ['bevel_depth', 'bevel_resolution', 'resolution_u', 'use_fill_caps']} if obj.type == 'CURVE' else None)))
    obj.to_mesh_clear()

atlas=json.loads((root/'public/models/atlas.json').read_text())
blobs=[(root/'public'/c['url'].lstrip('/')).read_bytes() for c in atlas['chunks']]
pairs=[]
for r in raw:
 p=next((p for p in atlas['parts'] if p['conceptId']==r['id']),None)
 if not p or r['type']!='MESH':continue
 s=np.array(r['vertices']);t=np.frombuffer(blobs[p['chunk']],dtype='<f4',count=p['vertexCount']*3,offset=p['positions']).reshape(-1,3).astype(float)
 faces=np.frombuffer(blobs[p['chunk']],dtype='<u4',count=p['indexCount'],offset=p['indices']).reshape(-1,3)
 pairs.append(dict(name=r['name'],id=r['id'],s=s,t=t,sf=r['triangles'],tf=faces.tolist(),bvh=BVHTree.FromPolygons(t.tolist(),faces.tolist(),all_triangles=True)))

def fit(a,b):
 ac=a.mean(0);bc=b.mean(0);aa=a-ac;bb=b-bc;u,d,vt=np.linalg.svd(aa.T@bb);q=np.eye(3);q[-1,-1]=np.linalg.det(u@vt);rot=u@q@vt;scale=np.sum(d*np.diag(q))/np.sum(aa**2);return scale*rot,bc-ac@(scale*rot)

def nearest(bvh,points):return np.array([list(bvh.find_nearest(Vector(p))[0]) for p in points])
# Matched bone centroids initialize; all refinements use labeled surfaces.
axis=np.array([[1,0,0],[0,0,-1],[0,1,0.]])
bones=[p for p in pairs if any(x in p['name'] for x in ['Scapula','Radius','Humerus'])]
# The fixed axis map supplies an anatomically plausible initialization.
a=np.array([p['s'].mean(0)@axis for p in bones]);b=np.array([p['t'].mean(0) for p in bones]);delta,tr=fit(a,b);mat=axis@delta
for step in range(160):
 aa=[];bb=[]
 for p in bones:
  sample=p['s'][np.linspace(0,len(p['s'])-1,min(800,len(p['s'])),dtype=int)];mapped=sample@mat+tr;target=nearest(p['bvh'],mapped)
  aa.append(sample);bb.append(target)
  sbvh=BVHTree.FromPolygons((p['s']@mat+tr).tolist(),p['sf'],all_triangles=True)
  ts=p['t'][np.linspace(0,len(p['t'])-1,min(800,len(p['t'])),dtype=int)];ss=nearest(sbvh,ts)
  aa.append((ss-tr)@np.linalg.inv(mat));bb.append(ts)
 newmat,newtr=fit(np.concatenate(aa),np.concatenate(bb));change=np.max(abs(mat-newmat))+np.max(abs(tr-newtr));mat,tr=newmat,newtr
 if step%10==0:print('FIT',step,change,flush=True)
 if change<1e-7:break
results=[]
for p in pairs:
 mapped=p['s']@mat+tr;d1=np.linalg.norm(mapped-nearest(p['bvh'],mapped),axis=1)
 sbvh=BVHTree.FromPolygons(mapped.tolist(),p['sf'],all_triangles=True);d2=np.linalg.norm(p['t']-nearest(sbvh,p['t']),axis=1);ds=np.concatenate([d1,d2])*1000
 baseline=p['s']@axis;baseline_distances=np.linalg.norm(baseline-nearest(p['bvh'],baseline),axis=1)*1000
 results.append(dict(axisOnlyRmsMm=float(np.sqrt(np.mean(baseline_distances**2))),id=p['id'],name=p['name'],role=('fit' if any(p is q for q in bones) else 'holdout'),rmsMm=float(np.sqrt(np.mean(ds**2))),meanMm=float(ds.mean()),p95Mm=float(np.percentile(ds,95)),maxMm=float(ds.max())))
report=dict(matrixRowVector=mat.tolist(),translation=tr.tolist(),scale=float(np.cbrt(np.linalg.det(mat))),iterations=step+1,lastTransformDelta=float(change),measurements=results)
(root/'work/open-assets-review/registration-fit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

# Export the actual evaluated curve tube, not a hand-drawn centerline.
blob = bytearray()
parts = []

def append(values, dtype):
    while len(blob) % 4:
        blob.append(0)
    offset = len(blob)
    blob.extend(np.asarray(values, dtype=dtype).tobytes())
    return offset

for row in raw:
    if 'musculocutaneous-nerve' not in row['id']:
        continue
    positions = (np.array(row['vertices']) @ mat + tr).astype('<f4')
    indices = np.array(row['triangles'], dtype='<u4')
    # The left source object is mirrored. Reverse winding before recomputing normals.
    mirrored = np.linalg.det(np.array(row['matrix'])[:3, :3]) < 0
    if mirrored:
        indices = indices[:, [0, 2, 1]]
    faces = positions[indices].astype(float)
    face_normals = np.cross(faces[:, 1]-faces[:, 0], faces[:, 2]-faces[:, 0])
    assert np.all(np.linalg.norm(face_normals, axis=1) > 1e-14), 'Degenerate source triangle'
    normals = np.zeros_like(positions, dtype=float)
    for corner in range(3):
        np.add.at(normals, indices[:, corner], face_normals)
    lengths = np.linalg.norm(normals, axis=1)
    assert np.all(lengths > 0) and np.all(np.isfinite(positions))
    normals /= lengths[:, None]
    quantized = np.rint(normals*32767).astype('<i2')
    assert np.max(indices) < len(positions)
    side = 'Left' if row['name'].endswith('.l') else 'Right'
    parts.append(dict(id='ZA-MCN-'+side[0], conceptId=row['id'], name=side+' musculocutaneous nerve',
                      system='nervous', chunk=0, positions=append(positions, '<f4'),
                      normals=append(quantized, '<i2'), indices=append(indices, '<u4'),
                      vertexCount=len(positions), indexCount=int(indices.size),
                      bounds=[positions.min(0).tolist(), positions.max(0).tolist()],
                      sourceObject=row['name'], sourceObjectType='CURVE', curveSettings=row['curveSettings'],
                      mirroredWindingCorrected=bool(mirrored)))
binary = bytes(blob)
(out/'upper-arm-nerves.bin').write_bytes(binary)
compressed = gzip.compress(binary, compresslevel=9, mtime=0)
(out/'upper-arm-nerves.bin.gz').write_bytes(compressed)
column_matrix = np.eye(4)
column_matrix[:3, :3] = mat.T
column_matrix[:3, 3] = tr
manifest = dict(version='Z-Anatomy upper-arm extension 1', sex='male',
    scope='Two source-derived musculocutaneous nerve tubes registered to Human Atlas; anatomical expert review pending',
    parts=parts, chunks=[dict(url='/models/extensions/upper-arm-nerves.bin', bytes=len(binary),
        gzip='/models/extensions/upper-arm-nerves.bin.gz', gzipBytes=len(compressed),
        sha256=hashlib.sha256(binary).hexdigest())], triangles=sum(p['indexCount']//3 for p in parts),
    concepts=[dict(id=p['conceptId'],name=p['name'],elements=[p['id']]) for p in parts],
    source=dict(id='zanatomy', url='https://github.com/Z-Anatomy/Models-of-human-anatomy',
        archiveUrl='https://raw.githubusercontent.com/Z-Anatomy/Models-of-human-anatomy/master/Z-Anatomy.zip',
        member='Z-Anatomy/Startup.blend', sha256=expected_hash, blenderVersion=bpy.app.version_string,
        license='CC-BY-SA-4.0 (upstream general declaration; preserve upstream exceptions)',
        attribution='/models/extensions/ATTRIBUTION.md',
        limitations='Object-specific author/source provenance is not supplied by upstream. No relicensing or blanket commercial clearance of the full archive is asserted.'),
    registration=dict(method='Labeled bidirectional nearest-surface similarity ICP; six bilateral bones fit, six muscles held out',
        sourceUnits='meters', sourceAxes='X left, Y posterior, Z superior',
        targetUnits='meters', targetAxes='X left, Y superior, Z anterior',
        matrixColumnVector=column_matrix.tolist(), uniformScale=report['scale'],
        iterations=report['iterations'], lastTransformDelta=report['lastTransformDelta'], measurements=results,
        sourceSceneUnits=dict(system=bpy.context.scene.unit_settings.system, scaleLength=bpy.context.scene.unit_settings.scale_length),
        limitations='Surface discrepancy includes source edits and atlas simplification. Bone/muscle agreement is not anatomical validation of the nerve path.'))
(out/'upper-arm-nerves.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps(dict(parts=len(parts), vertices=sum(p['vertexCount'] for p in parts),
    triangles=manifest['triangles'], bytes=len(binary), gzipBytes=len(compressed))))
