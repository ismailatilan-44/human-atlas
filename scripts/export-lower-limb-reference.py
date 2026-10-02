"""Package the current 119-object same-source reference; no atlas fitting.

Blender --background --disable-autoexec work/open-assets-review/Startup.blend \
  --python scripts/export-lower-limb-reference.py

The immutable 87-object baseline and append-only source export are owned by the
foot soft-tissue audit. Earlier 87-object producer evidence remains historical.
"""
import hashlib
import json
import runpy
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'public/models/lower-limb-nerve-reference'
producer = ROOT/'data/model-candidates/foot-soft-tissue-source-audit-v1/export.py'
api = runpy.run_path(str(producer), run_name='atlas_source_export')
report = api['build_candidate'](output_dir=OUT, render='--render' in sys.argv)
p = OUT/'atlas.json'
manifest = json.loads(p.read_text())
manifest['version'] = 'Z-Anatomy independent lower-limb and intrinsic-foot reference3'
manifest['releaseStatus'] = 'packaged_reference;anatomical_expert_review_pending'
manifest['packaging'] = dict(producer='scripts/export-lower-limb-reference.py',
    sourceExport='data/model-candidates/foot-soft-tissue-source-audit-v1/export.py',
    sourceCandidateManifestSha256=report['manifestSha256'],
    inclusion='Source-preserved D1 reference with disclosed mesh/group limits; not regional anatomy acceptance')
p.write_text(json.dumps(manifest,indent=2)+'\n')
assert manifest['chunks'][0]['sha256'] == '038387150768d7c34670bdce332ad4870dc15fbcbb622c0e441ab064cc979350'
print(json.dumps(dict(parts=len(manifest['parts']),binarySha256=report['binarySha256'],
    publicManifestSha256=hashlib.sha256(p.read_bytes()).hexdigest())))
