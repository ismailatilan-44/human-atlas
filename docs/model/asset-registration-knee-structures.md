# Diz yapılarını kaydetme ve aktarma — 22 Eylül 2026

İndirilen Z-Anatomy dosyasındaki sağ/sol medial ve lateral menisküs ile ön/arka çapraz bağın sekiz gerçek mesh nesnesi, mevcut Human Atlas diz koordinatlarına ayrı paket olarak aktarıldı. Dönüşüm alt ekstremite referanslarından ölçüldü. Anatomik uzman incelemesi bekliyor; bu paket tüm diz anatomisini veya bağ tutunmalarının doğruluğunu tamamlanmış saymaz.

## Paket ve kimlikler

- `public/models/extensions/knee-structures.json`, `.bin`, `.bin.gz`
- 8 parça, 3.232 vertex, 6.232 üçgen; binary 132.960 bayt, gzip 63.653 bayt.
- Parça sistemi `connective`; her parça tek kavrama bağlı. Konumlar atlas metre koordinatlarında; görüntüleyicide ikinci dönüşüm uygulanmaz.
- Paket kendi chunk dizinini 0’dan başlatır; atlaslarla birleştirilirken chunk indisleri yeniden eşlenmeli.
- Ayrı atıf: `public/models/extensions/KNEE-ATTRIBUTION.md`. Paylaşılan `ATTRIBUTION.md` değiştirilmedi.

| Kaynak nesne | Parça kimliği | Kavram kimliği | Vertex / üçgen |
| --- | --- | --- | ---: |
| `Medial meniscus.l` | `ZA-KNEE-MM-L` | `atlas:left-medial-meniscus` | 144 / 284 |
| `Medial meniscus.r` | `ZA-KNEE-MM-R` | `atlas:right-medial-meniscus` | 144 / 284 |
| `Lateral meniscus.l` | `ZA-KNEE-LM-L` | `atlas:left-lateral-meniscus` | 236 / 468 |
| `Lateral meniscus.r` | `ZA-KNEE-LM-R` | `atlas:right-lateral-meniscus` | 236 / 468 |
| `Anterior cruciate ligament.l` | `ZA-KNEE-ACL-L` | `atlas:left-anterior-cruciate-ligament` | 840 / 1576 |
| `Anterior cruciate ligament.r` | `ZA-KNEE-ACL-R` | `atlas:right-anterior-cruciate-ligament` | 840 / 1576 |
| `Posterior cruciate ligament.l` | `ZA-KNEE-PCL-L` | `atlas:left-posterior-cruciate-ligament` | 396 / 788 |
| `Posterior cruciate ligament.r` | `ZA-KNEE-PCL-R` | `atlas:right-posterior-cruciate-ligament` | 396 / 788 |

## Kaynak geometri ve taraf doğrulaması

Kaynak dosya SHA-256 `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`; hedef atlas SHA-256 `c359f4bcd2cba90b7411d66d5e9fc04dc81294d46cd5c1e8b212c824f2e5bbee`. Exporter her ikisini okumadan önce denetler. Blender 5.2.0 LTS `--disable-autoexec` ile çalıştı; gömülü kaynak scripti çalıştırılmadı, kaynak `.blend` kaydedilmedi.

Sekiz nesnenin türü MESH. Sol/sağ son eki dünya X koordinatıyla doğrulandı; sol X pozitif, sağ X negatif. Sol nesnelerin negatif dünya determinantı için üçgen winding ters çevrildi. “Medial meniscus” nesneleri kaynakta “Lateral meniscus” adlı koleksiyona da üyedir; koleksiyon adı semantik eşleme veya ilişki kanıtı olarak kullanılmadı. Seçim gerçek nesne adı ve dünya konumuna dayanır.

Menisküslerin kaynakta görünür Subdivision modifier’ı var. Paket viewport düzeyi 1’in değerlendirilmiş yüzeyini korur; kaynak render düzeyi 2’ye yükseltilmedi. Medial menisküs tabanda 36 vertex/37 polygon iken değerlendirilmiş yüzeyi 144 vertex/284 üçgen; lateral 60/59’dan 236/468’e gelir. Çapraz bağlarda modifier yok. Vertex konumu, anatomik yol ve topoloji elle düzenlenmedi; decimation veya deformasyon uygulanmadı.

## Dize özel koordinat kaydı

Kaynak eksenleri X sol, Y arka, Z üst; hedef X sol, Y üst, Z ön. Her iki sistem metre cinsinde. Üst kol dönüşümü okunmadı veya doğrulanmış kabul edilmedi.

Önce iki taraflı femur/tibia/fibula merkezleriyle başlayan, etiketli iki yönlü en yakın yüzey similarity ICP tüm kemikleri kullanarak başlangıç dönüşümünü kurar. Ardından diz yapı merkezinin kaynakta/hedefte düşey ±75 mm çevresindeki sabit örnek maskeleriyle dize özgü tek uniform ölçek/dönüş/öteleme ölçülür. Eşleşmeler farklı kemik kimlikleri arasında kurulmaz. Diz paketini uzun kemik şaftlarının bölge dışındaki biçim farklarıyla sürüklememek için bölgesel fit kullanılır. Her iki patella fit dışında bağımsız kontrol olarak tutulur.

Başlangıç 59 iterasyonda, yerel fit 36 iterasyonda yakınsadı. Son katsayı değişimi `8.60309282077476e-08` (eşik `1e-7`). Uniform ölçek **0.9650434495**. Tam 4×4 dönüşüm manifesttedir. Bu dönüşüm yalnız bu diz paketinin kaydıdır; tüm bacağa veya başka bölgeye doğrulanmadan taşınmaz.

Son ölçümler tüm vertexlerden karşı yüzeyin üçgenlerine iki yönde yapılır; vertex ağırlıklıdır, yüzey alanı ağırlıklı değildir. Diz-yerel rapor, son yapı merkezi çevresinde düşey ±100 mm’lik değerlendirme aralığını kullanır; bu, ±75 mm fit maskesinden daha geniştir. Tablodaki milimetreler geometri farkıdır, klinik hata sınırı değildir.

| Kaynak kemik | Rol | Diz RMS mm | Diz p95 mm | Diz maksimum mm | Tüm kemik RMS mm |
| --- | --- | ---: | ---: | ---: | ---: |
| Femur.l | fit | 1.137 | 2.087 | 3.785 | 8.186 |
| Femur.r | fit | 1.150 | 2.111 | 4.122 | 8.219 |
| Tibia.l | fit | 2.754 | 5.848 | 8.046 | 8.197 |
| Tibia.r | fit | 2.760 | 5.969 | 8.007 | 8.280 |
| Fibula.l | fit | 3.505 | 5.544 | 6.409 | 7.781 |
| Fibula.r | fit | 3.475 | 5.526 | 6.677 | 7.598 |
| Patella.l | holdout | 2.782 | 4.776 | 5.421 | 2.782 |
| Patella.r | holdout | 2.899 | 4.851 | 5.413 | 2.899 |

Femur diz çevresinde yaklaşık 1,14 mm RMS, tibia 2,75–2,76 mm, fibula 3,47–3,50 mm fark gösterir. Fit dışında bırakılan patellalar 2,78–2,90 mm RMS fark taşır. Tibia yerel maksimumu yaklaşık 8 mm’dir. Uzun kemiklerin uzak uçlarında tüm-kemik ölçümü daha kötüdür; bu durum manifestte gizlenmez. Anatomik şekil farkını silmek için lokal deformasyon veya her yapıya ayrı kaydırma yapılmadı.

## Paket teknik kontrolü

Float32 XYZ konumlar, normalize Int16 XYZ normaller ve Uint32 indisler little-endian yazılır; her alan 4 bayt hizalıdır. Binary/gzip uzunlukları ve gzip geri açılımı, SHA-256, bütün indislerin aralığı, sonlu koordinatlar, üçgen sayısı, tam Float32 bounds ve sıfır alanlı üçgen bulunmaması kontrol edildi. Normaller açı ağırlığıyla hesaplanır; ince kaynak üçgenlerde yüzey alanı ağırlığının oluşturduğu gölgeleme yön hatasını geometriyi değiştirmeden önler. Paket normalleriyle her üçgenin ortalama interpolasyon yönü yüz normaliyle pozitif skaler çarpım verir; maksimum normal uzunluğu kuantizasyon hatası `0.000024` altında.

Topoloji envanteri: menisküsler ve arka çapraz bağlar tek bağlı bileşen, sıfır sınır kenarı ve sıfır ikiden fazla yüz paylaşan kenar taşır. Her ön çapraz bağ kaynakta altı bağlı bileşen ve 96 sınır kenarı içerir; bu parçalar/uçlar korunur, uydurma kapak veya birleşim oluşturulmaz. Bu kontrol yüzeylerin kendisiyle kesişmediğini veya anatomik olarak doğru olduğunu kanıtlamaz.

Binary SHA-256: `506d10c89b029e4555cbb5565fb6ee909f2e74814729e7cac72e2767e17c595b`. Teknik raporlar `work/open-assets-review/knee-registration-report.json` ve `knee-buffer-check.json` altında.

## Görsel kontrol

Aşağıdaki görüntüler bu tur okunarak incelendi:

- `work/open-assets-review/knee-source-target-front.png`
- `work/open-assets-review/knee-source-target-oblique.png`
- `work/open-assets-review/knee-registered-bilateral.png`

Karşılaştırma görüntülerinin sol paneli kaynak kemikler + kaynak yüzeyler, sağ paneli mevcut atlas kemikleri + binary’den yeniden okunan ihraç yüzeyleridir. Ölçek ve kamera eşleşir. Renkler: medial menisküs turkuaz, lateral menisküs mavi, ön çapraz bağ sarı, arka çapraz bağ pembe. Kemikler görünürlük için saydamdır; uzun kemiklerin görüntüdeki kesik uçları yalnız QA kadrajı içindir, atlas geometrisi kırpılmadı.

İki menisküs tibial plato/femur kondilleri çevresinde; çapraz bağlar eklem arasında ve iki tarafta uygun genel yönde görünüyor. Gros eksen/sağ-sol hatası gözlenmedi. Kaynak ve sadeleştirilmiş hedef kemik şekilleri farklı; tutunma yüzeyi uyumu, menisküs kalınlığı, ince lokal çakışmalar ve bağ anatomisi uzman kabulüyle doğrulanmış sayılmaz. Bu inceleme tarayıcı etkileşim veya anatomik eğitim kabul testinin yerine geçmez.

## Yeniden üretme

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend \
  --python scripts/export-knee-structures.py -- --render
```

`--render` olmadan yalnız paket ve ölçüm raporu oluşturulur. Script yeni QA sahnesi kurar; kaynak sahnenin render/compositor ayarlarını devralmaz. Ana atlas/graph dosyalarına ve paylaşılan atıf dosyasına yazmaz. Kaynak Blender dosyasındaki ilgisiz oesophagus/profile dependency-cycle uyarısı görüldü; seçili diz meshleri okunabildi ve dışa aktarıldı.

Upstream genel CC BY-SA 4.0 bildirimi ve nesneye özel kökenin eksikliği diz atıf dosyasında korunur. Bu pakette iç kulak/böbrek nesnesi yoktur; tüm arşiv için ticari kullanım onayı veya yeniden lisanslama iddiası kurulmaz.
