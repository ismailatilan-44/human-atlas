# Ayak kemikleri hedef adayları — v1

2 Ekim 2026, başlangıç revision'ı `41723bdf937ce50976c118230b0a29441700d4a2`. [proposal.json](proposal.json) yalnız aday kanıttır; aktif atlas, hedef listesi veya yayın değiştirilmez. Entegrasyon ve kapanış sahibi root'tur.

**38 hedefin tamamı iki dataset içinde ayrı kaynak kavramına ve tek parçaya bağlıdır:** 10 bilateral metatars ve 28 bilateral ayak falanksı; toplam 76 dataset-qualified temsil. Ana BodyParts3D 4.0 atlasındaki 38 FMA kavramı/38 FJ parçası ile bağımsız Z-Anatomy referansındaki 38 kaynak nesnesi korunur. İki datasetin aynı koordinat, örnek veya yüzey geometrisine sahip olduğu iddia edilmez. Sıfır anatomik uzman kabulü vardır.

## Ana atlasın bireysel parça kanıtı

| Hedef | Sol kavram / parça | Sağ kavram / parça |
| --- | --- | --- |
| 1. metatars | `FMA24508` / `FJ3241` | `FMA24507` / `FJ3351` |
| 2. metatars | `FMA24510` / `FJ3244` | `FMA24509` / `FJ3353` |
| 3. metatars | `FMA24512` / `FJ3247` | `FMA24511` / `FJ3355` |
| 4. metatars | `FMA24514` / `FJ3250` | `FMA24513` / `FJ3357` |
| 5. metatars | `FMA24516` / `FJ3253` | `FMA24515` / `FJ3359` |
| 1. parmak distal falanks | `FMA32651` / `FJ3182` | `FMA32650` / `FJ3192` |
| 1. parmak proximal falanks | `FMA43254` / `FJ3329` | `FMA43253` / `FJ3310` |
| 2. parmak distal falanks | `FMA32653` / `FJ3179` | `FMA32652` / `FJ3189` |
| 2. parmak middle falanks | `FMA32643` / `FJ3293` | `FMA32642` / `FJ3300` |
| 2. parmak proximal falanks | `FMA32635` / `FJ3328` | `FMA32634` / `FJ3319` |
| 3. parmak distal falanks | `FMA32655` / `FJ3180` | `FMA32654` / `FJ3190` |
| 3. parmak middle falanks | `FMA32645` / `FJ3294` | `FMA32644` / `FJ3301` |
| 3. parmak proximal falanks | `FMA32637` / `FJ3311` | `FMA32636` / `FJ3320` |
| 4. parmak distal falanks | `FMA32657` / `FJ3181` | `FMA32656` / `FJ3191` |
| 4. parmak middle falanks | `FMA32647` / `FJ3295` | `FMA32646` / `FJ3302` |
| 4. parmak proximal falanks | `FMA32639` / `FJ3312` | `FMA32638` / `FJ3321` |
| 5. parmak distal falanks | `FMA32659` / `FJ3185` | `FMA32658` / `FJ3195` |
| 5. parmak middle falanks | `FMA230988` / `FJ3298` | `FMA230986` / `FJ3305` |
| 5. parmak proximal falanks | `FMA32641` / `FJ3315` | `FMA32640` / `FJ3324` |

Her satırdaki kavramın `elements` alanı bir mevcut `parts` kaydına çözülür; parça `conceptId` ve kaynak adı da aynı kavramı gösterir. Nonzero vertex/index sayıları, sonlu bounds, ayrı parça kimlikleri ve knowledge graph geometri bağı kontrol edildi. Bunlar isim eşleşmesinden daha ileri manifest kanıtıdır; binary yüzey kalitesi, doğru anatomi veya kullanıcı akışı kabulü değildir. Tutulan resmî ISA ad ve eleman tablolarının tam satır/üyelik karşılıkları JSON'dadır.

## Terimler ve etiket önerileri

38 yeni ana-atlas bireysel TR/EN etiket önerisi mevcut referanstaki taraf/digit/segment ayrımını sürdürür. Latince dört kayıtta (bilateral birinci/beşinci metatars) tam sayısal kaynak satırıyla doğrulanmıştır. Diğer 34 kayıtta parmağa özgü Latin `null` kalır: 28 falanks ve ikinci–dördüncü metatarsların altı taraflı kaydı. Kaynağın `1510*1`, `1511*2`, `1512*1`, `1496*2` vb. yıldızlı satırları resmî bağımsız sayısal TA2 kimliği diye kullanılmaz; ham metin ve satır numarası korunur. Örneğin kaynak `Os quatum metatarsi` yazımı otomatik düzeltilmez.

Bütün 38 hedefte ayrıca tam eşleşen genel sayısal terim kanıtı vardır: TA2 1496 `Metatarsal bone / Os metatarsi`; TA2 1510 `Proximal phalanx of foot / Phalanx proximalis pedis`; TA2 1511 `Middle phalanx of foot / Phalanx media pedis`; TA2 1512 `Distal phalanx of foot / Phalanx distalis pedis`. Genel term, parmağa özgü Latince görünüm etiketi yerine geçirilmez. Birinci/beşinci metatarsın özel sayısal satırları TA2 1500 ve 1502'dir. Bunlar sabitlenmiş Z-Anatomy dağıtımlı TA2 tablosunun birebir kanıtıdır; bu çalışma yeni bir resmî TA2–FMA crosswalk yayımlamaz. Türkçe editoryaldir ve uzman incelemesi bekliyor.

## Mevcut kaynak ebeveynleri ve gezinme

Kaynak PART-OF tablosunda ve mevcut `knowledge.json` içinde **38 doğrudan ilişki zaten vardır**: 28 falanks ilgili tarafın ilgili toe kavramına, 10 metatars aynı tarafın foot proper kavramına bağlıdır. `existingRelationshipEvidence` bu mevcut kayıtları, kaynak satırını ve `reuse_existing_graph_navigation; do_not_add_duplicate` kararını taşır. Yeni ilişki önerisi sayısı sıfırdır. Z-Anatomy tarafına yeni grup veya part_of aktarılmaz. Articulates_with ve attaches_to ilişkileri bu alt görevin dışındadır.

On dört ebeveynin tam kaynak adları, IDs, parça listeleri ve kemik kapsamları `parentScopeRecords` içinde; TR/EN/LA önerileri `mainParentLabelProposals` içindedir. On toe etiketi için genel parmağa tam uyan sayısal TA2 171–175 terimleri vardır (kaynak big toe görünümde great toe olarak normalize edilir). İki foot proper etiketi için kapsamı tam karşılayan Latince doğrulanmadığından `null` bırakılır; daha geniş `Foot / Pes` yerine kullanılmaz.

Toe kaynak seçimleri başparmakta iki, diğer parmaklarda üç **falanks kemiği** gösterir; parmağın tüm deri, kas, tendon, damar/sinir, kıkırdak veya kapsülünü göstermez. Foot proper kaynak seçimleri yalnız beş **metatars** içerir; tarsallar ve yumuşak dokular o parça kümesinde yoktur. Ebeveynlerin anatomik adları mevcut kaynak kimlikleridir; eksik doku kapsamı `representationNoteTr` ve `scopeNoteTr` alanlarında açık yazılmıştır. Parça üyeliğinden yeni anatomik bağ çıkarılmadı.



Gerçek yerel UI'da görülen immediate-parent fallback nedeniyle iki mevcut ayak ebeveyni eklendi: `FMA11344` left foot ve `FMA11343` right foot. TR `Ayak`, EN `Foot`, LA `Pes` eşlemesi sabit tabloda TA2 **166**, CSV **168** satırına birebir uyar; taraf ayrı tutulur. Her seçimdeki **26** mevcut parça (yedi tarsal, beş metatars, 14 falanks), PART-OF ad ve tam eleman üyelik tablolarıyla doğrulandı. Tam FJ listeleri ve parça adları `parentScopeRecords` içindedir. `representationNoteTr` yalnız bu kemik gösterimini belirtir; ayağın tüm kas, arter, sinir, tendon veya yumuşak dokularını içerdiği iddia edilmez. Önceki iki foot-proper etiketinin kapsamı ve Latin null durumu değişmedi.

`existingParentPathEvidence` on toe ve iki foot-proper kavramından aynı tarafın ayağına giden **12 zaten mevcut** PART-OF kaydını kaynak satırlarıyla doğrular. Bunlar yeni relationship değildir; root mevcut graph navigation'ını kullanır. Toplam 38+12 kaynak-yolu kaydı incelenmiştir, yeni relationship sayısı sıfırdır. Etiket önerileri 38 bireysel +14 ebeveyn =52; bunların 16'sında exact kapsamlı Latin vardır, 36'sında gerekçeli null korunur.

## Kaynaklar, doğrulama ve devir

Resmî BodyParts3D arşiv kaynakları: [ISA adları](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_parts_list_e.txt), [ISA eleman üyelikleri](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt), [PART-OF adları](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_parts_list_e.txt), [PART-OF eleman üyelikleri](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_element_parts.txt), [PART-OF ilişkileri](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_inclusion_relation_list.txt). Terimler [sabit Z-Anatomy TA2 tablosundan](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv) okunmuştur. Önceden tutulmuş kaynak dosyaları 2 Ekim'de incelendi; bu alt görevde yeni web erişimi yapılmadı. Bütün girdi hash'leri JSON'dadır.

Yerel macOS/Python 3 üzerinde `python3 data/model-candidates/foot-bone-targets-v1/build.py --check` geçti: deterministik JSON; 38 benzersiz hedef; her datasette 38 ayrı tek-parçalı manifest bağı; 52 etiket önerisi (38 bireysel +14 ebeveyn); 38 bireysel ve 12 ebeveyn-yolu kaynak ilişkisinin mevcut graph eşitliği; exact numeric vs yıldızlı terim ayrımı; sıfır yeni ilişki ve sıfır uzman kabulü. Önceden entegre edilen 50 etiketle bireysel/ebeveyn önerilerin birebir eşitliği veya yokluğu idempotent conflict guard ile kontrol edildi; mevcut root düzenlemesi korundu. App/build/browser/geometri render testi yapılmadı; bu görev aktif yüzey değiştirmez.

Bir doğrulama düzeltmesi yapıldı: ebeveyn toe/foot-proper kavramları ISA tablosunda aranmamalıydı; doğru kaynak PART-OF ad/eleman tabloları ayrı okunarak aynı kavram/üyelik kanıtı doğrulandı. Geniş tarama veya varsayılan grup oluşturmak gerekmedi. Süre ölçümü [timing.json](timing.json) içinde tutulur. Dosyalar yalnız bu aday dizininde yazıldı; commit/push/yayın yapılmadı.

Sonraki eylem: root mevcut 38 bireysel kemiğin hedef kayıtlarını ve kapsamı açık 52 etiket önerisini entegre edip mevcut PART-OF gezinmesi üzerinden seçim→ilişki→geri dönüş akışını doğrular. Bu alt görevin çıktı sahipliği serbest bırakılmıştır; anatomik uzman, görsel kabul ve yayın kabulü açık kalır.


## Root integration — local acceptance

Root integration added all 52 proposals unchanged to active main labels, with existing graph/geometry preserved. The final deterministic candidate check passed after activation. v2 preserves all 66 historical targets and adds the 38 foot targets (104 total). TypeScript, interaction/source/target/inventory checks and desktop/mobile UI acceptance passed. Anatomical expert acceptance is still pending. Source revision and publication are recorded separately in the [owning action report](../../../docs/model/progress-report-2026-10-02.md); the preceding delegated/source audit remains historical evidence.
