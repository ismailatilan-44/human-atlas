# Model ürünü eylem ve süre raporu — 2 Ekim 2026

Hedef, tıp öğrencisinin bütün vücudu yapı ve alt yapı düzeyinde seçip kaynaklı adları, bağlamı ve ilişkileri üzerinden inceleyebilmesidir. Model önce, ders/quiz katmanı sonra gelir. Hedef henüz tamamlanmadı. [Kapsam sözleşmesi](model-scope-and-acceptance.md) bu hedefi ve bölgesel kabul koşullarını taşır.

Bu raporun ilk durum fotoğrafı `a0fd554` teslimine aittir. Gün içindeki sonraki model teslimi aşağıdaki ek kayıtta ayrı izlenir; ilk fotoğraftaki aday/yayın durumları tarihî kanıt olarak korunur.

**Son doğrulanmış ürün teslimi:** `1fbaeac664282f4c6314357b4eda5e5a106e9144`, canlıda 2 Ekim 2026. Bağımsız alt ekstremite referansı 87 nesne, 87 TR/EN etiket, 53 doğrulanmış Latin ad ve 12 dal bağlantısıyla yayımlandı. Ana model 2.290 parça ve 309 etiket; dört dataset toplamı 2.410 paketli parça. 66 önerilen alt ekstremite hedefinin tamamında kaynak temsil bağı var; anatomik uzman kabulü sıfır ve hedef listesi eksiksiz değil. Bütün model hedefi açık; ayrıntılı yayın kanıtı son ek kayıttadır. Aşağıdaki önceki durum ve teslim bölümleri tarihî kayıtlardır.

## Gerçek durum ve yayın

Bu çalışma turu `codex/publish-model-explorer` dalında `547c1161068f0b8e863f06c91997325214b577eb` kaynak başlangıcından yürüdü. Başlangıçta `.agents/` ve `AGENTS.md` kullanıcıya ait izlenmeyen dosyalardı; yeni çıktılardan ayrı korundu. 2 Ekim uzak kontrolünde fork `main` ve geliştirme dalı aynı kaynak revision'ındaydı; `gh-pages` revision'ı `21a902f675be0d281883a5ac1e9be21c938eeb1c` idi.

[Canlı ürünün](https://ismailatilan-44.github.io/human-atlas/) `release.json` dosyası bugün `caa938a4745a570fad13e445dda6c34909cdf4e5` döndürdü. Bu tur arayüz değişmedi ve yeni yayın yapılmadı. Önceki masaüstü/mobil tarayıcı kabulü 26 Eylül raporunda tutuluyor; bugün yeni canlı UI kabulü yapıldığı iddia edilmiyor.

| Alan | Yayımdaki mevcut durum | Sınır |
| --- | --- | --- |
| Ana gövde | 2.234 temel + 56 kayıtlı ek = 2.290 model parçası | Yüzey sayısı anatomik tamamlanma değildir |
| Ayrı referanslar | Kadın pelvis 27, iç kulak 6 parça | Tam kadın vücudu veya iç kulağın bütün ince yapıları değildir |
| İsim ve ilişkiler | 275 etiket kaydı, 3.514 grafik kavramı, 1.524 ilişki | Bütün çeviriler ve işlevsel ilişkiler tamamlanmış değildir |
| İlk bölgesel kontrol | 65 hedef grubu: 61 mevcut, 3 kısmi, 1 doğrulanmamış | Bütün vücudun hedef listesi veya tamamlanma paydası değildir |

Önceki teslimlerde seçme, arama, izolasyon, çevre saydamlığı ve ilişki üzerinden gezinme çalışır hâle getirildi; sinir, diz, tiroid, omurilik, pleksus ve akciğer paketleri eklendi. Yanlış akciğer kaynak üyeliği incelenmiş seçimlerde düzeltildi; ham üyelik korunuyor. Ayrıntılı tarihî kanıtlar [teslim planında](2026-09-20-delivery-plan.md) ve [26 Eylül raporunda](progress-report-2026-09-26.md).

## Bu tur yapılan işler

| İş | Somut çıktı ve durum | Sonraki kabul koşulu |
| --- | --- | --- |
| P1 kaynak envanteri | [Üretici](../../scripts/build-model-inventory.mjs), [makine envanteri](../../data/anatomy/model-inventory.json), [okunabilir envanter](model-inventory.md) hazır | Her bölge/aile için tek tek yapı, taraf ve gereken ayrıntı hedeflerini açmak |
| Kapsam matrisi | 13 bölge × 4 aile × D0–D3 = 208 bekleyen hücre; kaynak ve incelenmiş seçimler ayrı korunuyor | Hücreler eksik yapı sayısı değildir; hepsi hedef açılımı/kabul bekliyor |
| Bölgesel eşleme | 3.572 dataset kimlikli katalog kaydından 127'si mevcut kanıtla planlama kuyruğuna bağlı; 3.445'i bölgesel eşleme için denetlenmemiş | İsim veya parça sayısından otomatik yokluk/tamlık çıkarmadan kalan kayıtları incelemek |
| P2 distal sinir geometrisi | Sol/sağ tibial ve ortak fibular sinir için dört gerçek kaynak eğrisi ve kendi kaynak kemikleriyle 14 nesneli aday paket hazır; buffer ve kaynak/çıktı görsel kontrolleri yapıldı | Ana gövdeyle distal yerleşim kabulü başarısız; aktif modele kayıt yapılmadı |
| P2 aday isim/ilişki | [Aday incelemede](../../data/model-candidates/distal-leg-nerve-metadata/REVIEW.md) dört TR/EN/TA2-Latince etiket ve dört aynı taraflı siyatik dal ilişkisi hazır | Geometri kararı, uygulama entegrasyonu ve anatomik inceleme; aktif etiket/grafiğe eklenmedi |

Envanter üç referanstaki toplam 2.323 aktif model parçasını kapsar. 3.572 katalog kaydı kaynak kavramları, proje kavramları ve seçim varyantlarını içerir; 3.572 bağımsız anatomik yapı demek değildir. Altı kaynak yüzey işareti ve iki çözülmemiş humeral konum ayrı izlenir. P1'in ilk teknik çıktısı tamamdır; bütün vücudun tek tek hedef envanteri henüz tamam değildir.

## Yeni kaynak bulgusu ve alınan karar

Distal sinirlerde mevcut siyatik dönüşümü kaynak uç sürekliliğini korudu; ancak alt bacakta aynı dönüşüm yeterli olmadı. Bağımsız kaynak–hedef kemik yüzeyi karşılaştırmasında tibia RMS yaklaşık 6,5 mm, fibula yaklaşık 9,3–9,6 mm; ayak bileği ölçüm bandında yaklaşık 10–13 mm fark bulundu. Bunlar **kemik yüzeyleri arasındaki uyum ölçüleridir**, sinirin gerçek anatomik konum hatası ölçümü değildir. Kaynak ve hedef bağlamlarının yan yana görsel incelemesinde tibial sinirin medial ayak bileğiyle ilişkisi değişiyor.

Bu nedenle dört siniri mevcut gövdeye kabul edilmiş gibi eklememe kararı alındı. Kaynağın kendi kemik bağlamını koruyan ayrı 14 nesneli aday paket hazır: 21.232 üçgen ve 242.442 gzip byte. Bu paket bir ürün referansı olarak arayüze eklenmiş sayılmıyor. Kaynak nesne, taraf, kontrol noktası, dönüşüm, lisans, bağlam kemiklerindeki kaynak kusurları ve yerleşim sorunu [registration kaydında](asset-registration-distal-leg-nerves.md) korunuyor. [Karşılaştırma görseli](../../data/model-candidates/distal-leg-nerves/source-target-posterior.png) ve [ölçüm kaydı](../../data/model-candidates/distal-leg-nerves/registration-report.json) incelenebilir. Anatomi uzmanı kabulü yoktur.

## Açık iş ve teslim sırası

1. P1'i her bölgede kaynak kimlikli tek tek hedef, taraf ve ayrıntı listesine açmak. İlk 65 hedefi tüm hedefin yerine koymamak.
2. Distal sinirlerin ana gövdeye doğru yerleşimi için bölgesel kaynak/dönüşüm alternatifini değerlendirmek. Dört etiket ve dal ilişkisini ancak kabul edilen temsil üzerine bağlamak; ayrı referansta siyatik ebeveyn geometrisinin bulunmadığını korumak.
3. Üst ekstremite sinirleri ve pleksus ayrıntıları; ardından el/ayak yapıları, eklem/bağ/tutunmalar, kardiyopulmoner iç yapılar, abdomen, pelvis, baş-boyun ve merkezi sinir sistemi paketleri.
4. Çok dilli isim ve gereken işlevsel ilişkileri aynı bölgesel teslimle tamamlamak; gerçek cihaz performansı ve anatomik uzman değerlendirmesini ayrı kabul etmek.
5. Gerekli ince D3 yapıları ve kadın/diğer referans kapsamını açık hedef olarak sürdürmek. Ders katmanını kabul edilen yapı kimliklerine sonradan bağlamak.

Açık kaynaklar önemli bir başlangıç gövdesi sağlar. Farklı kaynakların aynı referans birey, ölçek, taraf, ayrıntı ve lisansa sahip olması garanti değildir; bugünkü distal yerleşim bulgusu bunun somut örneğidir. Model indirmenin ardından kimlik, bağımsız seçilebilirlik, konum, isim, ilişki ve kullanım kabulü gerekir.

## Süre tahmini ve güven düzeyi

Ölçülmüş paket üretim hızımız ve tamamlanmış tek tek hedef paydamız yok. Aşağıdaki aralıklar önceki kaba teknik emek tahminidir; kesin takvim veya otomatik arka plan çalışma vaadi değildir. Varsayım, haftada yaklaşık **30–40 saat aktif teknik çalışma** ve mevcut kaynaklara erişimdir. Uzman incelemesi bekleme süresi dahil değildir.

| Teslim | Kaba teknik emek aralığı | Tahminin sınırı |
| --- | --- | --- |
| P1'in tek tek yapı/ayrıntı hedeflerine açılması | 2–4 hafta | Bugünkü kaynak kataloğu hazır; kalan anatomi denetiminin büyüklüğü henüz ölçülmedi |
| Öncelikli bölgesel model paketleri | 2–4 ay | Kaynak yerleşimi veya ayrıntı eksikleri paket bazında süreyi değiştirebilir |
| Bütün bölgelerde güçlü D1 ve öncelikli D2 deneyimi | 6–12 ay | Şimdilik düşük güvenli planlama aralığı; P1 hedef sayısı sonrası yeniden hesaplanmalı |
| Yaygın D2/D3 ve bütün gerekli uzman kabulü | Güvenilir tek tarih yok | İnce yapı kaynağı ve değerlendirme kapasitesi henüz belirli değil |

Bu aralıklar toplanacak ardışık süreler değildir; farklı teslim seviyeleridir. Aktif tur dışındaki zaman çalışma saati sayılmadı. 26 Eylül–2 Ekim arasındaki doğrulanmış commit/yayın geçmişinde yeni ürün sürümü yok. Bu turun başlangıç/üretim süreleri ölçülmediği için toplam aktif emek **bilinmiyor**. Önemli yeniden çalışma nedeni: distal kaynağın ana gövdeyle ayak bileği çevresinde uyumsuzluğu ve ayrı kaynak bağlamına dönüş.

## Kontrol kanıtı ve raporlama

- `node scripts/build-model-inventory.mjs --check`: yerelde geçti; kimlik/üyelik uçları ve üretilen dosyaların güncelliği doğrulandı. Ortam: Node `v24.18.1`.
- `npm run check`: envanter teslimini hazırlayan işte yerelde geçti; bu tur aktif uygulama kaynakları değiştirilmedi.
- Distal aday: dört sinirin ve 14 nesneli kaynak paketinin buffer/topoloji kontrolleri; dört render; son tekrar üretimde aynı iki binary SHA doğrulandı. `node scripts/validate-atlas.mjs` değişmeyen temel atlas için geçti; adayın yerleşim kabulünü kanıtlamaz. Blender `5.2.0 LTS`, `--disable-autoexec` ile çalıştı. Teknik export geçmesi ana gövde yerleşim kabulü değildir.
- Aday metadata: dört benzersiz kimlik, dört aynı taraflı dal ilişkisi, dört manifest bağı ve iki TA2 terim çifti kontrol edildi. Son geometri kararı manifesti değiştirdiği için hash kontrolü tekrarlandı; altı giriş hash'i ve ayrı kaynak referansındaki dört sinir bağı geçti.
- Canlı: yalnız `release.json` kaynak revision'ı bugün yeniden kontrol edildi. Yeni build, CI veya canlı UI kabulü bu tur yapılmadı.

Her anlamlı teslimde bu kayıt düzeniyle sonuç, kaydedilen kaynak revision'ı, kabul kanıtı, açık kusur, süre tahminindeki değişiklik ve sıradaki tek somut adım raporlanır. Sürekli çalışan geliştirme veya periyodik rapor otomasyonu kurulmuş değildir. Kullanıcıdan şu an teknik bir işlem beklenmiyor; hedef ayrıntısını netleştirmek için ileride ders kapsamı, anatomik kabul için yetkin değerlendirici gerekecek.

**Sıradaki somut adım:** P1'de alt ekstremite yapı/ayrıntı hedeflerini kaynak kimliklerine açmak; reddedilen distal yerleşim için gerekli temsil ve kaynak alternatifini bu hedeflere bağlamak.

## Aynı gün sonraki model teslimi — yerel kabul

Başlangıç revision'ı `a0fd554`. Bağımsız [alt ekstremite sinir referansı](lower-limb-nerve-reference-review.md) arayüze eklendi: 21 seçilebilir kaynak nesnesi, altı sinir eğrisi/15 kemik, 21 ayrı TR/EN/LA etiket ve dört aynı taraflı dal ilişkisi. Dört distal sinire aynı kaynaktan iki siyatik sinir ve proksimal kemik bağlamı eklendi. Kaynak boyunca komşuluk tek ortak eksen dönüşümüyle korunur; başarısız ana-gövde yerleşimi hâlâ kabul edilmez. Ana sahne 2.290 parça ve ana etiket dosyası 275 kayıt olarak kalır.

[Bireysel hedef başlangıcı](lower-limb-targets-v1.md) 33 kesin TA2 teriminden 66 sağ/sol D1/seçilmiş D2 gereksinimi açar. 48 hedefte gözlenen kaynak parça bağı vardır; 18'i bağlanmamıştır. Bunlar proje önerileridir ve sıfır anatomik uzman kabulü taşır. Metatars/parmak kemikleri, iç kaslar, tendon/fasya/retinakulum, ven/lenf, ince dallar ve D3 dahil açılmamış hedefler görünür kalır. Genel P1 veya bir bölge tamamlandı sayılmaz.

Yeni katalog dört dataset için 3.593 kavram/seçim ve 2.344 parça kaydı içerir. Dataset ile ayrılmış 1.528 ilişki, ana 1.524 ve yeni referansın dört dal bağlantısından oluşur. 192 kayıt mevcut kanıt/hedef önerisiyle planlama kuyruğuna bağlı, 3.401 kayıt bu eşleme açısından denetlenmemiştir. Hedef matrisi hâlâ 208 bekleyen hücredir.

Yerel kontrol: TypeScript; etkileşim validator'ında referansa bağımsız yükleme, kaynak kimliği ve dal uçları, ana-gövde innervasyonlarının referansa taşınmaması; envanter ve hedef dosyalarının üretim/güncellik kontrolleri geçti. Blender iki export'ta aynı binary/gzip/manifest SHA üretti; önceki 14 nesnenin dizileri değişmedi. Gerekli ilk geometri ve terim kontrol kanıtları kendi kayıtlarında tutulur.

Gerçek Chromium UI: 1440×1000 Türkçe arama → sol tibial seçim → odak → aynı taraf siyatik → ortak fibular dal → izolasyon ve kaynak bağlantısı görüldü. 390×844 mobilde dal/izolasyon/Latince ad/geri dönüş; 320×568'de seçili sinir kadrajı incelendi. İlk mobil kadraj kamera araçlarıyla çakıştı; ölçülen araç sınırı fit hesabına dahil edildi. Kısa portre ekranında panel açıkken kamera preset araçları gizlenerek model alanı ayrıldı; orbit/zoom etkileşimi devam eder. Bu düzeltme nedeniyle ilgili yerel kontroller tekrarlandı. Fiziksel cihaz performansı ve uzman incelemesi bekler.

Yerel görseller: [masaüstü tibial odak](../../output/playwright/lower-limb-desktop-tibial-focus.png), [390×844 düzeltilmiş kadraj](../../output/playwright/lower-limb-mobile-fibular-fixed.png), [320×568 düzeltilmiş kadraj](../../output/playwright/lower-limb-small-mobile-fixed.png). Bu yerel fotoğraf canlı sürüm kabulünden önce kaydedildi; yayın sonucu sonraki ek kayıtta tutulur. İngilizce sağ ortak fibular → sağ siyatik akışında ebeveynin iki aynı taraf dalı görüldü. Ana modele dönüş 2.290 parçayı yükledi, seçimi ve geri geçmişini temizledi.

Süre tahmini değişmedi: tam tek tek hedef paydası ve ölçülmüş paket üretim hızı hâlâ yok. Bu turun toplam aktif üretim süresi ölçülmedi; önemli yeniden çalışma nedeni mobil kadraj çakışmasıdır. Sıradaki paket, henüz bağlanmamış distal sinir dalları ve ayak bileği destek hedeflerinin gerçek kaynak alt nesnelerini denetlemektir.

## Aynı teslimin yayın kabulü — 2 Ekim 2026

Kaynak `09879bf300d38eae14054fcdd55ea4fdc121d1fc`, fork `main` ve `codex/publish-model-explorer` dallarına force kullanmadan gönderildi. Statik dal `1a13ccf4136780b8c9b4b9a4ab8dbb0d40024f6f`; [Pages #36984762689](https://github.com/ismailatilan-44/human-atlas/actions/runs/36984762689) başarılı. Canlı `release.json` kaynak SHA ile eşleşti. `npm run deploy:pages` içindeki üretim build ve mevcut explorer-catalog güncellik kontrolü geçti. Üretim JS gzip 337,62 KB; büyük JS paketi uyarısı sürüyor. Bu teslimde uzman incelemesi veya fiziksel cihaz performansı kapanmadı.

Gerçek [canlı adreste](https://ismailatilan-44.github.io/human-atlas/) Chromium 390×844 akışı: ayrı referans 21 parçayla yüklendi; ASCII `sag tibial` tek doğru taraf sonucu verdi; tibial → sağ siyatik → sağ ortak fibular düğme geçişleri çalıştı. Son dal izolasyonda ve Latince `(R)` adıyla incelendi; sinir geometri alanında araçların altında/panelin üstünde görünür. [Canlı ekran kanıtı](../../output/playwright/lower-limb-live-mobile-fibular.png). Bu gezinmeden sonra tarayıcı konsolunda hata veya uyarı yoktu. Yerel masaüstü/iki mobil kabul yukarıda ayrı kayıttadır; canlıda bu tur yalnız 390×844 akışı tekrarlandı.

Entegrasyon sahibi root; kaynak geometri ve metadata alt görevleri tamamlandı, entegrasyon sahipliği devredildi. Rapor hazırlanırken bu alt görevlerde çalışan ajan kalmadı. Kullanıcının izlenmeyen `.agents/` ve `AGENTS.md` dosyaları, eski render log'u ve geçici tarayıcı çıktıları teslimden ayrı korundu. Sürekli/periyodik rapor otomasyonu kurulmadı; anlamlı her teslimde bu kayıt sonuç, revision, kabul, engel, tahmin değişikliği ve sonraki adımla güncellenir.

**Sıradaki tek somut eylem:** 18 bağlanmamış alt ekstremite hedefinin gerçek kaynak nesnelerini denetlemek; önce distal sinir dalları ve ayak bileği bağları, ardından fibular arter. Kaynakta yokluk, anatomik tamlık veya ana gövde uyumu isim/parça sayısından çıkarılmayacak. Ders katmanı model hedefinden sonra kalır. Senden şu an kurulum veya kod işlemi beklenmiyor; kapsamlı anatomik kabul yetkin değerlendiriciye ihtiyaç duyuyor. Kesin bitiş tarihi için tüm tek tek hedef listesi ve birkaç bölgesel paketin ölçülmüş üretim hızı hâlâ eksik.

## Sonraki model teslimi — 87 nesneli yerel kabul

Başlangıç `e879fc92e1bfa6226898d12cdca2863e365858e0`, dal `codex/publish-model-explorer`; başlangıç uzak main/dal eşleşmesi doğrulandı. Önceki tur ürün/yayın ve kayıt değiştirerek ilerleme sağladı. Bu tur 18 hedefin kaynağı denetlendi; tamamının aynı Z-Anatomy dosyasında bağımsız geometrisi bulundu. Alt ekstremite referansı 21 → **87 nesneye** çıktı: 16 sinir, iki fibular arter, altı ayak bileği bağı, 63 kemik. Önceki 21 nesnenin konum/normal/indeks dizileri byte düzeyinde aynı kaldı. Tek ortak eksen dönüşümü dışında konum/ölçek/şekil değişmedi; ana gövdeye reddedilen yerleşim hâlâ kabul edilmez. Gzip geometri 1.462.468 byte; 125.372 üçgen.

[Kaynak/geometri raporu](../../data/model-candidates/lower-limb-unbound-source-audit/REVIEW.md) 18 birincil nesneyi, 48 yeni ayak kemiğini, sourceObject/part/concept kimliklerini, spline kapsamını ve kusurları izler. Bağlar kaynakta tek dörtgen + kalınlık/yüzey işlemlerinden türetilmiş kaba şerit yüzeyleridir; yüksek ayrıntılı eklem bağları olarak kabul edilmez. Medial plantar sinirde üç kaynak spline'ından biri tek noktadır ve yüzey üretmez; bu noktadan yapay dal çizilmedi. Yeni sekiz kemikte küçük yerel normal uyuşmazlıkları, önceki kemik kusurları ve uzman inceleme sınırı açık korunur. İki export aynı binary/gzip/manifest hash'lerini verdi; eşleşen kaynak/decoded render'lar görüldü. Entegrasyon sahibi ayrıca plantar karşılaştırmasını ve lateral bağ görselini açtı.

Referans metadata **87 TR/EN, 53 kesin Latin etiket ve 12 kaynaklı dal ilişkisi** içerir. 34 dijite özgü Latin ad için kaynak özel/yıldızlı satırları resmî TA2 kimliği yapılmadı; null alan, ayrı genel tip terimi ve görünür İngilizce fallback açıklaması korundu. Yeni sekiz dal ilişkisi TTUHSC kaynağıyla deep/superficial fibular → common fibular ve medial/lateral plantar → tibial olarak aynı tarafla açıldı. Sural sinire tek ebeveyn, arter/bağ/besleme ilişkilerine çıkarım eklenmedi. Ana atlas **34 yeni TR/EN/LA etiketle 309 kayda** çıktı; başlangıç listesindeki 44 ana-gövde temsili üç dilde adlandırıldı. Ana atlas geometri/grafik/üyelikleri değişmedi. [Ana etiket kanıtı](../../data/model-candidates/lower-limb-main-labels/REVIEW.md).

66 önerilen hedefin tamamında kaynak temsil bağı vardır; bağlanmamış hedef sayısı sıfırdır. Bu **bölgesel tamamlanma veya anatomik kabul değildir**: gerekli ilişkiler/ayrıntı/bağlam ve uzman inceleme açık, hedef listesi eksiksiz değildir. Yeni ayak metatars/falanks geometrisi bağlam olarak vardır; dijit/segment gereksinimlerine tek tek açılması hâlâ bekler. Katalog dört dataset için 3.659 kayıt/2.410 parça/1.536 ilişki; 258 planlama eşlemesi, 3.401 denetlenmemiş bölgesel eşleme ve 208 bekleyen kapsam hücresi taşır.

BP3D denetiminde fibular arter için iki doğrulanmış 4.3 aday bulundu. FJ2093/FJ2197 ana 4.0 pakette kaynak FMA70801/dorsal dijital arter grubu adını taşırken 4.3'te FMA43923/FMA43922 peroneal arter olarak dönüyor. Eski metadata mevcut adı destekliyor; ortak FJ numarası geometri eşitliği sayılmadı. Bu nedenle ana kimlik düzeltilmedi; aday ve kaynak sürümü uyuşmazlığı [ayrı raporda](../../data/model-candidates/lower-limb-unbound-mapping/REVIEW.md) kaldı. Bu tur hedef bağı bağımsız Z-Anatomy referansından sağlandı. Araştırma kontrolünün 'şu anda bağlanmamış' filtresi hedeflerin bağlanmasıyla başarısız oldu; sabit dokuz terim/iki tarafla düzeltilip üretim ve --check geçti. Bu tekrar nedeni ve güncel/hash ile tarihî keşif başlangıcı ayrımı kayıtta var.

Yerel kontroller geçti: TypeScript, mevcut etkileşim validator'ı (87 dataset parçaları, tibial/plantar aynı taraf uçları, ana grafik izolasyonu ve değişmeyen 2.290 ana parça), 66 hedef üretim/güncelliği, 34 ana etiket proposal güncelliği, BP3D aday kontrolü ve envanter --check. Dosya biçimi kontrolü geçti; kopya upstream lisans metni değiştirilmez. Fiziksel cihaz veya anatomist kabulü yoktur. Üretim build/yayın bu yerel kabulün sonrasında ayrı kaydedilecek.

Gerçek Chromium yerel akışları: 1440×1000 `sol kayik` → tek navicular → `Os naviculare (L)` izolasyonu; kaynak ayak bağlamında medial plantar → tibial → lateral plantar ve TTUHSC kaynak bağlantısı; 390×844 `sol on talofibular` → Latince tek bağ ve çevre; 320×568 sağ ikinci metatars izolasyonu → görünür çözümlenmemiş Latin açıklaması ve geri dönüş. Konsol hata/uyarı kaydı boş. [Ana navicular](../../output/playwright/lower-limb-main-navicular-latin.png), [plantar bağlam](../../output/playwright/lower-limb-reference-plantar-context.png), [mobil bağ](../../output/playwright/lower-limb-mobile-ankle-ligament-context.png), [küçük mobil Latin](../../output/playwright/lower-limb-small-mobile-latin-unresolved.png). Son iki açıklama kullanıcı için sadeleştirildi; spline/kontrol noktası ayrıntısı kaynak kayıtlarında kaldı.

Bu devam turunun ilk kontrolü 08:42:27 UTC'de kaydedildi. Kapanış/yayın zamanı teslim sonunda ayrıca tutulacak; bu aralık duvar süresidir, kesin aktif insan/ajan emeği değildir. BP3D bounded denetimi ölçülen 6m12s; metadata genişlemesi 7m31s; paralel oldukları için toplanmaz. Geometri görevinin bütün aktif süresi bilinmiyor; ölçülen Python inceleme/render 26,82s. Önemli yeniden çalışmalar tek noktalı spline sınır kontrolü, render kadrajı, değişen bağlanma durumuna bağlı araştırma filtresi ve küçük mobil açıklama görünürlüğüdür. Büyük hedefin süre aralığı değiştirilmedi; tüm hedef paydası/ölçülmüş paket hızı yok.

**Sıradaki somut eylem:** yeni ayak kemiklerini dijit/segment/ayrıntı hedeflerine açmak ve kaynaklı kemik/bağ komşuluk-tutunma kanıtını denetlemek; ardından tam model planındaki üst ekstremite ve diğer bölgesel açık işleri sürdürmek. Kaba bağ şekli ile doğrulanmış footprint aynı kabul edilmez. Bütün model hedefi aktif; ders katmanı sonraki fazda kalır.

## 87 nesneli teslimin canlı kabulü — 2 Ekim 2026

Kaynak `1fbaeac664282f4c6314357b4eda5e5a106e9144`, fork `main` ve `codex/publish-model-explorer` dallarına force kullanmadan gönderildi. Statik dal `1a83345c9c6ee8c954cbf742a9af3d4e9bffa47c`; [Pages #36989651012](https://github.com/ismailatilan-44/human-atlas/actions/runs/36989651012) tamamlandı/başarılı. 09:35:45 UTC kapanış kontrolünde canlı `release.json` tam kaynak SHA ile eşleşti ve üç uzak dal yeniden okundu. `npm run deploy:pages` içindeki üretim build ve explorer-catalog güncellik kontrolü geçti. Üretim JS gzip 348,45 KB; büyük paket uyarısı sürüyor. Bu kayıt doküman teslimidir; yeni ürün build'i gerektirmez.

Gerçek [canlı adreste](https://ismailatilan-44.github.io/human-atlas/) Chromium 390×844: referans 87 parçayla yüklendi; ASCII `sag fibular arter` tek doğru taraf sonucundan seçilip odaklandı, kaynak kemikleriyle kısmi damar seyri görüldü. ASCII `sag derin fibular` → sağ derin fibular → sağ ortak fibular → sağ yüzeyel fibular gerçek düğme akışı çalıştı. Ortak fibularda siyatik ebeveyn ve iki aynı taraflı dal görüldü; yüzeyel fibular izolasyonu, Latin `Nervus fibularis superficialis (R)` adı ve TTUHSC kaynak bağlantısı doğrulandı. [Canlı arter](../../output/playwright/lower-limb-live-fibular-artery.png) ve [canlı dal/Latin izolasyonu](../../output/playwright/lower-limb-live-fibular-branches.png) açılarak incelendi. Konsol 0 hata/0 uyarı. Bir ilk otomasyon locator'ı iki metin arasındaki boşluğu içermediği için zaman aşımına uğradı; erişilebilir snapshot'taki gerçek adla tekrarlandı ve geçti. Bu uygulama hatası olarak raporlanmaz.

İlk kontrol 08:42:27 UTC, ürün kabul kapanışı 09:35:45 UTC: **53 dakika 18 saniye duvar süresi**. Bu süre paralel iş ve beklemeyi kapsar, aktif insan/ajan saatleri toplamı değildir. Eski kayıtlardaki bilinmeyen süreler geriye dönük tahmin edilmedi. Entegrasyon root tarafından kapatıldı; kaynak ve metadata alt görevleri tamamlandı. Kullanıcının izlenmeyen `.agents/`, `AGENTS.md`, eski render log'u ve önceki geçici ekran çıktıları korunur.

**Açık kabul koşulları:** kaba bağ yüzeyleri, 34 çözümlenmemiş dijite özgü Latin etiket, ince sinir/damar dalları, eksiksiz bireysel hedef listesi, ana gövdeyle farklı kaynakların uyumu, kaynak kemik kusurları, fiziksel cihaz performansı ve anatomik uzman incelemesi. Parça veya bağlanmış hedef sayısı tamamlanma yüzdesi yapılmadı. Tahmin değişmedi: haftada 30–40 saat aktif teknik çalışma varsayımıyla hedef envanteri 2–4 hafta, öncelikli paketler 2–4 ay, bütün bölgelerde güçlü D1/seçilmiş D2 6–12 ay; güven düşük, uzman bekleme süresi hariç. Yaygın D2/D3 için güvenilir bitiş tarihi yok.

**Sıradaki tek eylem:** kaynakta mevcut ayak kemiklerini parmak numarası/segment/ayrıntı hedeflerine açmak ve temsil sınırlarını kaydetmek; ardından ilgili kemik/bağ ilişkilerini kaynakla denetlemek. Kullanıcıdan şu an kurulum veya kod işlemi beklenmiyor. Modelin bütünü tamamlanmadı; ders katmanı sonraki fazda. Her anlamlı teslimde bu rapor sonuç, revision, kabul, açık iş, süre/tahmin ve sonraki eylemle güncellenir; sürekli çalışma veya periyodik rapor otomasyonu kurulmuş değildir.
