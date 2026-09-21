# Model odaklı ürün: durum ve teslim planı

İlk plan: 20 Eylül 2026. Güncel durum: 22 Eylül 2026, yerel kod, TypeScript/build ve tarayıcı kontrolü. Kodlanmış özellikler ile kullanıma hazır teslim ayrı tutulur.

## Hedef ve sınır

Human Atlas temelinde, anatomik yapıları seçilebilir, adlandırılmış, bağlantıları izlenebilir ve bölge düzeyinde incelenebilir bir model deneyimi. Önce model ve etkileşim; ders, quiz ve AI daha sonra. İlk çalışan entegrasyon örneği omuz–kol; nihai kapsam bu bölgeyle sınırlı değil.

“İlk sürüm hazır”: mevcut tüm vücut görüntüleyici çalışır; pilot bölgede eksik sinirler aynı sahneye eklenir, etiketler ve kaynaklı ilişkiler görünür ve tıklanabilir; odaklanma/gizleme/saydamlık çalışır; bilinen sınıflandırma ve kamera hataları düzeltilir; masaüstü ve dar ekranda uçtan uca denenir. Bu ölçüt bütün insan anatomisinin ve varyasyonlarının eksiksizliği iddiası değildir.

## Doğrulanan mevcut durum — 22 Eylül, uygulama turu

- Yerel dal `codex/model-explorer`. Bu çalışma kapsamında yayınlanmış yeni sürüm yok; upstream repo için oturum açmış hesabın yetkisi READ. Mevcut kodu upstream'e yazma/merge yapılmadı.
- Devralınan temel 2.234 parça/3.432 kaynak kavramıdır. İki Z-Anatomy siniri eklenerek 2.236 parçaya ulaşıldı. Kaynaklar/atıflar ayrı korunur.
- 1.367 PART-OF + 32 pilot ilişki arayüzde gezilebilir; 33 etiket kaydı/47 kimlik için TR/EN/LA arama var. Bütün atlasın çevirisi ve işlevsel ilişkileri tamamlanmış değil.
- Beş yanlış sistem ataması uygulama yüklemesinde düzeltiliyor; omuriliğin kısmi temsili açıklanıyor.
- Altı kaynak tutunma yüzeyinden türetilen landmark noktası sahnede gösteriliyor. Tüm kemik landmark geometrisi diye atanmıyor. İki humerus orta-iç tutunma noktası hâlâ unresolved.
- Odaklanma, saydam çevre, gizleme, önceki seçim/kamera durumuna dönüş, mobil panel alanı ve kaynak bağlantıları uygulandı. WebMCP seçim callback'inin eski state tutması düzeltildi.
- 1440×900 masaüstü, 390×844 ve 320×568 mobil ekranlarda görsel denetim yapıldı. Biceps → sinir, saydam çevre, yan görünüm, gizleme → geri dönüş; kapsam listesi → radius tüberozitesi işareti geçişleri görüldü. Fiziksel cihaz testi/uzman doğrulaması yapılmadı.
- Bölgesel katalog: 5 bölge, 65 hedef grubu. 51 mevcut (3 bilateral yüzey işareti grubu dahil), 1 kısmi, 12 eksik, 1 konumu doğrulanmamış. Bunlar tüm anatominin yüzdesi değildir. Kullanıcıya açılabilir kapsam paneli eklendi.
- TypeScript, üretim build ve kaynak bilgi grafiği güncellik kontrolü geçti. Build büyük JavaScript paketi uyarısı veriyor; bu performans optimizasyonu açık.
- Sonraki aktarım sırası: bilateral median sinir → diz menisküs/çapraz bağ paketi → bilateral sciatic sinir → thyroid. Brakiyal pleksus, omurilik, kadın referansı ve koklea ayrı kapsam/temsil kararları gerektiriyor. Hazır adaylar docs/model/regional-coverage.md içinde.

## Teslim sırası

| Sıra | İş | Tamamlanma ölçütü | Sorumlu / durum |
| --- | --- | --- | --- |
| 1 | Mevcut görüntüleyiciyi düzeltmek | Yanlış sistem atamaları düzeltilmiş; kısmi temsil tam yapı diye sunulmuyor; izolasyonda ön/yan/arka kamera çalışıyor. Veri düzeltmeleri tekrar üretimde korunuyor. | Asistan / uygulandı; pilot görsel akış doğrulandı |
| 2 | Pilot asset aktarımı | Sağ/sol musculocutaneous sinir kaynak geometrileri ihraç edilmiş, mevcut kas/kemiklerle eksen, ölçek ve konum karşılaştırması yapılmış, sahnede ayrı seçilebiliyor. Kaynak ve atıf kaydı korunuyor. | Asistan / iki sinir aktarıldı; seçimi ve saydam bağlamı sahnede doğrulandı |
| 3 | Etiket ve ilişki arayüzü | Yapı seçildiğinde başlangıç, tutunma, sinir ve damar bağlantıları gösteriliyor; mevcut geometriye tıklayarak geçiliyor; geometri/konum bekleyen kayıtlar doğru durumla sunuluyor. Pilot çok dilli isimler ve landmark etiketleri kaynak/inceleme kaydı taşıyor. | Asistan / arayüz ve altı landmark uygulandı; iki konum unresolved |
| 4 | Kullanılabilir pilot teslimi | Çevreyi koruyarak odaklanma, parça gizleme/saydamlık ve önceki görünüme dönüş çalışıyor. Masaüstü ve dar ekran akışları denenmiş, kullanıcıya çalışan önizleme verilmiş. | Asistan / yerel önizleme ve üç ekran boyutunda pilot doğrulama var; yayın bekliyor |
| 5 | Bölgesel kapsamı genişletmek | Her bölge için hedef yapı listesi ve var/eksik/kısmi durumu belli; hazır kaynaklardan gerekenler aktarılmış; aynı etkileşimler korunmuş. Anatomik inceleme bulguları kayıtlı. | Asistan / 65 hedeflik katalog ve gezinme hazır; yeni bölge aktarımları ve uzman incelemesi bekliyor |

Pilot tüm vücudu yeniden modelleme işi değildir. Mevcut kullanılabilir geometriler korunur. Aktarım denemesi başarısız çıkarsa nedenine göre alternatif kaynak veya sınırlı model düzenlemesi seçilir; tüm veri tabanı gereksiz yere değiştirilmez.

## Kullanıcıdan gerekenler

Şu an teknik ilerlemeyi engelleyen kullanıcı girdisi yok. Repo bulma, asset indirme, kaynak araştırma, gerektiğinde kazıma, kimlik eşleştirme, kod ve doğrulama asistanın mevcut yetkili kapsamıdır. Blender kurulu; MCP bağlantısı bu işlerin ön koşulu değildir ve kurulmuş sayılmaz.

Çalışan pilot sonrasında kullanıcıdan model üzerinde çalışma deneyimine dair geri bildirim yararlı olacaktır. Uygun bir anatomi hocası/alan uzmanının incelemesi, eğitim doğruluğunu değerlendirmeye katkı sağlar; teknik prototipin başlaması bu kişinin bulunmasını beklemez. Ders akışı ve müfredat girdileri sonraki faza aittir.

## Önceki planlamanın eksiği

Önceki sıra denetim → kaynak incelemesi → ilişki verisi → pilot entegrasyon → genişletme idi. 20 Eylül itibarıyla ilk üç aşamada hazırlık yapılmış, pilot entegrasyona geçilmemişti. 22 Eylül itibarıyla ilk entegrasyon kodlandı; kullanılabilirlik kabulü henüz tamamlanmadı. Araştırma/veri sayıları kullanıcıya teslim edilmiş ürün özelliği gibi değerlendirilmemeli. Bundan sonraki ilerleme ölçütü çalışan, denenmiş kullanıcı akışlarıdır; yeni araştırma yalnız açık uygulama sorusunu çözmek için yapılır.
