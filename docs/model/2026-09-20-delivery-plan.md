# Model odaklı ürün — teslim planı ve güncel durum

İlk plan: 20 Eylül 2026. Güncelleme: 22 Eylül 2026. Kod, kaynak paketi, görsel kabul ve yayın birbirinden ayrı izlenir.

## Hedef

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

- 2.234 temel parça + 38 yeni parça: bilateral muskülokutan/median/siyatik sinirler, sekiz diz yüzeyi, üç tiroid yüzeyi, bir omurilik sinir dokusu yüzeyi ve 20 kısmi pleksus parçası. Altı tutunma referans noktası ayrı gösterilir; bağımsız yüzey gibi sayılmaz.
- Beş yanlış beyin parçası sistem ataması yüklemede düzeltilir.
- FMA7647 artık mevcut FJ1737 merkez kanalını ve yeni BP43-FJ4426 uzunlamasına sinir dokusunu birlikte içerir. Kök, zar, ayrı segment ve gri/beyaz madde modelleri tamamlandı diye sunulmaz. Kavram genişletmesi manifestte açıkça izinlidir; izinsiz kimlik çakışmaları reddedilir.
- Tiroid FMA9603: sağ/sol lob ve isthmus, resmî BodyParts3D 4.3 kaynağından. Stilize Z-Anatomy tiroidi görsel incelemede yetersiz bulundu ve aktif kayda alınmadı.
- Grafik: 3.486 kavram, 1.457 ilişki; çoğunluğu kaynak PART-OF hiyerarşisidir. Bütün atlasın işlevsel bağlantıları tamamlandı anlamına gelmez. Siyatik bağlantılarında tibial/common-fibular bölüm ayrımı arayüzde korunur.
- Seçme, odak, çevre saydamlığı, gizleme, önceki görünüm/kamera, sistem filtresi, bölge seçimi ve kapsam paneli çalışır. Çok dilli etiketler seçilmiş bölgelere uygulanır; bütün atlas çevirisi tamamlanmış değildir.
- Katalog: 61 mevcut, 3 kısmi, 0 eksik, 1 doğrulanmamış hedef grubu; mevcutların 3’ü ayrı kadın pelvis, 1’i ayrı iç kulak referansındadır. Üç mevcut satır toplam altı yüzey referans noktasıdır. Güncel makine kaydı `data/anatomy/coverage.json`.

## Doğrulama ve sınırlar

TypeScript, beş kaynak grafiği testi, temel atlas buffer kontrolü ve etkileşim/yerleşim doğrulayıcısı geçti. Etkileşim doğrulayıcısı artık tüm kayıtlı extension'ları yükler; mevcut geometriyi koruyan kavram genişletmesini ve izinsiz tekrarın reddini kontrol eder. Yeni exporter'lar kaynak hash'lerini ve binary/geometri koşullarını kontrol eder.

Masaüstü, 390×844 ve 320×568 örnek akışları incelendi. Son `/human-atlas/` üretim önizlemesinde siyatik arama/seçimi, kas bağlantısına geçiş, katman preset'inin eski paneli temizlemesi, mobil ön çapraz bağ, tiroid üçlü seçimi ve omurilik iki parçalı seçimi/yan görünümü görüldü. Bunlar fiziksel telefon performansı veya klinik anatomik onay değildir. Büyük JS paket uyarısı ve gerçek cihaz performansı açık kalite konularıdır.

BodyParts3D 4.0 temel geometri BY 4.0; yeni canlı 4.3 tiroid/omurilik BY-SA 2.1 Japan; Z-Anatomy parçaları kendi atıf/köken kayıtlarıyla ayrıdır. Tek lisans altında hepsi temizlendi varsayımı yapılmaz. Kaynak yüzey kusurları ve kapsam sınırları ilgili kayıt raporlarında korunur.

## Kalan teslim sırası

| İş | Bitiş ölçütü | Güncel durum |
| --- | --- | --- |
| Çalışan ilk yayını vermek | Gerçek adreste model ve temel inceleme akışları çalışır | 2.252 parçalı sürüm canlı; son omurilik/tiroid akışları gerçek adreste doğrulandı |
| Brakiyal pleksus | Kaynak parçalar doğru ad/kapsamla, ölçülmüş yerleşim ve tıklanabilir seçimle görünür | 20 trunk/division/posterior-cord parçası kayıtlı; 23 üç dilli kavram ve 22 kaynak grup ilişkisi. Kökler/iki kordon yok; boyun4–5mm/ilk kaburga8mm uyum sınırı arayüzde belirtilir. Yerel görsel kabul yapıldı, yeni yayın sırada |
| Kadın pelvis referansı | Erkek modele karışmayan ayrı sahne; uterus ve sağ/sol ovaryum kendi kaynaklarıyla, uygun pelvis bağlamında | Resmî HRA kaynaklarından 27 parça / 31 kavram içeren ayrı paket ve sahne seçici yerelde hazır; veri ayrımı ve TypeScript kontrolü geçti. Masaüstü ve 390×844 arayüzde kadraj, seçim/saydamlık, iki referans arasında temiz geçiş ve TR/LA etiketler doğrulandı; 90e054c sürümünde canlı; gerçek yayında geometri, Türkçe arama ve seçim doğrulandı |
| Koklea | İki gerçek yüzey, kaynak/atıf ve temporal bölge uyumu doğrulanır | Ana atlasa farklı kafatası uyumu uygulanmadı. Kaynağın kendi temporal kemikleriyle 6 parçalı ayrı referans hazır; tek uniform eksen dönüşümüyle konum ilişkileri korunur. Koklea seçimi ve arama yerelde doğrulandı, yayın sırada. NC-SA bileşen koşulu ve köken çıkarımı açık |
| İki humeral tutunma konumu | Kanıtlı konum veya açık unresolved durumu; kemik bütünü landmark diye sunulmaz | 158 ilgili Z-Anatomy nesnesi incelendi; kemikle eşleştirilmiş gerçek footprint/işaret yok. Tendon yüzeyleri ayrı aday olarak saklandı; iki konum null, uydurma koordinat yok |
| Etiket/ilişki kapsamı | Bölge bölge kaynaklı isimler ve ilişkiler; kullanıcı parça üzerinden bağlantılarına gider | Pilot, önkol, diz, siyatik, tiroid ve omurilikte seçilmiş bağlantılar var; daha geniş kapsam açık |
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

Ana atlas yerelde 2.272 parça. İç kulak ayrı 6 parça; kadın pelvis ayrı 27 parça. Kaynak model çerçeveleri karıştırılmaz. Kayıtlı pleksus, kök ve iki kordon eksikleriyle kısmi kabul edilir; temas/cerrahi hassasiyet iddiası yok. İç kulakta başlangıçta dört duyusal yüzey ve saydam temporal kemikler görünür. Koklea yüzeyinden doğrudan seçim, Türkçe arama, yakın görünüm ve referans değiştirme kontrol edildi. Bölgesel sahnelerin zemininin her karede yanlışlıkla geri açılması düzeltildi.
