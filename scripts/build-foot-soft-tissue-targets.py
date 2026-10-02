"""Preserve v2's104 identities and add32 source-scoped foot soft-tissue targets."""
import copy
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SEED = 'data/anatomy/regional-targets-lower-limb-v2.json'
AUDIT = 'data/model-candidates/foot-soft-tissue-metadata-v1/activation-proposal.json'
read = lambda p:json.loads((ROOT/p).read_text())
seed, audit = read(SEED), read(AUDIT)
targets = copy.deepcopy(seed['targets'])
main = {i:l for l in read('data/anatomy/labels.json')['entries'] for i in l['ids']}
ref = {i:l for l in read('data/anatomy/lower-limb-reference.json')['labels'] for i in l['ids']}
for label in audit['mainLabelProposals']: assert main[label['ids'][0]] == label
for label in audit['referenceLabelProposals']: assert ref[label['ids'][0]] == label
for source in audit['targetProposals']:
    target = copy.deepcopy(source)
    target['sourceAudit'] = AUDIT
    target['representationReview'] = 'observed_source_binding; independent reference frames; expert pending'
    target['technicalAcceptance'] = 'source_identity_and_manifest_binding_verified; target_level_anatomical_acceptance_pending'
    target['labelIntegration'] = 'source-scoped TR/EN active;exact Latin or explicit unresolved'
    target['requiredRelationships'] = ['Selected source-backed attachment/innervation facts where verified',
        'Head/group relationship inheritance forbidden; remaining required relationships open']
    for representation in target['representations']:
        if representation['datasetId'] == 'lower-limb-nerve-reference':
            representation['sourceManifest'] = 'public/models/lower-limb-nerve-reference/atlas.json'
            representation['status'] = 'source_preserved_reference_packaged;expert_acceptance_pending'
            representation['locator'] = 'concepts/'+representation['conceptId']
        manifest = read(representation['sourceManifest'])
        concept = next(c for c in manifest['concepts'] if c['id'] == representation['conceptId'])
        assert concept['elements'] == representation['partIds']
        if representation.get('sourceObject'):
            part = next(p for p in manifest['parts'] if p['id'] == representation['partIds'][0])
            assert part['sourceObject'] == representation['sourceObject']
    targets.append(target)
assert targets[:104] == seed['targets'] and len({t['id'] for t in targets}) == len(targets) == 136
summary = dict(targets=136,preservedV2Targets=104,newSourceScopedFootTargets=32,
    sourceMuscleTargets=30,compoundSesamoidTargets=2,withObservedRepresentation=136,unbound=0,
    newTargetsWithMainBinding=28,activeNewMainLabels=38,anatomicallyAccepted=0)
paths = [SEED,AUDIT,'public/models/atlas.json','public/models/lower-limb-nerve-reference/atlas.json',
    'data/anatomy/labels.json','data/anatomy/lower-limb-reference.json','scripts/build-foot-soft-tissue-targets.py']
result = dict(schemaVersion=3,scopeVersion='lower-limb-target-seed-v3',complete=False,
    supersedes='v2 original file and104 target identities preserved',generatedBy='python3 scripts/build-foot-soft-tissue-targets.py',
    scope='Non-exhaustive knee/leg/ankle/foot D1 and selected D2 targets, including source-scoped intrinsic foot muscles and sesamoid groups',
    countingPolicy='Bilateral project requirements;compound source selections are not independently accepted numbered structures',
    inputSnapshots=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in paths],
    summary=summary,targets=targets,
    unexpandedRequirements=['Independent numbered interosseous/lumbrical source-reference identities',
        'Individual medial/lateral sesamoid identities and articular/support regions',
        'Other lower-limb muscle subdivisions including gastrocnemius heads','Tendons,fascia,retinacula and complete joints/supports/bursae',
        'Venous/lymphatic paths and cutaneous/muscular/digital nerve branches/territories',
        'D0 context and target-level expert acceptance','D3 and all other whole-body regions'],
    caveats=seed['caveats']+audit['limits'])
doc='''# Alt ekstremite yapı hedefleri — v3

Bu sürüm **136 proje hedefi** taşır: [v2'nin](lower-limb-targets-v2.md) 104 hedefi ve değerleri aynen korunur; 32 kaynak kapsamlı ayak hedefi eklenir. Otuz hedef kas nesnesi/başı/grubu, ikisi sesamoid grubudur. Hepsinde gözlenen kaynak bağı vardır; **sıfır anatomik uzman kabulü**. Liste eksiksiz değildir ve hiçbir bölge/kapsam hücresi kapanmaz.

[Makine kaydı](../../data/anatomy/regional-targets-lower-limb-v3.json), [kaynak geometri](../../data/model-candidates/foot-soft-tissue-source-audit-v1/REVIEW.md) ve [etiket/ilişki incelemesi](../../data/model-candidates/foot-soft-tissue-metadata-v1/REVIEW.md) ayrı kimlik, kapsam ve açık koşulları korur. Önceki v1/v2 kayıtları tutulur; güncel envanter sonraki [v4 hedeflerini](lower-limb-targets-v4.md) kullanır; v3'ün 136 kimliği korunur.

Referansta iki taraflı kaynak kasları, ayrı flexor hallucis brevis/adductor hallucis başları ve çoğul interosseöz/lumbrikal gruplar vardır. Grubun birkaç bağlı bileşeni olması numaralı anatomik kimlik kanıtı değildir. Lumbrikal kaynak grubu tek bağlı bileşendir; dört ayrı kas kabul edilmez. Her sesamoid seçimi iki bağlı bileşeni birlikte içerir; medial/lateral kimlik atanmaz. Ana modelin zaten mevcut dört lumbrikal ve üç plantar interosseöz kası her tarafta kendi bireysel kimlikleriyle kalır; iki kaynak eşdeğer geometri değildir. 28 yeni hedefin ana kaynakta da gözlenen bağları vardır; EDB/dorsal interosseöz ana eşlemesi bu sınırlı denetimde çözümlenmemiştir, yokluk iddiası değildir.

İki bütün adlandırılmış kas için 12 referans ve 8 ana model başlangıç/tutunma/innervasyon bağlantısı kaynakla açılır. Bütün kemiğe geçiş tutunma footprint'i değildir; kas başlarına/gruplarına ilişki mirası uygulanmaz. Diğer gerekli kas ilişkileri, eklem destekleri, ince dallar, ayrı numaralı grup/kemik kimlikleri ve uzman incelemesi açıktır.

Üretim: `python3 scripts/build-foot-soft-tissue-targets.py`; yazmadan güncellik kontrolü: `--check`. Kontrol 104 eski hedefin aynen korunmasını, 136 benzersiz kimliği, dataset içindeki exact parça üyeliğini ve yeni aktif etiketlerin dondurulmuş kaynak önerisine eşitliğini kapsar. Anatomik veya bütün bölge kabulü değildir.
'''
for path,content in [('data/anatomy/regional-targets-lower-limb-v3.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n'),
                     ('docs/model/lower-limb-targets-v3.md',doc)]:
    if '--check' in sys.argv: assert (ROOT/path).read_text() == content, f'{path} stale'
    else: (ROOT/path).write_text(content)
print(json.dumps(summary))
