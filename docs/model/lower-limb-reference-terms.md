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
