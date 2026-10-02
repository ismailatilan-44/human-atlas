"""Activate the reviewed P3 requirement seed without accepting its anatomy."""
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = 'data/model-candidates/upper-limb-target-inventory-v1/proposal.json'
OUTPUT = 'data/anatomy/regional-targets-upper-limb-v1.json'
CORRECTIONS = 'data/model-candidates/upper-limb-target-inventory-v1/term-corrections.json'
read = lambda p: json.loads((ROOT/p).read_text())
sha = lambda p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
audit = read(AUDIT)
targets = copy.deepcopy(audit['targets'])
correction_record = read(CORRECTIONS)
assert sha(correction_record['sourceTable']) == correction_record['sourceTableSha256']
corrected_targets = 0
for correction in correction_record['corrections']:
    for target in targets:
        term = target['termEvidence']
        if term.get('numericId') != correction['numericId']:
            continue
        assert term['en'] == correction['en'] and term['la'] == correction['pinnedLatin']
        term['pinnedSourceLatin'] = term['la']
        term['la'] = correction['correctedLatin']
        term['correctionEvidence'] = correction['primaryEvidence']
        term['scope'] = 'Pinned English/numeric row; Latin separately corrected from published IFAA terminology; formal crosswalk pending'
        corrected_targets += 1
assert corrected_targets == 2
assert len(targets) == len({t['id'] for t in targets}) == 352
assert all(t['regionId'] == 'shoulder-axilla-arm' and t['ownerPackage'] == 'P3' for t in targets)
assert all(not t['complete'] and not t['anatomicallyAccepted'] and not t['absenceClaim'] for t in targets)
assert all(t['expertReview'] == 'pending' for t in targets)
families = Counter(t['familyId'] for t in targets)
assert dict(families) == audit['summary']['families']
names = Counter(t['name'] for t in targets)
assert all(count == 2 for count in names.values())
for name in names:
    assert {t['side'] for t in targets if t['name'] == name} == {'left', 'right'}
for name in ['Lateral cord of brachial plexus', 'Medial cord of brachial plexus'] + [
        f'{level} root contribution to brachial plexus' for level in ['C5', 'C6', 'C7', 'C8', 'T1']]:
    assert names[name] == 2

graph = read('data/anatomy/knowledge.json')
entities = {e['id']: e for e in graph['entities']}
relation_ids = {r['id'] for r in graph['relations']}
paths = {AUDIT, CORRECTIONS, 'scripts/build-upper-limb-targets.py', 'data/anatomy/knowledge.json'}
mesh_targets = anchor_targets = 0
for target in targets:
    assert set(target['existingRelationshipIds']) <= relation_ids
    assert target['requiredRelationshipTypes']
    for binding in target['representations']:
        assert binding['datasetId'] == 'male-body'
        assert binding['conceptId'] in entities
        if binding['sourceManifest']:
            paths.add(binding['sourceManifest'])
            manifest = read(binding['sourceManifest'])
            concept = next(c for c in manifest['concepts'] if c['id'] == binding['conceptId'])
            assert concept == binding['sourceConcept']
            assert concept['elements'] == binding['partIds']
            parts = {p['id']: p for p in manifest['parts']}
            assert all(parts[p]['vertexCount'] > 0 and parts[p]['indexCount'] > 0 for p in binding['partIds'])
        for field, collection in [('surfaceAnchor', 'anchors'), ('unresolvedAnchor', 'unresolved')]:
            if not binding.get(field):
                continue
            recorded = binding[field]
            paths.add(recorded['manifest'])
            actual = next(a for a in read(recorded['manifest'])[collection]
                          if a['conceptId'] == binding['conceptId'])
            assert actual == {k: v for k, v in recorded.items() if k != 'manifest'}
    mesh_targets += any(b['partIds'] for b in target['representations'])
    anchor_targets += any(b.get('surfaceAnchor') for b in target['representations'])
assert mesh_targets == 132 and anchor_targets == 6
summary = dict(audit['summary'], observedMeshTargets=mesh_targets,
               attachmentReferencePointTargets=anchor_targets, anatomicallyAccepted=0,
               exactPinnedLatinTargets=332, separatelyCorrectedLatinTargets=corrected_targets,
               unresolvedExactLatinTargets=18)
result = dict(schemaVersion=1, scopeVersion='upper-limb-target-seed-v1',
    status='active_project_requirements;anatomical_acceptance_pending', complete=False,
    sourceAudit=AUDIT, sourceAuditRevision=audit['sourceRevision'],
    sourceObservationCapturedAt=audit['snapshotCapturedAt'],
    scopeContract=audit['scopeContract'], summary=summary, targets=targets,
    unexpandedRequirements=audit['unexpandedRequirements'], sources=audit['sources'],
    inputSnapshots=[dict(path=p, sha256=sha(p)) for p in sorted(paths)],
    caveats=audit['limits'] + [
        'Requirement activation is not geometry, label, relationship, regional or expert acceptance',
        '138 observations include six attachment reference points; these are not six segmented bone landmarks',
        'The 204 targets with no complete binding remain requirements, not asserted anatomical absences',
        'Future representation changes require a reviewed version; historical target observations remain traceable'])
doc = '''# Omuz, aksilla ve kol yapı hedefleri — v1

**352 sağ/sol proje gereksinimi** aktif iş envanterine alındı: 100 kemik/eklem/destek, 76 kas/baş/fasya, 164 sinir/damar/lenf ve 12 kompartıman/geçit hedefi. Bunlar 176 tarafsız gereksinimin iki tarafıdır; anatomik yapı veya tamamlanma yüzdesi değildir. **Sıfır uzman kabulü**, eksiksiz olmayan sürümlü başlangıç kapsamı. Bütün vücut kapsamı ve bütün ince hedeflerin açılımı devam eder.

[Makine kaydı](../../data/anatomy/regional-targets-upper-limb-v1.json) [incelenmiş adayın](../../data/model-candidates/upper-limb-target-inventory-v1/REVIEW.md) 352 kimliğini ve 350 hedef kaydını aynen korur; iki taraflı bir Latin kaynak hatası ayrıca kanıtlanmış terimle düzeltilir. 132 hedef model üyeliği, altısı yalnız tutunma referans noktası taşır. Sekiz kavram geometrisiz, iki humeral işaret çözümlenmemiş; 204 hedefte bu sınırlı kaynak incelemesi tam hedefin pozitif bağını bulmadı. Bu durum **kaynakta veya anatomide yokluk değildir**. İlişkili kısmi kaynak parçaları ayrıca korunur.

C5–T1 katkıları, medial/lateral kordlar ve adlandırılmış terminal/kutanöz/motor dallar bağsız olsalar da zorunlu açık hedeflerdir. Kaynağın karışık kök demeti spline sayısından C5–T1 olarak adlandırılmaz. Bütün kas, baş, kaynak seçim grubu, bağımsız yapı ve tutunma referans noktası ayrı temsil kapsamlarıdır. Pectoralis major kaynak seçiminin ayrı klaviküler parçasını kapsamaması ve tek medial brachial vein yüzeyinin çoğul ven hedefini tamamlamaması görünür kalır.

332 hedefte sabitlenmiş numeric TA2 Latin terimi vardır; iki superior lateral brachial cutaneous hedefinin yanlış bölgeye ait Latin sütunu [IFAA'nın A14.2.03.061 terimiyle](https://ifaa.unifr.ch/Public/EntryPage/TA98RATChangesNew.html) ayrı kaynak kanıtı üzerinden düzeltilir. Özgün hatalı değer korunur; kaynak CSV değiştirilmez. 18 kök/özel geçit/tutunma ayrıntısında kesin Latin ad verilmez. Genel destek terimi ayrıntının kimliği yerine kullanılmaz. Mevcut ilişki kimlikleri kanıt olarak tutulur; gereken ilişki kümesini tamamlamaz. Yeni etiket, ilişki veya geometri bu envanter işlemiyle eklenmez.

Üretim: `python3 scripts/build-upper-limb-targets.py`; yazmadan kontrol: `--check`. Kontrol benzersiz/iki taraflı 352 kimliği, dört aileyi, C5–T1/kord gereksinimlerini, mevcut manifest üyeliğini, altı gerçek referans noktasını, iki null işareti ve mevcut ilişki uçlarını doğrular. Giriş hash'leri yeni kaynak durumunu tarihî aday gözleminden ayrı izler. Ürün görseli veya anatomik ayrıntı kabulü değildir. [Genel envanter](model-inventory.md) bu gereksinimleri katalog ve bekleyen bölge/ayrıntı hücrelerine bağlar.
'''
for path, content in [(OUTPUT, json.dumps(result, ensure_ascii=False, indent=2)+'\n'),
                      ('docs/model/upper-limb-targets-v1.md', doc)]:
    if '--check' in sys.argv:
        assert (ROOT/path).read_text() == content, f'{path} stale'
    else:
        (ROOT/path).write_text(content)
print(json.dumps(summary))
