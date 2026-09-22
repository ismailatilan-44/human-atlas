# Model etiketleri ve görüntüleme düzeltmeleri

22 Eylül 2026. `app/atlas-metadata.ts` kaynak manifesti değiştirmeden uygulanır. Görüntüleyici atlası yüklerken `prepareAtlas` çağırmalı; kavram kapsamı için `getRepresentationNote` sonucunu göstermelidir.

## İncelenen düzeltmeler

- `FJ1730`, `FJ1731`, `FJ1752`, `FJ1767`, `FJ1814` parçalarının sistemi `nervous` olarak düzeltilir. Kimlik, geometri, paket ofsetleri ve kavram bağlantıları korunur. Kanıt: [8 Eylül denetimi, M-01](2026-09-08-audit.md) ve orada bağlantılanan BodyParts3D PART-OF tablosu.
- İlk denetimde `FMA7647` yalnız merkez kanalla temsil ediliyordu (M-02). Sonraki BodyParts3D 4.3 aktarımı uzunlamasına sinir dokusunu ekledi. Güncel not kök, zar ve segment ayrıntılarının bulunmadığını belirtir; diğer kavramlarda not olmaması tam temsil anlamına gelmez.

## Etiket kaynağı ve sınırları

[Z-Anatomy upstream TA2.csv](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv) İngilizce–Latince eşlemeleri okunup doğrulandı. Dosya SHA-256: `0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974`. Sabit commit dosyası ayrıca indirilerek hash eşitliği kontrol edildi. Bu Z-Anatomy dağıtımındaki TA2 tablosudur; FIPAT'ın Türkçe bir yayını değildir.

| TA2 kimliği | İngilizce temel terim | Latince temel terim |
| --- | --- | --- |
| 2464 | Biceps brachii muscle | Musculus biceps brachii |
| 2465 | Long head of biceps brachii | Caput longum musculi bicipitis brachii |
| 2466 | Short head of biceps brachii | Caput breve musculi bicipitis brachii |
| 2468 | Coracobrachialis muscle | Musculus coracobrachialis |
| 6421 | Musculocutaneous nerve | Nervus musculocutaneus |
| 1143 | Scapula | Scapula |
| 1180 | Humerus | Humerus |
| 1210 | Radius | Radius |
| 1159 | Coracoid process | Processus coracoideus |
| 1163 | Supraglenoid tubercle | Tuberculum supraglenoideum |
| 1216 | Radial tuberosity | Tuberositas radii |
| 4632 | Brachial artery | Arteria brachialis |

Türkçe metinler kaynak terimlerin editoryal çevirisi/transliterasyonudur; resmi Türkçe terminoloji onayı veya anatomist incelemesi iddiası taşımaz. Sağ/sol mevcut manifest ve pilot kimliklerinden alınır. Latince temel terim aynen korunur; taraf için `L` (sol) ve `R` (sağ) eklenir. Yeni Latince çekim üretilmez.

Humerus orta iç tutunma bölgesi proje tarafından tanımlanmış bir bölgedir. Bağımsız bir TA2 terimiymiş gibi Latince ad uydurulmadı; Latince seçiminde kaynak İngilizce adı korunur. Bu davranış tüm pilot dışı kimlikler için de geçerlidir. Arama İngilizce kaynak adını, pilot Türkçe/Latince adları ve sınırlı yaygın adları birlikte kapsar; Türkçe aksanlar olmadan da arama terimleri üretilir.

Bu paket yalnız iki taraflı biceps/korakobrakiyal kas pilotunun etiketlerini kapsar; bütün atlasın çevrildiği veya omuz–kol anatomisinin tamamlandığı anlamına gelmez. Yeni innervasyon, tutunma ilişkisi, geometri veya landmark koordinatı eklenmedi. Mevcut manifest, bilgi grafiği ve kaynak hash kayıtları değiştirilmedi.

## Bölgesel genişletme

Aynı sabit TA2.csv hash'i tekrar doğrulanarak bilateral median sinir, medial/lateral menisküs, ön/arka çapraz bağ adları eklendi (TA2 6459, 1888, 1885, 1890, 1891). Türkçe adlar editoryal; kaynak Latince terim aynen saklanır. Bu isim ekleri yeni anatomik ilişki veya uzman doğruluk onayı değildir.

Önkol bağlantıları için pronator teres, flexor carpi radialis, palmaris longus, flexor digitorum superficialis; ayrıca thyroid adları eklendi (TA2 2478, 2481, 2482, 2486, 3863). TA2.csv 2486 Latince hücresinde yinelenen superficialis bulunduğundan o hücre aktarılmadı; LA modunda İngilizce kaynak adına geri düşer. Şüpheli kaynak terimi sessizce düzeltilmedi veya resmi Latin karşılık olarak sunulmadı.

Siyatik sinir sağ/sol kimlikleri, aynı sabit TA2.csv kaynağındaki 6569 / Sciatic nerve / Nervus ischiadicus satırına bağlandı. Türkçe Siyatik sinir etiketi editoryal çeviridir. Tiroid etiketi aday içindir; düşük detaylı kaynak aktif sahneye kabul edilmedi.

Siyatik ilişkilerinin hedefleri TA2 2639/2640 (biceps femoris uzun/kısa baş), 2641 (semitendinosus), 2642 (semimembranosus) satırlarıyla iki taraflı etiketlendi.

BodyParts3D 4.3 FMA9603 tiroid etiketi aynı TA2 3863 kaydına bağlandı. Sağ/sol loblar TA2 3864, isthmus TA2 3866; Türkçe etiketler editoryal, Latince kaynak terimi aynen korundu. Diz ilişkilerinin femur/tibia uçlarına TA2 1360/1397 yan işaretli etiketleri eklendi.

FMA7647 omurilik / Medulla spinalis TA2 6049; FMA78497 merkez kanal / Canalis centralis TA2 6127. FMA242005 sinir dokusu için Türkçe editoryal etiket eklendi; doğrulanmış ayrı Latince satır olmadığından Latin alanı boş ve kaynak İngilizcesi yedek.

## Doğrudan bölgesel hedeflerin etiketleri — 22 Eylül

65 hedefin doğrudan bağlandığı 83 dataset/kavram çifti denetlendi. Başlangıçta 45 kimlikte TR etiketi ve 47 kimlikte LA etiketi yoktu. Kaynak ID/adları resmi BP3D tablolarıyla, 43 Latin çifti sabit Z-Anatomy TA2 dağıtımıyla karşılaştırıldı. 45 yeni TR/EN etiketi ve 43 kaynak Latin karşılığı `labels.json` dosyasına aktarıldı. Kaynak listesi, öncesi snapshot ve kararlar [aday incelemesinde](../../data/model-candidates/coverage-labels/REVIEW.md); etiket kayıtları aynı adayın kavram bazındaki kanıtına bağlanır. Türkçe çeviriler editoryaldir.

Deltoid ve quadriceps `zone` kimlikleri bütün kas diye yeniden adlandırılmadı; iki grupta LA boş kaldı. İki proje tanımlı humeral tutunma bölgesinin LA boşluğu korunur. Günlük Türkçe aramada alt çene, yemek borusu, soluk borusu, köprücük kemiği, uyluk kemiği, kaval kemiği ve diz kapağı eşanlamları kullanılır. Bu iş alt parçaların, tüm ilişki uçlarının veya bütün atlasın çevrildiği anlamına gelmez.

Yerel arayüzde `karaciger` sorgusu Karaciğer seçimini buldu; aynı 60 parça korunarak LA modunda Hepar gösterildi. Saydam çevre görünümü ve kaynaklı bağlantı paneli görüldü.

21 yeni tekil kafatası kemiği etiketi ve `atlas:skull-bones` / Ossa cranii grup adı eklendi. Mandibulanın mevcut etiketi korundu; 22 kemikte kaynak FJ→FMA tekil eşleşme kanıtı [kafatası incelemesinde](../../data/model-candidates/skull-labels/REVIEW.md). 16 rotator manşet kas/sinir etiketi ayrıca eklendi; kaynak terimler [ilişki incelemesinde](../../data/model-candidates/rotator-cuff-relations/REVIEW.md). Aktif labels.json toplam155 kayıt içerir; bu sayı benzersiz anatomi veya tam çeviri sayısı değildir.

Entegrasyon sonrası çalışma zamanı denetimi:65 hedef,83 doğrudan dataset/kavram bağı; TR 0,EN 0,LA 4 fallback. [Sonuç](../../data/model-candidates/coverage-labels/ui-label-audit-after.json). Denetim betiği orijinal pre-integration snapshotını artık ezmez.

Dört ek kemik sistemi düzeltmesi FJ3263/FJ3369(inferior nasal concha), FJ3265/FJ3371(lacrimal bone) için kaynak IS-A bone-organ yollarına dayanır. FJ1504/FJ1504M subscapularis kasları skeletal→muscular olarak düzeltilir: resmi IS-A tablosunda FMA32520 intrinsic muscle of shoulder→FMA13413 subscapularis→FMA13414/FMA13415; satır 1141,467,468. Yalnız görüntüleme metadatası değişir; ham atlas, kimlikler ve vertexler korunur.
