"""Integrate the frozen source-reviewed proposal; preserve existing identities."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = 'data/model-candidates/foot-soft-tissue-metadata-v1/activation-proposal.json'
MANIFEST = 'public/models/lower-limb-nerve-reference/atlas.json'
read = lambda p: json.loads((ROOT/p).read_text())
proposal = read(AUDIT)
manifest = read(MANIFEST)
assert len(manifest['parts']) == 119
concepts = {c['id']:c for c in manifest['concepts']}
parts = {p['id']:p for p in manifest['parts']}

def merge(rows, additions, key):
    existing = {key(r):r for r in rows}
    assert len(existing) == len(rows), 'Duplicate existing identity'
    for row in additions:
        identity = key(row)
        assert identity not in existing or existing[identity] == row, f'Conflicting identity {identity}'
        if identity not in existing:
            rows.append(copy.deepcopy(row))
            existing[identity] = row

def merge_sources(rows, additions):
    existing = {s['id']:s for s in rows}
    for source in additions:
        if source['id'] in existing:
            assert existing[source['id']]['url'] == source['url'], 'Conflicting source URL'
            continue
        source = copy.deepcopy(source)
        if source.get('path'):
            source['sha256'] = hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()
        rows.append(source)
        existing[source['id']] = source

main = read('data/anatomy/labels.json')
merge(main['entries'], proposal['mainLabelProposals'], lambda l:tuple(l['ids']))
assert len(main['entries']) == 399
reference = read('data/anatomy/lower-limb-reference.json')
for label in proposal['referenceLabelProposals']:
    cid = label['ids'][0]
    assert concepts[cid]['elements'] == label['geometryPartIds']
    assert parts[label['geometryPartIds'][0]]['sourceObject'] == label['sourceObject']
merge(reference['labels'], proposal['referenceLabelProposals'], lambda l:tuple(l['ids']))
relations = [{k:v for k,v in r.items() if k != 'datasetId'}
             for r in proposal['relationProposals'] if r['datasetId'] == reference['datasetId']]
merge(reference['relations'], relations, lambda r:r['id'])
merge_sources(reference['sources'], proposal['sources'])
assert len(reference['labels']) == 119 and len(reference['relations']) == 84
assert all(r['subject'] in concepts and r['object'] in concepts for r in reference['relations'])
reference['descriptionTr'] = ('Kaynağın kendi kemik bağlamındaki kısmi sinir/arter seyirleri, seçilmiş ayak bileği '
    'bağları, ayak kasları ve sesamoid grupları. Ana gövdeye yerleştirilmiş değildir; tam ağ veya bütün ayak ayrıntısı değildir.')
reference['counts'].update(labels=119, muscleObjects=30, sesamoidGroupObjects=2,
    boneContextObjects=65, verifiedDisplayLatin=83, unresolvedSpecificLatin=36,
    muscleOriginRelations=4, muscleInsertionRelations=4, muscleInnervationRelations=4, totalRelations=84)
assert sum(l['la'] is not None for l in reference['labels']) == 83
reference['review']['terminology'] = ('119 TR/EN labels;83 exact pinned numeric-table Latin display terms; '
    '34 digit-specific and two source-typo Latin displays unresolved; Turkish editorial, expert pending')
reference['review']['relationshipEvidence'] = ('12 nerve branches,48 bone articulations,12 ligament attachments; '
    'four muscle origins,four insertions,four innervations from selected direct teaching facts. '
    'No model footprints,contact,motor branch geometry or expert acceptance.')
for predicate in ['originates_at','inserts_at','innervates']:
    definition = dict(id=predicate, symmetric=False, transitive=False,
        meaning='Selected directly sourced typical anatomy; not specimen or geometric contact validation')
    if not any(p['id'] == predicate for p in reference['relationshipPredicates']):
        reference['relationshipPredicates'].append(definition)
reference['notAsserted'] = ['Complete muscle innervation or skin territories' if x == 'Muscle innervation or skin territories'
    else x for x in reference['notAsserted']]
for limit in ['Independent numbered identities within compound muscle/sesamoid source objects',
              'Whole-muscle relationship inheritance to individual source heads']:
    if limit not in reference['notAsserted']: reference['notAsserted'].append(limit)
snapshot_paths = [AUDIT, MANIFEST, 'scripts/integrate-foot-soft-tissue.py',
    'data/model-candidates/foot-soft-tissue-source-audit-v1/new-object-mapping.json',
    'data/model-candidates/foot-soft-tissue-source-audit-v1/evaluated-candidates.json']
reference['softTissueInputSnapshots'] = [dict(path=p, sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in snapshot_paths]
reference['softTissueInputNote'] = 'Frozen pre-activation proposal preserves intake inputs; current candidate proposal can refresh active hashes independently.'
sources = read('data/anatomy/sources.json')
merge_sources(sources, proposal['sources'])
module = dict(schemaVersion=1, scope='Selected bilateral abductor hallucis and extensor hallucis brevis origins/insertions; '
    'whole-bone context and named regions, not footprints or complete foot network', entities=[],
    relations=[{k:v for k,v in r.items() if k != 'datasetId'} for r in proposal['relationProposals'] if r['datasetId'] == 'male-body'],
    sourceAudit=AUDIT)
assert len(module['relations']) == 8
for path, value in [('data/anatomy/labels.json',main), ('data/anatomy/lower-limb-reference.json',reference),
                    ('data/anatomy/sources.json',sources), ('data/anatomy/foot-muscles.json',module)]:
    content = json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    if '--check' in sys.argv: assert (ROOT/path).read_text() == content, f'{path} needs integration'
    else: (ROOT/path).write_text(content)
print('PASS 399 main labels;119 reference labels;84 reference and8 new main relations; source scope preserved')
