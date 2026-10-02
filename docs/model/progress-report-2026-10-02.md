# Model ürünü eylem ve süre raporu — 2 Ekim 2026

Hedef, tıp öğrencisinin bütün vücudu yapı ve alt yapı düzeyinde seçip kaynaklı adları, bağlamı ve ilişkileri üzerinden inceleyebilmesidir. Model önce, ders/quiz katmanı sonra gelir. Hedef henüz tamamlanmadı. [Kapsam sözleşmesi](model-scope-and-acceptance.md) bu hedefi ve bölgesel kabul koşullarını taşır.

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
