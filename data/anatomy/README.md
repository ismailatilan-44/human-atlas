# Kaynaklı anatomi bağlantıları

Bu dizin aktif viewer'ın kaynaklı anatomi verilerini içerir. Viewer `explorer.json` üzerinden ilişkileri kullanır; kayıtlı harici geometri ana sahnede, bağımsız referanslar kendi datasetlerinde çalışır. Güncel kapsam için [README](../../README.md), üretim ve kontrol sırası için [ajan iş akışı](../../docs/model/agent-workflow.md) okunmalıdır. Ders/quiz girdileri bu dizinde değil, ayrı `data/study/` kayıtlarında tutulur.

## Güncel veri sahipliği — 21 Ekim 2026

Yerel `fb39d24` tabanında ana graph 3.516 kavram ve 1.539 ilişki, ana model 2.292 parça, bölgesel etiket modülü 403 kayıt içerir. Bağımsız alt/üst ekstremite graph'ları sırasıyla 112 ve 26 ilişki taşır. Bunlar anatomik tamlık sayıları değildir; güncel sayım ve dataset sınırları [üretilen envanterde](../../docs/model/model-inventory.md), yerel/yayın kabulü [güncel teslim kaydında](../../docs/model/progress-report-2026-10-21.md) bulunur.

| Girdi / çıktı | Güncel sahibi ve kullanımı |
| --- | --- |
| `sources.json`, bölgesel JSON modülleri | Ana graph'ın kaynak, kavram, ilişki ve kanıt girdileri. Etkin modül listesi `scripts/build-anatomy-knowledge.mjs` içindeki `buildKnowledge()` fonksiyonunda; yalnız ilk `upper-arm.json` pilotu değildir. |
| `labels.json`, `coverage.json` | Yazılmış bölgesel etiketler ve 65 tarihî pilot hedef. Coverage satırları bütün vücudun tamlık paydası değildir. |
| `knowledge.json` | Ana manifest, kayıtlı ekler ve bölgesel modüllerden üretilen graph. Elle düzenlenmez. |
| `explorer.json` | Viewer'ın kullandığı küçültülmüş ana graph projeksiyonu; `scripts/build-explorer-catalog.mjs` üretir. Elle düzenlenmez. |
| `lower-limb-reference.json`, `upper-limb-reference.json` | Kendi kaynak/koordinat çerçevelerindeki bağımsız referansların etiket ve ilişki modülleri; ana graph'a birleştirilmez. |
| `model-inventory.json` | Beş datasetin gerçek kaynak/seçim kimlikleri, sürümlü hedefler ve açık kapsam matrisi; `scripts/build-model-inventory.mjs` üretir. |
| `../study/*.json`, `app/study-packs.ts` | Ayrı yazılmış, sonlu tanıma modülleri. Öğrenme etkisi veya anatomik uzman kabulü kanıtı değildir. |

Girdi değiştiğinde yalnız ilgili çıktıları üretin; sıra knowledge → explorer → inventory'dir. Paketleme ve tarihî aktivasyon scriptlerinin kapsamı için [iş akışındaki kontrol yönlendirmesini](../../docs/model/agent-workflow.md#frozen-activation-versus-reusable-validation) izleyin. Güncel yalnız-okuma doğrulama:

```sh
node scripts/build-anatomy-knowledge.mjs --check
node scripts/build-explorer-catalog.mjs --check
node scripts/build-model-inventory.mjs --check
node --test scripts/anatomy-knowledge.test.mjs
```

Ana graph `attaches_to` ve `branch_of` gibi sonraki ilişki türlerini de destekler. Bağımsız alt ekstremite graph'ında ayrıca `articulates_with` vardır; aşağıdaki ilk-pilot tablosu bütün ürünün güncel predicate listesi değildir. `registered_geometry`, kaynak yüzey işareti ve bağımsız referans kapsamları sonraki paketlerde eklenmiştir. Kaynakla desteklenmiş kayıt anatomist onayı değildir; geometri yakınlığı tek başına ilişki kanıtı sayılmaz.

## Tarihî pilot — 9 Eylül 2026

Aşağıdaki pilot sayıları, temsil durumları ve genişletme sırası **9 Eylül 2026 tarihli ilk alımın tarihî kaydıdır**; bugünkü ürün durumunu veya bekleyen iş listesini belirtmez. Güncel kaynaklar `sources.json`, bölgesel modüller ve aktif manifestlerden üretilir; `knowledge.json` ve `explorer.json` elle düzenlenmez.

### İlk kapsam

- Mevcut atlasın 3.432 kavramı; bunlar benzersiz veya tam modellenmiş anatomik yapı sayısı değildir.
- BodyParts3D resmî tablosundan 1.367 PART-OF ilişkisi. Kaynağın parent/child sütunları `child → part_of → parent` yönüne dönüştürülür.
- Biceps ve coracobrachialis odaklı iki taraflı pilot: 12 ek kavram ve 32 ilişki. Toplam 3.444 kavram, 1.399 ilişki.
- Z-Anatomy'deki 16 nesneyle aday eşleştirme. 14'ü mevcut geometri kavramlarına alternatif kaynak; 2'si henüz Human Atlas geometrisine sahip olmayan musculocutaneous sinirlerdir.

### Dosyalar

| Dosya | İşlev |
| --- | --- |
| `sources.json` | URL, tarih, kaynak dosya hash'i, atıf ve kullanım/inceleme kaydı |
| `vendor/bodyparts3d/partof_inclusion_relation_list.txt` | Hash ile sabitlenmiş resmî ilişki tablosu |
| `upper-arm.json` | Araştırılarak seçilmiş pilot kavramlar, ilişkiler ve asset adayları |
| `knowledge.json` | Kaynaklar ve pilot veriden tekrar üretilen birleşik bağlantı verisi; elle düzenlenmez |

BodyParts3D, © The Database Center for Life Science licensed under CC Attribution 4.0 International. [Resmî kaynak ve tablolar](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html), [lisans](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html).

Pilot ilişkiler için [UAMS kas tablosu](https://medicine.uams.edu/neuroscience/education/medical-school-courses/human-structure-module/anatomy-tables/muscle-tables/muscles-of-the-upper-limb/) ve [TTUHSC El Paso diseksiyon kaynağı](https://anatomy.ttuhscep.edu/musculoskeletal_system/axilla_ans.html) okundu. Bağlantılarda ilgili satır/sütun kaydı bulunur. Sayfaların metinleri ve görselleri kopyalanmadı; seçili anatomik olgular ilişki olarak kaydedildi. İki eğitim kaynağının birbiriyle uyumu, iki bağımsız örneklem araştırması olarak sayılmaz.

### İlişki anlamları

| İlişki | Yön |
| --- | --- |
| `part_of` | Alt yapı → içinde yer aldığı yapı |
| `originates_at` | Kas veya başı → başlangıç bölgesi |
| `inserts_at` | Kas → tutunma bölgesi |
| `innervates` | Sinir → uyardığı kas |
| `supplies` | Atardamar → beslediği yapı |
| `passes_through` | Geçen yapı → içinden geçtiği yapı |

Bu türler birbirinin yerine kullanılmaz. Genel komşuluk, eklemleşme, işlev ve varyasyon ilişkileri bu pilotta yoktur. Geometri yakınlığı veya Blender koleksiyon üyeliği tek başına anatomik ilişki kanıtı sayılmaz. Yapı çiftinin ilişkisiz olduğunu da grafikte kenar bulunmamasından çıkarmamak gerekir.

### İnceleme ve geometri durumu

`source_imported` doğrudan kaynak tablodan alınan ilişkiyi, `source_supported` araştırma kaynağıyla desteklenen pilot ilişkiyi belirtir. `expertReview: pending` kayıtları anatomist onayından geçmiş sayılmaz. Genel anatomi açıklamalarının sağ ve sol modele uygulanması, örneğe özel doğrulama değildir; bu sınırlama her pilot ilişkiye yazıldı.

Tüm mevcut kavramlar başlangıçta `representationStatus: unknown` taşır. Mevcut parçalarla kurulan bileşik biceps seçimi `composite_unreviewed`, sinir adayları `external_candidate`, kemik üzerindeki etiket bölgeleri `landmark_unanchored` olarak ayrılır. Landmark için uydurma koordinat veya tüm kemiği o landmarkın geometrisi gibi gösteren bir eşleme üretilmedi. Biceps aponevrozu, diğer kaslar, sinir kökleri ve varyasyonlar bu pilotla tamamlanmış sayılmaz.

Z-Anatomy adayları kaynak dosyadaki ad/taraf ve nesne türü üzerinden eşleştirildi. Kaynak Blender SHA-256, önceki denetimdeki dosyayı tanımlar. Bu eşleştirme koordinat kaydı, yüzey eşitliği veya kullanım koşullarının nesne düzeyinde çözülmüş olduğu anlamına gelmez. `candidate_not_registered` kayıtları aktarım, eksen/birim, pozisyon, yakın plan doğruluk ve kaynak/lisans incelemesi bekler. Yeni varlıklar için FMA kimliği uydurulmadı; proje içi `atlas:` kimlikleri kullanıldı.

### Çalıştırma

Proje kökünden:

```sh
node scripts/build-anatomy-knowledge.mjs
node scripts/build-anatomy-knowledge.mjs --check
node --test scripts/anatomy-knowledge.test.mjs
node scripts/build-anatomy-knowledge.mjs --entity atlas:left-biceps-brachii
```

Oluşturucu çevrimdışı çalışır. Kaynak dosyası hash'i değişirse sessizce devam etmez. İnceleme sonrası kaynak kaydı bilinçli güncellenmelidir. Eksik uç, bilinmeyen kanıt kaynağı, yinelenen ilişki, ters taraf bağlantısı ve PART-OF döngüsü doğrulamada reddedilir. Kanıtı özellikle belirtilmiş orta hattı aşan ilişkiler için `crossesMidline` alanı desteklenir; pilotta kullanılmaz.

### Genişletme sırası

1. Pilot sinir geometrilerini mevcut kas/kemiklerle aynı sahnede konumlandırıp doğrulamak; landmark etiket noktalarını belirlemek.
2. Omuz–kol kapsamını brakiyal pleksus, diğer ana sinirler, rotator manşet ve ilişkileriyle genişletmek.
3. Aynı kayıt yapısını dirsek/el, kalça/diz/ayak, baş-boyun, gövde ve pelvis bölgelerinde uygulamak; her bölgeye kapsam listesi eklemek.
4. Gereken her yapı için sırasıyla mevcut atlası, doğrudan indirilebilir kaynak/veri tablolarını, API'leri ve gerekli durumda sayfa kazımasını kullanmak. Otomatik aday eşleşmelerini incelenmiş ilişki veya hazır geometri diye işaretlememek.
5. Viewer'da seçili yapıdan bağlantılı yapılara gezinme ve etiket görüntüleme eklemek. Bu adım pilot tarihinde bekliyordu; güncel üründe uygulanmıştır.
