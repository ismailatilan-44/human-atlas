"""Project exactly two audited left cords; preserve every decoded geometry byte."""
import copy, gzip, hashlib, json, math, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
G = 'data/model-candidates/upper-limb-bp3d43-geometry-audit-v1'
M = 'data/model-candidates/upper-limb-bp3d43-cord-metadata-v1'
read = lambda p: json.loads((ROOT/p).read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
def write(p, b):
    if isinstance(b, dict): b = (json.dumps(b, ensure_ascii=False, indent=2)+'\n').encode()
    if isinstance(b, str): b = b.encode()
    if '--check' in sys.argv: assert (ROOT/p).read_bytes() == b, p+' stale'
    else: (ROOT/p).write_bytes(b)
evidence = read(G+'/acceptance-evidence.json')
for filename, expected in evidence['packageFileSha256'].items():
    assert sha((ROOT/G/filename).read_bytes()) == expected, filename
source = read(G+'/atlas.json'); proposal = read(M+'/proposal.json')
blob = (ROOT/G/'anatomy.bin').read_bytes()
assert sha(blob) == source['chunks'][0]['sha256']
parts = copy.deepcopy([p for p in source['parts'] if p['id'] in ['BP43-FJ4274', 'BP43-FJ4275']])
assert len(parts) == 2 and all(p['side']=='left' for p in parts)
output = bytearray()
for part in parts:
    for field, size in [('positions',part['vertexCount']*12),('normals',part['vertexCount']*6),('indices',part['indexCount']*4)]:
        while len(output)%4: output.append(0)
        data = blob[part[field]:part[field]+size]
        part[field] = len(output); output.extend(data)
        assert bytes(output[part[field]:part[field]+size]) == data
    positions = struct.unpack_from('<'+'f'*(part['vertexCount']*3), output, part['positions'])
    indices = struct.unpack_from('<'+'I'*part['indexCount'], output, part['indices'])
    assert all(math.isfinite(v) for v in positions)
    assert all(i < part['vertexCount'] for i in indices)
    for axis in range(3):
        assert abs(min(positions[axis::3])-part['bounds'][0][axis]) < 1e-6
        assert abs(max(positions[axis::3])-part['bounds'][1][axis]) < 1e-6
    part['datasetId'] = 'male-body'
    part['representation'] = 'source_anatomical_surface'
compressed = gzip.compress(bytes(output),mtime=0)
base = '/models/extensions/left-cords-bp3d43'
manifest = dict(version='BP3D4.3 two left cords v1',status='registered_source_reference;expert_review_pending',sex='unknown',
    parts=parts, concepts=[c for c in source['concepts'] if c['id'] in ['FMA45239','FMA45241']],
    triangles=sum(p['indexCount']//3 for p in parts),chunks=[dict(url=base+'.bin',bytes=len(output),gzip=base+'.bin.gz',gzipBytes=len(compressed),sha256=sha(output))],
    source={**source['source'],'attribution':'/models/extensions/LEFT-CORDS-BP3D43-ATTRIBUTION.md'},
    registration={**source['registration'],'method':'Existing BP3D native frame; nine independent bone holdouts; no fitting or per-object change'},
    limitations=['Only short left lateral/medial source cord surfaces; no complete course, right side or C5–T1 contribution.',
                  'Medial source speck and nonmanifold diagnostics preserved; no repair.',
                  'Cross-source physical nerve continuity and anatomical expert acceptance pending.'],
    inputSnapshots=[dict(path=p,sha256=sha((ROOT/p).read_bytes())) for p in [G+'/atlas.json',G+'/anatomy.bin',M+'/proposal.json']])
write('public'+base+'.json',manifest);write('public'+base+'.bin',bytes(output));write('public'+base+'.bin.gz',compressed)
write('public/models/extensions/LEFT-CORDS-BP3D43-LICENSE.html',(ROOT/G/'UPSTREAM-LICENSE.html').read_bytes())
write('public/models/extensions/LEFT-CORDS-BP3D43-ATTRIBUTION.md', '''# Two left BodyParts3D 4.3 cords

Database Center for Life Science (DBCLS), BodyParts3D official Data4.3 / Objects4.3 / FMA3.0.
Source: https://lifesciencedb.jp/bp3d/ . License: CC BY-SA 2.1 Japan, https://creativecommons.org/licenses/by-sa/2.1/jp/ .
The original captured notice is preserved in LEFT-CORDS-BP3D43-LICENSE.html. This license is separate from application code, BP3D4.0 and Z-Anatomy assets.

Exactly FJ4274/BP29122/FMA45239 and FJ4275/BP29196/FMA45241 are projected from the audited candidate. The native coordinate transform, authored normals, vertices, indices and source defects are unchanged; only buffer offsets and packaging change. No mirroring, bridging, fitting, smoothing or removal of the medial speck. Source demographic detail is unknown.

These are short left source segments, not the entire plexus or complete cord course. Nine source-frame bone holdouts support bounded placement; contact with other-source nerves, right cords, C5–T1 contributions and anatomical expert acceptance remain open. See docs/model/left-cords-local-acceptance.md and the immutable candidate audits.
''')
entities=copy.deepcopy(proposal['entities'])
for e in entities: e['geometryPartIds']=[];e['representationStatus']='missing_geometry';e['geometryNote']='Short source segment; complete course and cross-source continuity not asserted; expert review pending.'
relations=copy.deepcopy(proposal['relations'])
for r in relations:r['status']='source_supported'
labels=copy.deepcopy(proposal['labels'])
for label in labels:
    label.pop('datasetDecision',None);label['datasetId']='male-body'
    label['representationNoteTr']=label['scopeNoteTr']+' Kısa kaynak segmentidir; diğer kaynak sinirleriyle fiziksel birleşme iddiası yoktur.'
    if label['ids']==['FMA45241']:label['representationNoteTr']+=' Kaynaktaki çok küçük ayrı parça ve yüzey kusurları korunmuştur.'
write('data/anatomy/left-cords.json',dict(schemaVersion=1,scope='Two left source cords only; expert pending',entities=entities,relations=relations,labels=labels,deferredRelations=proposal['deferredRelations']))
print(json.dumps(dict(parts=2,triangles=manifest['triangles'],decodedSha256=sha(output),relations=3,labels=2)))
