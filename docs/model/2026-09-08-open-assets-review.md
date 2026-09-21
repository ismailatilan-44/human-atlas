# Açık anatomi assetleri — 8 Eylül 2026

## Sonuç

Mevcut Human Atlas paketindeki eksikler, bütün açık kaynak ekosisteminde eksik oldukları anlamına gelmiyor. İncelenen Z-Anatomy kaynak dosyasında periferik sinirler, menisküsler ve çapraz bağlar bulunuyor. İlk model geliştirme adımı olarak yeni geometri üretimi yerine kaynak dosyasının kontrollü web aktarımını denemek daha uygun.

Bu, bütün tıp eğitimi kapsamının tamamlandığı veya geometrilerin anatomik olarak doğrulandığı anlamına gelmez. Çalışma dosya ve nesne envanteri denetimidir; yakın plan görsel inceleme ve uzman değerlendirmesi yapılmadı.

## Gerçekten incelenen dosyalar

| Kaynak | Denetim | Bulgular |
| --- | --- | --- |
| Yerel BodyParts3D paketi | Önceki tam manifest/binary envanteri; `2026-09-08-audit.md` | 2.234 parça. Bazı beyin yapıları yanlış sistemde; bazı kavramlar kısmi geometriye bağlı. |
| [Z-Anatomy kaynak arşivi](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/Z-Anatomy.zip) | 86.734.957 bayt ZIP indirildi; içindeki 306.838.281 bayt `Startup.blend`, Blender 5.2.0 LTS ile arka planda okundu; gömülü scriptler kapalıydı. | 7.184 nesne: 4.569 mesh, 951 curve, 1.660 yazı, 3 ışık, 1 kamera. Meshlerin yalnız 2.964'ünde yüzey poligonu var; 1.605'i sıfır poligonlu. Bunlar anatomik yapı sayısı değildir. |
| [Vanatome 1.4.0](https://github.com/vixotic/Vanatome/blob/main/public/models/z-anatomy-1.4.0-manifest.json) | Tam manifest ve katalog, 11.301.584 bayt nervous GLB indirildi; GLB başlığı/JSON, node adları ve manifest eşlemeleri okundu. | Manifestte 749 node eşlemeli yapı ID'si var. Sinir paketinde 234 node bulunuyor. Median, musculocutaneous ve sciatic nerve adları bu pakette/manifestte eşleşmedi; paket beyin yapılarına odaklanıyor. |
| [HuBMAP HRA kadın organları v1.2](https://github.com/hubmapconsortium/ccf-3d-reference-object-library/tree/main/VH_Female/v1.2) | Uterus ve sol ovaryum GLB'leri indirildi; başlık/JSON ve node/mesh içerikleri okundu. | Uterus dosyasında 11 node, 10 mesh; sol ovaryumda 1 node, 1 mesh. Kadın anatomisi için somut ek kaynak adayları. Bu örnek sürüm, HRA'nın güncel toplam kapsamı olarak sunulmuyor. |

Vanatome ve HRA örnek GLB'lerinin dosya uzunlukları başlıklarla uyuşuyor. Vanatome sinir paketinin SHA-256 değeri katalogla uyuşuyor. Bu kontroller yüzeylerin anatomik doğruluğunu veya görünümünü kanıtlamaz.

İndirilen `Startup.blend` SHA-256 değeri, Vanatome manifestindeki `sourceBlendSha256` ile de birebir eşleşiyor (`9f08a17e…135afcd`). Dolayısıyla burada saptanan kaynak/paket kapsam farkı yalnız farklı Blender sürümlerine bağlanamaz: aynı kaynak dosyada bulunan bazı yapılar, incelenen hazır web paketine dahil edilmemiş.

## Z-Anatomy'de mevcut boşlukların karşılığı

| Aranan yapı | Kaynak dosyada bulunan gerçek nesne türü | Web aktarımına etkisi |
| --- | --- | --- |
| Median nerve, sol/sağ | Her biri 2 spline, 20 kontrol noktası olan CURVE | Yalnız mesh ihraç eden bir işlem bunları kaybeder; eğrilerin kalınlığı ve bağlantıları korunmalı. |
| Musculocutaneous nerve, sol/sağ | Her biri 1 spline, 6 kontrol noktası olan CURVE | Eğriden yüzeye aktarım gerekir. |
| Sciatic nerve, sol/sağ | Her biri 20 kontrol noktası olan CURVE | Aynı aktarım ihtiyacı. |
| Brachial plexus | Adında bu ifade geçen 22 geometrili CURVE; kök, trunk, division ve posterior cord örnekleri | Bu sayı pleksusun bütün parçalarının eksiksizliğini kanıtlamaz. |
| Medial/lateral meniscus, sol/sağ | Yüzey poligonları bulunan ayrı MESH'ler | Model dosyasında var; aktarım ve görsel kalite kontrolü gerekir. |
| Anterior/posterior cruciate ligament, sol/sağ | Ayrı MESH'ler; ön bağlar 808, arka bağlar 404 taban poligon | Kaynak nesnenin varlığı doğrulandı; değerlendirilen son yüzey kalitesi henüz incelenmedi. |
| Coracoid process, radial tuberosity, supraglenoid tubercle | İsimli FONT ve 2 vertex/0 polygon işaret nesneleri | İsimli nesne bulunması ayrı bir anatomik yüzey olduğu anlamına gelmiyor. Mevcut kemik üzerinde işaret/alan seçimi tasarlanabilir. |
| Ovary, uterus | Nesne adlarında eşleşme yok | İncelenen erkek kaynakta temsil doğrulanmadı; HRA'dan ayrı kadın model bağlamında değerlendirilmesi uygun. |

Kaynakta biceps başlarına ait kas yüzeyleri yanında `Muscular insertions` koleksiyonunda küçük tutunma yüzeyleri de var. Bazı kaslar sinir adı taşıyan koleksiyonlara dahil edilmiş. Bu ilişki verisi için yararlı bir başlangıç adayıdır; koleksiyon üyeliği otomatik olarak doğrulanmış innervasyon ilişkisine çevrilmemeli.

## Lisans ve erişim durumu

- [BodyParts3D'nin güncel resmi sayfası](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html) CC BY 4.0 bildiriyor. Bu, türev dosyalardaki ek malzemeyi otomatik yeniden lisanslamaz.
- [Z-Anatomy License.txt](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/License.txt) genel olarak CC BY-SA 4.0 bildirirken iç kulak referansı/uyarlaması için CC BY-NC-SA 4.0, bir böbrek kaynağı için CC BY-NC 4.0 da listeliyor. Dosya bunları “reference/included and adapted” olarak birlikte tanımlıyor; her nesnenin hangi kaynaktan geldiği bu metinden kesin ayrıştırılamıyor. Dolayısıyla bütün arşiv için tek ve sorunsuz ticari kullanım sonucu çıkarılmadı.
- [Vanatome asset lisansı](https://github.com/vixotic/Vanatome/blob/main/ASSET-LICENSE.md) yazılımın MIT lisansı ile Z-Anatomy'den türetilen assetlerin lisansını ayırıyor. Upstream bildirimleri esas alıyor. Katalogdaki eski `Z-Anatomy/Models` bağlantısı bu incelemede 404 döndü; erişilebilen kaynak `Models-of-human-anatomy` deposu.
- [HRA kaynak deposu](https://github.com/hubmapconsortium/ccf-3d-reference-object-library) CC BY 4.0 lisansı taşıyor; kullanılan sürüm ve atıf bilgileri ithalat kayıtlarına dahil edilmeli.
- Vayu AI Anatomy'nin yazar yazısı okundu; yazıda verilen `RamRam633/Vayu-AI-Anatomy` deposu web ve GitHub API üzerinden 404 döndü. Bu nedenle ilan edilen yapı sayısı veya performansı bağımsız doğrulanmış sayılmadı; assetleri incelenen kaynaklar arasında değil.

## Kalan ihtiyaç ve önerilen sıra

1. Z-Anatomy kaynağından bir omuz–kol örneğinde kemik, kas, damar, sinir ve tutunma yüzeylerini birlikte dışa aktarmak. Bu bir model aktarım denemesi; ders modülü değil.
2. Nesne türlerini ayırmak: anatomik yüzey, eğri, yazı, işaret, tutunma yüzeyi. Anatomik yapı sayısını Blender nesne sayısıyla karıştırmamak.
3. Kalıcı parça kimliklerini, sol/sağ bilgisini, bölge ve sistem ilişkilerini korumak. Türkçe/Latince/İngilizce adlandırmayı bu kimliklere bağlamak.
4. Kaynak/atıf/lisans kaydını parça veya güvenilir alt paket düzeyinde tutmak; belirsiz malzemeyi ayrı değerlendirmek.
5. Web örneğinde yakınlaşma, seçim, gizleme, saydamlık ve komşulukları incelemek; kaynak geometriyle görsel karşılaştırmak ve anatomik doğruluğu değerlendirmek.
6. Ancak bu karşılaştırmada kalan somut eksikler için başka asset veya özel modelleme kararı vermek. Kadın ve erkek referansları bağlamsız biçimde aynı gövdeye yapıştırılmamalı.

Bu tur viewer veya yayınlanan model değiştirilmedi. Aday ana geometri kaynağı olarak Z-Anatomy öneriliyor; Vanatome hazır web paketleri ve izleyici mimarisi için referans, HRA ise uygun organlar için tamamlayıcı aday. Nihai kaynak seçimi henüz yapılmadı.

## Kanıt ve tekrar

Dosya URL'leri, SHA-256 değerleri ve seçilmiş nesne kayıtları `2026-09-08-open-assets-evidence.json` içinde. İndirilen arşivler ve tam Blender envanteri Git'in yok saydığı `work/open-assets-review/` altında yerel tutuluyor. `inspect_blend.py` yalnız envanter okur; kaynak dosyaya yazmaz.

Blender eski dosyayı okurken arayüz sürüm uyarlama uyarıları ve oesophagus/profile ilişkisinde bir dependency cycle bildirdi. İncelenen sinir ve eklem nesneleri envanterden okunabildi; bütün kaynak için hatasız export iddia edilmiyor.
