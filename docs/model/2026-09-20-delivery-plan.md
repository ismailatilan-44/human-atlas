# Model odaklı ürün: durum ve teslim planı

İlk plan: 20 Eylül 2026. Güncel durum: 22 Eylül 2026, yerel kod, TypeScript/build ve tarayıcı kontrolü. Kodlanmış özellikler ile kullanıma hazır teslim ayrı tutulur.

## Hedef ve sınır

Human Atlas temelinde, anatomik yapıları seçilebilir, adlandırılmış, bağlantıları izlenebilir ve bölge düzeyinde incelenebilir bir model deneyimi. Önce model ve etkileşim; ders, quiz ve AI daha sonra. İlk çalışan entegrasyon örneği omuz–kol; nihai kapsam bu bölgeyle sınırlı değil.

“İlk sürüm hazır”: mevcut tüm vücut görüntüleyici çalışır; pilot bölgede eksik sinirler aynı sahneye eklenir, etiketler ve kaynaklı ilişkiler görünür ve tıklanabilir; odaklanma/gizleme/saydamlık çalışır; bilinen sınıflandırma ve kamera hataları düzeltilir; masaüstü ve dar ekranda uçtan uca denenir. Bu ölçüt bütün insan anatomisinin ve varyasyonlarının eksiksizliği iddiası değildir.

## Doğrulanan mevcut durum — 22 Eylül, son durum kontrolü

- Yerel dal `codex/model-explorer`. İlk pilot `fc87870` commit'iyle `ismailatilan-44/human-atlas` fork'una gönderildi. Median/diz ve son arayüz değişiklikleri henüz commit edilmedi. Yeni yayın yapılmadı; Pages workflow dosyası hazır, uzak Actions run sayısı kontrol anında sıfır. Orijinal Vercel adresi bizim geliştirmemizi göstermiyor.
- Devralınan temel 2.234 parça. Kayıtlı paketlerle toplam 2.246 parça: sağ/sol muskülokutan ve median sinirler; sağ/sol medial/lateral menisküs ve ön/arka çapraz bağlar. Median paketi ana sinir gövdelerini içerir, tüm dalları içermez.
- Kaynak grafiğinde 3.456 kavram, 1.423 ilişki var: 1.367 hiyerarşik PART-OF ve 56 ek ilişki. Sayı bütün atlasın işlevsel bağlantılarının tamamlandığı anlamına gelmez. Son 12 diz bağlantısı kemik düzeyinde tutunmadır; hassas tutunma koordinatı değildir. Arayüz kataloğu bu grafikten yeniden üretildi.
- 52 çok dilli etiket kaydı mevcut; bütün atlasın Türkçe/Latince çevirisi tamamlanmış değil. Beş yanlış sistem ataması uygulama yüklemesinde düzeltiliyor; omuriliğin kısmi temsili açıklanıyor.
- Altı kaynak tutunma yüzeyinden türetilen referans noktası sahnede gösteriliyor. İki humerus orta-iç tutunma noktası hâlâ unresolved.
- Odaklanma, saydam çevre, gizleme, önceki seçim/kamera durumuna dönüş, mobil panel ve kaynak bağlantıları uygulandı. Önceki görsel kontrolde 1440×900, 390×844 ve 320×568 boyutları; biceps → sinir, yüzey işareti, gizleme → geri dönüş ve yeni median/diz seçimi incelendi. Son değişikliklerin tamamı yeniden görsel kabulden geçmiş sayılmaz. Fiziksel cihaz/uzman incelemesi yapılmadı.
- Bölgesel katalog: 5 bölge, 65 hedef grubu. 55 mevcut (3 bilateral yüzey işareti grubu dahil), 2 kısmi, 7 eksik, 1 konumu doğrulanmamış. Bunlar bütün anatominin yüzdesi değildir. Katalog özet sayaçları güncel satırlardan yeniden hesaplandı.
- Tiroid paketi dosya olarak hazır ama sahneye kayıtlı değil. Kaynak düşük detaylı/stilize olduğu için ayrıntılı tiroid diye sunulmayacak. Siyatik aktarımı sürüyor; oluşturulan dosya varlığı tamamlanmış entegrasyon sayılmıyor.
- Bu durum kontrolünde TypeScript, beş bilgi grafiği testi ve `/human-atlas/` taban yoluyla üretim build geçti. Büyük JavaScript paketi uyarısı sürüyor. Yayın adresinde gerçek model yükleme ve son kullanıcı akışı kabulü bekliyor.
- Brakiyal pleksus, tam omurilik, kadın pelvis referansı, koklea ve iki humeral tutunma noktası açık kapsam. Kadın referansı ana erkek modele rastgele eklenmeyecek; kaynak bağlamı ayrı korunacak.

## Teslim sırası

| Sıra | İş | Tamamlanma ölçütü | Sorumlu / durum |
| --- | --- | --- | --- |
| 1 | Mevcut görüntüleyiciyi düzeltmek | Yanlış sistem atamaları düzeltilmiş; kısmi temsil tam yapı diye sunulmuyor; izolasyonda ön/yan/arka kamera çalışıyor. Veri düzeltmeleri tekrar üretimde korunuyor. | Asistan / uygulandı; pilot görsel akış doğrulandı |
| 2 | Pilot asset aktarımı | Sağ/sol musculocutaneous sinir kaynak geometrileri ihraç edilmiş, mevcut kas/kemiklerle eksen, ölçek ve konum karşılaştırması yapılmış, sahnede ayrı seçilebiliyor. Kaynak ve atıf kaydı korunuyor. | Asistan / iki sinir aktarıldı; seçimi ve saydam bağlamı sahnede doğrulandı |
| 3 | Etiket ve ilişki arayüzü | Yapı seçildiğinde başlangıç, tutunma, sinir ve damar bağlantıları gösteriliyor; mevcut geometriye tıklayarak geçiliyor; geometri/konum bekleyen kayıtlar doğru durumla sunuluyor. Pilot çok dilli isimler ve landmark etiketleri kaynak/inceleme kaydı taşıyor. | Asistan / arayüz ve altı landmark uygulandı; iki konum unresolved |
| 4 | Kullanılabilir pilot teslimi | Çevreyi koruyarak odaklanma, parça gizleme/saydamlık ve önceki görünüme dönüş çalışıyor. Masaüstü ve dar ekran akışları denenmiş, kullanıcıya çalışan önizleme verilmiş. | Asistan / yerel önizleme ve üç ekran boyutunda pilot doğrulama var; yayın bekliyor |
| 5 | Bölgesel kapsamı genişletmek | Her bölge için hedef yapı listesi ve var/eksik/kısmi durumu belli; hazır kaynaklardan gerekenler aktarılmış; aynı etkileşimler korunmuş. Anatomik inceleme bulguları kayıtlı. | Asistan / 65 hedeflik katalog; median ve diz eklendi, siyatik/tiroid ve diğer boşluklar açık |

Pilot tüm vücudu yeniden modelleme işi değildir. Mevcut kullanılabilir geometriler korunur. Aktarım denemesi başarısız çıkarsa nedenine göre alternatif kaynak veya sınırlı model düzenlemesi seçilir; tüm veri tabanı gereksiz yere değiştirilmez.

## Kullanıcıdan gerekenler

Şu an teknik ilerlemeyi engelleyen kullanıcı girdisi yok. Repo bulma, asset indirme, kaynak araştırma, gerektiğinde kazıma, kimlik eşleştirme, kod ve doğrulama asistanın mevcut yetkili kapsamıdır. Blender kurulu; MCP bağlantısı bu işlerin ön koşulu değildir ve kurulmuş sayılmaz.

Çalışan pilot sonrasında kullanıcıdan model üzerinde çalışma deneyimine dair geri bildirim yararlı olacaktır. Uygun bir anatomi hocası/alan uzmanının incelemesi, eğitim doğruluğunu değerlendirmeye katkı sağlar; teknik prototipin başlaması bu kişinin bulunmasını beklemez. Ders akışı ve müfredat girdileri sonraki faza aittir.

## Önceki planlamanın eksiği

Önceki sıra denetim → kaynak incelemesi → ilişki verisi → pilot entegrasyon → genişletme idi. 20 Eylül itibarıyla ilk üç aşamada hazırlık yapılmış, pilot entegrasyona geçilmemişti. 22 Eylül itibarıyla ilk entegrasyon kodlandı; kullanılabilirlik kabulü henüz tamamlanmadı. Araştırma/veri sayıları kullanıcıya teslim edilmiş ürün özelliği gibi değerlendirilmemeli. Bundan sonraki ilerleme ölçütü çalışan, denenmiş kullanıcı akışlarıdır; yeni araştırma yalnız açık uygulama sorusunu çözmek için yapılır.

## Sıradaki somut teslim ve bitiş ölçütleri

1. Hazır median/diz paketleri ve ilişkileriyle çalışan sürümü son görsel kontrolden geçirip yayımla; açılan gerçek adresi kullanıcıya ver. Kaynak/atıflar ve kapsam sınırları görünür olmalı.
2. Siyatik ve tiroid paketlerini kaynak kalitesine göre kabul et veya açık sınırlı temsil olarak işaretle; geometri, doğru taraf, konum, seçim, etiket ve kaynak kontrolü tamamlanmadan bitti sayma.
3. Kalan yedi eksik hedef grubunu sırayla kapat: yalnız somut boşluk için araştırma/aktarım. Tam kaynak bulunamazsa kalan temsil sınırını açık kaydet; eksik geometriyi varmış gibi sayma.
4. Kapsamlı etiket/ilişki zenginleştirmesini bölge bölge sürdür. İlk kullanılabilir atlas ile bütün anatominin tamamlanmasını ayrı değerlendir.
5. Model kullanımı oturduktan sonra ders akışlarını mevcut yapı kimliklerine ve kayıtlı sahnelere bağla. Bu aşama mevcut model teslimini geciktirmez.

Kullanıcıdan şimdi zorunlu teknik görev yok. Kullanım geri bildirimi ve ileride öğretim sırası/alan uzmanı değerlendirmesi yararlı girdilerdir; repo, indirme, Blender/MCP kurulumu veya entegrasyon kullanıcıya devredilmiş bir engel değildir.

## Yayın adayı — 22 Eylül sonraki entegrasyon

- Aktif model 2.248 parça: bilateral siyatik paket de kayıtlı. Sinirin ayrı tibial/fibular devamları yok; kısmi temsil notu görünür.
- Grafik 3.458 kavram / 1.431 ilişki. Siyatik–kas sekiz bağlantısında tibial/common-fibular bölüm ayrımı arayüzde korunur; doğrudan ayrışmamış kas dalı iddiası yok. Etiketler dizde femur/tibia ve posterior uyluk kaslarına genişletildi.
- Tiroid kaynak dosyası hazır olmasına rağmen yakın plan görsel kalite değerlendirmesi sonucu aktif registry'ye alınmadı. Alternatif kaynak çalışması sürüyor. Brakiyal pleksus ihracı sürüyor.
- `/human-atlas/` üretim derlemesi tarayıcıda yüklendi; 2.248 parça, siyatik arama/seçme, çevre saydamlığı ve arka görünüm çalıştı. Siyatikten biceps kısa başına gidiş ve ters bağlantıda bölüm metni görüldü. 390×844 mobilde ön çapraz bağ ve kemik bağlantıları, modelin panel üstünde kaldığı yakın plan incelendi. Katman preset'i eski seçimi ve paneli temizledi.
- Uzak yayın bu bölüm yazılırken henüz doğrulanmadı; Pages yalnız main dalından dağıtım kabul ediyor. Sonraki adım commit, fork main birleşimi, CI ve gerçek yayın adresi kontrolüdür.
