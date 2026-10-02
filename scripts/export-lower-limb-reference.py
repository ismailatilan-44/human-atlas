"""Package the current 137-object same-source reference; no atlas fitting.

Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
  --python scripts/export-lower-limb-reference.py

The immutable 119-object baseline and append-only source export are owned by the
foot support audit. Earlier 87/119-object producer evidence remains historical.
"""
import gzip
import hashlib
import json
import runpy
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'public/models/lower-limb-nerve-reference'
producer = ROOT/'data/model-candidates/foot-support-source-audit-v1/export.py'
api = runpy.run_path(str(producer), run_name='atlas_source_export')
report = api['build_candidate'](output_dir=OUT, render='--render' in sys.argv)
p = OUT/'atlas.json'
manifest = json.loads(p.read_text())
assert report['binarySha256'] == 'a207ccb80737956445c8966cc99d57a42dd59b30635d0178aea96e5fad97b70d'
excluded_ids = {'zanatomy:intersesamoid-ligament-l', 'zanatomy:intersesamoid-ligament-r'}
excluded = [part for part in manifest['parts'] if part['conceptId'] in excluded_ids]
assert len(excluded) == 2 and manifest['parts'][-2:] == excluded
manifest['parts'] = manifest['parts'][:-2]
manifest['concepts'] = [c for c in manifest['concepts'] if c['id'] not in excluded_ids]
binary = (OUT/'anatomy.bin').read_bytes()[:min(part['positions'] for part in excluded)]
assert len(binary) == max(part['indices']+part['indexCount']*4 for part in manifest['parts'])
baseline = gzip.decompress((producer.parent/'baseline119.bin.gz').read_bytes())
assert binary[:len(baseline)] == baseline and len(manifest['parts']) == len(manifest['concepts']) == 137
compressed = gzip.compress(binary, compresslevel=9, mtime=0)
(OUT/'anatomy.bin').write_bytes(binary)
(OUT/'anatomy.bin.gz').write_bytes(compressed)
manifest['chunks'][0].update(bytes=len(binary), gzipBytes=len(compressed), sha256=hashlib.sha256(binary).hexdigest())
manifest['triangles'] = sum(part['indexCount']//3 for part in manifest['parts'])
manifest['scope'] = ('Sixteen nerve curves, two fibular artery curves, twelve selected ligament objects, '
    'thirty source-named foot muscle objects, ten retinacula, two open plantar aponeuroses and65 bone objects. '
    'Two source-named intersesamoid meshes are candidate-only because they do not span both modeled sesamoid components. '
    'Source sheet/group limits, remaining networks/supports and expert anatomy acceptance stay open.')
manifest['excludedSourceObjects'] = [dict(sourceObject=part['sourceObject'], conceptId=part['conceptId'],
    reason='Source-space extent does not span both modeled sesamoid components; connecting geometry rejected',
    evidence='data/model-candidates/foot-support-source-audit-v1/intersesamoid-placement.json') for part in excluded]
manifest['version'] = 'Z-Anatomy independent lower-limb foot and support reference4'
manifest['releaseStatus'] = 'packaged_reference;anatomical_expert_review_pending'
manifest['packaging'] = dict(producer='scripts/export-lower-limb-reference.py',
    sourceExport='data/model-candidates/foot-support-source-audit-v1/export.py',
    sourceCandidateManifestSha256=report['manifestSha256'],
    inclusion='18 new source-preserved supports; two connecting geometries withheld; no regional anatomy acceptance')
p.write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'ATTRIBUTION.md').write_text((OUT/'ATTRIBUTION.md').read_text()+'\n## Active student reference packaging\n\n'
    'This package contains137 objects: the prior119 unchanged and18 selected support meshes. '
    'The139-object audit candidate retains two source-named intersesamoid meshes whose extent does not connect '
    'the two modeled sesamoid components. These two are excluded from active geometry and search; '
    'source/target identities remain in the candidate records. No source geometry is repaired or repositioned.\n')
print(json.dumps(dict(parts=len(manifest['parts']), binarySha256=manifest['chunks'][0]['sha256'],
    bytes=len(binary), gzipBytes=len(compressed), triangles=manifest['triangles'],
    publicManifestSha256=hashlib.sha256(p.read_bytes()).hexdigest())))
