"""Package the audited source-frame reference without changing geometry or main data."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'data/model-candidates/upper-limb-nerve-source-audit-v1'
METADATA = 'data/model-candidates/upper-limb-nerve-metadata-v1'
PUBLIC = 'public/models/upper-limb-nerve-reference'
DATA = 'data/anatomy/upper-limb-reference.json'
read = lambda p: json.loads((ROOT/p).read_text())
sha = lambda p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

manifest = read(f'{SOURCE}/atlas.json')
evidence = read(f'{SOURCE}/acceptance-evidence.json')
proposal = read(f'{METADATA}/proposal.json')
term_evidence = read(f'{METADATA}/source-evidence.json')
for group in ['packageFileSha256', 'auditFileSha256', 'openedRenderFileSha256']:
    for filename, expected in evidence[group].items():
        assert sha(f'{SOURCE}/{filename}') == expected, filename
frozen = read(f'{METADATA}/frozen-inputs.json')
# Hashes remain historical evidence. Relevant current identities are checked below;
# unrelated main labels/relations are allowed to evolve without invalidating geometry.
mutable_inputs = {'data/anatomy/knowledge.json', 'data/anatomy/labels.json',
                  'data/anatomy/brachial-plexus.json'}
for snapshot in frozen['inputSnapshots']:
    if snapshot['path'] not in mutable_inputs:
        assert sha(snapshot['path']) == snapshot['sha256'], snapshot['path']
current_entities = {e['id']: e for e in read('data/anatomy/knowledge.json')['entities']}
current_relations = {r['id']: r for r in read('data/anatomy/knowledge.json')['relations']}
current_labels = {i: e for e in (read('data/anatomy/labels.json')['entries'] + read('data/anatomy/brachial-plexus.json')['labels']) for i in e['ids']}
for entity in frozen['existingEntities']:
    current = current_entities[entity['id']]
    assert current['side'] == entity['side'] and current['name'] == entity['name'], entity['id']
for relation in frozen['existingRelations']:
    current = current_relations[relation['id']]
    for field in ['subject', 'predicate', 'object', 'evidence', 'qualifiers']:
        assert current.get(field) == relation.get(field), (relation['id'], field)
for label in frozen['existingLabels'] + frozen['contextExistingLabels']:
    for concept_id in label['ids']:
        current = current_labels[concept_id]
        for field in ['tr', 'en', 'la', 'side']:
            assert current.get(field) == label.get(field), (concept_id, field)
assert manifest['datasetId'] == proposal['datasetId'] == 'upper-limb-nerve-reference'
assert not manifest['compatibleWithMainAtlas'] and manifest['registration'] is None
assert len(manifest['parts']) == len(manifest['concepts']) == len(proposal['labels']) == 127
parts = {p['id']: p for p in manifest['parts']}
concepts = {c['id']: c for c in manifest['concepts']}
assert len(parts) == len(concepts) == 127
labels = copy.deepcopy(proposal['labels'])
for label in labels:
    label.pop('datasetDecision')
    assert len(label['ids']) == 1 and label['tr'] and label['en'] and label['scopeNoteTr']
    assert concepts[label['ids'][0]]['elements'] == label['geometryPartIds']
    part = parts[label['geometryPartIds'][0]]
    assert part['sourceObject'] == label['sourceObject']
    assert part['side'] == label['side'] or (part['side'] == 'midline' and label['side'] is None)
assert len({label['ids'][0] for label in labels}) == 127
assert sum(label['la'] is not None for label in labels) == 110
assert sum(label['la'] is None for label in labels) == 17
relations = copy.deepcopy(proposal['relations'])
source_titles = {
    'zanatomy-ta2-pinned': 'Z-Anatomy — pinned TA2 terminology',
    'ttuhsc-axilla-shoulder-tables': 'TTUHSC — Shoulder and arm anatomy tables',
    'ttuhsc-forearm-wrist-tables': 'TTUHSC — Forearm and wrist anatomy tables',
}
sources = [dict(source, title=source.get('title') or source_titles[source['id']])
           for source in copy.deepcopy(term_evidence['sources'])]
source_map = {s['id']: s for s in sources}
assert len(relations) == len({r['id'] for r in relations}) == 26
for relation in relations:
    assert relation['datasetId'] == manifest['datasetId'] and relation['predicate'] == 'branch_of'
    assert relation['subject'] in concepts and relation['object'] in concepts
    relation['status'] = 'active_source_supported;expert_review_pending'
    relation['qualifiers']['datasetDecision'] = 'independent_source_frame;not_registered_to_main'
    assert relation['evidence']
    for fact in relation['evidence']:
        assert source_map[fact['sourceId']]['title'] and source_map[fact['sourceId']]['url']
paths = [f'{SOURCE}/atlas.json', f'{SOURCE}/acceptance-evidence.json',
         f'{METADATA}/proposal.json', f'{METADATA}/source-evidence.json',
         f'{METADATA}/frozen-inputs.json', 'scripts/package-upper-limb-reference.py']
snapshots = [dict(path=p, sha256=sha(p)) for p in paths]
manifest = copy.deepcopy(manifest)
manifest['version'] = 'Z-Anatomy independent upper-limb nerve reference v1'
manifest['releaseStatus'] = 'active_independent_reference;anatomical_expert_review_pending'
manifest['packageInputSnapshots'] = snapshots
manifest['sourceCandidateManifestSha256'] = evidence['packageFileSha256']['atlas.json']
manifest['scope'] = proposal['scope']
active = dict(schemaVersion=1, datasetId=manifest['datasetId'],
    status='active_independent_reference;anatomical_expert_review_pending',
    descriptionTr=proposal['representationNoteTr'], labels=labels, relations=relations,
    sources=sources, inputSnapshots=snapshots,
    counts=dict(objects=127, primaryNerveObjects=54, contextNerveObjects=24,
                boneContextObjects=49, labels=127, exactDisplayLatin=110,
                unresolvedExactLatin=17, selectedBranchRelations=26),
    review=dict(geometry='Audited source/decoded export; source frame retained, no main fit',
                terminology='108 pinned numeric Latin +2 separate primary corrections;17 explicit nulls; editorial Turkish pending expert review',
                relationships='Selected cited branch facts; no fused junction/contact, full network or new motor innervation claim',
                anatomicalExpert='pending', productAcceptance='recorded in delivery status'),
    notAsserted=['Complete upper-limb/hand nerve network', 'Individually identified C5–T1 plexus contributions',
                 'Medial/lateral cord geometry', 'Individual numbered identities within muscular branch groups',
                 'Main-body registration or source-to-main continuity', 'Anatomical expert acceptance'])
outputs = {DATA: json.dumps(active, ensure_ascii=False, indent=2).encode()+b'\n',
           f'{PUBLIC}/atlas.json': json.dumps(manifest, indent=2).encode()+b'\n'}
for filename in ['anatomy.bin', 'anatomy.bin.gz', 'UPSTREAM-LICENSE.txt']:
    outputs[f'{PUBLIC}/{filename}'] = (ROOT/f'{SOURCE}/{filename}').read_bytes()
attribution = '''# Independent upper-limb nerve reference

The127 selected source objects are54 new named nerve/group curves,24 previously exported nerve objects re-evaluated in their original frame, and49 same-source bone-context objects. Exact object/part/concept names are in atlas.json; these are not127 distinct new anatomical structures. Source: Z-Anatomy/Startup.blend from the [Z-Anatomy archive](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/Z-Anatomy.zip). Pinned blend SHA256:9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd.

Attribution: **Z-Anatomy — The libre 3D atlas of anatomy — CC BY-SA4.0**; Gauthier Kervyn (design,3D,anatomy). Underlying model notice: **BodyParts3D — The Database Center for Life Science — CC BY-SA2.1 Japan**; Kousaku Okubo (original BodyParts3D model). The original database's current BY4.0 declaration does not relicense Z-Anatomy additions. Preserve these source notices and the verbatim [UPSTREAM-LICENSE.txt](./UPSTREAM-LICENSE.txt), retrieved2026-09-22 from the upstream License.txt.

Selected derivatives retain the upstream general [CC BY-SA4.0 declaration](https://creativecommons.org/licenses/by-sa/4.0/). Object-specific author/source lineage is not provided upstream; no blanket commercial clearance or relicensing is asserted. Upstream inner-ear/kidney exceptions are preserved in its complete notice and those object groups are not selected here. Application code and other datasets retain separate licenses.

Adaptations: curve-to-triangle conversion with source bevel/radii/splines, reflected winding correction, recomputed quantized normals, binary packing and gzip. All objects receive one orthonormal display-axis rotation, (x,y,z)→(x,z,-y), in metres. No main-body fitting, scale change, per-object placement, deformation, weld, cap, decimation or source repair is applied. Binary geometry remains byte-identical to the audited candidate. Bone defects and source group/truncated-curve scopes are retained.

127 dataset-scoped TR/EN labels accompany the source.110 exact Latin displays comprise108 pinned numeric terms and two separately cited IFAA corrections;17 numbered-bone terms remain unresolved.26 selected branch facts cite TTUHSC university teaching tables. These labels and facts do not establish model contact, a complete nerve network, root/cord identity or expert acceptance. See the source/metadata audits and docs/model/upper-limb-nerve-reference-review.md in the repository.
'''
outputs[f'{PUBLIC}/ATTRIBUTION.md'] = attribution.encode()
for path, content in outputs.items():
    if '--check' in sys.argv:
        assert (ROOT/path).read_bytes() == content, f'{path} stale'
    else:
        (ROOT/path).parent.mkdir(parents=True, exist_ok=True)
        (ROOT/path).write_bytes(content)
print(json.dumps(dict(mode='check' if '--check' in sys.argv else 'build', **active['counts'])))
