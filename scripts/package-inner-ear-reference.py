"""Package source-space ear candidate for the Y-up viewer using one exact rigid rotation.

No Blender, NumPy, registration, recentering, scaling, or main-atlas inputs required.
Raw candidate is read-only. Output: public/models/inner-ear-reference/atlas.{json,bin,bin.gz}.
"""
import copy
import gzip
import hashlib
import json
import math
import shutil
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'data/model-candidates/inner-ear-reference'
OUT = ROOT / 'public/models/inner-ear-reference'
OUT.mkdir(parents=True, exist_ok=True)
manifest_bytes = (SRC / 'inner-ear-reference.json').read_bytes()
source_manifest = json.loads(manifest_bytes)
assert source_manifest['datasetId'] == 'inner-ear-reference'
assert source_manifest['coordinateSystem']['atlasRegistration'] is None
assert source_manifest['coordinateSystem']['unit'] == 'meter'
assert source_manifest['coordinateSystem']['worldTransform'] == [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
source_chunk = source_manifest['chunks'][0]
raw = (SRC / source_chunk['url']).read_bytes()
assert hashlib.sha256(raw).hexdigest() == source_chunk['sha256']
assert gzip.decompress((SRC / source_chunk['gzip']).read_bytes()) == raw
assert len(source_manifest['chunks']) == 1
# Proper rigid axis permutation; right-handed, determinant +1.
matrix = [[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]]

def rotate(v):
    return (v[0], v[2], -v[1])

def bounds(points):
    return [[min(v[i] for v in points) for i in range(3)], [max(v[i] for v in points) for i in range(3)]]

output = bytearray(raw)
manifest = copy.deepcopy(source_manifest)
manifest['version'] = 'Z-Anatomy independent inner-ear reference, Y-up display 1'
manifest['status'] = 'independent_noncommercial_reference'
manifest['coordinateSystem'] = dict(unit='meter', x='left', y='superior', z='anterior',
                                     origin='Original source origin retained; uniform axis rotation only',
                                     atlasRegistration=None, compatibleWithMainAtlas=False)
manifest['appliedDisplayTransform'] = dict(matrixColumnVector=matrix,
    formula='(x, y, z) -> (x, z, -y)', uniformScale=1, translation=[0, 0, 0], determinant=1,
    appliesTo='Every part position and normal; bounds recomputed from rotated positions',
    sourceFrame='Source Z-Anatomy world meters, X left / Y posterior / Z superior',
    purpose='One uniform display axis rotation. Not anatomical registration to another dataset.')
manifest['sourceCandidate'] = dict(path='data/model-candidates/inner-ear-reference/inner-ear-reference.json',
    sha256=hashlib.sha256(manifest_bytes).hexdigest(), binarySha256=hashlib.sha256(raw).hexdigest(),
    sourceBlendSha256=source_manifest['source']['sha256'])
manifest['source']['attribution'] = '/models/inner-ear-reference/ATTRIBUTION.md'
manifest['source']['objectUrl'] = manifest['source']['archiveUrl']
manifest['source']['objectUrlScope'] = 'Archive URL; exact Blender object identity is recorded on each part.'
all_positions = []
proof_parts = []
for part, original in zip(manifest['parts'], source_manifest['parts']):
    count = part['vertexCount']
    source_positions = [struct.unpack_from('<fff', raw, part['positions'] + i * 12) for i in range(count)]
    source_normals = [struct.unpack_from('<hhh', raw, part['normals'] + i * 6) for i in range(count)]
    mapped = [rotate(v) for v in source_positions]
    for i, value in enumerate(mapped):
        struct.pack_into('<fff', output, part['positions'] + i * 12, *value)
    for i, value in enumerate(source_normals):
        struct.pack_into('<hhh', output, part['normals'] + i * 6, *rotate(value))
    readback = [struct.unpack_from('<fff', output, part['positions'] + i * 12) for i in range(count)]
    normal_readback = [struct.unpack_from('<hhh', output, part['normals'] + i * 6) for i in range(count)]
    assert readback == mapped
    assert normal_readback == [rotate(n) for n in source_normals]
    assert all(math.isfinite(c) for v in readback for c in v)
    # Inverse rotation exactly recovers every float32 source vertex (no translation/scale).
    assert [(v[0], -v[2], v[1]) for v in readback] == source_positions
    index_start = part['indices']
    index_end = index_start + part['indexCount'] * 4
    assert output[index_start:index_end] == raw[index_start:index_end]
    part['bounds'] = bounds(readback)
    part['quality']['sourceDimensionsMm'] = original['quality']['dimensionsMm']
    source_dims = original['quality']['dimensionsMm']
    part['quality']['dimensionsMm'] = [source_dims[0], source_dims[2], source_dims[1]]
    part['sourceObjectUrl'] = manifest['source']['archiveUrl']
    part['sourceObjectUrlScope'] = 'Archive member Z-Anatomy/Startup.blend; sourceObject is the exact object name.'
    part['attribution'] = '/models/inner-ear-reference/ATTRIBUTION.md'
    part['sourceCandidatePartId'] = original['id']
    part['geometryTransform'] = 'appliedDisplayTransform; same rigid rotation for all parts'
    all_positions.extend(readback)
    proof_parts.append(dict(id=part['id'], vertexCount=count, indexCount=part['indexCount'],
                            exactFloat32AxisPermutation=True, exactInt16NormalPermutation=True,
                            inverseRotationRecoversEverySourceVertex=True, triangleIndicesUnchanged=True))
manifest['bounds'] = bounds(all_positions)
packed = bytes(output)
compressed = gzip.compress(packed, compresslevel=9, mtime=0)
manifest['chunks'] = [dict(url='/models/inner-ear-reference/atlas.bin', gzip='/models/inner-ear-reference/atlas.bin.gz',
                          bytes=len(packed), gzipBytes=len(compressed), sha256=hashlib.sha256(packed).hexdigest(),
                          gzipSha256=hashlib.sha256(compressed).hexdigest())]
manifest['limitations'][0] = 'A single uniform rigid axis rotation preserves source geometry and adjacency. This is not registered to the main atlas.'
(OUT / 'atlas.bin').write_bytes(packed)
(OUT / 'atlas.bin.gz').write_bytes(compressed)
(OUT / 'atlas.json').write_text(json.dumps(manifest, indent=2) + '\n')
for name in ['ATTRIBUTION.md', 'UPSTREAM-LICENSE.txt', 'source-temporal-context.png', 'bilateral-inner-ear.png', 'left-ear-context.png', 'right-ear-context.png', 'visual-review.json']:
    shutil.copyfile(SRC / name, OUT / name)
attribution = (OUT / 'ATTRIBUTION.md').read_text()
attribution = attribution.replace('All objects retain their original shared world coordinates; there is no scaling, recentering, registration to another skull, local deformation or additional smoothing.', 'The raw candidate retains original shared world coordinates. This display package applies one uniform rigid rotation (x, y, z) → (x, z, −y) to all six objects and normals, and recomputes bounds. There is no scaling, recentering, registration to another skull, local deformation or additional smoothing. The inverse rotation exactly recovers every original float32 vertex.')
attribution = attribution.replace('Keep this notice and UPSTREAM-LICENSE.txt', 'Keep this notice and [UPSTREAM-LICENSE.txt](./UPSTREAM-LICENSE.txt)')
(OUT / 'ATTRIBUTION.md').write_text(attribution)
proof = dict(datasetId=manifest['datasetId'], sourceCandidate=manifest['sourceCandidate'],
             appliedDisplayTransform=manifest['appliedDisplayTransform'],
             parts=proof_parts, allPartsUseSameMatrix=True, indexBuffersUnchanged=True,
             noMainAtlasInputs=True, rawCandidateUnchanged=True,
             note='The inverse rotation exactly recovers every original float32 position; norms and inter-object distances are invariant under this determinant +1 permutation.')
assert (SRC / 'inner-ear-reference.json').read_bytes() == manifest_bytes
assert (SRC / source_chunk['url']).read_bytes() == raw
assert gzip.decompress((OUT / 'atlas.bin.gz').read_bytes()) == packed
(OUT / 'packaging-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
checksums = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'checksums.json'}
(OUT / 'checksums.json').write_text(json.dumps(checksums, indent=2) + '\n')
print(json.dumps(dict(datasetId=manifest['datasetId'], parts=len(manifest['parts']), triangles=manifest['triangles'],
                      binaryBytes=len(packed), gzipBytes=len(compressed), sourceCandidateSha256=manifest['sourceCandidate']['sha256'],
                      exactRotationVerified=True, output=str(OUT)), indent=2))
