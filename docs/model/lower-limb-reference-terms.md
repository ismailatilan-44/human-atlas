# Alt ekstremite referansı — 119 nesneli güncel metadata

2 Ekim yerel entegrasyonu:119 TR/EN,83 kesin Latin etiket ve84 kaynaklı ilişki. Önceki87 etiket/72 ilişki korunur;30 kas nesnesi veiki sesamoid grubu eklenir. İki kaynak yazım kusurlu Latin alan ile34 dijite özgü Latin alan null kalır. Baş/grup sınırları ve uzman incelemesi görünürdür. [Yeni metadata kanıtı](../../data/model-candidates/foot-soft-tissue-metadata-v1/REVIEW.md) ve [kaynak/geometri](../../data/model-candidates/foot-soft-tissue-source-audit-v1/REVIEW.md) ayrı izlenir.12 yeni kas ilişkisi yalnız iki bütün kas için başlangıç/tutunma/innervasyon gerçeklerini açar;model footprint veya motor dalı değildir. Yayın kabulü [eylem raporunda](progress-report-2026-10-02.md).

## 87 nesneli genişleme — tarihî kanıt

2 Ekim 2026; başlangıç kaynak revision'ı `e879fc92e1bfa6226898d12cdca2863e365858e0`. Aşağıdaki 21 nesneli ilk teslim kaydı tarihî kanıt olarak korunmuştur. Güncel [metadata](../../data/anatomy/lower-limb-reference.json) **87 etiket / 12 ilişki** içerir: 16 adlandırılmış sinir nesnesi, iki fibular arter nesnesi, altı ayak bileği bağ nesnesi ve 63 kemik bağlamı. İlk 21 etiket ve dört ilişki aynı alan/değerlerle korunmuştur; 66 yeni nesne kaydı eklenmiştir. Bu sayılar tam alt ekstremite ağı, bağımsız spline/dal sayısı veya anatomik bölge kabulü değildir.

## Yeni adlar ve Latin kapsamı

Bütün 87 nesnenin Türkçe ve İngilizce adı, kaynak nesne adı ve dataset/side alanı vardır. Kaynak `finger of foot` kimlikleri değiştirilmez; İngilizce görünüm `toe` kullanır. Parmak/metatars numarası `digit`, numaranın sistemi `digitSystem`, falanks düzeyi `phalanxPosition` alanında tutulur. Taraf, numara ve bağlam rolü birbirine karıştırılmaz. Türkçe karşılıklar editoryaldir, uzman incelemesi bekliyor.

**53 kayıtta** sayısal kimlikli sabit upstream TA2 satırına uyan Latince görünüm etiketi vardır. **34 kayıtta** özel Latince görünüm alanı `null` kalır: bilateral 14 ayak falanksı (28) ve bilateral ikinci–dördüncü metatarslar (6). Kaynak bunları `1510*1`, `1511*2`, `1512*1`, `1496*2` gibi yıldızlı genişletme kimlikleriyle verir; bu satırlar resmî bağımsız parmak TA2 kimliği sayılmaz. Örneğin dördüncü metatars satırında `Os quatum metatarsi` yazılıdır. Bu metin `sourceTableRow` altında kaynağın kendi yazımı olarak korunur; doğrulanmış görünüm terimi diye sunulmaz ve sessizce düzeltilmez.

Bu 34 kayıtta genel terim ayrı `genericTerm` alanındadır: metatarsal bone TA2 1496 / `Os metatarsi` (CSV 1571); proximal phalanx of foot TA2 1510 / `Phalanx proximalis pedis` (1588); middle phalanx of foot TA2 1511 / `Phalanx media pedis` (1594); distal phalanx of foot TA2 1512 / `Phalanx distalis pedis` (1599). Genel terim, parmağa özgü doğrulanmış Latince etiket yerine otomatik geçirilmemelidir. `latinUnavailableReason` görünümün bu kapsam eksikliğini açıklamasına izin verir. Birinci ve beşinci metatarsların sayısal TA2 satırları (1500/1502) birebir doğrulanmıştır.

## Yeni kaynaklı ilişkiler

[TTUHSC anterior/lateral leg and foot anatomy tables](https://anatomy.ttuhscep.edu/musculoskeletal_system/leg_tables.html) 2 Ekim 2026'da yeniden okundu. Nerves tablosunda deep/superficial fibular satırlarının Source sütunu common fibular; medial/lateral plantar satırlarının Source sütunu tibial verir. Bu dört doğrudan kaynak ilişkisi iki tarafta sekiz `branch_of` kaydı olarak eklendi. İlk dört tibial/common fibular → sciatic ilişkisi aynen korunur. Bütün uçlar aynı dataset ve aynı taraftadır; yalnız tipik anatomi ilişkisi ifade edilir, örneğe özgü tüp sürekliliği veya innervasyon çıkarılmaz. Eğitim tablosu yeniden dağıtılmaz, yalnız seçilmiş kaynak bilgileri/locator saklanır. Yardımcı foot_tables URL'sinin araç erişimi başarısız oldu; dört ilişkiyi de sağlayan leg_tables kaynağı başarılıydı ve tek yeni ilişkinin kaynağıdır.

Sural sinire tek ebeveyn atanmadı. Fibular arter için ana erkek atlasın ilişkileri aktarılmadı. Bu pakette damar besleme alanı, bağ tutunması, kemik komşuluğu veya yeni FMA eşlemesi üretilmedi.

## Geometri kapsamının metadata karşılığı

[Kaynak nesne eşlemesi](../../data/model-candidates/lower-limb-unbound-source-audit/new-object-mapping.json), [18 hedef nesne incelemesi](../../data/model-candidates/lower-limb-unbound-source-audit/evaluated-candidates.json) ve [48 yeni kemik bağlamı](../../data/model-candidates/lower-limb-unbound-source-audit/foot-context.json) geometri çalışanına aittir. Metadata yalnız bu kimlikleri, sourceObject değerlerini ve kayıtlı temsil sınırını devralır. Sinir/arter eğrileri kısmi kaynak gösterimidir; tüm damar veya sinir ağı olarak sunulmaz. Bağ nesneleri bütün eklemi veya doğrulanmış tutunma alanını temsil etmez.

Medial plantar sinirin her tarafında **üç yazılmış spline** vardır: kontrol noktası sayıları 4, 1, 2. İkisi tüp geometrisi üretir; tek noktalı spline için ek yüzey üretilmez. Sural sinirin üç, fibular arterin beş spline'ı kaynak nesnesinin iç kapsamıdır; ayrı anatomik dal kimlikleri değildir. Yeni kaynak/metin kabulü ile geometri, uygulama ve anatomik uzman kabulü ayrı tutulur.

## Doğrulama ve devir

Son kontrol 2 Ekim 2026 08:59:48 UTC'de geçti. Güncel 87 manifest kavramı ve bütün sourceObject değerleri metadata ile birebir eşleşti (manifest SHA-256 `a9b76a85da63937bd3c34230c902457d330cec7b75ab6df41c3db9b1cd8154ed`). Metadata SHA-256 `715dbb69409e6bea7824bb4e5a2a23be1cfaab387929b4be23b2baa5d6306b3e`. Kaydedilmiş başlangıç 08:52:17 UTC'den bu kontrole kadar 451 saniye; bunun öncesindeki okuma ve sonraki devir iletişimi ölçüme dahil değildir. Geometri çalışanının eşzamanlı foot-context kanıt düzeltmesinden sonra yalnız etkilenen hash yeniden alındı.

Metadata için hedefli yerel Python kontrolleri: 87 benzersiz kimlik ve 12 ilişki; başlangıç 21 etiket/dört ilişkinin `e879fc9` içeriğiyle eşitliği; bütün kaynak/TR/EN isimleri; 53 Latince alanın sayısal TA2 satır/kimliğiyle eşitliği; 34 null alanın gerekçesi ve genel-terim kanıtı; ilişkilerin çözülen aynı taraf uçları ve kaynakları; sural ebeveyn atanmaması. İlk `inputSnapshots` hash'leri tarihî `e879fc9` girdileri olarak korunur; ana etiket dosyasının eşzamanlı bağımsız genişlemesi bu eski kanıtı yeniden yazdırmaz. Yeni geometri kaynak kanıtlarının hash'leri `expansionInputSnapshots` içindedir.

Bu çalışan yalnız metadata ve bu terim kaydını günceller; ana labels/knowledge, hedef seed'i, uygulama ve yayın işlemleri entegrasyon sahibindedir. Geometrinin görsel kabulü, etkileşim akışı, dağıtım ve uzman kabulü bu rapordan çıkmaz. Sonraki eylem: entegrasyon sahibi 87 nesneli manifest eşitliğini, çok dilli aramayı, kapsam/null-Latin gösterimini ve ilişki→geri dönüş akışını paket kabulünde doğrular.

---

# Alt ekstremite sinir referansı — adlandırma ve ilişki kaydı

2 Ekim 2026. Metadata çalışmasının başlangıç revision'ı `a0fd55413018ec839e493719369be4f051df53dc`, dalı `codex/publish-model-explorer`. [26 Eylül raporu](progress-report-2026-09-26.md) `caa938a` yayınını anlatır; güncel yerel HEAD ile aynı değildir. Bu kayıt yalnız metadata teslimini doğrular; canlı yayın veya geometri kabulü değildir.

## Kapsam ve kullanıcı sonucu

[Dataset metadata](../../data/anatomy/lower-limb-reference.json), `lower-limb-nerve-reference` için 21 ayrı kimliği adlandırır: bilateral siyatik, tibial ve ortak fibular sinirlerin altı kaynak nesnesi ile 15 kemik bağlamı. Tibia, fibula, patella, talus, calcaneus, femur ve kalça kemiği bilateral; sacrum orta hattadır. Kaynak adları ve TR/EN/LA terimleri arama girdisi olarak hazırdır. Dört yönlü ilişki kaydı aynı tarafın tibial/ortak fibular sinirinden siyatik sinire `branch_of` yönündedir. İlişkiler kaynaklı eğitim bilgisi olup bu örneğin anatomik doğruluğunu veya tüplerin fiziksel birleşmesini kanıtlamaz.

Ana `labels.json` içindeki 275 etiket ve ana bilgi grafiği bu metadata çalışmasında değiştirilmedi. Var olan `atlas:*` sinir kimlikleri ve `zanatomy:*` kemik kimlikleri korunur. Aynı siyatik kimliği ana sahnede de bulunduğundan etiket ve ilişki erişimi dataset ile sınırlandırılmalıdır; ana sahnenin innervasyon ilişkileri bu referansa taşınmaz.

Sinirler kaynakta yazılmış kısmi eğrilerdir. Paket tam alt ekstremite ağı, kökler, distal dal nesneleri, innervasyon veya cilt dağılımı içermez. Kemikler yalnız bağlam olarak adlandırılmıştır; bu dosyada komşuluk veya eklem ilişkisi üretilmez. Türkçe karşılıklar editoryaldir; tüm anatomik uzman incelemeleri bekliyor.

## Terim kanıtı

İngilizce/Latince çiftler [Z-Anatomy'nin sabitlenmiş TA2 tablosundan](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv) birebir alınmıştır. Bu, upstream tablodaki terim eşleşmesidir; anatomik geometri veya bağımsız FMA eşlemesi kabulü değildir. Kaynak tablonun SHA-256 değeri `0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974`.

| İngilizce kaynak terimi | Birebir Latince | TA2 tablo kimliği | CSV satırı |
| --- | --- | ---: | ---: |
| Tibial nerve | `Nervus tibialis` | 6582 | 6665 |
| Common fibular nerve | `Nervus fibularis communis` | 6571 | 6654 |
| Sciatic nerve | `Nervus ischiadicus` | 6569 | 6652 |
| Tibia | `Tibia` | 1397 | 1472 |
| Fibula | `Fibula` | 1427 | 1502 |
| Patella | `Patella` | 1390 | 1465 |
| Talus | `Os tali` | 1448 | 1523 |
| Calcaneus | `Calcaneus` | 1468 | 1543 |
| Femur | `Os femoris` | 1360 | 1435 |
| Hip bone | `Os coxae` | 1307 | 1382 |
| Sacrum | `Os sacrum` | 1071 | 1109 |

Latince taraf eki türetilmedi. `side` ayrı alandır (`left`, `right`, `midline`); uygulama TR/EN taraf adını ve Latince `(L)`/`(R)` gösterimini ekleyebilir. Kaynak `.l`/`.r` nesne adları aliases içinde korunur. `Os femoris` ve `Os tali` dahil Latince değerler bu sabit tablonun tam metnidir; farklı bir eşanlamlıyla sessizce değiştirilmez.

## İlişki kanıtı ve sınırı

Dört `branch_of` kaydı [mevcut distal metadata önerisinden](../../data/model-candidates/distal-leg-nerve-metadata/proposal.json) sadece `datasetId` eklenerek aktarılmıştır. [TTUHSC tablosunun](https://anatomy.ttuhscep.edu/musculoskeletal_system/gluteal_tables.html) Nerves bölümünde sciatic satırının Branches/Notes sütunları ve tibial/fibular common satırlarının Source sütunları kullanılır. Kaynağın önceki incelemedeki erişim tarihi 2 Ekim 2026'dır; bu metadata alt görevinde yeniden web erişimi yapılmadı. Unsided tipik anatomi bilgisi yalnız aynı tarafın kaynak nesnelerine uygulanır; kayıtlardaki `physicalContinuityClaim: false`, `innervationInference: false` ve uzman bekliyor durumu korunur. Ek `part_of`, kök, innervasyon veya çizilmiş dal bağlantısı yoktur.

Kaynak `Z-Anatomy/Startup.blend` SHA-256: `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`. Bu değer önceki kaynak kanıtından devralınmıştır; geometri çalışanının paket kaydı nihai nesne/binary doğrulamasının sahibidir. Metadata lisans/atıf kaydı geometri bileşen lisanslarının yerini almaz.

## Doğrulama ve devretme

2 Ekim 2026, yerel macOS/Python 3 ortamında JSON üzerinde hedefli assertion kontrolü geçti: 21 benzersiz beklenen kavram kimliği; altı sinir/15 kemik rolü; 11 İngilizce/Latince terim çiftinin sabit CSV satır/kimlik karşılığı; bütün adlarda kaynak/TR/EN/LA ve doğru taraf alanları; dört ilişkinin aday kayıtla eşitliği (datasetId dışında); aynı taraf ve çözülen ilişki uçları; üç kaynak kaydının `id/title/url` alanları ve bütün kanıt kaynaklarının çözülmesi; beş input snapshot hash'inin doğruluğu. Kaynak metadata dosyası bu kontrolde SHA-256 `d7f49548fa7905b27eca3edf4246a1ae76ece854b717fbe6f659f0efa43bb7bd` üretti.

Bu alt görevde TypeScript/build, geometri decode/görsel inceleme, uygulama arama→seçim→odak/bağlam→ilişki→geri dönüş veya canlı yayın kontrolü yapılmadı. Entegrasyon sahibi bunları paket kabulü sırasında doğrular ve ana teslim kaydına işler. Geometriyi kabul edilmiş sayan durum eklenmedi; önceki başarısız ana-atlas kaydı ayrı kalır. Uzman anatomik kabulü açık kalır.

Sonraki eylem: entegrasyon sahibi bu metadata ile 21 nesneli export manifestinin kimliklerini birebir karşılaştırıp dataset içinde arama, aynı taraf ilişkisi ve geri dönüş akışını doğrular. Bu metadata çalışanı commit/push/yayın yapmadı. Süre ve bekleme ölçümleri bu alt görev için kaydedilmedi (bilinmiyor).


## Sonraki genişleme ve ayak ilişkileri — 2 Ekim

Yukarıdaki 21 nesneli metadata görevi tarihî kayıttır. Aktif referans şimdi 87 nesne/87 TR-EN/53 exact Latin etiket içerir; 34 digit-specific Latin null ve açıklanmış İngilizce fallback korunur. Mevcut 12 aynı taraflı sinir dalına 48 simetrik, geçişli olmayan kemik eklem ilişkisi ve 12 yönlü bağ–kemik tutunması eklenmiştir: toplam 72. Yeni etiket veya geometri bu ilişki paketinde değiştirilmez. [Kaynak ve locator kanıtı](../../data/model-candidates/foot-reference-relationships-v1/REVIEW.md); bu anatomi bilgisi mesh temasını, eklem yüzeyini veya tutunma koordinatını kanıtlamaz. Ana gövde ilişkileri taşınmaz. Entegrasyon/yayın/gerçek tarayıcı kabulü [owning raporda](progress-report-2026-10-02.md) izlenir; uzman incelemesi hâlâ açıktır.
