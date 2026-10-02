# Model odaklı ürün — teslim planı ve güncel durum

İlk plan: 20 Eylül 2026. Güncel durum: 2 Ekim 2026. Kod, kaynak paketi, görsel kabul ve yayın birbirinden ayrı izlenir.

**Güncel ürün:** [canlı atlas](https://ismailatilan-44.github.io/human-atlas/), kaynak `e005d53a9cb22cda52c39fb318248a83ba113fe8`; beş dataset, 2.587 parça, 3.836 kavram/seçim ve 1.674 ilişki. Ana atlas 2.290 parça/401 bölgesel etiket olarak korunur. Yeni bağımsız üst ekstremite referansı 127 nesne/127 TR-EN/110 Latin/26 dal ilişkisiyle yayımlandı. Statik dal `ee885b354bd5a97022c2b59c167ab480bab5f26f`, [Pages #37032342416](https://github.com/ismailatilan-44/human-atlas/actions/runs/37032342416) başarılı. Canlı release.json ve paket hash'leri eşleşti; gerçek 390×844 sağ deep-radial→radial→Geri→Latin/kaynak/izolasyon akışı görüldü, konsol 0 hata/uyarı. Yerel 1440×1000 ve320×568 kabulü ayrı kayıttadır; fiziksel cihaz ve anatomik uzman kabulü açık. [Ürün incelemesi](upper-limb-nerve-reference-review.md).

**Güncel iş kapsamı:** [352 üst hedef v2](upper-limb-targets-v2.md), [156 alt hedef v4](lower-limb-targets-v4.md) ve yeni [502 önkol–bilek–el hedefi](forearm-hand-targets-v1.md): toplam 1.010 gereksinim. Yeni seed'de 188 hedef için210 pozitif kaynak gözlemi,314 hedefte pozitif bağ yok;22 tekil intrinsik kas hedefi birleşik gruplarla kapatılmadı. Genel envanter762 katalog kaydını bölgesel işe bağlar,3.074 kayıt bu açıdan denetlenmemiştir.13 bölge/208 hücre ve uzman kabulü açık. Bu kaynak envanteri teslimi geometri/runtime değiştirmez; canlı ürün revision'ı e005d53 olarak kalır. [Eylem ve süre raporu](progress-report-2026-10-02.md), [envanter](model-inventory.md) ve [kapsam sözleşmesi](model-scope-and-acceptance.md) güncel takibi taşır.

**Sıradaki ürün işi:** teknik kaynak incelemesi tamamlanan iki sol BP3D4.3 medial/lateral kordunu kaynak kapsamıyla ana atlasa almak, etiket/ilişki ve gerçek masaüstü/mobil/canlı kabulünü kapatmak. Adaylar henüz aktif değildir; sağ kordlar, ayrı kök katkıları ve bütün pleksus devamlılığı kabul edilmedi. Ardından önkol–elde tekil intrinsik kaslar ve bilek destekleri denetlenir. Ders katmanı modelden sonra gelir.

**Ölçüm ve tahmin:**127 referans entegrasyon penceresi15:48:59→19:23:39 TRT,3h34m40s duvar süresi; aktif emek/bekleme dökümü bilinmiyor. Önkol aday üretim/doğrulaması8m09s; ön okuma bilinmiyor, paralel süreler toplanmaz. Önceki düşük güvenli bütün model planı30–40 aktif saat/hafta varsayımıyla hedef açılımı2–4 hafta, öncelikli paketler2–4 ay, bütün bölgelerde güçlü D1/seçilmiş D2 deneyimi6–12 ay. Kesin takvim veya sürekli arka plan çalışma taahhüdü değildir; aralıklar toplanmaz, uzman beklemesi hariçtir. Yaygın D3 için güvenilir tarih yok. Çalışan alt ajan kalmadı; root entegrasyon/kapanış sahibidir. Her anlamlı teslimde mevcut rapor güncellenir, periyodik otomasyon kurulmadı.

## Önceki durum fotoğrafları — 2 Ekim, 19:23 canlı kabulünden önce

Aşağıdaki kayıtlar önceki yerel/ara/yayın fotoğraflarını korur; güncel durum yukarıdadır.

**Yeni ürünün yerel kabulü:** bağımsız üst ekstremite referansı127 parça/127 TR-EN/110 Latin/26 dal ilişkisiyle üretim önizlemesinde kabul edildi.1440×1000,390×844,320×568 akışları ve null Latin gösterimi görüldü; konsol0 hata/uyarı. [Hedef v2](upper-limb-targets-v2.md) 352 gereksinime80 ek kaynak bağı taşır;178 mesh gözlemi,6 ayrı referans noktası,166 pozitif bağı bulunmamış hedef ve2 null humeral konum vardır. Yerel envanter5 dataset/2.587 parça/3.836 katalog/1.674 ilişki;590 sınıflandırılmış,3.246 denetlenmemiş kayıt. Önceki ana model/veri korunur,208 hücre ve uzman kabulü açık. Yayın bu yerel kabulden ayrı doğrulanacaktır. [Ürün incelemesi](upper-limb-nerve-reference-review.md).

**Son ara durum,16:12:42 TRT:**127 nesnelik üst ekstremite sinir referansı,127 TR/EN etiket,110 kaynaklı Latin ad ve26 dal ilişkisi yerel uygulamaya bağlandı; henüz commit edilmiş ürün/yayın değildir. Paket üretici kontrolü geçti; önceki yerel masaüstü/390 akışı görüldü. Hedef v2/genel envanter güncellemesi, son üretim/320 kontrolü ve canlı doğrulama bekler. İki sol BP3D4.3 kordunun geometri ve metadata alt işleri hazır, aktif modele alınmadı. [Kullanıcı durum talebi için güncel eylem/süre raporu](progress-report-2026-10-02.md#güncel-ara-rapor--kullanıcı-durum-talebi-161242-trt). Aşağıdaki geçmiş tahmin ve kaynak teslimi kayıtları bu daha yeni ürün kabulünü ima etmez.

15:13:41 TRT durumundaki canlı ürün: `363ad7ea5558e2338d4bbe478754af1129a40e95` — ana atlas 2.290 parça /401 bölgesel etiket; ayrı kadın pelvis 27, iç kulak 6 ve alt ekstremite 137 nesne. Alt ekstremitede 137 TR/EN, 101 kesin Latin etiket ve 112 ilişki vardır. Statik dal `3c713c7dc89881cb0413f33644b6af41b45eebf2`, [Pages #37005186679](https://github.com/ismailatilan-44/human-atlas/actions/runs/37005186679) başarılı; canlı release.json ve geometri hash'i eşleşti. 390×844 canlı sağ fleksör retinakulum → tibia → Geri/Latin/izolasyon/kaynak akışı doğrulandı; konsol sıfır hata/sıfır uyarı. Yerel masaüstü ve 320 kabulü ayrı kayıttadır. [Eylem/süre raporu](progress-report-2026-10-02.md), [envanter](model-inventory.md) ve [kapsam sözleşmesi](model-scope-and-acceptance.md) güncel takibi verir; eski kayıtlar tarihî kanıttır.

15:13:41 TRT ürün teslimi: dört dataset 3.709 kavram/seçim, 2.460 parça, 1.648 ilişki; [156 önerilen hedef](lower-limb-targets-v4.md) önceki 136 kaydı aynen koruyor; 154 aktif ürün bağı, iki aday intersesamoid hedefi var. 208 kapsam hücresi ve uzman kabulü açık. Referansa 18 destek nesnesi, ana modelde iki mevcut kavram etiketi ve iki datasette 32 seçilmiş tutunma ilişkisi eklendi. İki source-named intersesamoid mesh bağlantı kapsamı nedeniyle aktif üründen dışarıda. Açık yüzey/grup/baş kapsamları ve Latin boşlukları korunur.

16:12 ara durumundaki iş envanteri [352 üst ekstremite gereksinimini](upper-limb-targets-v1.md) de içerir: alt/üst toplam508 hedef, bağsız hedefler dahil, bölge/aile/ayrıntı hücrelerine bağlandı. Bu gereksinim etkinleştirmesi yeni ürün geometrisi, kapsam tamamlanması veya uzman kabulü değildir. 510 katalog kaydı iş kuyruğuna bağlı; 3.199 kayıt bu açıdan denetlenmemiştir. P3'te54 yeni adlandırılmış sinir eğrisi,24 mevcut aynı-kaynak siniri ve49 kemiği içeren127 nesnelik ayrı kaynak referansı kaynak/metadata denetimiyle hazır;127 TR/EN,110 kaynaklı Latin/17 null ve26 seçilmiş dal ilişkisi adaydır. [BP3D4.3 alternatif intake](../../data/model-candidates/upper-limb-bp3d43-intake-v1/REVIEW.md) iki sol kord için gerçek dosya/kimlik sağladı; kapsam/devamlılık/koordinat kabulü bekler. C5–T1 sinir gövdeleri ayrı pleksus kök katkısı diye kabul edilmez. Sıradaki tek ürün eylemi127 nesnelik bağımsız referansın etiket/ilişki ve masaüstü/mobil/yayın kabulüdür; tahmini2–6 aktif teknik saat, düşük güvenle. Bütün model ve sonraki ders katmanı hedefi devam eder.

Envanter/aday kaynak teslimi `decce81c9fe332de11b704b8e32aa11d7db96b85`, fork main/geliştirme dalında uzak sorguyla doğrulandı. Ölçülen bu tur15:16:57 →15:46:22 TRT,29m25s duvar süresi; ilk ön okuma/son kapanış belge push'u hariç. Canlı kaynak363ad7e değişmedi; bu tur yeni ürün/CI/deploy veya uzman kabulü yok. Bütün hedef/kimlik ve source-hash kontrolleri [rapor kapanışında](progress-report-2026-10-02.md#güncel-eylem-raporu--üst-ekstremite-hedefleri-ve-kaynak-seçimi) kayıtlıdır.

## Hedef

**Tarihî destek paketi ölçümü:** destek paketi 14:27:22 →15:13:41 TRT, 46m19s duvar süresi; kaynak/metadata, entegrasyon/yeniden çalışma, raporlama ve yayın beklemesi dahil, ilk ön okuma ölçülmedi. Paralel emek toplamı değildir. Kaba kaynak geometri, bağımsız numaralı grup kimlikleri, tam ağ/destek ayrıntısı, fiziksel cihaz ve anatomik uzman kabulü açık. [Son yayın ve ölçüm kanıtı](progress-report-2026-10-02.md#destek-paketinin-canlı-kabulü-ve-süre-kapanışı).

Tıp öğrencileri için anatomik yapıları seçilebilir, adlandırılmış, ilişkileri izlenebilir ve bölge düzeyinde incelenebilir bir model deneyimi. Human Atlas başlangıç tabanıdır; kullanılabilir parçalar yeniden modellenmez. Eksikler doğrulanmış açık kaynaklardan tamamlanır. Önce model, sonra ders akışının yapı kimliklerine ve kayıtlı sahnelere bağlanması. Ders/quiz/AI model tesliminin ön koşulu değildir.

Omuz–kol ilk entegrasyon örneğiydi; proje bu bölgeyle sınırlı değildir. 65 hedef grubu ilk bölgesel kontrol listesidir, bütün insan anatomisinin eksiksizlik ölçüsü değildir. İlk çalışan yayını vermek, kalan model kapsamını tamamlamakla aynı şey sayılmaz.

## Çalışan yayın ve kaynak kod

- Çalışan adres: https://ismailatilan-44.github.io/human-atlas/
- Kullanıcının fork'u: https://github.com/ismailatilan-44/human-atlas
- Kaynak dalı: `main`; yerel geliştirme dalı: `codex/publish-model-explorer`.
- Statik site `gh-pages` dalından yayımlanır. `npm run deploy:pages` kaynak commit'inden build alır, commit edilmemiş model adaylarını dışarıda bırakır, statik dalı force kullanmadan günceller. `release.json` yayımdaki kaynak commit'ini belirtir.
- İlk canlı sürüm `e8df81f`: 2.248 parça. Gerçek adres üzerinde model yükleme, siyatik seçimi, dört kas bağlantısı ve saydam arka görünüm görüldü.
- Yeni kaynak sürümü `9814150`: 2.252 parça; tiroid ve omurilik dokusu dahil. Kaynak main'e ve statik dal `0b4f4f7`'ye gönderildi. GitHub Pages build/deploy #35668377107 başarılı. Gerçek adreste 2.252 parça, Türkçe omurilik araması/iki parçalı seçim, tiroid üçlü seçim ve saydam ön görünüm doğrulandı; tarayıcı konsolunda hata görülmedi.
- Orijinal ashemag reposu ve orijinal Vercel yayını değiştirilmedi.

GitHub OAuth oturumu workflow dosyası yazma yetkisi vermediği için ilk Actions dosyasıyla push reddedildi. Mevcut repo yetkisiyle desteklenen statik Pages dalına geçildi. Ek yetki istenmedi; reddedilen workflow değişikliği yayın dalının kaynak geçmişine alınmadı. Eski `codex/model-explorer` yerel dalı tarihî çalışma kaydıdır; güncel dal değildir.

- Kadın pelvis sürümü `90e054c`: ana erkek model 2.252 parça olarak korunur, ayrı HRA sahnesi 27 parça içerir. Pages #35669678909 başarılı; gerçek yayın ve arama/seçim doğrulandı.

## Uygulanan model ve etkileşim

- 2.234 temel parça + 56 yeni parça: bilateral muskülokutan/median/siyatik sinirler, sekiz diz yüzeyi, üç tiroid yüzeyi, bir omurilik sinir dokusu yüzeyi 20 kısmi pleksus parçası ve 18 akciğer doku yüzeyi. Altı tutunma referans noktası ayrı gösterilir; bağımsız yüzey gibi sayılmaz.
- Beş beyin parçası, dört kafatası kemiği ve iki subskapularis kasının yanlış sistem ataması yüklemede düzeltilir.
- FMA7647 artık mevcut FJ1737 merkez kanalını ve yeni BP43-FJ4426 uzunlamasına sinir dokusunu birlikte içerir. Kök, zar, ayrı segment ve gri/beyaz madde modelleri tamamlandı diye sunulmaz. Kavram genişletmesi manifestte açıkça izinlidir; izinsiz kimlik çakışmaları reddedilir.
- Tiroid FMA9603: sağ/sol lob ve isthmus, resmî BodyParts3D 4.3 kaynağından. Stilize Z-Anatomy tiroidi görsel incelemede yetersiz bulundu ve aktif kayda alınmadı.
- Grafik: 3.514 kavram, 1.524 ilişki; çoğunluğu kaynak PART-OF hiyerarşisidir. Bütün atlasın işlevsel bağlantıları tamamlandı anlamına gelmez. Siyatik bağlantılarında tibial/common-fibular bölüm ayrımı arayüzde korunur.
- Seçme, odak, çevre saydamlığı, gizleme, önceki görünüm/kamera, sistem filtresi, bölge seçimi ve kapsam paneli çalışır. Çok dilli etiketler seçilmiş bölgelere uygulanır; bütün atlas çevirisi tamamlanmış değildir.
- Katalog: 61 mevcut, 3 kısmi, 0 eksik, 1 doğrulanmamış hedef grubu; mevcutların 3’ü ayrı kadın pelvis, 1’i ayrı iç kulak referansındadır. Üç mevcut satır toplam altı yüzey referans noktasıdır. Güncel makine kaydı `data/anatomy/coverage.json`.

## Doğrulama ve sınırlar

TypeScript, beş kaynak grafiği testi, temel atlas buffer kontrolü ve etkileşim/yerleşim doğrulayıcısı geçti. Etkileşim doğrulayıcısı artık tüm kayıtlı extension'ları yükler; mevcut geometriyi koruyan kavram genişletmesini ve izinsiz tekrarın reddini kontrol eder. Yeni exporter'lar kaynak hash'lerini ve binary/geometri koşullarını kontrol eder.

Masaüstü, 390×844 ve 320×568 örnek akışları incelendi. Son `/human-atlas/` üretim önizlemesinde siyatik arama/seçimi, kas bağlantısına geçiş, katman preset'inin eski paneli temizlemesi, mobil ön çapraz bağ, tiroid üçlü seçimi ve omurilik iki parçalı seçimi/yan görünümü görüldü. Bunlar fiziksel telefon performansı veya klinik anatomik onay değildir. Büyük JS paket uyarısı ve gerçek cihaz performansı açık kalite konularıdır.

BodyParts3D 4.0 temel geometri BY 4.0; yeni canlı 4.3 tiroid/omurilik BY-SA 2.1 Japan; Z-Anatomy parçaları kendi atıf/köken kayıtlarıyla ayrıdır. Tek lisans altında hepsi temizlendi varsayımı yapılmaz. Kaynak yüzey kusurları ve kapsam sınırları ilgili kayıt raporlarında korunur.

## Kalan teslim sırası

| İş | Bitiş ölçütü | Güncel durum |
| --- | --- | --- |
| Çalışan ilk yayını vermek | Gerçek adreste model ve temel inceleme akışları çalışır | 2.290 parçalı sürüm canlı; akciğer dokusu, pleksus, ayrı kadın pelvis ve iç kulak akışları gerçek adreste doğrulandı |
| Brakiyal pleksus | Kaynak parçalar doğru ad/kapsamla, ölçülmüş yerleşim ve tıklanabilir seçimle görünür | 20 trunk/division/posterior-cord parçası kayıtlı; 23 üç dilli kavram ve 22 kaynak grup ilişkisi. Kökler/iki kordon yok; boyun4–5mm/ilk kaburga8mm uyum sınırı arayüzde belirtilir. Yerel ve canlı görsel kabul yapıldı; becb591 sürümünde yayında |
| Kadın pelvis referansı | Erkek modele karışmayan ayrı sahne; uterus ve sağ/sol ovaryum kendi kaynaklarıyla, uygun pelvis bağlamında | Resmî HRA kaynaklarından 27 parça / 31 kavram içeren ayrı paket ve sahne seçici yerelde hazır; veri ayrımı ve TypeScript kontrolü geçti. Masaüstü ve 390×844 arayüzde kadraj, seçim/saydamlık, iki referans arasında temiz geçiş ve TR/LA etiketler doğrulandı; 90e054c sürümünde canlı; gerçek yayında geometri, Türkçe arama ve seçim doğrulandı |
| Koklea | İki gerçek yüzey, kaynak/atıf ve temporal bölge uyumu doğrulanır | Ana atlasa farklı kafatası uyumu uygulanmadı. Kaynağın kendi temporal kemikleriyle 6 parçalı ayrı referans hazır; tek uniform eksen dönüşümüyle konum ilişkileri korunur. Koklea seçimi ve Türkçe arama yerelde ve canlı yayında doğrulandı. NC-SA bileşen koşulu ve köken çıkarımı açık |
| İki humeral tutunma konumu | Kanıtlı konum veya açık unresolved durumu; kemik bütünü landmark diye sunulmaz | 158 ilgili Z-Anatomy nesnesi incelendi; kemikle eşleştirilmiş gerçek footprint/işaret yok. Tendon yüzeyleri ayrı aday olarak saklandı; iki konum null, uydurma koordinat yok |
| Etiket/ilişki kapsamı | Bölge bölge kaynaklı isimler ve ilişkiler; kullanıcı parça üzerinden bağlantılarına gider | Pilot, önkol, diz, siyatik, tiroid, omurilik ve rotator manşette seçilmiş bağlantılar var. 65 hedefin 83 doğrudan bağında TR/EN boşluğu kapandı; dört LA boşluğu bilinçli. Alt parça/diğer ilişki uçlarında genişleme açık |
| Kullanım kalitesi | Gerçek kullanıcı akışları, son masaüstü/mobil kabul; somut performans sorunları çözülür | Örnek akışlar geçti; yeni referanslar eklendikçe ilgili akışlar kontrol edilecek |
| Ders katmanı | Ders sırası modelin yapı kimlikleri/kayıtlı görünümüne bağlanır | Modelden sonraki aşama; henüz uygulanmadı |

Araştırma yalnız açık uygulama boşluğunu çözmek için yapılır. İndirilen veya teknik olarak geçerli bir dosya, kabul edilmiş kullanıcı deneyimi sayılmaz. Başarısız kaynakta alternatif aranır; modelin yetersizliğini örtmek için geometri/etiket uydurulmaz.

## Kullanıcıdan gerekenler

Şu an zorunlu teknik kullanıcı işi yok. Repo, indirme, kaynak araştırma, eşleştirme, model aktarımı, kod, Git ve yayın asistanın yetkili kapsamındadır. Blender kurulu; Blender MCP aktarımın ön koşulu değildir.

Çalışan yayın üzerindeki kullanım geri bildirimi yararlıdır. İleride ders sırası ve anatomi alan uzmanı değerlendirmesi eğitim değerini artırır; bunları beklemek mevcut teknik teslimi durdurmaz. Uzman incelemesi yapılmadan yapılmış gibi gösterilmez.

## Planlama düzeltmesi

İlk araştırma/veri hazırlığı aşaması çalışan arayüze geçişi geciktirdi. Bu, kullanıcı girdisi beklenmesinden kaynaklanmadı. İlerleme ölçütü artık araştırma/asset sayısı yerine kaynaklı, görüntülenmiş ve kullanılabilir akışlardır. Kalan işlerin varlığı ilk çalışan sürümün teslimini bekletmez; ilk yayın da kalan hedeflerin tamamlandığı iddiası değildir.

## Kadın pelvis sürümü için kabul — 22 Eylül 2026

27 yüzeyli ayrı HRA referansı, erkek sahnesine karışmadan yükleniyor. 31 kaynak kavramı aramada 29 ayrı geometri seçeneği olarak gösteriliyor; iki ovaryum aliası tekilleştirildi. TR/EN/LA görüntü etiketleri kaynak kimliklerini değiştirmiyor. Gerçek arayüzde kadın↔erkek geçişi, kamera/geçmiş temizliği, uterus seçimi/saydamlığı, mobil ovaryum seçimi, Türkçe arama ve Latince ad değişimi görüldü. Kapsam listesinden kadın sahnesine geçiş çalıştı. Üretim alt yolunda geometri yüklendi, tarayıcı hata kaydı boş. TypeScript, güncellenmiş veri ayrımı/etkileşim kontrolü, beş graph testi ve build geçti. Kaynak 90e054c ve statik dal f2da0d4 yayımlandı. Pages #35669678909 başarılı; canlı release.json 90e054cd7e24e3ead3abc6783eb7a72cf84feb66 döndü. Gerçek adreste pelvis geometrisi, iki Türkçe ovaryum sonucu ve sol ovaryum seçimi doğrulandı; konsol hatası yok.

## Pleksus ve iç kulak kabulü — 22 Eylül 2026

Ana atlas yayında 2.272 parça. İç kulak ayrı 6 parça; kadın pelvis ayrı 27 parça. Kaynak model çerçeveleri karıştırılmaz. Kayıtlı pleksus, kök ve iki kordon eksikleriyle kısmi kabul edilir; temas/cerrahi hassasiyet iddiası yok. İç kulakta başlangıçta dört duyusal yüzey ve saydam temporal kemikler görünür. Koklea yüzeyinden doğrudan seçim, Türkçe arama, yakın görünüm ve referans değiştirme kontrol edildi. Bölgesel sahnelerin zemininin her karede yanlışlıkla geri açılması düzeltildi.

Canlı kaynak `becb591ad9919cb4fa4d11a01f29cb73e47a06a8`; 22 Eylül durum kontrolünde release.json aynı sürümü döndürdü. Önceki yayın kabulünde ana atlas 2.272 parça, sol pleksus 10 parça/11 ilişki görüldü. Bu durum turunda canlı iç kulakta iki Türkçe koklea sonucu, sol koklea seçimi, kaynak kapsam açıklaması ve saydam temporal kemik bağlamı tekrar doğrulandı; konsol hata kaydı boş. Etiket denetimi adayı hazırlanıyor; henüz uygulamaya alınmış sayılmıyor.

## Etiket, kafatası ve rotator manşet kabulü — 22 Eylül

Yeni paket `87e9280` sürümünde canlı. Etiket dosyası 72 kayıttan 155 kayda çıktı: 45 kapsam-hedef etiketi, 21 tekil kafatası kemiği, bir 22-kemiklik grup ve 16 rotator manşet kas/sinir etiketi. 65 hedefin 83 doğrudan bağında çalışma zamanı denetimi TR 0/EN 0/LA 4 fallback gösterdi. Bu sayılar bütün atlas çevirisi değildir; dört Latin boşluğu iki kaynak zone ve iki proje tutunma bölgesidir.

Kaynak FMA46565, 43 yüzeyle aynen korunur; göz/hyoid içeren kapsamı açıklanır. Yeni atlas:skull-bones seçimi mevcut 22 kemik yüzeyini gösterir; coverage:skull buraya yönelir. Ham geometri değişmedi. Dört yanlış kemik sınıfı resmi IS-A tablosuyla düzeltildi. 22 kemikte TR/EN/LA etiket ve üyelik bağlantıları var.

Rotator manşetin iki taraflı dört kasına 26 başlangıç/tutunma/innervasyon ilişkisi eklendi. 16 kemik ilişkisi adlandırılmış bölge notuyla görüntülenir; kesin yüzey/koordinat iddiası yok. Sekiz sinir kavramının geometrisi henüz yok; model kaynağı bağlantısı gösterilmez, geometri kontrolleri devre dışı kalır. İki subskapularis yüzeyinin skeletal→muscular hatası resmi IS-A intrinsic-muscle-of-shoulder zinciriyle düzeltildi.

Kabul: ASCII karaciger→Karaciğer→Hepar aramasında 60 parça; 22 kemikli izole kafatası ve 22 adlandırılmış üye; sol supraspinatus için üç ilişki ve geometrisiz supraskapular sinire geçiş. 390×844 mobil görünümde subskapularis için dört ilişki, uzun bölge notunun satır kaydırması, iki ayrı sinir ve boş geometri durumu görüldü; konsol hatası yok. TypeScript, mevcut beş graph testi, genişletilmiş etkileşim kontrolü ve üretim derlemesi geçti. JS 326.63 KB gzip; büyük bundle uyarısı sürüyor.

Yayın kabulü: kaynak `87e9280e5274b416eec58d82193c383e0a8f2fa1`, statik dal `a04aa6c02863b644e5026559ecdfb9573be18625`. Pages #35672193897 başarılı; canlı release.json kaynak sürümüyle eşleşti. Gerçek adreste `kafatasi` araması 43 parçalık kaynak grubunu ve 22 kemiklik seçimi ayrı gösterdi; 22 kemiklik izole geometri ve Türkçe üyeler görüldü. Sol subskapularis kas olarak sınıflanıyor; dört kaynaklı bağlantı, tutunma bölgesi notu ve saydam çevre görünümü doğrulandı. Konsol hata kaydı boş.

Sonraki somut paket: temel modelin resmi IS-A sınıflarıyla kemik/kas katman denetimi ve toraks/abdomen hedeflerinden tek ilişki adımıyla erişilen organ alt yapılarının etiketleri. Bunlar hazırlanan aday çalışmalardır; mevcut yayında tamamlandı sayılmaz.

## Güncel durum ayrımı — 22 Eylül, kullanıcıya durum açıklaması

Canlı `release.json` yeniden kontrol edildi: `87e9280e5274b416eec58d82193c383e0a8f2fa1`. Aşağıdaki yeni işler bu yayına henüz dahil değildir:

- Yerelde 23 organ-komşusu etiketi eklendi; aktif etiket dosyası 178 kayda çıktı. Temsil sınırı gereken kayıtlarda açıklama gösterimi eklendi.
- Resmî kas sınıfı kanıtıyla 26 parçanın birincil görüntüleme katmanı kas olarak düzeltildi. Bunların 12'si farenks kasıdır; solunum bölgesiyle kaynak ilişkileri korunur. Bu, ham kaynak hiyerarşisini değiştiren bir karar değildir.
- 26 kas etiketi ve 23 ek organ-komşusu etiketi aday paketlerde hazır; aktif dosyaya entegrasyon ve son görsel kabul bekler. İkinci paketin Latince karşılıkları henüz doğrulanmış görüntü etiketleri değildir.
- BodyParts3D 4.3 eşlemesinde 18 pulmoner segment parankimi adayı bulundu. Geometri ve koordinat incelemesi sürüyor; tam akciğer/lob yüzeyi kabulü yapılmadı.

Sıradaki teslim önce etiket/sınıflandırma paketinin kontrol edilip yayımlanması, ardından doğrulanabilen organ yüzeyi eksiklerinin tamamlanmasıdır. Sonra bölgesel sinir/ilişki ayrıntıları ve kullanım kalitesi genişletilir. Ders katmanı daha sonra mevcut yapı kimlikleri ve kayıtlı görünümler üzerine kurulur.

Her bölgesel paket için kabul ölçütü: gerçekten bulunan yüzeyler ve eksikler açık; yapı adı/tarafı doğru; kaynak ve dönüşüm izlenebilir; seçme/odak/saydamlık ve mevcut ilişkiler çalışır; ilgili masaüstü/mobil akış görülür; yayımlanan sürüm doğrulanır. 65 hedeflik liste tüm tıp müfredatının bitiş ölçütü değildir. Tam müfredat kapsamı ayrıca yapılandırılmalıdır; uzman incelemesi ve gerçek cihaz performansı henüz kapanmış değildir.


## Akciğer dokusu, etiket ve katman paketi — yerel kabul, 22 Eylül

Yeni paket ana modele 18 BodyParts3D 4.3 segment dokusu yüzeyi ekler: toplam 2.290 parça (2.234 temel  + 56 ek). Ayrı kadın 27 / iç kulak 6 sahneleri değişmez. Geometri kaydı 41 kavram içerir; 24 mevcut akciğer/lob/segment kavramı eski üyeleri korunarak genişler. Sağ akciğer 165, sol 133 parça. Binary 3.463.404 byte / gzip 1.878.677 byte; dokuz bağımsız aynı-kimlikli toraks referansında uyarlama yapılmadan RMS 0,0043–0,0813 mm. Bu ölçüm anatomist onayı değildir. Üç dar kaynak aggregate çelişkisi kullanılmadı; FJ6598 kaynak topoloji/normal kusuru kayıtta korunur. [Kaynak raporu](../../data/model-candidates/lung-surfaces/REVIEW.md).

17 gerçek parankim→segment bağlantısı ve iki proje doku-seçim grubu/ilişkisi eklendi. Resmî 4.3 / FMA3.0 kaynak sorguları sürüm kimlikleriyle sabitlendi; mevcut 22 segment/lob/akciğer kenarı tekrar kullanılmaktadır. Grafik 3.514 kavram / 1.524 ilişki / 168 asset bağı. Doku grupları 9'ar yüzeyi birlikte seçip gizlemeye yarar. Tam parankim segmentasyonu veya tüm atlas ilişkilerinin bittiği iddia edilmez.

Etiket 155 → 271 kayıt:46 organ komşusu, 26 kas, 8 hepatovenöz segment, 17 parankim, 17 bronkopulmoner segment ve 2 doku grubu. 26 kas ile 9karaciğer dokusu parçasının katmanı düzeltildi. 12 geniş kaynak grubunun nitelemesi Latin modunda da korunur. Toraks/abdomen ilişkilerinden ulaşılan 48 komşuda TR/EN eksiği 0, Latin eksiği 25; bu bütün atlas çevirisi değildir.

Yerel görsel kabul: sağ 165 parçalı akciğer yüzeyi, sol 9 parçalı doku grubu, dokuyu gizledikten sonra 37 parçalı sol pulmoner arteri saydam çevrede inceleme; parankim 2 → segment 19 → lob 73 → akciğer 133 gerçek düğme akışı. Mobil 390×844 Türkçe arama iki ayrı segment/parankim sonucunu verdi, Latince segment başlığı ve geometri görüldü. Kas ve karaciğer katmanları ile kaynak-grubu dil değişimi de kontrol edildi. TypeScript, mevcut 5 grafik testi ve etkileşim doğrulayıcısı geçti; tarayıcı hata kaydı boş. Üretim derlemesi/yayın kabulü ayrıca kaydedilecek.

Açık yeni bulgu: eski sağ akciğer grubu içinde FJ2041/FJ2044 yüzeyleri akciğerin altında kalıyor. Mevcut kaynak üyeliği sessizce değiştirilmedi; sağ akciğer/üst lob/anterior segment seçiminde açıklama var. Eşleşmeleri ayrı aday çalışmada inceleniyor. Sonraki somut iş bu kaynak uyuşmazlığını çözmek ve ilgili damar/bronş alt adlarını genişletmek; daha geniş model kapsamı, gerçek cihaz ve uzman inceleme işleri açık kalır.

Yayın kabulü: kaynak `0a9414e5ea25f22280c2b2169e4c2a7a4a381c4f`, statik dal `363aa7a548009636e1f19a21c455573ede25f0a9`; Pages #35674866577 başarılı. Canlı release.json aynı kaynak SHA döndürdü. Gerçek adreste 2.290 parça yüklendi; ASCII `sol akciger dokusu` araması dokuz yüzeyli grubu buldu, izolasyonda geometri ve Türkçe açıklama görüldü. Konsol hata kaydı boş. Üretim JS 332,93 KB gzip; büyük paket uyarısı ve fiziksel cihaz/uzman inceleme sınırları sürüyor.

## Pulmoner kaynak üyeliği düzeltmesi — 22 Eylül, yerel kabul

FJ2041/FJ2044 kaynak4.0 kimlik/konum uyuşmazlığı doğrulandı; importer dönüşüm hatası desteklenmiyor.19 açık pulmoner/toraks seçimi bu iki yüzeyi dışarıda bırakıyor. Sağ akciğer163 ve sağ anterior segmental arter7 yüzey; ham kaynak seçimi165/9 yüzey olarak düğmeyle erişilebilir. Ham manifest/grafik/geometri değiştirilmez. İki yüzey doğrudan seçildiğinde kimliği doğrulanmamış damar olarak gösterilir, kaynak FMA8620 metadata içinde korunur.4.3'ün örtüşen yedi yüzeyi tekrar eklenmedi. Ana model2290 parça.

Mevcut etkileşim kontrolüne yalnız bu değişikliğin kaynak verisini koruması, extension sonrası163/165 üyeliği ve tekrar hazırlamada değişmemesi eklendi. TypeScript ve etkileşim kontrolü geçti. Gerçek arayüzde7/9 damar karşılaştırması,163/165 akciğer geçişi, belirsiz tek parçanın başlığı ve390×844 mobil geometri görüldü. Karşılaştırma düğmesi izolasyonu korur. Tarayıcı hata kaydı boş. Yayın doğrulaması ayrıca kaydedilecek.

Pulmoner seçim düzeltmesi kaynak `b1a7090feecf64c8dabdfd6526f6430fb12d3846`, statik `5f19aea5b59abbea364f23c373b3aa8dc33c7105` ile yayımlandı. Pages35675956943 başarılı; canlı release.json aynı kaynak sürümünü döndürdü.

Ek etiket paketi: FMA8620, FMA68677, FMA68683 ve FMA68201 için dört TR/EN kaydı eklendi; toplam 275. İki TA2 Latin terimi doğrulandı; iki ayrıntılı dalda Latin alanı boş. Kaynak FMA8620 Latin ifadesiyle TA2 adlandırmasının farkı kanıtta korunur. ASCII arama, Türkçe ana damardan posterior dala gerçek düğme geçişi, üç yüzeyin izolasyonu ve 390×844 uzun başlık görüldü; FMA8620 Latin başlığı doğrulandı. TypeScript geçti; tarayıcı hata kaydı boş. Kaynak `caa938a4745a570fad13e445dda6c34909cdf4e5`, statik `21a902f675be0d281883a5ac1e9be21c938eeb1c`; Pages #36210534954 başarılı, canlı release.json kaynak sürümüyle eşleşti. Gerçek yayında ASCII `sag on segment` iki ayrı 7/9 yüzeyli sonucu buldu, Türkçe başlık/alt dal bağlantısı göründü; tarayıcı hata kaydı boş.
