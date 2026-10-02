"""Reproduce the bounded main-body label proposal from pinned source records.

Exact source concepts and TA2 term scopes are inspection evidence, not a formal
ontology crosswalk or expert anatomical acceptance. --apply is idempotent.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
digest = lambda p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
table_path = 'work/open-assets-review/TA2.csv'
assert digest(table_path) == '0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
rows = [r[0].split(';') if len(r) == 1 else r for r in csv.reader(
    (ROOT / table_path).read_text(encoding='utf-8-sig').splitlines())]
manifest_path = 'public/models/atlas.json'
atlas = json.loads((ROOT / manifest_path).read_text())
concepts = {c['id']: c for c in atlas['concepts']}
parts = {p['id']: p for p in atlas['parts']}
inputs = json.loads((HERE / 'target-snapshot.json').read_text())
translations = {
    'Fibula': ('Fibula', ['kamış kemiği']),
    'Patella': ('Patella', ['diz kapağı kemiği']),
    'Talus': ('Talus', ['aşık kemiği']),
    'Calcaneus': ('Kalkaneus', ['topuk kemiği', 'calcaneus']),
    'Navicular bone': ('Kayık kemiği', ['naviküler kemik', 'os naviculare']),
    'Cuboid bone': ('Küp kemiği', ['kuboid kemik', 'os cuboideum']),
    'Medial cuneiform bone': ('Medial kama kemiği', ['medial kuneiform kemik']),
    'Intermediate cuneiform bone': ('Ara kama kemiği', ['orta kuneiform kemik']),
    'Lateral cuneiform bone': ('Lateral kama kemiği', ['lateral kuneiform kemik']),
    'Extensor digitorum longus': ('Uzun parmak ekstansör kası', ['uzun parmak açıcı kas']),
    'Extensor hallucis longus': ('Uzun başparmak ekstansör kası', ['uzun başparmak açıcı kas']),
    'Flexor digitorum longus': ('Uzun parmak fleksör kası', ['uzun parmak bükücü kas']),
    'Flexor hallucis longus': ('Uzun başparmak fleksör kası', ['uzun başparmak bükücü kas']),
    'Soleus muscle': ('Soleus kası', ['soleus']),
    'Anterior tibial artery': ('Ön tibial arter', ['anterior tibial arter']),
    'Posterior tibial artery': ('Arka tibial arter', ['posterior tibial arter']),
    'Popliteal artery': ('Popliteal arter', ['diz arkası atardamarı']),
}
entries, evidence = [], {}
for target in inputs['targets']:
    term = target['terminology']['en']
    representation = next(r for r in target['representations'] if r['datasetId'] == 'male-body')
    cid = representation['conceptId']
    if cid in inputs['alreadyLabeledConceptIds']:
        continue
    assert term in translations
    concept = concepts[cid]
    assert concept['name'] == representation['sourceName']
    assert concept['elements'] == representation['partIds']
    exact = [(i, r) for i, r in enumerate(rows, 1)
             if len(r) >= 3 and r[0] == str(target['terminology']['ta2TableId'])]
    assert len(exact) == 1
    line, row = exact[0]
    assert row[1] == term and row[2] == target['terminology']['la']
    side = target['side']
    assert side in ['left', 'right'] and side in concept['name'].lower()
    for pid in concept['elements']:
        part = parts[pid]
        assert (1 if side == 'left' else -1) * sum(b[0] for b in part['bounds']) / 2 > 0
    # Bind direct source parts only when their own concept identity matches;
    # branch surfaces inside an artery aggregate do not receive its trunk name.
    ids = [cid] + [pid for pid in concept['elements'] if parts[pid]['conceptId'] == cid]
    tr, aliases = translations[term]
    entry = dict(ids=ids, tr=tr, en=row[1], la=row[2], side=side,
                 aliases=aliases, ta2Id=int(row[0]),
                 evidenceRef=f'data/model-candidates/lower-limb-main-labels/source-evidence.json#{cid}')
    if term == 'Anterior tibial artery':
        entry['representationNoteTr'] = 'Kaynak seçimi dört yüzeyi birlikte gösterir: anterior tibial arter, dorsalis pedis, arkuat ve lateral tarsal arter. Ana arter yüzeyi ile kaynak grubunun kapsamı ayrıdır; bütün dalların eksiksizliği kabul edilmemiştir.'
    elif term == 'Posterior tibial artery':
        entry['representationNoteTr'] = 'Kaynak seçimi beş yüzeyi birlikte gösterir: posterior tibial arter, medial/lateral plantar arter, plantar ark ve yüzeyel medial plantar arter. Ana arter yüzeyi ile kaynak grubunun kapsamı ayrıdır; bütün dalların eksiksizliği kabul edilmemiştir.'
    elif term == 'Popliteal artery':
        entry['representationNoteTr'] = 'Tek kaynak popliteal arter yüzeyi seçilir. Ayrı geniküler dalların ve bölgesel damar ağının eksiksizliği bu etiketle kabul edilmez.'
    entries.append(entry)
    evidence[cid] = dict(targetId=target['id'], side=side,
        sourceConcept=dict(id=cid, name=concept['name'], elements=concept['elements']),
        sourceParts=[dict(id=pid, name=parts[pid]['name'], conceptId=parts[pid]['conceptId'],
                          bounds=parts[pid]['bounds']) for pid in concept['elements']],
        terminology=dict(ta2TableId=int(row[0]), en=row[1], la=row[2],
                         locator=f'CSV line {line}; English/Latin columns',
                         fmaCrosswalk='not_asserted'),
        translationStatus='Turkish editorial; anatomical expert review pending',
        geometryStatus='Existing source membership preserved; target anatomical/detail acceptance pending')
assert len(entries) == 34
all_ids = [i for e in entries for i in e['ids']]
assert len(all_ids) == len(set(all_ids))
snapshots = [dict(path=p, sha256=digest(p)) for p in [table_path, manifest_path,
    'data/model-candidates/lower-limb-main-labels/target-snapshot.json',
    'data/model-candidates/lower-limb-main-labels/build-proposal.py']]
outputs = {
    'proposal.json': dict(schemaVersion=1, scope='34 missing main-body lower-limb labels',
                         expertReview='pending', entries=entries),
    'source-evidence.json': dict(schemaVersion=1, inputSnapshots=snapshots,
                                formalOntologyCrosswalk=False, records=evidence),
}
for filename, value in outputs.items():
    content = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    if '--check' in sys.argv:
        assert (HERE / filename).read_text() == content, filename + ' is stale'
    else:
        (HERE / filename).write_text(content)
if '--apply' in sys.argv:
    labels_path = ROOT / 'data/anatomy/labels.json'
    labels = json.loads(labels_path.read_text())
    by_id = {i: e for e in labels['entries'] for i in e['ids']}
    for entry in entries:
        conflicts = [by_id[i] for i in entry['ids'] if i in by_id]
        if conflicts:
            assert all(e == entry for e in conflicts), entry['ids']
        else:
            labels['entries'].append(entry)
    labels['scope'] = 'Reviewed regional labels including organ neighbors, skull bones, rotator cuff, hepatic segments, lung tissue/segments and named knee/leg/foot bones, muscles and arterial groups. Source identities and geometric scope preserved; not a complete atlas translation.'
    labels_path.write_text(json.dumps(labels, ensure_ascii=False, indent=2) + '\n')
    by_id = {i: e for e in labels['entries'] for i in e['ids']}
    for target in inputs['targets']:
        cid = next(r['conceptId'] for r in target['representations'] if r['datasetId'] == 'male-body')
        assert all(by_id[cid].get(language) for language in ['tr', 'en', 'la'])
print(json.dumps(dict(newLabels=len(entries), auditedMainTargets=len(inputs['targets']),
                     sourcePartAliases=len(all_ids)-len(entries), expertReview='pending')))
