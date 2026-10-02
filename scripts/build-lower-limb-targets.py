"""Reproduce a non-exhaustive, individually identified lower-limb target seed.

Requirements are project proposals, not an authoritative medical syllabus.
Observed source-label bindings are candidates for anatomical acceptance, not
an independently verified TA2-to-FMA ontology crosswalk.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = 'work/open-assets-review/TA2.csv'
EXPECTED_TA2 = '0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
digest = lambda p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
assert digest(TABLE) == EXPECTED_TA2, 'Pinned terminology changed'
rows = [row[0].split(';') if len(row) == 1 else row for row in
        csv.reader((ROOT / TABLE).read_text(encoding='utf-8-sig').splitlines())]
atlas_path = 'public/models/atlas.json'
reference_path = 'public/models/lower-limb-nerve-reference/atlas.json'
atlas = json.loads((ROOT / atlas_path).read_text())
reference = json.loads((ROOT / reference_path).read_text())
base = {c['id']: c for c in atlas['concepts']}
ref = {c['id']: c for c in reference['concepts']}

# Exact source labels are recorded independently of the TA2 terminology identity.
# Tuple: term, family, detail, bilateral base IDs/names, bilateral reference IDs.
SEEDS = [
 ('Tibia','skeletal-support','D1',['FMA24478','FMA24477'],['left tibia','right tibia'],['zanatomy:tibia-l','zanatomy:tibia-r']),
 ('Fibula','skeletal-support','D1',['FMA24481','FMA24480'],['left fibula','right fibula'],['zanatomy:fibula-l','zanatomy:fibula-r']),
 ('Patella','skeletal-support','D1',['FMA24487','FMA24486'],['left patella','right patella'],['zanatomy:patella-l','zanatomy:patella-r']),
 ('Talus','skeletal-support','D1',['FMA24483','FMA24482'],['left talus','right talus'],['zanatomy:talus-l','zanatomy:talus-r']),
 ('Calcaneus','skeletal-support','D1',['FMA24498','FMA24497'],['left calcaneus','right calcaneus'],['zanatomy:calcaneus-l','zanatomy:calcaneus-r']),
 ('Navicular bone','skeletal-support','D1',['FMA24501','FMA24500'],['navicular bone of left foot','navicular bone of right foot'],None),
 ('Cuboid bone','skeletal-support','D1',['FMA24529','FMA24528'],['left cuboid bone','right cuboid bone'],None),
 ('Medial cuneiform bone','skeletal-support','D1',['FMA24522','FMA24521'],['left medial cuneiform bone','right medial cuneiform bone'],None),
 ('Intermediate cuneiform bone','skeletal-support','D1',['FMA24524','FMA24523'],['left intermediate cuneiform bone','right intermediate cuneiform bone'],None),
 ('Lateral cuneiform bone','skeletal-support','D1',['FMA24526','FMA24525'],['left lateral cuneiform bone','right lateral cuneiform bone'],None),
 ('Tibialis anterior muscle','muscle-tendon-fascia','D1',['FMA22545','FMA22544'],['left tibialis anterior','right tibialis anterior'],None),
 ('Extensor digitorum longus','muscle-tendon-fascia','D1',['FMA22549','FMA22548'],['left extensor digitorum longus','right extensor digitorum longus'],None),
 ('Extensor hallucis longus','muscle-tendon-fascia','D1',['FMA22547','FMA22546'],['left extensor hallucis longus','right extensor hallucis longus'],None),
 ('Fibularis longus muscle','muscle-tendon-fascia','D1',['FMA22553','FMA22552'],['left fibularis longus','right fibularis longus'],None),
 ('Fibularis brevis muscle','muscle-tendon-fascia','D1',['FMA22555','FMA22554'],['left fibularis brevis','right fibularis brevis'],None),
 ('Tibialis posterior muscle','muscle-tendon-fascia','D1',['FMA65019','FMA65018'],['left tibialis posterior','right tibialis posterior'],None),
 ('Flexor digitorum longus','muscle-tendon-fascia','D1',['FMA65017','FMA65016'],['left flexor digitorum longus','right flexor digitorum longus'],None),
 ('Flexor hallucis longus','muscle-tendon-fascia','D1',['FMA65015','FMA65014'],['left flexor hallucis longus','right flexor hallucis longus'],None),
 ('Soleus muscle','muscle-tendon-fascia','D1',['FMA22559','FMA22558'],['left soleus','right soleus'],None),
 ('Tibial nerve','neurovascular-lymph','D1',None,None,['atlas:left-tibial-nerve','atlas:right-tibial-nerve']),
 ('Common fibular nerve','neurovascular-lymph','D1',None,None,['atlas:left-common-fibular-nerve','atlas:right-common-fibular-nerve']),
 ('Deep fibular nerve','neurovascular-lymph','D2',None,None,None),
 ('Superficial fibular nerve','neurovascular-lymph','D2',None,None,None),
 ('Sural nerve','neurovascular-lymph','D1',None,None,None),
 ('Medial plantar nerve','neurovascular-lymph','D2',None,None,None),
 ('Lateral plantar nerve','neurovascular-lymph','D2',None,None,None),
 ('Anterior tibial artery','neurovascular-lymph','D1',['FMA43897','FMA43896'],['left anterior tibial artery','right anterior tibial artery'],None),
 ('Posterior tibial artery','neurovascular-lymph','D1',['FMA43899','FMA43898'],['left posterior tibial artery','right posterior tibial artery'],None),
 ('Fibular artery','neurovascular-lymph','D1',None,None,None),
 ('Popliteal artery','neurovascular-lymph','D1',['FMA77381','FMA77380'],['left popliteal artery','right popliteal artery'],None),
 ('Anterior talofibular ligament','skeletal-support','D2',None,None,None),
 ('Posterior talofibular ligament','skeletal-support','D2',None,None,None),
 ('Calcaneofibular ligament','skeletal-support','D2',None,None,None),
]
targets = []
for term, family, detail, ids, source_names, ref_ids in SEEDS:
    matches = [(line, row) for line, row in enumerate(rows, 1)
               if len(row) >= 3 and row[1] == term]
    assert len(matches) == 1, f'Ambiguous exact terminology: {term}'
    line, row = matches[0]
    for index, side in enumerate(['left','right']):
        representations = []
        if ids:
            c = base[ids[index]]
            assert c['name'] == source_names[index]
            representations.append(dict(datasetId='male-body', conceptId=c['id'],
                sourceName=c['name'], partIds=c['elements'], sourceManifest=atlas_path,
                locator=f"concepts/{c['id']}", identityReview='exact_source_label_candidate; expert_pending'))
        if ref_ids:
            c = ref[ref_ids[index]]
            representations.append(dict(datasetId='lower-limb-nerve-reference', conceptId=c['id'],
                sourceName=c['name'], partIds=c['elements'], sourceManifest=reference_path,
                locator=f"concepts/{c['id']}", identityReview='preserved_named_source_object; expert_pending'))
        region = 'hip-thigh-knee' if term in ['Patella','Popliteal artery'] else 'leg-ankle-foot'
        relations = {'skeletal-support':['joint/support context where applicable'],
          'muscle-tendon-fascia':['originates_at','inserts_at','motor innervation'],
          'neurovascular-lymph':['named source/branch hierarchy','verified targets or territories','cross-region continuity']}[family]
        targets.append(dict(id=f'lower-limb-v1:ta2:{row[0]}:{side}', regionId=region,
          familyId=family, side=side, requiredDetail=detail,
          requirementStatus='project_proposed; curriculum_and_expert_acceptance_pending',
          terminology=dict(ta2TableId=int(row[0]),en=row[1],la=row[2],sourcePath=TABLE,
            locator=f'CSV line {line}; English/Latin columns',
            scope='Unsided term; laterality is an explicit project target field, not a lateralized TA2 identifier',
            fmaCrosswalk='not_asserted'),
          representations=representations,
          representationReview='observed_source_binding; detail_and_visual_review_pending' if representations
            else 'unbound_after_exact_label_seed_audit; broader_source_and_subobject_audit_pending',
          absenceClaim=False, requiredRelationships=relations,
          technicalAcceptance='pending_target_level_reconciliation',expertReview='pending',
          openCriteria=['required scope and laterality acceptance','independent geometry and detail review',
            'labels and required relationships','context and product journey','named anatomical expert review']))

for target in targets:
    for representation in target['representations']:
        manifest = atlas if representation['datasetId']=='male-body' else reference
        part_ids = {p['id'] for p in manifest['parts']}
        assert representation['partIds'] and set(representation['partIds']) <= part_ids
assert len(targets)==66 and len({t['id'] for t in targets})==66
snapshots=[dict(path=p,sha256=digest(p)) for p in [TABLE,atlas_path,reference_path,'scripts/build-lower-limb-targets.py']]
summary=dict(targets=len(targets),terms=len(SEEDS),withObservedRepresentation=sum(bool(t['representations']) for t in targets),
 unbound=sum(not t['representations'] for t in targets),anatomicallyAccepted=0)
result=dict(schemaVersion=1,scopeVersion='lower-limb-target-seed-v1',complete=False,
 generatedBy='python3 scripts/build-lower-limb-targets.py',
 scope='Non-exhaustive individually identified knee/leg/ankle/foot D1 and selected D2 requirements',
 countingPolicy='Bilateral project targets, not independent anatomy counts or a whole-body completion denominator',
 inputSnapshots=snapshots,summary=summary,targets=targets,
 unexpandedRequirements=['metatarsals and phalanges','intrinsic foot muscles and gastrocnemius heads',
 'tendons, fascia and retinacula','complete joints, supports and bursae','venous and lymphatic paths',
 'cutaneous/muscular/digital nerve branches and territories','D0 context acceptance','D3 targets',
 'all other regions of the full model-scope-v1 contract'],
 caveats=['Exact source-label correspondence is an inspection candidate, not a formal TA2/FMA crosswalk.',
 'Unbound means this bounded seed did not bind geometry; it is not absence in all sources.',
 'Active source concept membership can include multiple pieces; independent detail is not assumed.',
 'No region/family cell is closed and no anatomical acceptance is declared.'])
doc=f'''# Alt ekstremite yapı hedefleri — ilk bireysel liste

Bu sürüm {summary['targets']} sağ/sol proje hedefini, {summary['terms']} kesin TA2 teriminden açar. D1 ve seçilmiş D2 için **eksiksiz olmayan başlangıç listesidir**; bütün bölge veya bütün P1 kabulü değildir. Gereken ayrıntı ve taraf, uzman/müfredat incelemesi bekleyen proje gereksinimidir.

{summary['withObservedRepresentation']} hedefte mevcut kaynak kavramı veya bağımsız referans nesnesiyle gözlenen parça bağı vardır; {summary['unbound']} hedef henüz bağlanmamıştır. Bu sayılar anatomik kabul veya tamamlanma yüzdesi değildir. Kaynak üyelikleri aynen saklanır. İsim eşleşmesi bağımsız alt geometriyi, doğru konumu veya resmî TA2–FMA eşlemesini kanıtlamaz.

[Makine listesi](../../data/anatomy/regional-targets-lower-limb-v1.json), terim/satır kimliği, taraf, gereken ayrıntı, dataset, kaynak kavramı ve parça bağlarını, ilişkileri ve açık kabul koşullarını taşır. `python3 scripts/build-lower-limb-targets.py` üretir; `--check` dosyaları değiştirmeden güncelliği doğrular. Sabit TA2 kaynağı önceki intake altındaki yerel dosyadır; SHA doğrulanmadan üretim yapılmaz.

| Terim | TA2 | Ayrıntı | Sol / sağ gözlenen bağ sayısı |
| --- | ---: | --- | --- |
'''
for i,(term,_,detail,_,_,_) in enumerate(SEEDS):
    pair=targets[2*i:2*i+2]
    doc+=f"| {term} | {pair[0]['terminology']['ta2TableId']} | {detail} | {len(pair[0]['representations'])} / {len(pair[1]['representations'])} |\n"
doc+='''
Tibia/fibula/patella/talus/calcaneus iki ayrı gövdeye ait temsillerle kayıtlıdır; geometrileri birleştirilmez. Tibial/ortak fibular sinirler ayrı alt ekstremite referansındadır. Yeni referansın ana gövdeye distal kaydı kabul edilmemiştir. Arter kavramlarının birden çok parça içermesi açıkça listelenir; dal kapsamı ayrıca denetlenecek.

Ayak parmak/metatars kemikleri, iç kaslar, gastrocnemius başları, tendon/fasya/retinakulum, tam eklem desteği, ven/lenf, ince sinir dalları ve D3 hedefleri açılmaya devam edecek. Sıfır uzman kabulü vardır; kayıtlar hiçbir kapsam hücresini kapatmaz. Sonraki somut iş: bağlanmamış distal sinir ve ayak bileği bağ hedeflerini kaynak alt nesneleriyle denetlemek.

Doğrulama: 66 benzersiz hedef, 33 kesin TA2 terim/satır çifti, elle seçilmiş mevcut kaynak kavramlarının tam ad karşılıkları ve tüm gözlenen parça bağlarının kendi manifestinde çözülmesi. Bu kontrol geometri/görsel/uzman kabulü değildir.
'''
for p,content in [('data/anatomy/regional-targets-lower-limb-v1.json',json.dumps(result,indent=2)+'\n'),
                  ('docs/model/lower-limb-targets-v1.md',doc)]:
    if '--check' in sys.argv: assert (ROOT/p).read_text()==content, f'{p} is stale'
    else: (ROOT/p).write_text(content)
print(json.dumps(summary))
