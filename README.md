# Human Atlas

**İnsan anatomisini üç boyutta keşfetmek, yapılar arasındaki ilişkileri izlemek ve öğrendiklerini tekrar etmek için açık kaynak bir çalışma alanı.**

Human Atlas, tıp ve sağlık bilimleri öğrencilerinin anatomik yapıları adları, konumları ve çevreleriyle birlikte incelemesi için geliştiriliyor. Tarayıcıda bir yapıyı bulabilir, çevresinden ayırarak inceleyebilir, kaynaklı ilişkilerini takip edebilir ve kaldığın görünümü daha sonra yeniden açabilirsin.

**[Atlası aç](https://ismailatilan-44.github.io/human-atlas/)** · [Kapsam ve yol haritası](docs/model/model-scope-and-acceptance.md) · [Geliştirme rehberi](docs/model/agent-workflow.md)

## Vizyonumuz

Anatomi çalışırken bir yapının adını öğrenmek, onun vücuttaki yerini ve diğer yapılarla ilişkisini anlamakla birlikte ilerlemeli. Human Atlas ile bütün vücuttan bölgelere, bölgelerden tekil yapılara ve zamanla daha ince ayrıntılara geçilebilen bir öğrenme ortamı kurmayı hedefliyoruz.

Bu vizyonun merkezinde model üzerinde çalışmak var: bir sinirin seyrini izlemek, bir kemiği komşularıyla birlikte görmek, bir organın parçaları arasında gezinmek ve aynı yapıya farklı açılardan yeniden bakmak. Türkçe, İngilizce ve Latince adları kaynak kimlikleriyle bir arada sunarak öğrencinin model ile kullandığı ders kaynakları arasında bağlantı kurmasını istiyoruz.

Ürünü bölge bölge genişletiyoruz. Her yeni pakette yapının kaynağı, temsil ettiği ayrıntı ve henüz karşılanmayan hedefler izlenebilir kalıyor. Öğrenci ve anatomist değerlendirmeleriyle hem model kapsamını hem çalışma deneyimini geliştirmek, yol haritamızın bir parçası.

## Bugün neler yapabilirsin?

- **Bul ve keşfet.** Anatomik adlarla veya kaynak kimlikleriyle ara; modeli döndür, yakınlaştır ve bir yapıyı doğrudan seç. Desteklenen bölgesel kayıtlarda Türkçe, İngilizce ve kaynakla doğrulanmış Latince adları kullan.
- **Bağlamı incele.** Seçime odaklan, çevredeki yapıları saydamlaştır veya gizle. Mevcut kaynaklı ilişkiler üzerinden başka bir yapıya geç ve geri dön.
- **Parçaları ayrı gör.** Görünür parçaları baktığın açıdan ayrılmış bir düzende incele. Kafatası çalışma alanında 22 kemiği seç, hazır yönleri kullan veya seçili kemiği ayırıp yerine döndür.
- **Tanıma pratiği yap.** Kafatası, sağ ve sol ayak bileği çevresi ve sağ üst ekstremite için dört sınırlı modülde inceleme, hatırlama, geri bildirim ve tekrar adımlarını izle. Yeni bir çalışma başlatabilir, yarım oturuma devam edebilir veya önceki sonucunu açabilirsin.
- **Kaldığın yere dön.** Seçimini, kamera açını ve görünürlük ayarlarını içeren en fazla 12 sahne kaydet. Çalışma geçmişin ve tekrar tarihlerin de aynı tarayıcıda saklanır.

Hesap veya API anahtarı gerekmez. Kayıtlar cihazlar arasında eşitlenmez; tarayıcı verilerini temizlemek yerel sahneleri ve çalışma geçmişini siler. Parçaları ayırma, incelemeyi kolaylaştıran bir gösterimdir; anatomik hareket simülasyonu değildir.

## İlk keşif

1. [Atlası aç](https://ismailatilan-44.github.io/human-atlas/) ve **Kafatası · 22 kemik** alanına geç.
2. Bir kemik seç; modeli döndür, **Odaklan** ile yakından incele ve çevre bağlamını açıp kapat.
3. **Geri** ile önceki seçimine dön veya görünümü **Kayıtlı sahneler** üzerinden sakla.
4. **Çalışma ve tekrar** bölümünden bir modül seçip yeni çalışma başlat.

<a id="model-explorer-work"></a>

## Mevcut model kapsamı

Ana vücut, BodyParts3D erişkin erkek referansını ve seçilmiş bölgesel ekleri içerir. Dört ek referans kendi kaynak koordinatlarında ayrı açılır; tek bir vücut modelinde birleştirilmez.

| Model | Paketli parça | İçerik |
| --- | ---: | --- |
| Ana vücut | 2.292 | 2.234 parçalık BodyParts3D tabanı ve 58 kayıtlı ek parça |
| Kadın pelvis referansı | 27 | Uterus, iki ovaryum ve pelvis kemikleri |
| İç kulak referansı | 6 | İki taraflı koklea, vestibüler kompleks ve temporal kemik bağlamı |
| Alt ekstremite referansı | 137 | Seçilmiş sinir, arter, bağ, ayak kası ve destek yapıları ile kemik bağlamı |
| Üst ekstremite sinir referansı | 127 | Adlandırılmış sinirler, dal grupları ve kemik bağlamı |

Bu sayılar paketli geometriyi anlatır; benzersiz anatomik yapı sayısı veya tamamlanma oranı değildir. Güncel sayımlar ve kaynak bağlantıları [model envanterinde](docs/model/model-inventory.md), açık bölgesel hedefler [kapsam planında](docs/model/model-scope-and-acceptance.md) tutulur.

Proje geliştirme aşamasındadır. Bütün vücut ayrıntıları ve tüm adların çevirisi henüz tamamlanmış değildir. Anatomik uzman değerlendirmesi, fiziksel mobil cihaz kabulü ve öğrenme etkisinin değerlendirilmesi açık işlerdir. Çalışma modülleri sınırlı yapı tanıma pratiği sunar. Yerel kontroller ve yayımlanmış sürümlerin kanıtları [teslim kaydında](docs/model/progress-report-2026-10-21.md) ayrı izlenir.

## Yerel kurulum

Node.js **22.13 veya üzeri** gerekir; CI ortamı **22.23.2** kullanır. Tarayıcıya hazır model dosyaları depoda bulunur.

```sh
git clone https://github.com/ismailatilan-44/human-atlas.git
cd human-atlas
npm ci
npm run dev
```

Uygulamayı [localhost:3016](http://localhost:3016) adresinde aç. React, TypeScript, Three.js ve Vite üzerine kurulu uygulamanın arayüzü Tailwind CSS ve shadcn/ui kullanır.

## Geliştiriciler ve ajanlar için başlangıç

Yeni bir işe başlarken [AGENTS.md](AGENTS.md) yönergelerini oku; mevcut dalı, commit'i ve çalışma ağacındaki değişiklikleri kontrol et. [Kapsam planı](docs/model/model-scope-and-acceptance.md) ürün hedefini, [son teslim kaydı](docs/model/progress-report-2026-10-21.md) tarihli sonuçları ve açık işleri taşır. Bu kayıtların sürümlerini çalıştığın kaynakla karşılaştır; yapılacak işi kullanıcının güncel isteğiyle sınırla.

| İhtiyaç | Başvurulacak yer |
| --- | --- |
| Hangi dosya değişmeli, hangi çıktı üretilmeli, hangi kontrol çalışmalı? | [Kaynak → üretici → kontrol rehberi](docs/model/agent-workflow.md#ownership-and-dependency-order) |
| Mevcut modelde ne var, hangi hedefler açık? | [Model envanteri](docs/model/model-inventory.md) ve [kapsam planı](docs/model/model-scope-and-acceptance.md) |
| Kaynak, geometri veya terminoloji çalışması nasıl yürütülür? | [Depoya ait uzmanlık yönergeleri](.agents/skills/) ve göreve ait bölgesel kayıt |
| Görünür davranış nasıl sınanır? | [Tarayıcı QA rehberi](docs/model/development-qa.md) |
| Teslim nasıl kaydedilir ve README ne zaman güncellenir? | [Dokümantasyon bakım akışı](docs/model/agent-workflow.md#readme-maintenance) ve [teslim kaydı](docs/model/progress-report-2026-10-21.md) |

İşe başlamadan önce gözlenebilir sonucu ve kabul kanıtını belirle. İlgili değişikliği ve doğrulamayı tamamladıktan sonra sonucu, denenen ortamı ve kalan işi teslim kaydına işle. Ürünün özellikleri, kapsamı, kurulumu veya geliştirme giriş noktaları değiştiğinde README'yi aynı teslimde güncelle; ayrıntılı test günlükleri ve sürüm geçmişi ilgili kayıtlarda kalsın.

## Geliştirme ve doğrulama

Değiştirdiğin alana uygun kontrolleri [geliştirme rehberinden](docs/model/agent-workflow.md) seç. Yaygın komutlar:

```sh
npm run check                              # TypeScript
node --test scripts/anatomy-knowledge.test.mjs
node scripts/validate-atlas.mjs
node scripts/validate-interactions.mjs
node scripts/build-model-inventory.mjs --check
npm run build                              # dist/ altında statik çıktı
npm run check:ci                            # Tam otomatik doğrulama kapısı
```

[CI iş akışı](.github/workflows/code-checks.yml), veri üretim kontrollerini, testleri, tip denetimini, doğrulayıcıları, üretim derlemesini ve aktarım bütçesini çalıştırır. Görsel veya etkileşim değişikliklerinde ilgili kullanıcı akışını tarayıcıda da doğrula; [geliştirme QA rehberi](docs/model/development-qa.md) bu kontrolleri açıklar.

Üretim çıktısı statik bir sunucuda barındırılabilir. Bu projenin GitHub Pages yayını için `npm run deploy:pages` kullanılır; yayın betiği kaynak değişikliklerinin commit edilmesini ve `fork` adlı uzak depoya gönderilmesini bekler. Yeni klonda bu uzak adını ayrıca yapılandırmak gerekir. Kaynak commit'i ile yayımlanan çıktı arasındaki bağ `release.json` içinde tutulur.

## Katkıda bulun

Arayüz iyileştirmeleri, yeniden üretilebilir hata bildirimleri, kaynaklı terminoloji düzeltmeleri ve kapsamı belirli model katkıları değerlidir. Hata bildirirken kullandığın referansı, yaptığın adımları, beklediğin sonucu ve tarayıcı/cihaz bilgilerini ekle.

Anatomi veya model değişikliklerinde önce [kaynak → üretici → kontrol akışını](docs/model/agent-workflow.md) oku. Kaynak kimliklerini, koordinat bağlamını ve bileşen atıflarını koru. Çalışma modüllerinin sınırları [çalışma tasarımında](docs/model/study-regions-v2.md), öğrenci ve anatomist değerlendirmesi için sonraki adımlar [değerlendirme paketinde](docs/model/learning-review-packet.md) yer alır.

## Kaynak proje ve lisanslar

Human Atlas, [ashemag/human-atlas](https://github.com/ashemag/human-atlas) projesinden fork edilerek geliştiriliyor. İlk 3B görüntüleyici altyapısı için ashemag'a teşekkür ederiz. Bu depodaki geliştirmeler bölgesel model paketleri, çok dilli metadata, ilişki gezinmesi, kayıtlı sahneler ve çalışma deneyimi üzerine kuruludur.

Uygulama kodu [MIT lisansını](LICENSE) ve özgün telif bildirimini korur. Anatomik modeller BodyParts3D, Z-Anatomy ve Human Reference Atlas gibi ayrı kaynaklardan gelir; bileşenlerin kendi lisans ve atıf koşulları vardır. İç kulak paketindeki ticari olmayan kullanım ve aynı lisansla paylaşım koşulları dahil tüm ayrıntılar [veri kaynakları ve atıflar](public/ATTRIBUTION.md) belgesinden erişilebilir.
