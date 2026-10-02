#!/usr/bin/env python3
"""Add exact scoped reference observations; never modify the version-1 source."""
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
R = D.parents[2]
MANIFEST = 'data/model-candidates/upper-limb-nerve-source-audit-v1/atlas.json'
LABELS = 'data/model-candidates/upper-limb-nerve-metadata-v1/proposal.json'
EVIDENCE = 'data/model-candidates/upper-limb-nerve-metadata-v1/source-evidence.json'
DATASET = 'upper-limb-nerve-reference'
OPEN_NAMES = ['Lateral cord of brachial plexus', 'Medial cord of brachial plexus'] + [
    f'{level} root contribution to brachial plexus' for level in ['C5', 'C6', 'C7', 'C8', 'T1']
]


def read(path):
    return json.loads((R / path).read_text())


def generate():
    frozen = json.loads((D / 'frozen-inputs.json').read_text())
    baseline = frozen['baseline']
    hashes = {x['path']: x['sha256'] for x in frozen['sources']}
    for path in (MANIFEST, LABELS, EVIDENCE):
        assert hashlib.sha256((R / path).read_bytes()).hexdigest() == hashes[path], path
    manifest, labels, source_evidence = read(MANIFEST), read(LABELS), read(EVIDENCE)
    assert manifest['datasetId'] == DATASET and not manifest['compatibleWithMainAtlas']
    assert manifest['registration'] is None
    assert len(manifest['parts']) == len(manifest['concepts']) == 127
    parts = {p['id']: p for p in manifest['parts']}
    concepts = {c['id']: c for c in manifest['concepts']}
    evidence = {e['conceptId']: e for e in source_evidence['entries']}
    candidates = {}
    for label in labels['labels']:
        if label['ta2TableId'] is None:
            continue
        key = label['ta2TableId'], label['side']
        assert key not in candidates, 'No ambiguous term/side collisions allowed'
        candidates[key] = label
    targets = copy.deepcopy(baseline['targets'])
    additions, unchanged_ids, unmatched_sources = [], [], []
    used_concepts = set()
    for target, previous in zip(targets, baseline['targets']):
        label = candidates.get((target['termEvidence'].get('numericId'), target['side']))
        if not label:
            unchanged_ids.append(target['id'])
            continue
        # Three distinct identity gates: exact numeric term+pair, side, and
        # exact source-object/part membership with group scope compatibility.
        term = target['termEvidence']
        assert term['en'] == label['en'] == label['sourceEnglish'] == target['name']
        assert term['la'] == label['la'] and label['la'] is not None
        assert label['datasetId'] == DATASET
        cid = label['ids'][0]
        concept, ev = concepts[cid], evidence[cid]
        assert concept['elements'] == label['geometryPartIds'] == [ev['partId']]
        part = parts[ev['partId']]
        assert part['conceptId'] == cid and part['sourceObject'] == label['sourceObject'] == ev['sourceObject']
        assert part['side'] == label['side'] == target['side']
        assert part['vertexCount'] > 0 and part['indexCount'] > 0
        group = ev['representationKind'] == 'source_group_of_muscular_branches'
        assert (target['targetKind'] == 'named_group') == group
        assert target['name'] not in OPEN_NAMES
        used_concepts.add(cid)
        rationale = {
            'numericTerm': term['numericId'], 'exactEnglishPair': term['en'],
            'exactLatinPair': term['la'], 'side': target['side'],
            'termEvidence': copy.deepcopy(term), 'labelEvidence': label['evidence'],
            'sourceIdentity': {'sourceObject': part['sourceObject'], 'partId': part['id'], 'conceptId': cid},
            'scopeGate': 'Plural target group matches plural authored source group; individual branch identities remain unassigned' if group else 'Named source object and target agree at the same unsided numeric term and side; full course/detail acceptance remains open',
            'sourceExtentLocator': f"{EVIDENCE} / entries / conceptId={cid} / sourceExtent",
            'notUsed': ['fuzzy name similarity', 'source collection hierarchy', 'geometric proximity', 'group-to-individual substitution', 'BP3D 4.3 intake'],
        }
        binding = {
            'datasetId': DATASET, 'conceptId': cid, 'sourceName': concept['name'],
            'sourceManifest': MANIFEST, 'sourceManifestSha256': hashes[MANIFEST],
            'runtimeManifestExpected': 'public/models/upper-limb-nerve-reference/atlas.json',
            'runtimeAcceptance': 'root_owned; candidate_source_observation_only',
            'partIds': concept['elements'], 'sourceConcept': concept,
            'observedParts': [{k: part[k] for k in ('id', 'name', 'conceptId', 'system', 'vertexCount', 'indexCount', 'bounds', 'sourceObject')}],
            'status': 'source_reference_membership_observed',
            'sourceRole': part['role'], 'representationKind': ev['representationKind'],
            'selectionScope': 'source_group_not_individual_branches' if group else 'single_named_source_object_extent',
            'detailAcceptance': 'pending; source extent and nonempty geometry do not establish complete target anatomy',
            'frame': {'datasetId': DATASET, 'independentReference': True, 'compatibleWithMainAtlas': False, 'registration': None, 'coordinateSystem': manifest['coordinateSystem']},
            'sourceExtent': ev['sourceExtent'],
            'sourceScope': part['sourceScope'], 'scopeNoteTr': label['scopeNoteTr'],
            'bindingRationale': rationale,
        }
        target['representations'].append(binding)
        target['bindingStatus'] = 'observed_manifest_or_anchor'
        target['bindingObservationHistory'] = [{
            'scopeVersion': baseline['scopeVersion'], 'bindingStatus': previous['bindingStatus'],
            'representationCount': len(previous['representations']), 'sourcePath': frozen['baselinePath'],
            'sourceSha256': hashes[frozen['baselinePath']],
            'note': 'All previous representation objects and relationship observations remain unchanged in this record.',
        }]
        target['addedReferenceObservation'] = {
            'version': 'upper-limb-target-seed-v2', 'datasetId': DATASET,
            'sourceRole': part['role'], 'mainBodyGeometryChanged': False,
            'completeTargetAccepted': False,
        }
        additions.append({
            'targetId': target['id'], 'name': target['name'], 'side': target['side'],
            'conceptId': cid, 'partId': part['id'], 'sourceObject': part['sourceObject'],
            'sourceRole': part['role'], 'previousBindingStatus': previous['bindingStatus'],
            'previousRepresentationCount': len(previous['representations']),
            'newlyGeometryObserved': not any(b['partIds'] for b in previous['representations']),
            'sourceGroup': group, 'rationale': rationale,
        })
    for label in labels['labels']:
        if label['ids'][0] not in used_concepts:
            unmatched_sources.append({'sourceObject': label['sourceObject'], 'conceptId': label['ids'][0], 'partIds': label['geometryPartIds'], 'numericTerm': label['ta2TableId'], 'reason': 'No exact numeric-term/same-side requirement in unchanged352 scope; custom/null or unrelated context is not a substitute.'})
    for old, new in zip(baseline['targets'], targets):
        if new['id'] in unchanged_ids:
            assert new == old
        else:
            assert new['representations'][:-1] == old['representations']
            rebuilt = copy.deepcopy(new)
            rebuilt['representations'] = rebuilt['representations'][:-1]
            rebuilt['bindingStatus'] = old['bindingStatus']
            del rebuilt['bindingObservationHistory'], rebuilt['addedReferenceObservation']
            assert rebuilt == old, 'Only additive representation and versioned observational status may differ'
        assert not new['complete'] and not new['anatomicallyAccepted'] and not new['absenceClaim']
        assert new['expertReview'] == 'pending'
    protected = [t for t in targets if t['name'] in OPEN_NAMES]
    assert len(protected) == 14 and all(not t['representations'] for t in protected)
    assert len(targets) == len({t['id'] for t in targets}) == 352
    assert len(additions) == 80 and len(unchanged_ids) == 272
    assert sum(x['newlyGeometryObserved'] for x in additions) == 46
    assert sum(x['sourceGroup'] for x in additions) == 8
    assert len(unmatched_sources) == 47
    corrected = [t for t in targets if t['termEvidence'].get('numericId') == 6442]
    assert len(corrected) == 2 and all(t['termEvidence']['correctionEvidence'] for t in corrected)
    statuses = dict(sorted(Counter(t['bindingStatus'] for t in targets).items()))
    summary = dict(baseline['summary'])
    summary.update(
        bindingStatusCounts=statuses, observedMeshTargets=sum(any(b['partIds'] for b in t['representations']) for t in targets),
        addedReferenceBindings=80, targetsUnchanged=272, newlyGeometryObservedTargets=46,
        previouslyUnboundNowReferenceBound=38, previouslyMeshlessNowReferenceBound=8,
        additionalReferenceToPreviouslyGeometrized=34, sourceGroupBindings=8,
        addedPrimaryNerveBindings=46, addedContextNerveBindings=24, addedContextBoneBindings=10,
        expertAccepted=0, anatomicallyAccepted=0,
        mainBodyGeometryChanges=0, newLabels=0, newRelationships=0, newGeometry=0,
    )
    result = copy.deepcopy(baseline)
    result.update(
        scopeVersion='upper-limb-target-seed-v2',
        status='candidate_versioned_source_reference_observations;root_activation_pending',
        previousScopeVersion=baseline['scopeVersion'], previousSummary=baseline['summary'],
        targets=targets, summary=summary,
        versionEvidence={'baselinePath': frozen['baselinePath'], 'baselineSha256': hashes[frozen['baselinePath']], 'capturedAt': frozen['capturedAt'], 'inputs': frozen['sources']},
    )
    result['caveats'] += [
        'Version2 adds observations in an independent source reference; it does not give the same concepts main-body geometry.',
        '80 added bindings include8 plural muscular-branch groups; none establish individual branch targets or complete networks.',
        '352 requirement IDs, all term corrections, prior representations, required relationships and expert/open-region criteria are preserved.',
        '14 C5–T1 and medial/lateral cord requirements remain unbound; BP3D4.3 intake contributes no active observation.',
        'Source candidate manifest is pinned; root must confirm runtime manifest membership and product flow before activating this version.',
    ]
    diff = {
        'schemaVersion': 1, 'status': 'candidate_only', 'fromVersion': baseline['scopeVersion'],
        'toVersion': result['scopeVersion'], 'summary': summary, 'additions': additions,
        'unchangedTargetIds': unchanged_ids, 'unmatchedSourceObjects': unmatched_sources,
        'protectedUnboundTargetIds': [t['id'] for t in protected],
        'stillUnboundTargetIds': [t['id'] for t in targets if not t['representations']],
        'expertAccepted': 0,
    }
    validation = {'status': 'passed', 'requirements': 352, 'idsRetained': 352, 'unchangedTargets': 272,
                  'additiveOnlyTargets': 80, 'priorRepresentationObjectsPreserved': True,
                  'termEvidencePreservedForAllTargets': True, 'expertAcceptanceUnchanged': True,
                  'exactTermSideScopeGates': 80, 'protectedUnboundTargets': 14,
                  'sourceObjectsNotForcedIntoTargetScope': 47, 'runtimeChecksRun': False}
    return {'proposal.json': result, 'binding-diff.json': diff, 'validation.json': validation}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for filename, data in generate().items():
        content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
        path = D / filename
        if args.check:
            assert path.read_text() == content, f'Stale candidate output: {filename}'
        else:
            path.write_text(content)
    print('PASS: 352 preserved targets; 80 additive reference bindings; 272 unchanged; 14 protected root/cord targets unbound')


if __name__ == '__main__':
    main()
