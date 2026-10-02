"""Integrate frozen source-scoped support labels and selected teaching facts."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = 'data/model-candidates/foot-support-metadata-v1/activation-proposal.json'
MANIFEST = 'public/models/lower-limb-nerve-reference/atlas.json'
read = lambda p: json.loads((ROOT/p).read_text())
sha = lambda p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
proposal, manifest = read(AUDIT), read(MANIFEST)
EXCLUDED = {'zanatomy:intersesamoid-ligament-l', 'zanatomy:intersesamoid-ligament-r'}
assert len(manifest['parts']) == 137
assert len(proposal['referenceLabelProposals']) == 20
assert len(proposal['mainLabelProposals']) == 2
assert len(proposal['relationProposals']) == 32
concepts = {c['id']: c for c in manifest['concepts']}
parts = {p['id']: p for p in manifest['parts']}
main_manifest = read('public/models/atlas.json')
main_concepts = {c['id']: c for c in main_manifest['concepts']}

def merge(rows, additions, key):
    existing = {key(r): r for r in rows}
    assert len(existing) == len(rows), 'Duplicate identity'
    for row in additions:
        identity = key(row)
        assert identity not in existing or existing[identity] == row, f'Conflicting identity {identity}'
        if identity not in existing:
            rows.append(copy.deepcopy(row))
            existing[identity] = row

def sources(rows):
    existing = {s['id']: s for s in rows}
    for source in proposal['sources']:
        if source['id'] in existing:
            assert existing[source['id']]['url'] == source['url'], 'Conflicting source URL'
            continue
        source = copy.deepcopy(source)
        if source.get('path'): source['sha256'] = sha(source['path'])
        rows.append(source)
        existing[source['id']] = source

main = read('data/anatomy/labels.json')
bindings = {b['conceptId']: b for b in proposal['mainBindingAudit']}
for label in proposal['mainLabelProposals']:
    assert main_concepts[label['ids'][0]]['elements'] == bindings[label['ids'][0]]['partIds']
merge(main['entries'], proposal['mainLabelProposals'], lambda r: tuple(r['ids']))
assert len(main['entries']) == 401
reference = read('data/anatomy/lower-limb-reference.json')
active_reference_labels = [l for l in proposal['referenceLabelProposals'] if l['ids'][0] not in EXCLUDED]
assert len(active_reference_labels) == 18 and not (EXCLUDED & set(concepts))
for label in active_reference_labels:
    cid = label['ids'][0]
    assert concepts[cid]['elements'] == label['geometryPartIds']
    assert parts[label['geometryPartIds'][0]]['sourceObject'] == label['sourceObject']
    assert parts[label['geometryPartIds'][0]]['side'] == label['side']
    assert label['representationNoteTr'] and label['la']
merge(reference['labels'], active_reference_labels, lambda r: tuple(r['ids']))
reference_relations = [{k: v for k, v in r.items() if k != 'datasetId'}
    for r in proposal['relationProposals'] if r['datasetId'] == reference['datasetId']]
assert len(reference_relations) == 28
for relation in reference_relations:
    assert relation['subject'] in concepts and relation['object'] in concepts
    assert relation['predicate'] == 'attaches_to' and relation['attachmentNoteTr']
merge(reference['relations'], reference_relations, lambda r: r['id'])
assert len(reference['labels']) == 137 and len(reference['relations']) == 112
assert sum(l['la'] is not None for l in reference['labels']) == 101
sources(reference['sources'])
reference['descriptionTr'] = ('Kaynağın kendi kemik bağlamındaki kısmi sinir/arter seyirleri, seçilmiş bağlar, '
    'ayak kasları, sesamoid grupları, retinakulumlar ve plantar aponevroz. '
    'Ana gövdeye yerleştirilmiş değildir; tam ağ veya bütün ayak ayrıntısı değildir.')
reference['counts'].update(labels=137, verifiedDisplayLatin=101, unresolvedSpecificLatin=36,
    retinaculumObjects=10, plantarAponeurosisObjects=2, ligamentObjects=12,
    attachmentRelations=40, totalRelations=112)
reference['review']['terminology'] = ('137 TR/EN labels; 101 exact pinned numeric-table Latin terms; '
    '34 digit-specific and two source-typo Latin displays unresolved; Turkish editorial, expert pending')
reference['review']['supportGeometry'] = ('18 source-preserved objects; two source-named intersesamoid meshes '
    'withheld because their source extent does not bridge the modeled sesamoid components. Open inferior fibular retinacula and '
    'plantar aponeuroses remain source sheets, not volumetric or layered reconstructions. '
    'Selected teaching attachment facts do not assert model contact, footprints, tunnel contents or expert acceptance.')
reference['review']['relationshipEvidence'] = ('12 nerve branches, 48 bone articulations, 40 selected ligament/fascial '
    'attachments and12 muscle facts. Selected typical teaching anatomy, not model contact, complete endpoint sets or expert acceptance.')
for predicate in reference['relationshipPredicates']:
    if predicate['id'] == 'attaches_to':
        predicate['meaning'] = 'Sourced structure attaches to named bone/region; bone geometry is not an attachment footprint'
for limit in ['Complete retinacular tunnels, contents and tendon relationships',
              'Volumetric or layer-complete plantar fascia and ligament representations']:
    if limit not in reference['notAsserted']: reference['notAsserted'].append(limit)
paths = [AUDIT, MANIFEST, 'scripts/integrate-foot-supports.py',
    'data/model-candidates/foot-support-source-audit-v1/new-object-mapping.json',
    'data/model-candidates/foot-support-source-audit-v1/evaluated-candidates.json']
reference['supportInputSnapshots'] = [dict(path=p, sha256=sha(p)) for p in paths]
reference['supportInputNote'] = 'Frozen pre-activation proposal; source-sheet limits retained; selected teaching facts only.'
reference['excludedSupportCandidates'] = [dict(conceptId=cid,
    reason='Source mesh does not span the two modeled sesamoid components; not accepted as connecting geometry',
    sourceReview='data/model-candidates/foot-support-source-audit-v1/intersesamoid-placement.json') for cid in sorted(EXCLUDED)]
bibliography = read('data/anatomy/sources.json')
sources(bibliography)
main_relations = [{k: v for k, v in r.items() if k != 'datasetId'}
    for r in proposal['relationProposals'] if r['datasetId'] == 'male-body']
assert len(main_relations) == 4
for relation in main_relations:
    assert relation['subject'] in main_concepts and relation['object'] in main_concepts
    assert relation['predicate'] == 'attaches_to' and relation['attachmentNoteTr']
module = dict(schemaVersion=1, scope='Selected bilateral long plantar ligament attachment bone/region facts; '
    'not a complete endpoint set, source-specimen geometry or footprint acceptance', entities=[],
    relations=main_relations, sourceAudit=AUDIT)
for path, value in [('data/anatomy/labels.json', main),
                    ('data/anatomy/lower-limb-reference.json', reference),
                    ('data/anatomy/sources.json', bibliography), ('data/anatomy/foot-supports.json', module)]:
    content = json.dumps(value, ensure_ascii=False, indent=2)+'\n'
    if '--check' in sys.argv: assert (ROOT/path).read_text() == content, f'{path} needs integration'
    else: (ROOT/path).write_text(content)
print('PASS 18 active/2 withheld reference labels and2 main labels; 137/101 reference terms; 28 reference and4 main relations')
