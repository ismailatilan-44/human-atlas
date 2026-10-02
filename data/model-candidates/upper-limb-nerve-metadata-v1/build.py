#!/usr/bin/env python3
"""Deterministic candidate-only labels and binding audit; no active-data writes."""
import argparse
import hashlib
import json
from pathlib import Path

D = Path(__file__).resolve().parent
R = D.parents[2]
TA_URL = 'https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv'
IFAA_URL = 'https://ifaa.unifr.ch/Public/EntryPage/TA98RATChangesNew.html'
AXILLA_URL = 'https://anatomy.ttuhscep.edu/musculoskeletal_system/axilla_tables.html'
FOREARM_URL = 'https://anatomy.ttuhscep.edu/musculoskeletal_system/forearm_tables.html'
TR = {
    'Ulnar nerve': 'Ulnar sinir',
    'Radial nerve': 'Radial sinir',
    'Axillary nerve': 'Aksiller sinir',
    'Medial brachial cutaneous nerve': 'Kolun medial deri siniri',
    'Superior lateral brachial cutaneous nerve': 'Kolun üst lateral deri siniri',
    'Inferior lateral brachial cutaneous nerve': 'Kolun alt lateral deri siniri',
    'Medial antebrachial cutaneous nerve': 'Önkolun medial deri siniri',
    'Lateral antebrachial cutaneous nerve': 'Önkolun lateral deri siniri',
    'Posterior antebrachial cutaneous nerve': 'Önkolun posterior deri siniri',
    'Anterior branch of medial antebrachial cutaneous nerve': 'Önkolun medial deri sinirinin anterior dalı',
    'Posterior branch of medial antebrachial cutaneous nerve': 'Önkolun medial deri sinirinin posterior dalı',
    'Lateral pectoral nerve': 'Lateral pektoral sinir',
    'Medial pectoral nerve': 'Medial pektoral sinir',
    'Dorsal scapular nerve': 'Dorsal skapular sinir',
    'Long thoracic nerve': 'Uzun torasik sinir',
    'Thoracodorsal nerve': 'Torakodorsal sinir',
    'Suprascapular nerve': 'Supraskapular sinir',
    'Superior subscapular nerve': 'Üst subskapular sinir',
    'Inferior subscapular nerve': 'Alt subskapular sinir',
    'Muscular branches of axillary nerve': 'Aksiller sinirin kas dalları',
    'Muscular branches of median nerve': 'Median sinirin kas dalları',
    'Muscular branches of radial nerve': 'Radial sinirin kas dalları',
    'Muscular branches of ulnar nerve': 'Ulnar sinirin kas dalları',
    'Anterior interosseous nerve of forearm': 'Önkolun anterior interosseöz siniri',
    'Posterior interosseous nerve of forearm': 'Önkolun posterior interosseöz siniri',
    'Deep branch of radial nerve': 'Radial sinirin derin dalı',
    'Superficial branch of radial nerve': 'Radial sinirin yüzeyel dalı',
}
CONTEXT_TR = {
    'Clavicle': 'Klavikula', 'Scapula': 'Skapula', 'Humerus': 'Humerus',
    'Radius': 'Radius', 'Ulna': 'Ulna',
    'First rib': 'Birinci kaburga', 'Second rib': 'İkinci kaburga',
    'Third rib': 'Üçüncü kaburga', 'Fourth rib': 'Dördüncü kaburga',
    'Fifth rib': 'Beşinci kaburga', 'Sixth rib': 'Altıncı kaburga',
    'Seventh rib': 'Yedinci kaburga', 'Eighth rib': 'Sekizinci kaburga',
    'Vertebra C3': 'Üçüncü servikal omur (C3)',
    'Vertebra C4': 'Dördüncü servikal omur (C4)',
    'Vertebra C5': 'Beşinci servikal omur (C5)',
    'Vertebra C6': 'Altıncı servikal omur (C6)',
    'Vertebra C7': 'Yedinci servikal omur (C7)',
    'Vertebra T1': 'Birinci torakal omur (T1)',
    'Vertebra T2': 'İkinci torakal omur (T2)',
    'Scaphoid bone': 'Skafoid kemik', 'Lunate bone': 'Lunatum kemiği',
    'Triquetrum bone': 'Triquetrum kemiği', 'Pisiform bone': 'Pisiform kemik',
    'Trapezium bone': 'Trapezium kemiği', 'Trapezoid bone': 'Trapezoid kemik',
    'Capitate bone': 'Kapitat kemik', 'Hamate bone': 'Hamat kemik',
}
# Audited university table facts. Endpoints must resolve to exact handoff objects.
BRANCHES = [
    ('Suprascapular nerve', 'Superior trunk of brachial plexus', 'suprascapular', 'Source', 'axilla'),
    ('Superior subscapular nerve', 'Posterior cord of brachial plexus', 'upper subscapular', 'Source', 'axilla'),
    ('Inferior subscapular nerve', 'Posterior cord of brachial plexus', 'lower subscapular', 'Source', 'axilla'),
    ('Thoracodorsal nerve', 'Posterior cord of brachial plexus', 'thoracodorsal (middle subscapular)', 'Source', 'axilla'),
    ('Axillary nerve', 'Posterior cord of brachial plexus', 'axillary', 'Source', 'axilla'),
    ('Radial nerve', 'Posterior cord of brachial plexus', 'radial', 'Source', 'axilla'),
    ('Superior lateral brachial cutaneous nerve', 'Axillary nerve', 'axillary', 'Branches', 'axilla'),
    ('Inferior lateral brachial cutaneous nerve', 'Radial nerve', 'radial', 'Branches', 'axilla'),
    ('Posterior antebrachial cutaneous nerve', 'Radial nerve', 'radial', 'Branches', 'axilla'),
    ('Lateral antebrachial cutaneous nerve', 'Musculocutaneous nerve', 'musculocutaneous', 'Branches', 'axilla'),
    ('Deep branch of radial nerve', 'Radial nerve', 'radial, deep', 'Source', 'forearm'),
    ('Superficial branch of radial nerve', 'Radial nerve', 'radial, superficial', 'Source', 'forearm'),
    ('Anterior interosseous nerve of forearm', 'Median nerve', 'interosseous, anterior', 'Source', 'forearm'),
]


def evaluated_extent(f, obj):
    g = next(x['geometry'] for x in f['evaluatedObjects'] if x['sourceObject'] == obj)
    return {
        'sourceObjectType': g['sourceObjectType'],
        'sourceWorldBounds': g['sourceWorldBounds'],
        'displayBounds': g['displayBounds'],
        'evaluatedVertices': g['evaluatedVertices'],
        'evaluatedTriangles': g['evaluatedTriangles'],
        'evaluatedWorldGeometrySha256': g['evaluatedWorldGeometrySha256'],
        'sourceSplines': [
            {'index': i, 'type': s['type'], 'controlPoints': s['controlPoints'],
             'cyclic': s['cyclic'], 'sourceWorldEndpoints': [s['sourceWorldControlPoints'][0], s['sourceWorldControlPoints'][-1]],
             'displayEndpoints': s['displayEndpoints']}
            for i, s in enumerate(g.get('splines', []))
        ],
        'splineCheck': next((s for s in f['splineChecks'] if s['sourceObject'] == obj), None),
        'locator': 'evaluated-candidates.json / objects / sourceObject; spline-checks.json / objects / sourceObject',
        'scope': 'Whole named source object in one independent source frame; endpoint coordinates carry no inferred anatomical terminal landmark.',
    }


def context_records(f):
    labels, evidence = [], []
    old = {i: e for e in f['contextExistingLabels'] for i in e['ids']}
    terms = {t['english']: t for t in f['contextTerminologyRows']}
    for m in f['contextMapping']:
        obj, cid = m['sourceObject'], m['conceptId']
        name = obj[:-2] if obj.endswith(('.l', '.r')) else obj
        original = terms[name]
        # T1 is explicitly the first thoracic vertebra. Use its numeric row,
        # preserving the distinct starred source-name row as evidence.
        t = terms['First thoracic vertebra'] if name == 'Vertebra T1' else original
        numeric = t['tableId'].isdigit()
        generic = None
        if not numeric:
            generic = terms['Rib' if name.endswith('rib') else 'Cervical vertebra' if ' C' in name else 'Thoracic vertebra']
        tr = old[cid]['tr'] if cid in old else CONTEXT_TR[name]
        note = 'Aynı kaynağın bağımsız referans çerçevesindeki bağlam nesnesidir; ana gövdeye yerleştirilmiş sayılmaz.'
        if m['system'] == 'nervous':
            note += ' Kaynak eğrinin kapsamı tüm sinir ağı veya bütün dalların tamamlandığını göstermez.'
        if not numeric:
            note += ' Numaraya özgü kesin Latin ad yalnız özel ek kaynak satırında bulundu; resmi sayısal terim olarak sunulmaz.'
        refs = [{'sourceId': 'zanatomy-ta2-pinned', 'locator': f"CSV line {t['csvLine']}; row {t['tableId']}; English/Latin pair" if numeric else f"CSV line {original['csvLine']}; custom row {original['tableId']}; numeric generic row {generic['tableId']} is broader scope only"}]
        label = {
            'ids': [cid], 'datasetId': f['datasetId'], 'datasetDecision': f['referenceDecision'],
            'sourceObject': obj, 'sourceEnglish': name, 'tr': tr, 'en': name,
            'la': t['latin'] if numeric else None,
            'side': None if m['side'] == 'midline' else m['side'],
            'aliases': old.get(cid, {}).get('aliases', []),
            'geometryPartIds': [m['partId']],
            'ta2TableId': int(t['tableId']) if numeric else None,
            'latinStatus': 'exact_unsided_numeric_pinned_term' if numeric else 'unresolved_exact_numbered_term_custom_source_row_only',
            'translationStatus': 'editorial_turkish_expert_review_pending',
            'expertReview': 'pending', 'scopeNoteTr': note, 'evidence': refs,
            'role': 'context',
        }
        if cid in old:
            assert all(label[k] == old[cid][k] for k in ('tr', 'en', 'la', 'side'))
        labels.append(label)
        evidence.append({
            'conceptId': cid, 'partId': m['partId'], 'sourceObject': obj,
            'side': m['side'], 'role': 'context',
            'representationKind': 'same_source_nerve_context' if m['system'] == 'nervous' else 'same_source_bone_context',
            'sourceNamedRow': original, 'displayExactTerm': t if numeric else None,
            'broaderGenericTerm': generic,
            'genericScopeNote': 'Generic term is supporting class evidence, never a replacement Latin label for this numbered bone.' if generic else None,
            'nameCorrespondence': 'Source T1 equals first thoracic vertebra; use numeric TA2 1063 while retaining custom source row 1063*1' if name == 'Vertebra T1' else 'Exact unsided source name match',
            'existingLabelReused': cid in old,
            'sourceExtent': evaluated_extent(f, obj),
            'existingMainBinding': 'same_canonical_nerve_id_in_different_dataset' if cid in old else 'source_bone_identity_only; no automatic main-FMA merge',
        })
    return labels, evidence


def generate():
    f = json.loads((D / 'frozen-inputs.json').read_text())
    assert f['sourceBlendSha256'] == '9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
    # Active graph/labels are frozen observations; source handoffs are immutable.
    for snap in f['inputSnapshots']:
        if '/upper-limb-nerve-source-audit-v1/' in snap['path'] or snap['path'].endswith('/TA2.csv'):
            assert hashlib.sha256((R / snap['path']).read_bytes()).hexdigest() == snap['sha256'], f"Changed source handoff: {snap['path']}"
    mapping = f['mapping']
    by_object = {m['sourceObject']: m for m in mapping + f['contextMapping']}
    discovery = {o['name']: o for o in f['discovery']}
    terms = {t['english']: t for t in f['selectedTerminologyRows']}
    existing = {e['id']: e for e in f['existingEntities']}
    old_labels = {i: e for e in f['existingLabels'] for i in e['ids']}
    entries, evidence, conflicts, audit = [], [], [], []
    for m in mapping:
        name, side, cid = m['sourceObject'][:-2], m['side'], m['conceptId']
        o, t = discovery[m['sourceObject']], terms[name]
        assert t['tableId'].isdigit(), 'Starred/custom rows cannot supply verified numeric Latin'
        grouped = name.startswith('Muscular branches of ')
        remnant = [i for i, count in enumerate(o['pointsPerSpline']) if count < 2]
        latin, term_status = t['latin'], 'exact_unsided_numeric_pinned_term'
        term_evidence = [{'sourceId': 'zanatomy-ta2-pinned', 'locator': f"TA2 {t['tableId']}; CSV line {t['csvLine']}; English and Latin columns"}]
        defect = None
        if name == 'Superior lateral brachial cutaneous nerve':
            assert latin == 'Nervus cutaneus lateralis posterioris femoris'
            latin = 'Nervus cutaneus lateralis superior brachii'
            term_status = 'primary_IFAA_term_verified_pinned_Latin_conflict_retained'
            term_evidence = [{'sourceId': 'ifaa-ta98-rat-terminology', 'locator': 'TA code A14.2.03.061; Remedy column; superior lateral brachial cutaneous nerve'}]
            defect = {'pinnedTableId': 6442, 'pinnedLatin': t['latin'], 'issue': 'Pinned Latin names a femoral region while English names the brachial nerve', 'displayLatin': latin, 'correctionAuthority': term_evidence[0], 'scope': 'Separately sourced display term, not an edit to the pinned table or a claim that its erroneous cell was verified.'}
            conflicts.append({'type': 'pinned_terminology_wrong_region', 'conceptId': cid, **defect})
        aliases = list(old_labels.get(cid, {}).get('aliases', []))
        tr = old_labels.get(cid, {}).get('tr', TR[name])
        note = 'Kaynak nesnenin mevcut seyri gösterilir; tüm sinir ağı, bütün dallar veya anatomik uzman kabulü değildir.'
        if grouped:
            note = 'Kaynakta kas dalları adıyla tek nesnede gruplanmış eğriler gösterilir; tek tek kas hedefleri ya da bağımsız adlandırılmış dallar belirlenmiş değildir.'
        if remnant:
            note += ' Kaynaktaki tek kontrol noktalı spline görünür bir dal olarak sayılmaz.'
        if name == 'Posterior interosseous nerve of forearm':
            note += ' Derin radial dal ile sınırı kaynak tanımına bağlıdır; eşanlamlılık veya dal ayrımı bu geometriyle kesinleştirilmez.'
        if defect:
            note += ' Sabit kaynak tablosundaki yanlış bölgeyi adlandıran Latin alanı yerine ayrı IFAA terminoloji kanıtı kullanılır.'
        label = {'ids': [cid], 'datasetId': f['datasetId'], 'datasetDecision': f['referenceDecision'], 'sourceObject': m['sourceObject'], 'sourceEnglish': name, 'tr': tr, 'en': name, 'la': latin, 'side': side, 'aliases': aliases, 'geometryPartIds': [m['partId']], 'ta2TableId': int(t['tableId']), 'latinStatus': term_status, 'translationStatus': 'editorial_turkish_expert_review_pending', 'expertReview': 'pending', 'scopeNoteTr': note, 'evidence': term_evidence, 'role': 'primary'}
        entries.append(label)
        old = existing.get(cid)
        old_relations = [r['id'] for r in f['existingRelations'] if r['subject'] == cid or r['object'] == cid]
        prior_slug = None
        if name in ('Superior subscapular nerve', 'Inferior subscapular nerve'):
            source_slug = 'superior' if name.startswith('Superior') else 'inferior'
            prior_slug = f'atlas:{side}-{source_slug}-subscapular-nerve'
            conflicts.append({'type': 'canonical_id_reconciled_before_handoff', 'sourceObject': m['sourceObject'], 'discardedProvisionalId': prior_slug, 'retainedCanonicalId': cid, 'basis': f"Existing canonical label establishes identical TA2 {t['tableId']} English/Latin term and laterality", 'preserveRelationIds': old_relations})
        audit.append({'conceptId': cid, 'sourceObject': m['sourceObject'], 'partId': m['partId'], 'existingGraphBinding': 'same_canonical_id_meshless' if old else 'new_candidate_identity_no_existing_exact_binding', 'existingEntity': old, 'preserveRelationIds': old_relations, 'existingLabelReused': cid in old_labels, 'discardedProvisionalId': prior_slug, 'integrationAction': 'Preserve canonical ID and facts; geometry-state/qualifier update is root-owned after dataset acceptance' if old else 'Candidate identity only; dataset and geometry acceptance remain pending', 'fmaCrossReference': None, 'fmaStatus': 'not_established_by_this_bounded_source_object_audit'})
        evidence.append({'conceptId': cid, 'partId': m['partId'], 'sourceObject': m['sourceObject'], 'side': side, 'lateralityEvidence': 'Source .l/.r suffix and immutable mapping; not independent specimen validation', 'term': t, 'displayTermEvidence': term_evidence, 'termConflict': defect, 'representationKind': 'source_group_of_muscular_branches' if grouped else 'named_nerve_source_curve', 'sourceCurveScope': {'type': o['type'], 'splineCount': o['splines'], 'controlPointCounts': o['pointsPerSpline'], 'nonRenderingSinglePointSplineIndices': remnant, 'sourceWorldControlPointBounds': o['bounds'], 'collections': o['collections'], 'sourceScope': m['scope'], 'limitations': 'Control-point bounds are not evaluated mesh bounds. Multiple splines are not automatically named branches; group labels do not identify individual muscle targets.'}, 'planningTargetIds': [t['id'] for t in f['planningTargets'] if t['name'] == name and t['side'] == side]})
    relations = []
    for child, parent, row, column, source in BRANCHES:
        for suffix in ('l', 'r'):
            a, b = by_object[child + '.' + suffix], by_object[parent + '.' + suffix]
            relations.append({'id': f"{a['conceptId']}|branch_of|{b['conceptId']}", 'subject': a['conceptId'], 'predicate': 'branch_of', 'object': b['conceptId'], 'datasetId': f['datasetId'], 'status': 'candidate_source_supported', 'expertReview': 'pending', 'evidence': [{'sourceId': 'ttuhsc-axilla-shoulder-tables' if source == 'axilla' else 'ttuhsc-forearm-wrist-tables', 'locator': f'Nerves table / {row} row / {column} column'}], 'qualifiers': {'semantics': 'Named branch-to-parent anatomy; distinct from collection membership and part_of', 'laterality': 'Same-side bilateral application of general educational anatomy; not specimen validation', 'geometry': 'No claim of model contact, fused junction, exact branch level or complete course', 'scope': 'non_exhaustive; no innervation inferred', 'datasetDecision': f['referenceDecision']}})
    unresolved = [
        {'topic': 'Posterior interosseous versus deep radial branch', 'decision': 'Preserve separate source objects; withhold branch_of or equivalent_to', 'reason': 'Primary reference describes variable definitions: synonym, continuation after supinator, or distal articular branch. Geometry alone cannot decide.', 'sourceId': 'ttuhsc-forearm-wrist-tables', 'locator': 'Nerves / interosseous, posterior and radial, deep / Notes'},
        {'topic': 'Plural muscular branches', 'decision': 'Eight bilateral source groups, not individually identified muscle branches; no individual-spline branch_of or innervates', 'reason': 'Source names and table hierarchy do not establish each spline muscle target.'},
        {'topic': 'Medial/lateral cords and C5–T1 roots', 'decision': 'No new inferred identities or geometry', 'reason': 'Unresolved roots are excluded; markers/text/collections are not named renderable curves.'},
        {'topic': 'Anterior/posterior medial antebrachial cutaneous branches', 'decision': 'Labels supported; no edge in this selected set', 'reason': 'No separate primary connectivity claim was audited; naming alone was not promoted to an edge.'},
        {'topic': 'Other source nerves and fine hand branches', 'decision': 'Outside this selected 27-base handoff', 'reason': 'The geometry audit separately identified Subclavian nerve.l/.r for a later candidate; exclusion is not absence. Fine palmar/digital groups and complete networks remain open.'},
    ]
    for item in evidence:
        item['sourceExtent'] = evaluated_extent(f, item['sourceObject'])
    context_labels, context_evidence = context_records(f)
    primary_labels = list(entries)
    entries.extend(context_labels)
    evidence.extend(context_evidence)
    proposal = {'schemaVersion': 1, 'status': 'candidate_only_not_integrated', 'sourceRevision': f['observedHead'], 'sourceBlendSha256': f['sourceBlendSha256'], 'datasetId': f['datasetId'], 'datasetDecision': f['referenceDecision'], 'scope': '127 source objects: 54 new nerve/group curves, 24 existing nerve context curves and 49 bone context objects; not a complete shoulder, upper-limb or hand nerve network', 'labels': entries, 'relations': relations, 'preserveMainOnlyRelationIds': [r['id'] for r in f['existingRelations']], 'representationNoteTr': 'Adlandırılmış kaynak sinir eğrileri, gruplanmış kas dalları ve kemik bağlamı aynı bağımsız kaynak çerçevesinde korunur. Tam üst ekstremite sinir ağı, köklerin tamamı ve bütün el dalları temsil edilmiş değildir. Ana gövde yerleşimi kabul edilmemiştir; anatomik uzman incelemesi bekler.'}
    sources = [
        {'id': 'zanatomy-ta2-pinned', 'url': TA_URL, 'sha256': '0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974', 'use': 'Numeric unsided pairs except row6442 conflict; no formal FMA crosswalk or constructed sided Latin'},
        {'id': 'ifaa-ta98-rat-terminology', 'title': 'IFAA — Changes Due to Regular Anatomical Terminology Rules', 'url': IFAA_URL, 'retrievedOn': '2026-10-02', 'locator': 'A14.2.03.061 / Remedy', 'verifiedLatin': 'Nervus cutaneus lateralis superior brachii', 'use': 'Primary correction authority for display term; pinned table unchanged'},
        {'id': 'ttuhsc-axilla-shoulder-tables', 'url': AXILLA_URL, 'retrievedOn': '2026-10-02', 'use': 'Selected branch facts with locators; no copied table or illustrations'},
        {'id': 'ttuhsc-forearm-wrist-tables', 'url': FOREARM_URL, 'retrievedOn': '2026-10-02', 'use': 'Selected branch facts and definition caveat; no full territories or copied tables'},
    ]
    source_evidence = {'schemaVersion': 1, 'status': 'candidate_only', 'sources': sources, 'sourceBlendSha256': f['sourceBlendSha256'], 'inputSnapshots': f['inputSnapshots'], 'frozenInputSha256': hashlib.sha256((D / 'frozen-inputs.json').read_bytes()).hexdigest(), 'entries': evidence, 'conflicts': conflicts, 'unresolved': unresolved, 'intakeBoundary': 'Same pinned Z-Anatomy source as prior extensions. Object-specific lineage and redistribution attribution belong to the geometry audit; this package does not relicense the source or accept its frame.'}
    binding = {'schemaVersion': 1, 'status': 'observational_candidate_audit', 'entries': audit, 'preservedExistingEntities': f['existingEntities'], 'preservedExistingRelations': f['existingRelations'], 'contextEndpointBindings': [{'sourceObject': x['sourceObject'], 'conceptId': x['conceptId'], 'partId': x['partId'], 'side': x['side']} for x in f['contextMapping'] if x['system'] == 'nervous'], 'prohibitedInference': 'Name agreement is not accepted registration; a separate reference does not confer main-body geometry.'}
    assert len(entries) == len({e['ids'][0] for e in entries}) == 127
    assert len({e['geometryPartIds'][0] for e in entries}) == 127
    assert len(terms) == 27 and len(relations) == 26
    assert len(existing) == 8 and len(f['existingRelations']) == 10
    assert len({r['id'] for r in relations}) == len(relations)
    assert all(r['subject'].split(':')[1].split('-')[0] == r['object'].split(':')[1].split('-')[0] for r in relations)
    assert sum(e['representationKind'] == 'source_group_of_muscular_branches' for e in evidence) == 8
    assert sum(bool(e.get('sourceCurveScope', {}).get('nonRenderingSinglePointSplineIndices')) for e in evidence) == 2
    assert all(e['datasetId'] == 'upper-limb-nerve-reference' and 'femoris' not in (e['la'] or '') for e in entries)
    assert sum(e['la'] is None for e in entries) == 17
    assert {e['sourceObject'] for e in entries} == set(by_object)
    for label in primary_labels:
        old = old_labels.get(label['ids'][0])
        if old:
            assert all(label[k] == old[k] for k in ('tr', 'en', 'la', 'side'))
    report = {'status': 'passed', 'scope': 'candidate metadata validation only', 'labels': 127, 'primaryNerveLabels': 54, 'contextNerveLabels': 24, 'contextBoneLabels': 49, 'selectedBranchRelations': 26, 'existingMainOnlyMotorRelationsPreserved': 10, 'existingMeshlessCanonicalIdsRetained': 8, 'reconciledSubscapularIds': 4, 'primaryCorrectedLatinLabels': 2, 'numericPinnedLatinLabels': 108, 'unresolvedExactNumberedLatin': 17, 'sourceGroupLabels': 8, 'primaryObjectsWithSinglePointRemnant': 2, 'planningTargetMatches': len(f['planningTargets']), 'mainGeometryAccepted': False, 'separateReferenceDecision': 'selected_by_root; runtime_acceptance_pending', 'applicationChecksRun': False, 'sourceExpertReview': 'pending'}
    return {'proposal.json': proposal, 'source-evidence.json': source_evidence, 'identity-binding-audit.json': binding, 'validation.json': report}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, obj in generate().items():
        text = json.dumps(obj, ensure_ascii=False, indent=2) + '\n'
        path = D / name
        if args.check:
            assert path.read_text() == text, f'Stale candidate output: {name}'
        else:
            path.write_text(text)
    print('PASS: 127 labels (110 Latin, 17 null), 26 selected branch edges, 8 canonical bindings, 10 retained main-only motor facts')


if __name__ == '__main__':
    main()
