# Kaynaklı anatomi bağlantıları

9 Eylül 2026. Human Atlas temel model olarak korunur. Bu paket mevcut parça kimliklerini, kaynaklı anatomik ilişkileri ve ek asset adaylarını bir araya getirir. Ders/quiz içeriği içermez. Viewer henüz bu veriyi kullanmıyor; harici geometri sahneye eklenmedi.

## İlk kapsam

- Mevcut atlasın 3.432 kavramı; bunlar benzersiz veya tam modellenmiş anatomik yapı sayısı değildir.
- BodyParts3D resmî tablosundan 1.367 PART-OF ilişkisi. Kaynağın parent/child sütunları `child → part_of → parent` yönüne dönüştürülür.
- Biceps ve coracobrachialis odaklı iki taraflı pilot: 12 ek kavram ve 32 ilişki. Toplam 3.444 kavram, 1.399 ilişki.
- Z-Anatomy'deki 16 nesneyle aday eşleştirme. 14'ü mevcut geometri kavramlarına alternatif kaynak; 2'si henüz Human Atlas geometrisine sahip olmayan musculocutaneous sinirlerdir.

## Dosyalar

| Dosya | İşlev |
| --- | --- |
| `sources.json` | URL, tarih, kaynak dosya hash'i, atıf ve kullanım/inceleme kaydı |
| `vendor/bodyparts3d/partof_inclusion_relation_list.txt` | Hash ile sabitlenmiş resmî ilişki tablosu |
| `upper-arm.json` | Araştırılarak seçilmiş pilot kavramlar, ilişkiler ve asset adayları |
| `knowledge.json` | Kaynaklar ve pilot veriden tekrar üretilen birleşik bağlantı verisi; elle düzenlenmez |

BodyParts3D, © The Database Center for Life Science licensed under CC Attribution 4.0 International. [Resmî kaynak ve tablolar](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html), [lisans](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html).

Pilot ilişkiler için [UAMS kas tablosu](https://medicine.uams.edu/neuroscience/education/medical-school-courses/human-structure-module/anatomy-tables/muscle-tables/muscles-of-the-upper-limb/) ve [TTUHSC El Paso diseksiyon kaynağı](https://anatomy.ttuhscep.edu/musculoskeletal_system/axilla_ans.html) okundu. Bağlantılarda ilgili satır/sütun kaydı bulunur. Sayfaların metinleri ve görselleri kopyalanmadı; seçili anatomik olgular ilişki olarak kaydedildi. İki eğitim kaynağının birbiriyle uyumu, iki bağımsız örneklem araştırması olarak sayılmaz.

## İlişki anlamları

| İlişki | Yön |
| --- | --- |
| `part_of` | Alt yapı → içinde yer aldığı yapı |
| `originates_at` | Kas veya başı → başlangıç bölgesi |
| `inserts_at` | Kas → tutunma bölgesi |
| `innervates` | Sinir → uyardığı kas |
| `supplies` | Atardamar → beslediği yapı |
| `passes_through` | Geçen yapı → içinden geçtiği yapı |

Bu türler birbirinin yerine kullanılmaz. Genel komşuluk, eklemleşme, işlev ve varyasyon ilişkileri bu pilotta yoktur. Geometri yakınlığı veya Blender koleksiyon üyeliği tek başına anatomik ilişki kanıtı sayılmaz. Yapı çiftinin ilişkisiz olduğunu da grafikte kenar bulunmamasından çıkarmamak gerekir.

## İnceleme ve geometri durumu

`source_imported` doğrudan kaynak tablodan alınan ilişkiyi, `source_supported` araştırma kaynağıyla desteklenen pilot ilişkiyi belirtir. `expertReview: pending` kayıtları anatomist onayından geçmiş sayılmaz. Genel anatomi açıklamalarının sağ ve sol modele uygulanması, örneğe özel doğrulama değildir; bu sınırlama her pilot ilişkiye yazıldı.

Tüm mevcut kavramlar başlangıçta `representationStatus: unknown` taşır. Mevcut parçalarla kurulan bileşik biceps seçimi `composite_unreviewed`, sinir adayları `external_candidate`, kemik üzerindeki etiket bölgeleri `landmark_unanchored` olarak ayrılır. Landmark için uydurma koordinat veya tüm kemiği o landmarkın geometrisi gibi gösteren bir eşleme üretilmedi. Biceps aponevrozu, diğer kaslar, sinir kökleri ve varyasyonlar bu pilotla tamamlanmış sayılmaz.

Z-Anatomy adayları kaynak dosyadaki ad/taraf ve nesne türü üzerinden eşleştirildi. Kaynak Blender SHA-256, önceki denetimdeki dosyayı tanımlar. Bu eşleştirme koordinat kaydı, yüzey eşitliği veya kullanım koşullarının nesne düzeyinde çözülmüş olduğu anlamına gelmez. `candidate_not_registered` kayıtları aktarım, eksen/birim, pozisyon, yakın plan doğruluk ve kaynak/lisans incelemesi bekler. Yeni varlıklar için FMA kimliği uydurulmadı; proje içi `atlas:` kimlikleri kullanıldı.

## Çalıştırma

Proje kökünden:

```sh
node scripts/build-anatomy-knowledge.mjs
node scripts/build-anatomy-knowledge.mjs --check
node --test scripts/anatomy-knowledge.test.mjs
node scripts/build-anatomy-knowledge.mjs --entity atlas:left-biceps-brachii
```

Oluşturucu çevrimdışı çalışır. Kaynak dosyası hash'i değişirse sessizce devam etmez. İnceleme sonrası kaynak kaydı bilinçli güncellenmelidir. Eksik uç, bilinmeyen kanıt kaynağı, yinelenen ilişki, ters taraf bağlantısı ve PART-OF döngüsü doğrulamada reddedilir. Kanıtı özellikle belirtilmiş orta hattı aşan ilişkiler için `crossesMidline` alanı desteklenir; pilotta kullanılmaz.

## Genişletme sırası

1. Pilot sinir geometrilerini mevcut kas/kemiklerle aynı sahnede konumlandırıp doğrulamak; landmark etiket noktalarını belirlemek.
2. Omuz–kol kapsamını brakiyal pleksus, diğer ana sinirler, rotator manşet ve ilişkileriyle genişletmek.
3. Aynı kayıt yapısını dirsek/el, kalça/diz/ayak, baş-boyun, gövde ve pelvis bölgelerinde uygulamak; her bölgeye kapsam listesi eklemek.
4. Gereken her yapı için sırasıyla mevcut atlası, doğrudan indirilebilir kaynak/veri tablolarını, API'leri ve gerekli durumda sayfa kazımasını kullanmak. Otomatik aday eşleşmelerini incelenmiş ilişki veya hazır geometri diye işaretlememek.
5. Viewer'da seçili yapıdan bağlantılı yapılara gezinme ve etiket görüntüleme eklemek. Bu arayüz işi henüz uygulanmadı.
