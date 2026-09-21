"""Copy the reviewed standalone HRA candidate into its separate public endpoint.
Usage: python3 scripts/package-female-pelvis.py
No geometry conversion, source edits or male atlas/registry changes occur here.
"""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/model-candidates/female-pelvis'
TARGET = ROOT / 'public/models/female-pelvis'
BASE_URL = '/models/female-pelvis/'
manifest = json.loads((SOURCE / 'female-pelvis.json').read_text())
assert manifest['datasetId'] == 'female-pelvis' and manifest['sex'] == 'female'
assert manifest['source']['url']
assert manifest['coordinateFrame']['maleAtlasCompatible'] is False

# Validate every source before writing any public file. Input relative file names
# are intentionally restricted to this one standalone candidate directory.
outputs = {}
for chunk in manifest['chunks']:
    raw_name = chunk['url']
    compressed_name = chunk['gzipUrl']
    for name in (raw_name, compressed_name):
        assert Path(name).name == name and name not in ('.', '..'), name
    raw = (SOURCE / raw_name).read_bytes()
    compressed = (SOURCE / compressed_name).read_bytes()
    assert len(raw) == chunk['bytes']
    assert len(compressed) == chunk['gzipBytes']
    assert hashlib.sha256(raw).hexdigest() == chunk['sha256']
    assert gzip.decompress(compressed) == raw
    outputs[raw_name] = raw
    outputs[compressed_name] = compressed
    chunk['url'] = BASE_URL + raw_name
    chunk['gzip'] = BASE_URL + compressed_name
    del chunk['gzipUrl']

manifest['source']['attribution'] = BASE_URL + 'ATTRIBUTION.md'
outputs['ATTRIBUTION.md'] = (SOURCE / 'ATTRIBUTION.md').read_bytes()
outputs['atlas.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
TARGET.mkdir(parents=True, exist_ok=True)
changed = []
for name, data in outputs.items():
    path = TARGET / name
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)
        changed.append(name)
print(json.dumps({
    'endpoint': BASE_URL + 'atlas.json',
    'parts': len(manifest['parts']),
    'triangles': manifest['triangles'],
    'changedFiles': changed,
    'binarySha256': manifest['chunks'][0]['sha256'],
    'status': 'packaged for separate UI acceptance; not deployed by this script',
}, indent=2))
