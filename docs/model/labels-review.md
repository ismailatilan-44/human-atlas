# Omuz–kol pilotu: etiket ve görüntüleme düzeltmeleri

22 Eylül 2026. `app/atlas-metadata.ts` kaynak manifesti değiştirmeden uygulanır. Görüntüleyici atlası yüklerken `prepareAtlas` çağırmalı; kavram kapsamı için `getRepresentationNote` sonucunu göstermelidir.

## İncelenen düzeltmeler

- `FJ1730`, `FJ1731`, `FJ1752`, `FJ1767`, `FJ1814` parçalarının sistemi `nervous` olarak düzeltilir. Kimlik, geometri, paket ofsetleri ve kavram bağlantıları korunur. Kanıt: [8 Eylül denetimi, M-01](2026-09-08-audit.md) ve orada bağlantılanan BodyParts3D PART-OF tablosu.
- `FMA7647` için Türkçe kısmi temsil notu verilir: yerel geometri yalnız merkez kanaldır. Kanıt: aynı denetimin M-02 kaydı. Diğer kavramlarda not olmaması tam temsil anlamına gelmez.

## Etiket kaynağı ve sınırları

[Z-Anatomy upstream TA2.csv](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv) İngilizce–Latince eşlemeleri okunup doğrulandı. Dosya SHA-256: `0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974`. Sabit commit dosyası ayrıca indirilerek hash eşitliği kontrol edildi. Bu Z-Anatomy dağıtımındaki TA2 tablosudur; FIPAT'ın Türkçe bir yayını değildir.

| TA2 kimliği | İngilizce temel terim | Latince temel terim |
| --- | --- | --- |
| 2464 | Biceps brachii muscle | Musculus biceps brachii |
| 2465 | Long head of biceps brachii | Caput longum musculi bicipitis brachii |
| 2466 | Short head of biceps brachii | Caput breve musculi bicipitis brachii |
| 2468 | Coracobrachialis muscle | Musculus coracobrachialis |
| 6421 | Musculocutaneous nerve | Nervus musculocutaneus |
| 1143 | Scapula | Scapula |
| 1180 | Humerus | Humerus |
| 1210 | Radius | Radius |
| 1159 | Coracoid process | Processus coracoideus |
| 1163 | Supraglenoid tubercle | Tuberculum supraglenoideum |
| 1216 | Radial tuberosity | Tuberositas radii |
| 4632 | Brachial artery | Arteria brachialis |

Türkçe metinler kaynak terimlerin editoryal çevirisi/transliterasyonudur; resmi Türkçe terminoloji onayı veya anatomist incelemesi iddiası taşımaz. Sağ/sol mevcut manifest ve pilot kimliklerinden alınır. Latince temel terim aynen korunur; taraf için `L` (sol) ve `R` (sağ) eklenir. Yeni Latince çekim üretilmez.

Humerus orta iç tutunma bölgesi proje tarafından tanımlanmış bir bölgedir. Bağımsız bir TA2 terimiymiş gibi Latince ad uydurulmadı; Latince seçiminde kaynak İngilizce adı korunur. Bu davranış tüm pilot dışı kimlikler için de geçerlidir. Arama İngilizce kaynak adını, pilot Türkçe/Latince adları ve sınırlı yaygın adları birlikte kapsar; Türkçe aksanlar olmadan da arama terimleri üretilir.

Bu paket yalnız iki taraflı biceps/korakobrakiyal kas pilotunun etiketlerini kapsar; bütün atlasın çevrildiği veya omuz–kol anatomisinin tamamlandığı anlamına gelmez. Yeni innervasyon, tutunma ilişkisi, geometri veya landmark koordinatı eklenmedi. Mevcut manifest, bilgi grafiği ve kaynak hash kayıtları değiştirilmedi.
