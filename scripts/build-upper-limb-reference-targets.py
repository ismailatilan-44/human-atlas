"""Activate additive source-reference observations; preserve the v1 requirements."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'data/anatomy/regional-targets-upper-limb-v1.json'
CANDIDATE = 'data/model-candidates/upper-limb-target-bindings-v2/proposal.json'
MANIFEST = 'public/models/upper-limb-nerve-reference/atlas.json'
METADATA = 'data/anatomy/upper-limb-reference.json'
ACCEPTANCE = 'docs/model/upper-limb-reference-product-acceptance.json'
OUTPUT = 'data/anatomy/regional-targets-upper-limb-v2.json'
read = lambda p: json.loads((ROOT/p).read_text())
sha = lambda p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

baseline, candidate, manifest, metadata, acceptance = map(
    read, [BASELINE, CANDIDATE, MANIFEST, METADATA, ACCEPTANCE])
assert sha(BASELINE) == candidate['versionEvidence']['baselineSha256']
for entry in candidate['versionEvidence']['inputs']:
    assert sha(entry['path']) == entry['sha256'], entry['path']
assert acceptance['status'] == 'local_production_product_flow_accepted;expert_review_pending'
# Preserve the dated UI acceptance. A producer-only repack may refresh input hashes,
# but all non-provenance fields must match its independently pinned old payload.
repack = {e['path']: e for e in read('data/anatomy/upper-limb-reference-repack-evidence.json')['files']}
for entry in acceptance['inputSnapshots']:
    if entry['path'] in repack:
        proof = repack[entry['path']]
        assert proof['historicalSha256'] == entry['sha256']
        payload = read(entry['path'])
        payload.pop('inputSnapshots', None)
        payload.pop('packageInputSnapshots', None)
        assert hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest() == proof['semanticSha256']
    else:
        assert sha(entry['path']) == entry['sha256'], entry['path']
assert acceptance['datasetId'] == manifest['datasetId'] == metadata['datasetId'] == 'upper-limb-nerve-reference'
assert not manifest['compatibleWithMainAtlas'] and manifest['registration'] is None
concepts = {c['id']: c for c in manifest['concepts']}
parts = {p['id']: p for p in manifest['parts']}
labels = {i: label for label in metadata['labels'] for i in label['ids']}
assert len(concepts) == len(parts) == len(labels) == 127
assert [t['id'] for t in candidate['targets']] == [t['id'] for t in baseline['targets']]
result = copy.deepcopy(candidate)
added = changed = 0
for target, old in zip(result['targets'], baseline['targets']):
    assert target['representations'][:len(old['representations'])] == old['representations']
    for field in old:
        if field not in ['representations', 'bindingStatus', 'bindingObservationHistory']:
            assert target[field] == old[field], (target['id'], field)
    extras = target['representations'][len(old['representations']):]
    changed += bool(extras)
    for binding in extras:
        assert binding['datasetId'] == manifest['datasetId']
        assert binding['runtimeManifestExpected'] == MANIFEST
        concept = concepts[binding['conceptId']]
        assert concept == binding['sourceConcept']
        assert concept['elements'] == binding['partIds'] == labels[concept['id']]['geometryPartIds']
        assert labels[concept['id']]['side'] == target['side']
        assert all(parts[p]['vertexCount'] > 0 and parts[p]['indexCount'] > 0 for p in binding['partIds'])
        binding.update(activeProductBinding=True, runtimeManifest=MANIFEST,
                       runtimeManifestSha256=sha(MANIFEST),
                       runtimeAcceptance='local_production_product_flow_accepted;detail_and_expert_acceptance_pending',
                       productAcceptanceRecord=ACCEPTANCE)
        added += 1
assert len(result['targets']) == 352 and added == changed == 80
assert sum(t == old for t, old in zip(result['targets'], baseline['targets'])) == 272
assert sum(any(b['partIds'] for b in t['representations']) for t in result['targets']) == 178
assert all(not t['complete'] and not t['anatomicallyAccepted'] and t['expertReview'] == 'pending'
           for t in result['targets'])
result['status'] = 'active_project_requirements;source_reference_bindings_active;anatomical_acceptance_pending'
result['representationObservationCapturedAt'] = candidate['versionEvidence']['capturedAt']
result['productAcceptance'] = {'path': ACCEPTANCE, 'scope': 'Representative local production flows; not per-target anatomical detail or deployed acceptance'}
paths = [BASELINE, CANDIDATE, MANIFEST, METADATA, ACCEPTANCE, 'scripts/build-upper-limb-reference-targets.py']
result['activationInputSnapshots'] = [{'path': p, 'sha256': sha(p)} for p in paths]
result['caveats'].append('80 additional runtime reference bindings retain an independent source frame; no main-body registration or expert criterion is closed')
doc = '''# Omuz, aksilla ve kol yapı hedefleri — v2

352 mevcut gereksinim korunur; [v1](upper-limb-targets-v1.md) tarihî gözlem olarak değişmez. [Makine kaydı](../../data/anatomy/regional-targets-upper-limb-v2.json), bağımsız üst ekstremite sinir referansından 80 ek ürün bağı taşır: 46 birincil sinir/grup, 24 sinir bağlamı ve 10 kemik bağlamı. 272 hedef kaydı aynıdır; önceki bütün temsiller, kimlikler, terim kanıtları, gereken ilişkiler ve uzman kriterleri korunur.

Hedef düzeyinde geometri gözlemi 132→178; altı tutunma referans noktası ayrı kalır. 166 hedefte pozitif temsil bağı bulunmadı; iki humeral konum çözümsüzdür. Bunlar kaynakta/anatomide yokluk veya tamamlanma sayısı değildir. Sıfır uzman kabulü; bütün bölge hücreleri açık. Yeni gözlemler ana gövde geometrisini değiştirmez.

Sekiz çoğul kas dalı hedefi yalnız aynı kapsamlı kaynak gruplarına bağlanır; tek tek numaralı dallar veya tam kas uçları değildir. Bilateral C5–T1 katkıları ve medial/lateral kordların 14 gereksinimi açık ve değişmeden kalır. Referanstaki 47 nesne bu sınırlı 352 hedefe zorla eşlenmez; başka bölge/kapsam incelemesi gerekir. Mevcut v1 Latin düzeltmeleri ve 18 kesin Latin boşluğu korunur.

[Kaynak eşleme kanıtı](../../data/model-candidates/upper-limb-target-bindings-v2/REVIEW.md) ile [ürün incelemesi](upper-limb-nerve-reference-review.md) farklı kabul aşamalarıdır. Temsil bağı kaynak üyeliği, taraf ve kullanılabilir seçimi gösterir; tam seyir, temas, ağ devamlılığı, D2 ayrıntı veya anatomik uzman kabulü değildir. Ana model ile ayrı referans aynı kaynak koordinatlarında birleşmiş sayılmaz.

Üretim: `python3 scripts/build-upper-limb-reference-targets.py`; yazmadan kontrol: `--check`. Üretici sabitlenmiş aday/v1 kimlik ve hash'lerini, public kavram/parça/etiket üyeliğini ve kayıtlı yerel üretim kabulünün giriş hash'lerini denetler. Canlı yayın ayrı teslim raporunda doğrulanır. [Genel envanter](model-inventory.md) tüm 508 alt/üst gereksinimi, bağsız kayıtlar dahil, bekleyen ayrıntı hücrelerine bağlar.
'''
for path, content in [(OUTPUT, json.dumps(result, ensure_ascii=False, indent=2)+'\n'),
                      ('docs/model/upper-limb-targets-v2.md', doc)]:
    if '--check' in sys.argv:
        assert (ROOT/path).read_text() == content, path + ' stale'
    else:
        (ROOT/path).write_text(content)
print(json.dumps({'targets':352, 'addedRuntimeBindings':added, 'unchangedTargets':272,
                  'meshObservedTargets':178, 'expertAccepted':0}))
