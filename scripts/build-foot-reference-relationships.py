"""Add bounded, cited foot relationships without changing source geometry.

Articulation is symmetric bone-level knowledge, not a segmented joint or a
measured specimen contact. Ligament attachments name bones/regions only.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'public/models/lower-limb-nerve-reference/atlas.json'
METADATA = 'data/anatomy/lower-limb-reference.json'
OUTPUT = 'data/model-candidates/foot-reference-relationships-v1'
manifest = json.loads((ROOT / MANIFEST).read_text())
metadata = json.loads((ROOT / METADATA).read_text())
concepts = {c['id']: c for c in manifest['concepts']}
labels = {i: label for label in metadata['labels'] for i in label['ids']}
dataset = metadata['datasetId']
sources = [dict(
    id='ttuhsc-foot-osteology', title='TTUHSC anatomy tables — foot osteology',
    url='https://anatomy.ttuhscep.edu/musculoskeletal_system/leg_tables.html',
    retrievedOn='2026-10-02', locator='Osteology table; selected bone and structure rows',
    use='Selected bone-level articulation facts; no source prose or images redistributed; no specimen contact or joint segmentation inferred'),
    dict(id='golano-ankle-ligaments-2010', title='Golanó et al. — Anatomy of the ankle ligaments (2010)',
    url='https://doi.org/10.1007/s00167-010-1100-x',
    inspectedUrl='https://diposit.ub.edu/bitstreams/2e6e7803-acea-4dc4-8832-b63ced732f00/download',
    doi='10.1007/s00167-010-1100-x', retrievedOn='2026-10-02',
    locator='Lateral collateral ligaments; journal pages 559–560, PDF pages 3–4',
    use='Selected attachment bone/region facts; no article figures, measurements or text redistributed; no model footprint or fascicle validation')]

# Each fact is stored once per side; traversal works in both directions.
articulations = [
    ('talus','tibia','talus row, Notes'),
    ('talus','fibula','talus row, Notes'),
    ('talus','calcaneus','talus/body and subtalar joint rows'),
    ('talus','navicular-bone','talus/head and navicular rows'),
    ('navicular-bone','medial-cuneiform-bone','navicular row, Notes; medial cuneiform row'),
    ('navicular-bone','intermediate-cuneiform-bone','navicular row, Notes; middle cuneiform row'),
    ('navicular-bone','lateral-cuneiform-bone','navicular row, Notes; lateral cuneiform row'),
    ('cuboid-bone','calcaneus','cuboid row, Notes'),
    ('cuboid-bone','fourth-metatarsal-bone','cuboid row, Notes'),
    ('cuboid-bone','fifth-metatarsal-bone','cuboid row, Notes'),
]
ordinals = ['first','second','third','fourth','fifth']
for digit, ordinal in enumerate(ordinals, 1):
    proximal = f'proximal-phalanx-of-{ordinal}-finger-of-foot'
    distal = f'distal-phalanx-of-{ordinal}-finger-of-foot'
    articulations.append((f'{ordinal}-metatarsal-bone', proximal,
                         'metatarsals/head and phalanx/base rows; corresponding digit'))
    segments = [proximal, distal] if digit == 1 else [
        proximal, f'middle-phalanx-of-{ordinal}-finger-of-foot', distal]
    for a, b in zip(segments, segments[1:]):
        articulations.append((a,b,'phalanx rows, Notes and base/head; next segment within the same digit'))
assert len(articulations) == 24

attachments = [
    ('anterior-talofibular-ligament','fibula','Anterior talofibular ligament section, p559',
     'Fibulanın lateral malleolünün ön kenarı; modelde ayrı tutunma yüzeyi/koordinatı işaretlenmedi.'),
    ('anterior-talofibular-ligament','talus','Anterior talofibular ligament section, p559',
     'Talus gövdesinin lateral eklem yüzeyi önündeki bölge; modelde ayrı tutunma yüzeyi/koordinatı işaretlenmedi.'),
    ('posterior-talofibular-ligament','fibula','Posterior talofibular ligament section, p560',
     'Lateral malleolün medial yüzündeki malleolar fossa; modelde ayrı tutunma yüzeyi/koordinatı işaretlenmedi.'),
    ('posterior-talofibular-ligament','talus','Posterior talofibular ligament section, p560–561',
     'Talusun posterolateral bölgesi; lif kapsamı ve varyasyonlar bu modelde doğrulanmadı.'),
    ('calcaneofibular-ligament','fibula','Calcaneofibular ligament section, p560',
     'Fibulanın lateral malleolünün ön bölgesi; modelde ayrı tutunma yüzeyi/koordinatı işaretlenmedi.'),
    ('calcaneofibular-ligament','calcaneus','Calcaneofibular ligament section, p560',
     'Kalkaneusun lateral yüzünün arka bölgesi; modelde ayrı tutunma yüzeyi/koordinatı işaretlenmedi.'),
]

relations = []
for side, suffix in [('left','l'),('right','r')]:
    for a,b,locator in articulations:
        subject, obj = f'zanatomy:{a}-{suffix}', f'zanatomy:{b}-{suffix}'
        assert labels[subject]['side'] == labels[obj]['side'] == side
        assert labels[subject]['componentRole'] == labels[obj]['componentRole'] == 'bone_context'
        relations.append(dict(id=f'{subject}|articulates_with|{obj}', subject=subject,
            predicate='articulates_with', object=obj, datasetId=dataset, status='source_supported',
            expertReview='pending', evidence=[dict(sourceId=sources[0]['id'],locator=f'Osteology table; {locator}')],
            qualifiers=dict(symmetric=True, transitive=False, scope='Typical bone-level anatomy, not specimen validation',
                laterality=side, geometryContactMeasured=False, jointGeometryClaim=False,
                sourceMapping='Preserved named same-side source objects; expert correspondence pending')))
    for ligament,bone,locator,note in attachments:
        subject, obj = f'atlas:{side}-{ligament}', f'zanatomy:{bone}-{suffix}'
        assert labels[subject]['side'] == labels[obj]['side'] == side
        assert labels[subject]['componentRole'] == 'ligament' and labels[obj]['componentRole'] == 'bone_context'
        relations.append(dict(id=f'{subject}|attaches_to|{obj}', subject=subject, predicate='attaches_to',
            object=obj, datasetId=dataset, status='source_supported', expertReview='pending',
            attachmentNoteTr=note, evidence=[dict(sourceId=sources[1]['id'],locator=locator)],
            qualifiers=dict(scope='Typical named attachment bone/region, not specimen validation',
                laterality=side, footprintSegmented=False, coordinatesAsserted=False,
                fasciclesVerified=False, anatomicalVariation='Not modeled or accepted by this bounded package')))
assert len(relations) == len({r['id'] for r in relations}) == 60
assert all(r['subject'] in concepts and r['object'] in concepts for r in relations)
for r in relations:
    assert all(concepts[i]['elements'] for i in [r['subject'],r['object']])
    if r['predicate'] == 'articulates_with':
        assert not any(s['subject'] == r['object'] and s['object'] == r['subject']
                       and s['predicate'] == r['predicate'] for s in relations)

predicates = [dict(id='articulates_with', symmetric=True, transitive=False,
    meaning='Named bones participate in a sourced anatomical articulation; no surface, capsule, cartilage or contact measurement implied'),
    dict(id='attaches_to', symmetric=False, transitive=False,
    meaning='Ligament attaches to named bone/region; bone geometry is not an attachment footprint')]
proposal = dict(schemaVersion=1, datasetId=dataset, discoveryRevision='41723bdf937ce50976c118230b0a29441700d4a2',
    inputSnapshots=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest())
                    for p in [MANIFEST,'scripts/build-foot-reference-relationships.py']],
    summary=dict(articulationFactsPerSide=24, articulationRelations=48, attachmentRelations=12,
                 totalNewRelations=60, expertAccepted=0),
    predicates=predicates, sources=sources, relations=relations,
    excludedClaims=['Complete foot joint network','Cuneiform-to-metatarsal digit mapping from generic wording',
      'Articular cartilage/capsule or ligament fascicles','Segmented attachment footprints or coordinates',
      'Measured model contact or specimen connectivity','Automatic transitive articulation',
      'Cross-dataset or cross-side relationships','Named anatomical expert acceptance'])
path = ROOT / OUTPUT / 'proposal.json'
content = json.dumps(proposal,ensure_ascii=False,indent=2)+'\n'
if '--check' in sys.argv:
    assert path.read_text() == content, 'Foot relationship proposal is stale'
else:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content)
if '--apply' in sys.argv:
    original = {r['id']:r for r in metadata['relations']}
    for r in relations:
        assert r['id'] not in original or original[r['id']] == r, f'Conflicting existing relation {r["id"]}'
        if r['id'] not in original: metadata['relations'].append(r)
    existing = {s['id']:s for s in metadata['sources']}
    for s in sources:
        assert s['id'] not in existing or existing[s['id']] == s, f'Conflicting source {s["id"]}'
        if s['id'] not in existing: metadata['sources'].append(s)
    metadata['relationshipPredicates'] = [metadata['predicate'],*predicates]
    metadata['counts']['articulationRelations'] = 48
    metadata['counts']['attachmentRelations'] = 12
    metadata['counts']['totalRelations'] = len(metadata['relations'])
    metadata['review']['relationshipEvidence'] = ('12 preserved same-side nerve branches; 48 sourced bone-level '
        'articulations and 12 ligament-to-bone attachments; no measured contact, footprints or expert acceptance')
    metadata['notAsserted'] = [x for x in metadata['notAsserted'] if x != 'Bone adjacency, ligament attachments or joint relationships']
    claim = 'Complete bone articulation/ligament network; segmented joint surfaces or attachment coordinates'
    if claim not in metadata['notAsserted']: metadata['notAsserted'].append(claim)
    (ROOT/METADATA).write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
if '--check' in sys.argv:
    active = {r['id']:r for r in metadata['relations']}
    assert all(active.get(r['id']) == r for r in relations), 'Proposed relationships not integrated'
    assert metadata['counts']['totalRelations'] == len(metadata['relations']) == 72
print(json.dumps(proposal['summary']))
