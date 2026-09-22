"""Package actual BP3D 4.3 lung parenchyma source surfaces without deformation.

/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  --python scripts/export-lung-bp3d43.py [-- --render]

The candidate directory retains source ZIPs, official mapping/license evidence,
registration measurements, source triangle exporter and optional actual-atlas renders.
This exporter does not register the package in the app or mutate the base atlas.
"""
import hashlib
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'data/model-candidates/lung-surfaces'
OUT = ROOT / 'public/models/extensions'
SOURCE_HASHES = {
    'direct-parent-source-evidence.json': 'f9084021a159bbc135130e365d424e89cba2b3b2c5692648656a3ea904331ec9',
    'lung-parenchyma-source.zip': 'ac848958f321318aa87cb0f8d2ca7cc590637ce52b3ba063f90a4b7e2c46baa4',
    'thoracic-references.zip': 'a688d2c76d1622cc999b7040f28a8a870dac643ba51fe91866bdf813e814dd40',
    'bp3d-v43-mapping.zip': 'fa6e9d5c92ed1e5bb86dcabfc5f5e039fdd9130ce28f05f1c33c71699e8f768a',
    'bp3d-live-license.html': '63d46abcf1b112da9f2d587677d0f4edb7d1654a3c9a8a2bfd1c3d080340512e',
}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for filename, expected in SOURCE_HASHES.items():
    assert sha(SRC / filename) == expected, filename
assert sha(ROOT / 'public/models/atlas.json') == 'c359f4bcd2cba90b7411d66d5e9fc04dc81294d46cd5c1e8b212c824f2e5bbee'
runpy.run_path(str(SRC / 'inspect-export.py'), run_name='__main__')
manifest = json.loads((SRC / 'lung-parenchyma.json').read_text())
manifest['status'] = 'registered_source_reference'
manifest['version'] = 'BodyParts3D 4.3 lung parenchyma reference 1'
manifest['source'].update({
    'downloadUrl': 'https://lifesciencedb.jp/bp3d/download.cgi',
    'mappingUrl': 'https://lifesciencedb.jp/bp3d/get-info.cgi?version=4.3&cmd=concept-objfiles-list',
    'mappingPayloadSha256': 'c3d16c891016da13447de2fc3241d05d92e8f9dc460e363233c03f420b935d4f',
    'licenseUrl': 'https://lifesciencedb.jp/bp3d/info/license/index.html',
    'licenseEvidenceSha256': SOURCE_HASHES['bp3d-live-license.html'],
    'attribution': '/models/extensions/LUNG-BP3D43-ATTRIBUTION.md',
})
manifest['chunks'][0].update({
    'url': '/models/extensions/lung-bp3d43.bin',
    'gzip': '/models/extensions/lung-bp3d43.bin.gz',
})
for suffix in ['bin', 'bin.gz']:
    (OUT / ('lung-bp3d43.' + suffix)).write_bytes((SRC / ('lung-parenchyma.' + suffix)).read_bytes())
(OUT / 'lung-bp3d43.json').write_text(json.dumps(manifest, indent=2) + '\n')
(OUT / 'LUNG-BP3D43-ATTRIBUTION.md').write_text((SRC / 'ATTRIBUTION.md').read_text())
print('PUBLIC_PACKAGE', len(manifest['parts']), 'parts;', manifest['triangles'], 'triangles;', manifest['extendsConceptIds'])
