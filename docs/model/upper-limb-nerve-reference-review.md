# Bağımsız üst ekstremite sinir referansı — ürün incelemesi

## Ürün ve kaynak kapsamı

Kaynak Z-Anatomy'nin sabitlenmiş `Startup.blend` dosyasıdır; SHA-256 `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`. [Nesne/geometri denetimi](../../data/model-candidates/upper-limb-nerve-source-audit-v1/REVIEW.md) ile [ad/ilişki kanıtı](../../data/model-candidates/upper-limb-nerve-metadata-v1/REVIEW.md) ayrı korunur. Public paket127 nesne/kavram içerir:54 ek adlandırılmış sinir/grup eğrisi,24 aynı-kaynak siniri ve49 bağlam kemiği;184.698 vertex ve366.040 üçgen. Bunlar127 yeni anatomik yapı değildir.

Tek ortonormal eksen dönüşümü `(x,y,z)→(x,z,-y)` uygulanır; metre birimi ve kaynak nesnelerin göreli yerleşimi korunur. Eski üst-kol dönüşümünün bütün boyun/klavikula/kaburga bağlamına uyumu yeterli görülmediğinden paket ayrı yüklenir. `compatibleWithMainAtlas:false`, `registration:null`; ana atlas, extension registry ve motor ilişkileri değişmez. Geometri binary/gzip'i denetlenmiş adayla byte-identical kalır; değişen manifest ürün/atıf durumunu açıkça kaydeder.

## Etiketler, ilişkiler ve sınırlar

127 TR/EN etiket;110 Latin gösterim (108 sabitlenmiş numeric terim ve iki ayrı IFAA düzeltmesi);17 numbered-bone Latin alanı gerekçeli null. Null durumda İngilizce kaynak adı ve görünür açıklama kullanılır. Türkçe adlar editoryal, uzman incelemesi bekler. Ana modelle aynı kavram kimliği kullanılması dataset koordinatlarını veya ilişki kümelerini birleştirmez.

26 seçilmiş `branch_of` olgusu doğrudan kaynaklı TTUHSC tablolarından gelir. Öğrenci bu referansın ebeveyn/dal seçimleri arasında gider ve geri döner. Ana modelin kas uçlarına ait motor bağlantıları bu referansa kopyalanmaz. Posterior interosseous/deep-radial sınırı için belirsiz ek kenar verilmez. Sekiz çoğul kas dalı nesnesi, ayrı numaralı motor dallar veya tam kas bağlantısı olarak sunulmaz.

Adlandırılmış kaynak seyri tam sinir ağı değildir. Bilateral ulnar eğrilerdeki tek noktadan oluşan sıfır-geometri spline kayıtları korunur; onlardan yüzey üretilmez. Bağlam kemiklerinin kaynak yüzey kusurları ve eğri grup kapsamları onarılmadan kaydedilmiştir. C5–T1 katkıları, medial/lateral kordlar ve bütün el dalları bu pakette ayrı temsil edilmez. Diğer BP3D4.3 iki sol kord adayı, bu paketin kabulüne veya parça toplamına dahil değildir. Kaynak geometrisi/etiket, süreklilik, anatomik uzman kabulü ve fiziksel cihaz performansı birbirinden ayrıdır.

## Ürün kabulü ve yeniden üretim

[Makine kabul kaydı](upper-limb-reference-product-acceptance.json) public paket/metadata hash'leri, kullanılan runtime dosya hash'leri, üretim bundle'ı ve root tarafından açılan ekranları saklar. Kabul temsilî öğrenci akışları içindir;352 hedefin tek tek anatomik ayrıntı kabulü değildir. Tarihî geliştirme ekranları ve başarısız320 denemesi son üretim kabulünün yerine kullanılmaz.

Yerel `/human-atlas/` üretim önizlemesinde1440×1000: ASCII sol supraskapular araması, tek doğru taraf, kaynak başlığı, üst gövde→Geri, Latin etiket, izolasyon; görünen sinir yüzeyine doğrudan tıklamada seçim ve127 parça bağlamına dönüş.390×844: İngilizce sağ deep-radial→radial→Geri, TTUHSC kaynak açılımı ve izolasyon.320×568: aynı seçim/izolasyon kadrajı ve null Latin C3 gösterimi; ana modele dönüşte2.290 parça, seçim/geçmiş/kamera temizliği. Küçük ekran panel içerikleri kaydırılarak okunur; ince kaynak sinir eğrisi büyütülmeden korunur. Canlı yayın kanıtı [teslim raporuna](progress-report-2026-10-02.md) ayrıca eklenir.

`python3 scripts/package-upper-limb-reference.py --check` frozen geometri/metadata kanıtlarını,127 unique kavram/parçayı, kaynak nesne/taraf kapsamını,110/17 Latin durumunu,26 kendi-dataset ilişki ucunu ve public dosyaların tam içeriğini kontrol eder. `python3 scripts/build-upper-limb-reference-targets.py --check` [v2 hedef projeksiyonunu](upper-limb-targets-v2.md) kontrol eder; önceki bütün temsiller korunur. `node scripts/build-model-inventory.mjs --check` tüm508 gereksinimi ve yeni dataset kaynak/etiket/ilişkilerini uzlaştırır.

`npm run check`, mevcut beş anatomy-knowledge testi, yeni dataset sınırını da içeren etkileşim doğrulayıcısı ve üretim build'i geçti. Geometri değişmediği için Blender render/export tekrarlanmadı; aktarım SHA eşliği ve önceki source/decoded görseller geçerli kalır. Büyük JS bundle uyarısı sürer. Ortam: macOS, Node24.18.1, Python3.9.6, headed Chromium; kaynak audit Blender5.2LTS. Fiziksel telefon ve anatomist değerlendirmesi yapılmadı.

## Atıf ve sahiplik

[Bileşen atfı](../../public/models/upper-limb-nerve-reference/ATTRIBUTION.md) Z-Anatomy CC BY-SA4.0 ve alttaki BodyParts3D CC BY-SA2.1 Japan bildirimlerini ayrı tutar; özgün lisans metni aynen kopyalanır. Object-specific köken zinciri upstream'de verilmediğinden toplu yeniden lisanslama varsayılmaz. Bu seçime iç kulak/böbrek istisna nesneleri alınmaz. Üniversite kaynaklarından seçilmiş olguların kanıtı tutulur; görseller veya uzun sayfa metinleri ithal edilmez.

Root ürün entegrasyonu ve yayın kapanışının tek sahibidir. Kaynak/metadata alt işler tamamlanmıştır. Yayın revision'ı ve ölçülen süre teslim raporunda kapanır; uzman/bütün bölge kabulü açık kalır. Sıradaki model işi iki sol BP3D4.3 kordunun dar kapsamlı entegrasyonudur; sağ kordlar ve kök katkıları ayrıca araştırılacaktır.
