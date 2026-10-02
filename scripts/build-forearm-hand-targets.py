"""Activate P4 requirements with current source-membership checks, not anatomy acceptance."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = 'data/model-candidates/forearm-hand-target-inventory-v1/proposal.json'
OUTPUT = 'data/anatomy/regional-targets-forearm-hand-v1.json'
cache = {}
def read(p):
    if p not in cache:
        cache[p] = json.loads((ROOT/p).read_text())
    return cache[p]
sha = lambda p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
candidate = read(CANDIDATE)
result = copy.deepcopy(candidate)
paths = {CANDIDATE, 'scripts/build-forearm-hand-targets.py',
         'data/model-candidates/forearm-hand-target-inventory-v1/frozen-inputs.json'}
assert len(result['targets']) == len({t['id'] for t in result['targets']}) == 502
observations = 0
for target in result['targets']:
    assert target['regionId'] == 'forearm-wrist-hand' and target['ownerPackage'] == 'P4'
    assert not target['complete'] and not target['anatomicallyAccepted'] and not target['absenceClaim']
    assert target['expertReview'] == 'pending'
    for binding in target['representations']:
        path = binding['sourceManifest']
        paths.add(path)
        manifest = read(path)
        concept = next(c for c in manifest['concepts'] if c['id'] == binding['conceptId'])
        assert concept == binding['sourceConcept']
        assert concept['elements'] == binding['partIds']
        parts = {p['id']:p for p in manifest['parts']}
        for observed in binding['observedParts']:
            actual = parts[observed['id']]
            assert all(actual[k] == v for k,v in observed.items()), (target['id'], observed['id'])
            assert actual['vertexCount'] > 0 and actual['indexCount'] > 0
        observations += 1
assert observations == 210
assert sum(bool(t['representations']) for t in result['targets']) == 188
assert sum(bool(t.get('relatedGroupEvidence')) and not t['representations'] for t in result['targets']) == 22
result['status'] = 'active_project_requirements;source_membership_observations;anatomical_acceptance_pending'
result['sourceAudit'] = CANDIDATE
result['activationInputSnapshots'] = [{'path':p,'sha256':sha(p)} for p in sorted(paths)]
doc = '''# Önkol, el bileği ve el hedefleri — v1

502 sağ/sol gereksinim aktif iş envanterine alındı:162 kemik/eklem/destek,176 kas/tendon/fasya,140 sinir/damar/lenf,24 kompartıman/geçit.162 D1 ve340 seçilmiş D2 hedefi; eksiksiz müfredat veya tamamlanma paydası değildir. [Makine kaydı](../../data/anatomy/regional-targets-forearm-hand-v1.json) [adayın](../../data/model-candidates/forearm-hand-target-inventory-v1/REVIEW.md) bütün502 kaydını aynen korur.

188 hedefte210 kaynak üyeliği gözlemi vardır:160 ana gövde ve50 bağımsız üst ekstremite referansı.314 hedefte bu sınırlı denetimde pozitif bağ bulunmadı; kaynakta/anatomide yokluk değildir.22 tekil lumbrikal/interosseöz hedefi, birleşik kaynak gruplarına bağlanmaz; yalnız ilgili grup kanıtı taşır. Sekiz kas bütününün kaynak başları bütün kas geometrisi yerine geçmez. Bu envanter yeni geometri/etiket/ilişki veya bölgesel/uzman kabulü eklemez.

Numeric terimler ve özgün satırlar korunur. Asterisk kaynak uzantıları numeric TA2 gibi sunulmaz;2486/4644/4646 şüpheli Latin değerleri kanıt olarak saklanır, aday gösteriminde verilmez. Grup, taraf, digit ve parça kapsamları ayrı kalır. Mevcut ilişki kimlikleri tarihî kanıttır; başka dataset'e yeni ilişki oluşturmaz.

Üretim `python3 scripts/build-forearm-hand-targets.py`; yazmadan `--check`. Üretici aday kimliklerini ve210 gözlemin güncel manifest kavram/parça/metadata eşliğini denetler. Adayın `build.py --check` kontrolü kendi frozen snapshot'ını kullanır; tarihî gözlem yeni aktif kaynak değişiminden bağımsızdır. [Genel envanter](model-inventory.md) tüm1.010 alt/üst/önkol gereksinimini bağsız hedefler dahil208 bekleyen hücreye bağlar. Kaynak seyri/teması, tekil ayrıntı ve uzman kabulü açık kalır. Sıradaki kaynak denetimi tekil intrinsik el kasları ve el bileği destekleridir.
'''
for path, content in [(OUTPUT,json.dumps(result,ensure_ascii=False,indent=2)+'\n'),
                      ('docs/model/forearm-hand-targets-v1.md',doc)]:
    if '--check' in sys.argv:
        assert (ROOT/path).read_text() == content, path+' stale'
    else:
        (ROOT/path).write_text(content)
print(json.dumps({'targets':502,'observedTargets':188,'observations':210,'unbound':314,'expertAccepted':0}))
