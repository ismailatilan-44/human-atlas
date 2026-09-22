# 65 hedef için bağlı kavram etiketleri — öneri incelemesi

22 Eylül 2026. Bu klasör **entegrasyon öncesi öneri ve denetim anlık görüntüsüdür**. Bu alt görev etkin etiket dosyalarını değiştirmedi; kök görev daha sonra 45 öneriyi ayrı olarak entegre etti. `inputHashes`, denetim çıktısı ve aşağıdaki fallback sayıları entegrasyon öncesini kaydeder; güncel UI durumunu göstermek amacıyla yeniden üretilmedi. Kapsam yalnız coverage.json içindeki 65 hedefin doğrudan `currentBindings` ve `separateReference` kimlikleri: **83 benzersiz dataset/kavram çifti** (78 erkek, 3 kadın pelvis, 2 koklea). Seçilen hedeflerin bütün alt parçaları veya atlasın tüm kavramları bu çalışmaya dahil değildir.

## Sonuç

- Türkçede **45**, Latincede **47** bağlı kimlik kaynak İngilizcesine düşüyor. İngilizce dilinde de aynı 45 kimlik kaynak adına geri dönüyor; İngilizce metnin görünmesi tek başına hata sayılmadı.
- **45 kimlik için TR/EN önerisi**, bunların **43’ü için Latince öneri** hazır.
- **4 Latin boşluğu bilinçli kalıyor:** iki BP3D `zone` grubu ve iki proje tanımlı humerus tutunma bölgesi.
- Kalan **36 bağlı kimlik** üç dilde mevcut etiket kullanıyor; bu sette yeni öneri yapılmadı. Kadın pelvis ve koklea etiketleri dataset-specific dispatcher’da zaten var.

Denetim gerçek `datasetLabel` fonksiyonunu geçici dosyaya bundle edip çalıştırdı. Sentinel fallback ile etiket bulunup bulunmadığı ölçüldü: `Sternum`, `Aorta`, `Ulna` gibi İngilizce ve Latincede aynı olabilen yazımlar yalnız metin eşitliğine bakılarak yanlış sınıflandırılmadı.

| Bölge | Bağlı kavram | TR fallback | LA fallback |
|---|---:|---:|---:|
| head-neck | 15 | 11 | 11 |
| thorax | 9 | 9 | 9 |
| abdomen-pelvis | 16 | 13 | 13 |
| upper-limb | 25 | 4 | 6 |
| lower-limb | 18 | 8 | 8 |

## Kaynak karşılaştırması ve sınır

45 önerinin tüm FMA kimlikleri ve İngilizce kaynak adları, [resmi BodyParts3D IS-A](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_parts_list_e.txt) veya [PART-OF](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_parts_list_e.txt) ad tablolarında birebir eşleşti. İndirilen tablolar, satır numaraları ve hashler bu klasörde saklandı.

43 Latin önerisi, daha önce kullanılan [sabit Z-Anatomy TA2.csv](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv) içindeki İngilizce–Latince çiftlerden aynen alındı. Bu tur tam FIPAT yayınevi PDF doğrulaması yapıldığı iddia edilmez: FIPAT sayfa/PDF erişimleri DNS/502 hatası verdi. [IFAA TAH cranium kaydı](https://ifaa.unifr.ch/Public/TNAEntryPage/auto/part/EN/TAH305%20P2F%20EN.htm) bağımsız olarak okunabildi; FMA46565 / skull / cranium eşleşmesini destekliyor, sayfa kendi durumunu work in progress olarak belirtiyor.

`ta2TableId` bu sabit upstream tablonun satır kimliğidir. Farklı TA2 baskılarındaki/yayınevi PDF’lerindeki numaralarla sessizce eşitlenmemelidir. Örneğin upstream laryngeal-cartilages satırı 3187 iken yayınevi arama sonucu aynı terimi farklı numarayla gösterir. Terim eşleşmesi ile numara eşleşmesi ayrıdır. Türkçe karşılıklar editoryaldir; resmi Türkçe terminoloji veya anatomist onayı iddiası yok.

## Kapsamı koruyan kararlar

- **FMA34676 / zone of deltoid:** Altı kaynak yüzey, sağ/sol acromial, clavicular ve spinal parçadır. Öneri “Deltoid kasının gösterilen bölümleri”; `Musculus deltoideus` tam kas adı bu grup için Latin etiket olarak aktarılmadı.
- **FMA22429 / zone of quadriceps femoris:** Sekiz kaynak yüzey, sağ/sol rectus femoris ve üç vastus parçasıdır. Öneri “Quadriceps femoris kasının gösterilen bölümleri”; `Musculus quadriceps femoris` bu kaynak zone kimliğinin yerine geçirilmedi.
- **Humerus orta iç tutunma bölgeleri:** Mevcut TR/EN etiketleri korunabilir; bağımsız resmi Latin eşleşmesi olmayan proje bölgesi için yeni Latince uydurulmadı. Kaynak kimlik/konum belirsizliği etiketle giderilmiş sayılmaz.
- Servikal omur, larinks kıkırdağı, kaburga, karpal ve tarsal sınıfları çok parçalı seçim olduğundan çoğul görüntü etiketi önerildi. Kaynak FMA ID/İngilizce ad, yüzey listesi ve çoğul seçimin tam anatomik grup iddiası taşımadığı notu korunuyor. Larinks grubunda kaynakta iki cricoid parçası bulunması ya da epiglottis görülmemesi yeniden adlandırmayla düzeltilmedi.
- Lateral ventrikülde Latince temel terim aynen korunur, taraf L/R işaretiyle verilir. Akciğerlerde kaynak tablonun doğrudan `Pulmo sinister` / `Pulmo dexter` çiftleri vardır; ayrıca ikinci taraf eki eklenmez.

## Yeni öneriler

| ID | Önerilen Türkçe | Önerilen Latince |
|---|---|---|
| FMA46565 | Kafatası | Cranium |
| FMA52748 | Mandibula | Mandibula |
| FMA50801 | Beyin | Encephalon |
| FMA62493 | Hipokampus | Hippocampus |
| FMA9915 | Servikal omurlar | Vertebrae cervicales |
| FMA55108 | Larinks kıkırdakları | Cartilagines laryngis |
| FMA78454 | Üçüncü ventrikül | Ventriculus tertius |
| FMA78469 | Dördüncü ventrikül | Ventriculus quartus |
| FMA75351 | İnterventriküler foramen | Foramen interventriculare |
| FMA78450 | Sol yan ventrikül | Ventriculus lateralis (L) |
| FMA78449 | Sağ yan ventrikül | Ventriculus lateralis (R) |
| FMA7088 | Kalp | Cor |
| FMA7310 | Sol akciğer | Pulmo sinister |
| FMA7309 | Sağ akciğer | Pulmo dexter |
| FMA7394 | Trakea | Trachea |
| FMA13295 | Diyafram | Diaphragma |
| FMA7574 | Kaburgalar | Costae |
| FMA7485 | Sternum | Sternum |
| FMA3734 | Aort | Aorta |
| FMA7131 | Özofagus | Oesophagus |
| FMA7197 | Karaciğer | Hepar |
| FMA7148 | Mide | Gaster |
| FMA7198 | Pankreas | Pancreas |
| FMA7196 | Dalak | Lien |
| FMA7203 | Böbrek | Ren |
| FMA7202 | Safra kesesi | Vesica biliaris |
| FMA7200 | İnce bağırsak | Intestinum tenue |
| FMA7201 | Kalın bağırsak | Intestinum crassum |
| FMA14544 | Rektum | Rectum |
| FMA15900 | Mesane | Vesica urinaria |
| FMA9600 | Prostat | Prostata |
| FMA16585 | Kalça kemiği | Os coxae |
| FMA16202 | Sakrum | Os sacrum |
| FMA13321 | Klavikula | Clavicula |
| FMA23466 | Ulna | Ulna |
| FMA23889 | Karpal kemikler | Ossa carpi |
| FMA34676 | Deltoid kasının gösterilen bölümleri | — bilinçli olarak önerilmedi |
| FMA9611 | Femur | Os femoris |
| FMA24476 | Tibia | Tibia |
| FMA24479 | Fibula | Fibula |
| FMA24485 | Patella | Patella |
| FMA22314 | Gluteus maximus kası | Musculus gluteus maximus |
| FMA22429 | Quadriceps femoris kasının gösterilen bölümleri | — bilinçli olarak önerilmedi |
| FMA70248 | Femoral arter | Arteria femoralis |
| FMA24491 | Tarsal kemikler | Ossa tarsi |

## Dosyalar ve entegrasyon sınırı

- `ui-label-audit.json`: 83 kimlikte mevcut gerçek TR/EN/LA çıktı ve fallback durumu.
- `proposals.json`: 45 öneri; 36 mevcut etiketi koruma listesi; 2 humeral Latin fallback’i koruma kararı. `la: null` olan iki zone önerisi bilerek çeviri içermez.
- `source-evidence.json`: kaynak URL/hashleri ve denetlenen app/data dosyalarının hashleri.
- `ta2-selected-rows.json`: yalnız önerilen Latin adları destekleyen upstream tablo satırları.
- `bp3d-*-parts-list-e.txt`: resmi indirilen FMA/ad tabloları.
- `audit-ui-labels.mjs`, `prepare-proposals.py`: yalnız bu aday klasörüne yazar. İlki çalışma zamanı dispatcher’ını, ikincisi sabit audit snapshotını ve yerel pinned TA2 tablosunu kullanır.

Root entegrasyonda önce snapshot hashlerini değerlendirmeli; UI kodu değişmişse audit tekrar üretilebilir. Öneriler geometri IDsine, source manifestine, kapsam durumuna veya bilgi grafiğine müdahale etmez. `en`, `tr`, `la`, `side`, `aliases` alanları mevcut label biçimiyle uyumludur; bu klasör active data kaynağı değildir.

Bu çalışma 3.432 veya bütün atlas kavramlarının çevrildiğini söylemez. 65 sınırlı hedefin doğrudan bağlı 83 kimliğinde, açık kalan 45 TR ve 47 LA fallback’i incelenmiştir.

## Entegrasyon kaydı

22 Eylül: Kök görev bu adayın incelenen verilerini etkin etiket/bilgi grafiği/görüntüleme katmanına uyguladı. Bu klasörün aday snapshotı korunur; güncel ürün durumu docs/model/2026-09-20-delivery-plan.md içinde izlenir.
