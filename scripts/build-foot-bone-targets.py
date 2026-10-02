"""Extend the preserved 66-target seed with 38 individual foot bone targets."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 'data/anatomy/regional-targets-lower-limb-v1.json'
AUDIT = 'data/model-candidates/foot-bone-targets-v1/activation-proposal.json'
seed = json.loads((ROOT/SEED).read_text())
audit = json.loads((ROOT/AUDIT).read_text())
main = json.loads((ROOT/'data/anatomy/labels.json').read_text())
byid = {i: row for row in main['entries'] for i in row['ids']}
for proposed in audit['mainIndividualLabelProposals'] + audit['mainParentLabelProposals']:
    assert byid[proposed['ids'][0]] == proposed, 'Foot label integration differs from source proposal'
targets = copy.deepcopy(seed['targets'])
for source in audit['targets']:
    row = copy.deepcopy(source)
    row['id'] = f'lower-limb-v2:{source["id"]}'
    row['sourceAuditTargetId'] = source['id']
    # Preserve the original target value; the immutable input snapshot below
    # now pins that historical proposal independently of its refreshed locator.
    row['sourceAudit'] = 'data/model-candidates/foot-bone-targets-v1/proposal.json'
    row['requiredRelationships'] = ['source-backed bone hierarchy', 'named articulating bones',
                                    'support/attachment context where required']
    row['technicalAcceptance'] = 'single_part_manifest_binding_verified; target_geometry_and_journey_review_pending'
    row['representationReview'] = 'observed_source_binding; independent_reference_frames; expert_pending'
    row['labelIntegration'] = 'main_and_reference_TR_EN_active; exact_LA_or_explicit_unresolved'
    row['openCriteria'] = ['Required joint/support detail and anatomical review',
                           'Complete required source-backed relationships',
                           'Source-frame-specific per-target visual/product reconciliation',
                           'Named anatomical expert acceptance']
    targets.append(row)
assert len(targets) == len({t['id'] for t in targets}) == 104
assert targets[:66] == seed['targets'], 'Existing target identities/status changed'
for target in targets:
    for r in target['representations']:
        manifest = json.loads((ROOT/r['sourceManifest']).read_text())
        c = next(c for c in manifest['concepts'] if c['id'] == r['conceptId'])
        assert c['elements'] == r['partIds']
summary = dict(targets=104, preservedV1Targets=66, newIndividualFootBoneTargets=38,
    metatarsalTargets=10, phalangealTargets=28,
    activeFootMainLabels=len(audit['mainIndividualLabelProposals'])+len(audit['mainParentLabelProposals']),
    withObservedRepresentation=sum(bool(t['representations']) for t in targets),
    unbound=sum(not t['representations'] for t in targets), anatomicallyAccepted=0)
inputs = [SEED,AUDIT,'public/models/atlas.json','public/models/lower-limb-nerve-reference/atlas.json',
          'data/anatomy/labels.json','data/anatomy/lower-limb-reference.json','scripts/build-foot-bone-targets.py']
result = dict(schemaVersion=2,scopeVersion='lower-limb-target-seed-v2',complete=False,
    supersedes='lower-limb-target-seed-v1; original file and 66 target identities preserved',
    generatedBy='python3 scripts/build-foot-bone-targets.py',
    scope='Non-exhaustive knee/leg/ankle/foot D1 and selected D2 requirements, including individual metatarsals/toe phalanges',
    countingPolicy='Bilateral project requirements; not anatomy counts or a whole-body completion denominator',
    inputSnapshots=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in inputs],
    summary=summary, targets=targets,
    unexpandedRequirements=['foot sesamoids and individually identified articular/support regions',
        'intrinsic foot muscles and gastrocnemius heads','tendons, fascia and retinacula',
        'complete joints, supports and bursae','venous and lymphatic paths',
        'cutaneous/muscular/digital nerve branches and territories','D0 context acceptance','D3 targets',
        'all other regions of the full model-scope-v1 contract'],
    caveats=seed['caveats'] + ['34 specific foot bone Latin labels and two foot-proper parent Latin labels remain unresolved.',
        'Generic TA2 bone/segment terms are not official digit-specific identities.',
        'Two independent dataset bindings do not prove equivalent coordinates, specimen or geometry.',
        'Source bone hierarchy, reference articulations and ligament attachments have distinct semantics; no cross-dataset borrowing.'])
doc = f'''# Alt ekstremite yapı hedefleri — v2

Bu sürüm **104 sağ/sol proje hedefi** taşır: [v1'in](lower-limb-targets-v1.md) 66 hedefi ve kimlikleri aynen korunur; 10 metatars ve 28 falanks için 38 bireysel D1 hedef eklenir. Liste eksiksiz değildir; 104 kaynak bağı, sıfır anatomik uzman kabulü vardır. Hiçbir kapsam hücresi kapanmaz.

[Makine listesi](../../data/anatomy/regional-targets-lower-limb-v2.json), [kaynak audit'i](../../data/model-candidates/foot-bone-targets-v1/REVIEW.md) ve [referans ilişki kanıtı](../../data/model-candidates/foot-reference-relationships-v1/REVIEW.md) kimlik, taraf, parmak, falanks düzeyi, dataset ve açık kabul koşullarını ayrı tutar. Her yeni hedef ana gövdede ve bağımsız referansta birer ayrı parçaya bağlıdır; iki gövde birbirine kayıtlı sayılmaz.

| Yeni hedef | Parmak/metatars | Taraf sayısı | Toplam hedef |
| --- | --- | ---: | ---: |
| Metatars kemiği | I–V | 2 | 10 |
| Proksimal falanks | I–V | 2 | 10 |
| Orta falanks | II–V | 2 | 8 |
| Distal falanks | I–V | 2 | 10 |

Başparmak için orta falanks hedefi açılmaz. Parmak ve taraf özel alanlardır; generic TA2 1496/1510/1511/1512 kimlikleri özel digit kimliği yapılmaz. Birinci/beşinci metatarsın dört taraflı exact Latin adı vardır; diğer 34 bireysel Latin etiket çözümlenmemiştir. Ana modeldeki on kaynak parmak ebeveyni sadece iki/üç falanksı, iki foot-proper ebeveyni sadece beş metatarsı seçer; bütün parmak veya ayak dokusu diye sunulmaz. İki ayak ebeveyni yalnız 26 kemik seçer; bu kapsam ve doğrulanmış Foot/Pes adı ayrı kaydedilir.

Ana gövdenin 38 mevcut PART-OF bağı korunur; yeni ilişki veya kaynak üyeliği eklenmez. Ayrı referansta 48 symmetric/nontransitive eklem ilişkisi ve 12 bağ→kemik bağlantısı vardır. Eklem yüzeyi, kapsül, kıkırdak, doğrulanmış fiziksel temas ve tutunma koordinatı bu bağlantılarla üretilmez. Her target'ın gereken ilişki/kapsam ve görsel incelemesi açık kalır.

Yeni liste `python3 scripts/build-foot-bone-targets.py` ile üretilir; `--check` giriş hash'lerini ve deterministik çıktıyı doğrular. Önce source audit üreticisi kendi güncel girişleriyle üretilebilir. Kontrol 104 benzersiz ID, değişmeyen 66 eski kayıt, 38 yeni hedefin iki dataset içindeki exact tek-parçalı üyeliği ve aktif {summary['activeFootMainLabels']} ana etiketin proposal eşitliğini kapsar; anatomik uzman veya bütün bölge kabulü değildir.

Sonraki açık işler: sesamoidler, ayrı eklem/tutunma bölgeleri, iç ayak kasları, tendon/fasya/retinakulum, tam eklem desteği, damar/lenf ve ince sinir dalları; bütün vücudun diğer bölge hedefleri de açılmaya devam eder. v1 makine/doküman kaydı tarihî ilk kapsam olarak korunur; güncel envanter sonraki [v4 hedeflerini](lower-limb-targets-v4.md) kullanır; v2'nin 104 hedefi aynen korunur.
'''
for path, content in [('data/anatomy/regional-targets-lower-limb-v2.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n'),
                      ('docs/model/lower-limb-targets-v2.md',doc)]:
    if '--check' in sys.argv: assert (ROOT/path).read_text() == content, f'{path} is stale'
    else: (ROOT/path).write_text(content)
print(json.dumps(summary))
