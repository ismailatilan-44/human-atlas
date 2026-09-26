# Model ürünü ilerleme raporu — 26 Eylül 2026

Bu rapor, tıp öğrencisi için model odaklı atlas hedefinin bugünkü durumunu gösterir. Kod, canlı yayın ve henüz incelenmemiş anatomik kapsam ayrı değerlendirilir. [Kapsam ve kabul planı](model-scope-and-acceptance.md) hedefin ayrıntısını taşır.

## Doğrulanmış durum

| Alan | Bugünkü kanıt | Açık sınır |
| --- | --- | --- |
| Canlı ürün | [Yayın](https://ismailatilan-44.github.io/human-atlas/) `release.json` kaynak `caa938a4745a570fad13e445dda6c34909cdf4e5` döndürüyor; Pages çalışması `36210534954` başarılı | Canlı ürünün açılması tüm anatomik kapsamın kabulü değildir |
| Geometri | Ana sahne 2.234 temel + 56 ek = 2.290 yüzey; kadın pelvis ayrı 27, iç kulak ayrı 6 | Yüzey sayısı bağımsız organ veya müfredat kapsamı sayısı değildir |
| Adlandırma ve bağlantı | 275 aktif etiket kaydı; bilgi grafiği 3.514 kavram / 1.524 ilişki | Etiketler seçilmiş bölgelerde yoğunlaşır; ilişkilerin çoğu kaynak PART-OF hiyerarşisidir |
| İlk kontrol listesi | 65 hedef grubundan 61 mevcut, 3 kısmi, 1 doğrulanmamış | 65 satır bütün insan anatomisi veya tamamlanma yüzdesi değildir |

22 Eylül'den bu rapora kadar tamamlanan işler: akciğer/toraks kaynak üyeliğinde böbrek seviyesine düşen FJ2041/FJ2044 yüzeyleri 19 incelenmiş seçimden çıkarıldı. Ham kaynak üyeliği ayrıca erişilebilir; sağ akciğer incelenmiş 163 / ham 165, sağ anterior segmental arter incelenmiş 7 / ham 9 parçadır. İki yüzeyin kesin damar kimliği hâlâ belirsizdir. Dört pulmoner dal etiketi Türkçe/İngilizce eklendi; ikisinde kaynaklı Latince ad var, iki alt dalda Latince alan boş bırakıldı. Bu sürüm yerel TypeScript ve etkileşim kontrolünden, masaüstü/mobil görsel incelemeden ve canlı arama/seçim doğrulamasından geçti. Canlı tarayıcı hata kaydı boştu.

## Şu anda yapılan iş ve sıradaki teslim

P0 kaynak üyeliği düzeltmesi ve damar etiketleri yayındadır. Bir sonraki iş **P1 kaynak kimlikli hedef envanteri**: [kapsam planındaki](model-scope-and-acceptance.md) 13 bölgeyi yapı ailesi ve gereken ayrıntı düzeyine açmak; mevcut, kısmi, aday ve henüz denetlenmemiş yapıları birbirinden ayırmak. Belge düzeyindeki matris hazırdır; yapı kimliklerini tek tek içeren sürümlü makine envanteri henüz üretilmedi. P1'in ilk teslimi, envanterin temel atlas ve kayıtlı uzantılarla uzlaştırılmış dosyası ve bölge bazında açık hedef listesidir. Sonraki somut model paketleri distal sinir devamları ve üst ekstremite ağ/ilişki ayrıntılarıdır; kaynak kimliği ve yerleşimi doğrulanabilen parçalar sırayla ürüne girer.

23–25 Eylül arasında bu görevde doğrulanmış yeni commit veya dağıtım yoktur. Çalışma aktif görev turlarında yürür; sürekli çalışan bir geliştirme süreci veya periyodik ilerleme otomasyonu kurulmuş değildir. Bu nedenle aşağıdaki takvim, kesintisiz emek varsayımıdır; uygulamanın kendiliğinden arka planda tamamlanacağı vaadi değildir.

## Süre tahmini

| Teslim düzeyi | Kaba süre | Bitişin neyi kanıtlayacağı |
| --- | --- | --- |
| P1 sürümlü kapsam envanteri | **2–4 hafta** | Bütün bölge/ailelerin kaynak kimlikli hedef ve açık durum listesi; bu bir model tamamlama tarihi değildir |
| Öncelikli bölgesel model paketleri | **2–4 ay** | Sinir devamları, seçilmiş eklem/organ alt yapıları, etiket ve ilişkilerin çalışan ürüne paket paket girmesi |
| Bütün bölgelerde güçlü D1 ve öncelikli D2 model deneyimi | **6–12 ay** | Ana organ/kemik/kas/damar/sinirlerin seçilebilirliği ve belirlenen önemli alt yapıların bölge kabulü; kapsam sürümü P1'de netleşir |
| Yaygın D2, ince D3 ve uzman anatomik kabulü | **Şimdi güvenilir tek tarih verilemez** | Kaynak ayrıntısı, farklı ölçekli modeller, lisans/köken çözümü ve anatomi uzmanı kapasitesi belirleyicidir |

Aralıklar yaklaşık **haftada 30–40 saat teknik çalışma**, mevcut açık kaynakların erişilebilirliği ve paketlerin birer birer doğrulanması varsayımına dayanır; uzman incelemesinin süresini kapsamaz. P1 gerçek hedef sayısını ve kaynak boşluklarını gösterince tahmin yeniden hesaplanmalıdır. Son iki satır için tek bir “% tamamlandı” değeri üretmiyorum: bugünkü 65 hedef bu payda olamaz.

## Raporlama düzeni

Her teslim raporunda kaynak commit'i ve canlı yayın sürümü, eklenen/doğrulanan yapılar, kabul için görülen gerçek kullanım akışı, hâlâ açık kimlik/konumlar ve bir sonraki paket kaydedilir. İlerleme, araştırılan dosya sayısıyla değil öğrencinin gerçekten seçip inceleyebildiği kaynaklı yapılarla ölçülür. Süre tahmini P1 sonrası ve kapsamı değiştiren her önemli kaynak bulgusundan sonra güncellenir.
