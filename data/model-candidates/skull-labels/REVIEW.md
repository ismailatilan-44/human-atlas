# Kafatası kemikleri — sınırlı etiket adayı

22 Eylül 2026. Yalnız `concept-selection-review/skull-bones-proposal.json` içindeki 22 kaynak kemik ve `atlas:skull-bones` proje grubu incelendi. Bu alt görev paylaşılan etiket, uygulama, grafik veya kaynak dosyalarını değiştirmedi.

**Sonuç:** 21 tekil FMA kimliği için 21 yeni TR/EN/LA kayıt. Mandibula (`FMA52748`) ve çalışma sırasında kök görevin eklediği `atlas:skull-bones` grubu zaten üç dilde etiketli; yeniden üretilmedi. Grubun Ossa cranii kaynak satırı kanıtta ayrıca korunuyor. Böylece 23 kimliklik bu dar kapsamda etiket boşluğu kalmaması için aday hazır. Bu ifade atlasın diğer kavramlarını kapsamaz.

22 FJ kimliğinin her biri mevcut manifestte tam bir FMA kavramının tek `elements` girdisiyle eşleşti. FMA kimlikleri ve kaynak İngilizce adları, resmi indirilen BodyParts3D IS-A/PART-OF tablolarında birebir eşleştirildi (büyük/küçük harf dışında). Kimlikler ve mevcut kaynak İngilizcesi `sourceEnglish` alanında korundu. İngilizce görünen etikette tarafsız kaynak terimi, `side` alanında left/right kullanıldı. Mevcut `anatomyLabel` yardımcı fonksiyonu Türkçe/İngilizce taraf önekini ve Latince L/R işaretini sağlar.

Latince terimler sabit [Z-Anatomy TA2.csv](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv) metninden aynen alındı. `ta2TableId` bu upstream tablonun kimliğidir; yayınevi PDF numarası olduğu iddia edilmez. Önceki incelemede FIPAT PDF erişimi başarısız olduğundan bu teslim yeni resmi yayınevi PDF doğrulaması olarak sunulmaz. Türkçe karşılıklar ve günlük arama adları editoryaldir; anatomist incelemesi bekler.

## Kapsamı etkileyen seçimler

- Alt burun konkası kemiği için osteoloji girdisi **740 / Inferior nasal concha bone / Concha nasalis inferior** (dosya satırı 742) kullanıldı. Solunum sistemi girdisi 3151 / Concha inferior nasi ile sessizce eşitlenmedi.
- **atlas:skull-bones:** satır 505, upstream ID **503 / Bones of cranium / Ossa cranii**. Terim eşleşmesi 22 üyeli proje seçiminin bağımsız anatomik doğrulaması değildir; üyelik önceki seçim incelemesinden alınır. Göz yapıları, lakrimal bez, hyoid, dişler ve işitme kemikçikleri grup dışında kalır.
- Mandibula dahil 22 kaynak kemik, kaynak FMA46565 grubunun tamamı olarak yeniden adlandırılmaz. Tekil lakrimal kemik ile lakrimal bez ayrı kavramlardır.

| ID | Parça | Türkçe taban etiket | İngilizce taban etiket | Latince | Taraf | TA2 tablo ID |
|---|---|---|---|---|---|---|
| FMA52740 | FJ3199 | Etmoid kemik | Ethmoid | Os ethmoideum | — | 721 |
| FMA52734 | FJ3200 | Frontal kemik | Frontal bone | Os frontale | — | 520 |
| FMA54738 | FJ3263 | Alt burun konkası | inferior nasal concha | Concha nasalis inferior | left | 740 |
| FMA53646 | FJ3265 | Lakrimal kemik | lacrimal bone | Os lacrimale | left | 744 |
| FMA53650 | FJ3269 | Maksilla | maxilla | Maxilla | left | 756 |
| FMA53648 | FJ3272 | Nazal kemik | nasal bone | Os nasale | left | 748 |
| FMA53656 | FJ3273 | Palatin kemik | palatine bone | Os palatinum | left | 798 |
| FMA52789 | FJ3274 | Parietal kemik | parietal bone | Os parietale | left | 504 |
| FMA52739 | FJ3281 | Temporal kemik | temporal bone | Os temporale | left | 641 |
| FMA52893 | FJ3287 | Zigomatik kemik | zygomatic bone | Os zygomaticum | left | 818 |
| FMA52735 | FJ3309 | Oksipital kemik | Occipital bone | Os occipitale | — | 552 |
| FMA54737 | FJ3369 | Alt burun konkası | inferior nasal concha | Concha nasalis inferior | right | 740 |
| FMA53645 | FJ3371 | Lakrimal kemik | lacrimal bone | Os lacrimale | right | 744 |
| FMA53649 | FJ3375 | Maksilla | maxilla | Maxilla | right | 756 |
| FMA53647 | FJ3378 | Nazal kemik | nasal bone | Os nasale | right | 748 |
| FMA53655 | FJ3379 | Palatin kemik | palatine bone | Os palatinum | right | 798 |
| FMA52788 | FJ3380 | Parietal kemik | parietal bone | Os parietale | right | 504 |
| FMA52738 | FJ3386 | Temporal kemik | temporal bone | Os temporale | right | 641 |
| FMA52892 | FJ3392 | Zigomatik kemik | zygomatic bone | Os zygomaticum | right | 818 |
| FMA52736 | FJ3394 | Sfenoid kemik | Sphenoid bone | Os sphenoideum | — | 584 |
| FMA9710 | FJ3395 | Vomer | Vomer | Vomer | — | 751 |

## Dosyalar ve tekrar üretim

`proposals.json` aktarılabilir yeni kayıtları ve korunan mandibula ve grup kayıtlarını; `source-evidence.json` kaynak satırlarını, URL/hashleri ve girdi snapshot hashlerini; `validation.json` sınırlı kontrolleri içerir. `python3 data/model-candidates/skull-labels/prepare-proposals.py` yalnız bu aday klasörüne yazar. Aktif etiketler değiştikten sonra yeniden çalıştırmak yeni bir denetim üretir; teslimdeki hashler entegrasyon öncesi snapshot olarak korunmalıdır.

## Entegrasyon kaydı

22 Eylül: Kök görev bu adayın incelenen verilerini etkin etiket/bilgi grafiği/görüntüleme katmanına uyguladı. Bu klasörün aday snapshotı korunur; güncel ürün durumu docs/model/2026-09-20-delivery-plan.md içinde izlenir.
