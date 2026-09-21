# Siyatik sinir aktarımı ve kalça–uyluk kaydı — 22 Eylül 2026

Z-Anatomy kaynak dosyasındaki `Sciatic nerve.l/.r` eğrileri, mevcut Human Atlas kalça–uyluk referansları üzerinden bağımsız olarak kaydedilip ayrı paket halinde aktarıldı. Kaynak nesnelerin bütün üç eğrisi korunur. Bu aktarım tüm lumbosakral pleksus, sinir kökleri, varyasyonlar veya alt ekstremite sinir ağı tamamlandı anlamına gelmez. Anatomik uzman incelemesi bekliyor.

## Paket

- `public/models/extensions/sciatic-nerves.json`, `.bin`, `.bin.gz`
- 2 parça, 4.968 vertex, 9.792 üçgen; binary 206.928 bayt, gzip 114.080 bayt.
- Sol: `ZA-SCI-L` → `atlas:left-sciatic-nerve`; sağ: `ZA-SCI-R` → `atlas:right-sciatic-nerve`.
- Sistem `nervous`; bir kavram bir parçaya bağlı. Konumlar Human Atlas metre koordinatlarında; görüntüleyicide ikinci dönüşüm gerekmez. Birleşik atlas oluşturulurken extension’ın 0’dan başlayan chunk indisleri yeniden eşlenir.
- Ayrı atıf: `public/models/extensions/SCIATIC-ATTRIBUTION.md`. Paylaşılan atıf, app, graph, registry ve coverage dosyaları bu aktarımda değiştirilmedi.

## Gerçek kaynak kapsamı ve mevcut atlas bağlamı

Ana atlas parça/kavram adlarında `sciatic` eşleşmesi yok. Ana atlasın `nervous` sınıfındaki parçaları arasında alt Y sınırı 1,05 metrenin altında olan parça bulunmadı. Bu teknik ad/sınıf/kutu sorgusu, başka yüzeylerin içindeki veya farklı adlandırılmış anatomik ayrıntıların yokluğunu kanıtlamaz. Geometri bağlamı için var olan hip bone, sacrum, femur ve yakın kaslar kullanıldı.

Kaynak her tarafta 3 BEZIER spline (12 + 4 + 4 = 20 kontrol noktası) içerir. Ana spline pelvis çevresinden posterior uyluğa, iki kısa spline proksimal bölümde uzanır. Kaynak kontrol noktalarına bakılarak L4–S3 kök etiketleri veya özgün dalların kimlikleri uydurulmadı.

Kaynak bevel_depth `0.0005000000237487257`, bevel_resolution `4`, resolution_u `12`, use_fill_caps `false`. Kontrol noktası radius değerleri 1–12 arasında değişir; sabit yarıçaplı yeni tüp çizilmedi. Her nesne 2.484 vertex/4.896 üçgene değerlendirilir. Sol eğrinin negatif dünya determinantı için winding düzeltildi; taraf hem `.l/.r` adı hem dünya X işaretiyle kontrol edildi.

| Parça | Atlas Y kapsamı (m) | Ana eğri proksimal uç XYZ (m) | Ana eğri distal uç XYZ (m) |
| --- | --- | --- | --- |
| ZA-SCI-L | 0.559898–1.005871 | 0.030193, 1.005647, -0.051454 | 0.078014, 0.560172, -0.036092 |
| ZA-SCI-R | 0.559835–1.005846 | -0.030387, 1.005623, -0.051433 | -0.077836, 0.560109, -0.036037 |

Distal uç yaklaşık Y=0,560 m’de, mevcut femurun distal Y≈0,446 m seviyesinin üzerinde biter; paket ayak/alt bacağı içermez. Kaynak `Tibial nerve.l/.r` ve `Common fibular nerve.l/.r` nesnelerinin proksimal uçları ana siyatik eğrinin distal ucuyla yaklaşık 0,00012–0,00018 mm içinde çakışır; bu kaynaktaki devam bağlantısını gösterir, anatomik doğruluk hassasiyeti değildir. Bu dört ayrı devam nesnesi ve distal dalları bu pakette **aktarılmadı**. Bütün kontrol noktaları, uç noktaları, radius dizileri ve ihraç edilmeyen nesnelerin uç mesafeleri manifestin `sourceExtent` alanında korunur.

## Bağımsız tam seyir kaydı

Kaynak SHA-256 `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`; hedef ana atlas SHA-256 `c359f4bcd2cba90b7411d66d5e9fc04dc81294d46cd5c1e8b212c824f2e5bbee`. Exporter ikisini de doğrular. Blender 5.2.0 LTS `--disable-autoexec` ile çalıştı, `.blend` kaydedilmedi.

Kaynak X sol/Y arka/Z üst eksenlerinden hedef X sol/Y üst/Z ön eksenlerine dönüşüm yalnız başlangıçtır. İki taraflı hip bone ve femur ile sacrumun eşlenmiş merkezleri ardından bütün kemik yüzeylerini kullanan etiketli iki yönlü en yakın yüzey similarity ICP çalışır. Eşleşmeler farklı kemik kimlikleri arasında kurulmaz. Diz veya üst kol dönüşümü okunmadı. Tek uniform ölçek/dönüş/öteleme iki siyatik eğriye birlikte uygulanır; lokal eğme, parça bazında kaydırma veya sinir yolunu çizerek düzeltme yapılmaz.

Bağımsız kontrol için iki taraflı piriformis, gluteus maximus, biceps femoris uzun başı ve semitendinosus fit dışında bırakıldı. Böylece proksimal kalça çevresi ve uyluk boyunca sekiz kas yüzeyi ölçülür. Tam seyirden kastedilen kaynak nesnenin pelvis–uyluk boyunca mevcut kapsamıdır; aktarılmayan tibial/fibular sinirlerin ayaktaki seyri değildir.

Uniform ölçek **1.0179763138**; 39 iterasyon, son katsayı değişimi `5.6719168841517804e-08` (eşik `1e-7`). Tam 4×4 matris manifestte. Son mesafeler tüm vertexlerden karşı yüzeyin üçgenlerine iki yönde ölçülür; vertex ağırlıklıdır, alan ağırlıklı değildir. “Sinir kapsamı” ölçümü, ihraç edilen geometri Y aralığının ±20 mm çevresindeki alt kümedir; fit sırasında maske olarak kullanılmadı.

| Kaynak referans | Rol | Tam RMS mm | p95 mm | Maksimum mm | Sinir kapsamı RMS mm |
| --- | --- | ---: | ---: | ---: | ---: |
| Hip bone.l | fit | 3.828 | 7.079 | 8.862 | 3.801 |
| Hip bone.r | fit | 3.832 | 6.849 | 8.985 | 3.817 |
| Sacrum | fit | 4.490 | 6.379 | 29.072 | 4.490 |
| Femur.l | fit | 2.705 | 5.507 | 7.926 | 2.325 |
| Femur.r | fit | 2.673 | 5.474 | 7.849 | 2.340 |
| Piriformis muscle.l | holdout | 1.953 | 4.123 | 6.029 | 1.953 |
| Piriformis muscle.r | holdout | 1.942 | 4.124 | 6.079 | 1.942 |
| Gluteus maximus muscle.l | holdout | 5.055 | 9.713 | 14.088 | 5.055 |
| Gluteus maximus muscle.r | holdout | 5.071 | 9.778 | 14.074 | 5.071 |
| Long head of biceps femoris.l | holdout | 4.699 | 8.536 | 13.255 | 4.215 |
| Long head of biceps femoris.r | holdout | 4.660 | 8.328 | 13.031 | 4.226 |
| Semitendinosus muscle.l | holdout | 4.955 | 9.807 | 11.719 | 3.905 |
| Semitendinosus muscle.r | holdout | 4.925 | 9.753 | 11.480 | 3.908 |

Piriformis bağımsız kontrolü 1,94–1,95 mm RMS; gluteus maximus 5,05–5,07 mm, biceps uzun başı 4,66–4,70 mm, semitendinosus 4,92–4,96 mm fark gösterir. Sacrumda maksimum yaklaşık 29,1 mm ayrışma vardır; kaynak/atlas yüzeyleri eşit kabul edilmez ve bu değer gizlenmez. Kaynak düzenlemeleri, model poz/şekil farkları ve hedef sadeleştirmesi bu ölçüme dahildir. Bunlar klinik hata sınırı veya sinirin anatomik yolunun onayı değildir.

## Teknik kontrol ve görsel inceleme

Paket Float32 konum, normalize Int16 normal, Uint32 indis kullanır; alanlar 4 bayt hizalıdır. Binary/gzip uzunlukları, gzip geri açılımı, SHA-256, sonlu koordinatlar, indis aralıkları, Float32 bounds, toplam üçgen sayısı ve sıfır alanlı üçgen bulunmaması kontrol edildi. Açı ağırlıklı normallerin üçgen yüzüyle interpolasyon yönü pozitif; maksimum kuantizasyon normal uzunluk hatası `0.000024` altında.

Her sinir, kaynaktaki üç ayrı tüp bileşenini ve 72 açık sınır kenarını korur; ikiden çok yüz paylaşan kenar yoktur. Uçlar kapatılmadı ve kaynak splineleri uydurma bağlantı meshleriyle birleştirilmedi. Bu teknik topoloji kontrolü kendisiyle kesişme veya anatomik tamlık kanıtı değildir. Render açık/kapalı yüzey tanımını değiştirmez.

Binary SHA-256: `d81e342e2254e7ec888a36992c0a1b7cedf37614c25b4b6f5219fed25fac3e0e`. Paket ilk export ve görsel QA export’unda aynı hash ile üretildi.

Bu tur görüntülenip incelenen QA görüntüleri:

- `work/open-assets-review/sciatic-source-target-posterior.png`
- `work/open-assets-review/sciatic-source-target-oblique.png`
- `work/open-assets-review/sciatic-registered-bilateral.png`

Kaynak–hedef karşılaştırmasının sol paneli kayıtlı kaynak kemik/kaslar ve özgün eğri yüzeyleri, sağ paneli mevcut atlas referansları ve binary’den yeniden okunan sinir yüzeyleridir. Aynı kamera/ölçek kullanılır. Her iki tarafta pelvis–uyluk genel yerleşimi korunuyor; gros eksen, ölçek veya taraf hatası gözlenmedi. Kaynak sinirin alt uylukta bitmesi görünür. Yakın kas sınırlarında şekil farkları sürer; ince komşuluk, kesişme ve kök/dal anatomisi uzman incelemesiyle doğrulanmış sayılmaz. Tarayıcı seçim/odaklama kabulü bu exporter kapsamı dışındadır.

## Yeniden üretme

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend \
  --python scripts/export-sciatic-nerves.py -- --render
```

`--render` olmadan paket ve ölçüm raporu üretilir. Yeni QA sahnesi kaynak compositor ayarlarından bağımsızdır. `work/open-assets-review/sciatic-registration-report.json`, `sciatic-source-inspection.json` ve `sciatic-buffer-check.json` yerel kanıtları tutar. Kaynak dosyada görülen ilgisiz oesophagus/profile dependency-cycle uyarısı bu eğrilerin okunmasını engellemedi.

Upstream genel CC BY-SA 4.0 bildirimi ve nesneye özgü köken bilgisinin eksikliği ayrı siyatik atıf dosyasında korunur. İç kulak/böbrek nesnesi aktarılmadı; bütün arşiv için ticari kullanım veya yeniden lisanslama sonucu çıkarılmadı.
