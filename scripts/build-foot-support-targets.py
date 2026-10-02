"""Preserve v3's136 identities and append20 source-scoped foot support targets."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 'data/anatomy/regional-targets-lower-limb-v3.json'
AUDIT = 'data/model-candidates/foot-support-metadata-v1/activation-proposal.json'
read = lambda p: json.loads((ROOT/p).read_text())
seed, audit = read(SEED), read(AUDIT)
assert len(seed['targets']) == 136 and len(audit['targetProposals']) == 20
targets = copy.deepcopy(seed['targets'])
EXCLUDED = {'zanatomy:intersesamoid-ligament-l', 'zanatomy:intersesamoid-ligament-r'}
main = {i: l for l in read('data/anatomy/labels.json')['entries'] for i in l['ids']}
ref = {i: l for l in read('data/anatomy/lower-limb-reference.json')['labels'] for i in l['ids']}
for label in audit['mainLabelProposals']: assert main[label['ids'][0]] == label
for label in audit['referenceLabelProposals']:
    if label['ids'][0] in EXCLUDED: assert label['ids'][0] not in ref
    else: assert ref[label['ids'][0]] == label
for source in audit['targetProposals']:
    target = copy.deepcopy(source)
    target['sourceAudit'] = AUDIT
    target['representationReview'] = 'source-scoped selectable support; open/coarse sheet limits; expert pending'
    target['technicalAcceptance'] = 'source_identity_and_manifest_binding_verified; anatomical_acceptance_pending'
    target['labelIntegration'] = 'source-scoped TR/EN and exact numeric-table Latin active'
    target['requiredRelationships'] = ['Selected28 reference/4 main attachment facts active; remaining endpoint and tendon/tunnel relationships pending',
        'Model contact, footprints, contents and cross-source registration remain unasserted']
    for representation in target['representations']:
        if representation['datasetId'] == 'lower-limb-nerve-reference':
            withheld = representation['conceptId'] in EXCLUDED
            representation['sourceManifest'] = ('data/model-candidates/foot-support-source-audit-v1/atlas.json'
                if withheld else 'public/models/lower-limb-nerve-reference/atlas.json')
            representation['status'] = ('candidate_only;source_extent_does_not_span_sesamoid_components;not_active'
                if withheld else 'source_preserved_reference_packaged;sheet_limits;expert_pending')
            representation['locator'] = 'concepts/'+representation['conceptId']
            representation['activeProductBinding'] = not withheld
            if withheld:
                target['technicalAcceptance'] = 'export_fidelity_verified;connecting_geometry_extent_rejected;candidate_only'
                target['labelIntegration'] = 'candidate TR/EN/LA retained; not active in student reference'
                target['representationReview'] = 'source-space extent failure; no accepted active representation'
                target['openCriteria'].append('Correct connecting geometry spanning the sesamoid components or alternative source')
        manifest = read(representation['sourceManifest'])
        concept = next(c for c in manifest['concepts'] if c['id'] == representation['conceptId'])
        assert concept['elements'] == representation['partIds']
        if representation.get('sourceObject'):
            part = next(p for p in manifest['parts'] if p['id'] == representation['partIds'][0])
            assert part['sourceObject'] == representation['sourceObject']
    assert target['expertReview'] == 'pending' and not target['anatomicallyAccepted']
    targets.append(target)
assert targets[:136] == seed['targets']
assert len({t['id'] for t in targets}) == len(targets) == 156
summary = dict(targets=156, preservedV3Targets=136, newSourceScopedSupportTargets=20,
    retinaculumTargets=10, plantarAponeurosisTargets=2, ligamentTargets=8,
    withObservedRepresentation=156, unbound=0, newTargetsWithMainBinding=2,
    activeProductBoundTargets=154, candidateOnlyTargets=2,
    activeNewReferenceLabels=18, activeNewMainLabels=2, anatomicallyAccepted=0)
paths = [SEED, AUDIT, 'public/models/atlas.json', 'public/models/lower-limb-nerve-reference/atlas.json',
    'data/anatomy/labels.json', 'data/anatomy/lower-limb-reference.json', 'scripts/build-foot-support-targets.py']
result = dict(schemaVersion=4, scopeVersion='lower-limb-target-seed-v4', complete=False,
    supersedes='v3 original file and136 target identities preserved',
    generatedBy='python3 scripts/build-foot-support-targets.py',
    scope='Non-exhaustive lower-limb D1 and selected D2 targets including source-scoped foot/ankle supports',
    countingPolicy='Bilateral source-scoped project requirements; sheet geometry is not expert or regional acceptance',
    inputSnapshots=[dict(path=p, sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in paths],
    summary=summary, targets=targets,
    unexpandedRequirements=seed['unexpandedRequirements']+[
        'Complete retinacular tunnel/content, plantar fascia layer and support attachment targets'],
    caveats=seed['caveats']+audit['limits'])
doc = '''# Alt ekstremite yapı hedefleri — v4

Bu sürüm **156 proje hedefi** taşır. [v3'ün](lower-limb-targets-v3.md) 136 hedefi ve değerleri aynen korunur; 20 kaynak kapsamlı destek hedefi eklenir: 10 retinakulum, iki plantar aponevroz ve sekiz bağ nesnesi. Hepsinde gözlenen kaynak temsil bağı vardır; 154 hedef aktif ürüne bağlıdır, iki intersesamoid hedef yalnız aday kayıttadır. **Sıfır anatomik uzman kabulü**. Liste eksiksiz değildir; hiçbir bölge veya kapsam hücresi kapanmaz.

[Makine kaydı](../../data/anatomy/regional-targets-lower-limb-v4.json), [geometri incelemesi](../../data/model-candidates/foot-support-source-audit-v1/REVIEW.md) ve [terim/kimlik incelemesi](../../data/model-candidates/foot-support-metadata-v1/REVIEW.md) ayrı kaynak kimliklerini ve açık koşulları taşır. Güncel envanter v4'ü kullanır; v1–v3 tarihî kayıtları tutulur.

Kaynağın açık inferior fibular retinakulum ve plantar aponevroz yüzeyleri korunur. Açık yüzey, tam hacim veya fasya katmanı kabulü değildir. Plantar calcaneonavicular bağ kaba kaynak biçimiyle gösterilir; ayrı kompleks alt parçaları veya tutunma yüzeyi üretilmez. Seçilmiş tutunma bölgesi bilgileri 28 referans ve dört ana model bağlantısıyla açılır. Bütün kemiğe geçiş modelde tutunma izi veya temas doğrulaması değildir. Retinakulum tünelindeki içerikler, tendon bağlantıları ve bütün tutunma uçları bu paketle tamamlanmaz. Ana modelde yalnız uzun plantar bağın iki taraflı mevcut parçası kesin kaynak üyeliğiyle eşlenir; diğer desteklerin ana karşılığı bu sınırlı incelemede çözülmemiştir, yokluk iddiası değildir. İki modelin konum veya yüzey eşdeğerliği kabul edilmez.

İntersesamoid adlı iki kaynak yüzeyi, kaynak koordinatlarında iki sesamoid bileşenini birleştirmediğinden öğrenci referansına eklenmez. Teknik aktarım eşitliği bu geometri kapsamını kabul ettirmez. Nesne, terim ve hedef kimlikleri aday kayıtta korunur; doğru bağlayıcı geometri veya alternatif kaynak gerekli kabul koşulu olarak açıktır. Bu iki hedef, aktif kaynak bağı bulunan 154 hedefe katılmaz.

Üretim: `python3 scripts/build-foot-support-targets.py`; yazmadan güncellik kontrolü: `--check`. Kontrol 136 eski hedefin aynı kalmasını, 156 benzersiz kimliği, dataset içindeki kesin parça üyeliğini ve yeni etiketlerin dondurulmuş öneriye eşitliğini kapsar. Anatomik uzman veya bütün bölge kabulü değildir.
'''
for path, content in [('data/anatomy/regional-targets-lower-limb-v4.json', json.dumps(result, ensure_ascii=False, indent=2)+'\n'),
                      ('docs/model/lower-limb-targets-v4.md', doc)]:
    if '--check' in sys.argv: assert (ROOT/path).read_text() == content, f'{path} stale'
    else: (ROOT/path).write_text(content)
print(json.dumps(summary))
