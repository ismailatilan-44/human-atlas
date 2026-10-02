#!/usr/bin/env python3
"""Candidate metadata for two actual left BP3D4.3 cords; no active writes."""
import argparse
import hashlib
import json
from pathlib import Path

D = Path(__file__).resolve().parent
R = D.parents[2]
UM_URL = 'https://sites.google.com/a/umich.edu/bluelink/curricula/m1-foundational-anatomy/sequence-7-neuroanatomy/brachial-plexus-subclavian-vessels-scalene-muscles/lablink'
TA_URL = 'https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv'
GEOMETRY = 'data/model-candidates/upper-limb-bp3d43-geometry-audit-v1/atlas.json'


def generate():
    f = json.loads((D / 'frozen-inputs.json').read_text())
    assert not f['activeCordConflicts'] and not f['activeLabelConflicts']
    for snapshot in f['inputSnapshots']:
        if '/objs/' in snapshot['path'] or snapshot['path'].endswith(('TA2.csv', 'FMA2Obj.txt')):
            assert hashlib.sha256((R / snapshot['path']).read_bytes()).hexdigest() == snapshot['sha256']
    labels, entities, objects, relations, optional = [], [], [], [], []
    exported = {p['id']: p for p in json.loads((R / GEOMETRY).read_text())['parts']}
    official_membership = (R / 'data/model-candidates/upper-limb-bp3d43-intake-v1/FMA2Obj.txt').read_text().splitlines()
    for o in f['intakeObjects']:
        cid, fj, bp = o['returnedConceptId'], o['sourcePartId'], o['returnedRepresentationId']
        lateral = cid == 'FMA45239'
        assert (cid, fj, bp) in [('FMA45239', 'FJ4274', 'BP29122'), ('FMA45241', 'FJ4275', 'BP29196')]
        term = o['termEvidence']
        assert term['numericId'] == (6415 if lateral else 6417)
        part_id = 'BP43-' + fj
        header = (R / o['path']).read_text().splitlines()[:10]
        assert '# File ID : ' + fj in header
        assert '# Representation ID : ' + bp in header
        assert '# Concept ID : ' + cid in header
        assert f'{cid}\tis_a\t{fj}' in official_membership
        assert exported[part_id]['conceptId'] == cid
        assert exported[part_id]['sourceId'] == fj and exported[part_id]['sourceRepresentationId'] == bp
        source_ref = {'sourceId': 'bp3d43-left-cord-objects', 'locator': o['path'] + ' / header lines2–7; FMA2Obj.txt line' + str(o['officialReturnedConceptMembership'][0]['line'])}
        label = {
            'ids': [cid], 'datasetId': None, 'datasetDecision': 'root_geometry_acceptance_required',
            'tr': 'Brakiyal pleksusun lateral kordonu' if lateral else 'Brakiyal pleksusun medial kordonu',
            'en': term['en'], 'la': term['la'], 'side': 'left',
            'aliases': [o['sourceName']], 'ta2TableId': term['numericId'],
            'sourcePartId': fj, 'sourceRepresentationId': bp, 'geometryPartIds': [part_id],
            'scopeNoteTr': 'Sol taraftaki özgün BP3D 4.3 kordon nesnesinin kaynak kapsamıdır; tam pleksus, kök katkıları veya dalların tamamı değildir. Anatomik uzman incelemesi bekler.',
            'evidence': [source_ref, {'sourceId': 'zanatomy-ta2-pinned', 'locator': f"TA2 {term['numericId']}; CSV line{term['csvLine']}; exact unsided English/Latin pair"}],
            'translationStatus': 'editorial_turkish_expert_review_pending',
            'expertReview': 'pending',
        }
        labels.append(label)
        entities.append({
            'id': cid, 'name': o['sourceName'], 'kind': 'nerve', 'side': 'left',
            'geometryPartIds': [part_id], 'representationStatus': 'candidate_geometry_unaccepted',
            'anatomicalCoverage': 'non_exhaustive', 'expertReview': 'pending',
            'sourcePartId': fj, 'sourceRepresentationId': bp, 'evidence': [source_ref],
        })
        objects.append({
            'conceptId': cid, 'sourceObjectPath': o['path'], 'sourceObjectSha256': o['sha256'],
            'sourcePartId': fj, 'sourceRepresentationId': bp, 'candidateExportPartId': part_id,
            'candidateManifest': GEOMETRY, 'sourceHeader': o['header'],
            'returnedMembership': o['officialReturnedConceptMembership'],
            'catalogDiscrepancy': o['catalogDiscrepancy'],
            'labelTerm': term,
            'mappingScope': 'Returned lateralized FMA concept ID is source identity; TA2 is an exact unsided terminology correspondence, not a new formal ontology crosswalk.',
            'sourceExtent': o['observedMesh'],
            'extentLimit': 'Raw index components are not named anatomical branches. Geometry owner separately audits exact-position connectivity, source defects, native frame and continuity.',
        })
        relations.append({
            'id': f'{cid}|part_of|atlas:left-brachial-plexus', 'subject': cid,
            'predicate': 'part_of', 'object': 'atlas:left-brachial-plexus',
            'status': 'candidate_source_supported', 'expertReview': 'pending',
            'evidence': [{'sourceId': 'umich-bluelink-brachial-plexus', 'locator': 'LEFT SIDE: divisions, cords and terminal branches; step9 identifying the medial/lateral/posterior cords of the brachial plexus'}],
            'qualifiers': {
                'semantics': 'Anatomical cord-to-plexus component relationship, not Blender collection or mesh selection membership',
                'laterality': 'Left is explicit in source OBJ header and university left-side lab section',
                'geometry': 'Does not extend or silently rewrite the existing ten-piece partial Z-Anatomy plexus selection',
                'scope': 'Typical anatomy; no complete plexus or full cord course assertion',
            },
        })
        root_name = 'lateral root of median nerve' if lateral else 'medial root of median nerve'
        optional.append({
            'id': f'{cid}|contributes_to|atlas:left-median-nerve', 'subject': cid,
            'predicate': 'contributes_to', 'object': 'atlas:left-median-nerve',
            'status': 'deferred_new_semantics_requires_root_review',
            'expertReview': 'pending',
            'evidence': [{'sourceId': 'umich-bluelink-brachial-plexus', 'locator': 'step12 / Median nerve / Note: formation from the lateral and medial contributions/roots from their respective cords'}],
            'qualifiers': {'viaStructure': root_name, 'viaStructureGeometry': 'not_proposed',
                           'semantics': 'Cord contributes through its named median-nerve root; not a direct branch_of or innervates claim',
                           'laterality': 'Left source identities only', 'rootLevelClaim': False,
                           'geometry': 'No root mesh, bridging segment, endpoint contact or fascicular path asserted'},
            'integrationGate': 'Requires explicit contribution predicate and visible via-root qualifier; otherwise retain as evidence only.',
        })
    relations.append({
        'id': 'atlas:left-musculocutaneous-nerve|branch_of|FMA45239',
        'subject': 'atlas:left-musculocutaneous-nerve', 'predicate': 'branch_of',
        'object': 'FMA45239', 'status': 'candidate_source_supported', 'expertReview': 'pending',
        'evidence': [{'sourceId': 'umich-bluelink-brachial-plexus', 'locator': 'step14 / Musculocutaneous nerve / Note: terminal branch of lateral cord'},
                     {'sourceId': 'ttuhsc-axilla-shoulder-tables', 'locator': 'Nerves table / musculocutaneous row / Source; lateral cord row / Branches'}],
        'qualifiers': {'semantics': 'Named terminal branch → anatomical parent cord',
                       'laterality': 'Same-side application to exact left source/canonical endpoints',
                       'geometry': 'No claim of physical joining between independently sourced BP3D and Z-Anatomy meshes',
                       'scope': 'No new motor territory or complete branch network inference'},
    })
    sources = f['intakeSources'] + [
        {'id': 'bp3d43-left-cord-objects', 'title': 'Official BP3D4.3 returned left cord objects',
         'url': 'https://lifesciencedb.jp/bp3d/', 'version': 'Data4.3 / Objects4.3 / FMA3.0',
         'use': 'Two original OBJ headers and official is_a file-membership rows only; no branch relation inferred from membership',
         'paths': [o['path'] for o in f['intakeObjects']]},
        {'id': 'zanatomy-ta2-pinned', 'url': TA_URL,
         'sha256': '0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974',
         'use': 'Exact numeric unsided cord terms; Turkish editorial translation; no fabricated sided Latin'},
        {'id': 'umich-bluelink-brachial-plexus', 'title': 'University of Michigan BlueLink — Brachial Plexus LabLink',
         'url': UM_URL, 'retrievedOn': '2026-10-02',
         'use': 'Selected anatomical component/branch/contribution facts with step locators only; no page prose, donor images or multimedia redistributed'},
        {'id': 'ttuhsc-axilla-shoulder-tables', 'url': 'https://anatomy.ttuhscep.edu/musculoskeletal_system/axilla_tables.html',
         'retrievedOn': '2026-10-02', 'use': 'Musculocutaneous branch parent corroboration; row/column locators only'},
    ]
    proposal = {
        'schemaVersion': 1, 'status': 'candidate_only_geometry_gate_pending',
        'scope': 'Only two left BP3D4.3 cord objects; other neural/root/right-side objects excluded',
        'datasetId': None, 'datasetDecision': 'root_may_activate_only_after_separate_geometry_acceptance',
        'labels': labels, 'entities': entities, 'relations': relations, 'deferredRelations': optional,
        'proposedPredicateIfNeeded': {'id': 'contributes_to', 'direction': 'cord → median nerve via named root',
                                     'transitive': False, 'outgoingLabelTr': 'Katkı verdiği sinir',
                                     'incomingLabelTr': 'Katkı veren kordon', 'requiredVisibleQualifier': 'viaStructure'},
        'activationGates': ['Geometry/native-frame/continuity review by geometry owner and root',
                            'Retain separate BP3D4.3 CC BY-SA2.1 Japan attribution',
                            'Preserve partial scope of existing plexus selection',
                            'No root contribution targets closed; no right mirroring or other neural file activation'],
    }
    evidence = {
        'schemaVersion': 1, 'sources': sources, 'inputSnapshots': f['inputSnapshots'],
        'objects': objects, 'existingGraphEndpointSnapshot': f['activeEndpointEntities'],
        'identityConflicts': f['activeCordConflicts'], 'labelConflicts': f['activeLabelConflicts'],
        'identityDecision': 'Retain actual returned FMA45239/FMA45241 with their FJ/BP pairs. No existing canonical concept conflict. Catalog FMA11195 does not override returned source identity.',
        'notInferred': ['complete cord extent', 'C5–T1 ventral root contributions', 'right-sided counterpart', 'branch names from component count', 'geometric contact or shared-source connectivity', 'new innervation'],
    }
    active_ids = {e['id'] for e in f['activeEndpointEntities']}
    ids = {e['id'] for e in entities}
    assert ids == {'FMA45239', 'FMA45241'} and not ids & active_ids
    assert len(labels) == 2 and len(relations) == 3 and len(optional) == 2
    assert all(r['subject'] in ids | active_ids and r['object'] in ids | active_ids for r in relations + optional)
    assert all(l['side'] == 'left' for l in labels)
    assert all(r['predicate'] != 'innervates' for r in relations + optional)
    assert not any(r['object'] == 'atlas:left-median-nerve' for r in relations)
    report = {'status': 'passed', 'labels': 2, 'newSourceConceptIds': 2,
              'existingIdentityConflicts': 0, 'actualSourceFjBpFmaPairsVerified': 2,
              'directAnatomicalRelations': 3, 'separatelyDeferredContributionFacts': 2,
              'rightSideObjects': 0, 'rootEntitiesAdded': 0, 'innervationAdded': 0,
              'geometryAccepted': False, 'applicationChecksRun': False,
              'anatomicalExpertReview': 'pending'}
    return {'proposal.json': proposal, 'source-evidence.json': evidence, 'validation.json': report}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, data in generate().items():
        content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
        path = D / name
        if args.check:
            assert path.read_text() == content, name
        else:
            path.write_text(content)
    print('PASS: 2 left cord labels/IDs, 3 direct relation candidates, 2 deferred contributions; geometry unaccepted')


if __name__ == '__main__':
    main()
