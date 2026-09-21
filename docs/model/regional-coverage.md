# Bölgesel model kapsamı — ilk sürüm hedefleri

22 Eylül 2026. Bu liste ilk sürümde gezinme ve yakın inceleme için seçilmiş somut hedefleri izler. Tıp müfredatı veya bütün insan anatomisi listesi değildir. Bir satır iki tarafı ya da alt yapı grubunu içerebilir; satır sayısı anatomik yapı sayısı değildir.

Makine kaydı: [coverage.json](../../data/anatomy/coverage.json). Mevcut ana atlas, bilgi grafiği, iki sinir extension’ı, altı konum içeren landmark extension’ı ve daha önce indirilmiş kaynak envanteri okundu. Startup.blend, HRA uterus ve sol ovaryum dosyalarının SHA-256 değerleri önceki denetim kaydıyla bu tur yeniden karşılaştırıldı. Yeni kaynak araştırması veya geometri aktarımı yapılmadı.

## Durumların anlamı

- **Mevcut:** Adlandırılmış kimlik ve paketlenmiş geometri veya kayıtlı yüzey referans noktası var. `representation: surface_anchor` olan kayıtlar yalnız noktadır; bağımsız/tam landmark geometrisi veya uzman onayı iddiası yok.
- **Kısmi:** İncelenmiş kanıt, adlandırılan hedefin yalnız bir bölümünün temsil edildiğini gösteriyor.
- **Eksik:** İncelenen atlas/extension içinde bağımsız hedef kaydı bulunamadı. Ad taraması başka yüzeyin içindeki ayrıntının veya olası tüm eş adların yokluğunu kanıtlamaz.
- **Doğrulanmamış:** Semantik hedef veya ilgili kemik yüzeyi var; bağımsız temsil ya da konum henüz doğrulanmadı.

Bütün hedeflerde anatomik uzman incelemesi bekliyor. Geometri varlığından `full` sonucu çıkarılmadı. Toplam 65 hedef satırının 51’i mevcut, 1’i kısmi, 12’si eksik, 1’i doğrulanmamış. Mevcut 51 satırın 3’ü toplam altı yüzey referans noktasıdır; yeni bağımsız yüzey geometrisi sayılmaz.

| Bölge | Mevcut | Kısmi | Eksik | Doğrulanmamış |
| --- | ---: | ---: | ---: | ---: |
| Baş ve boyun | 7 | 1 | 2 | 0 |
| Toraks | 8 | 0 | 0 | 0 |
| Abdomen ve pelvis | 13 | 0 | 3 | 0 |
| Üst ekstremite | 15 | 0 | 2 | 1 |
| Alt ekstremite | 8 | 0 | 5 | 0 |

## Baş ve boyun

| İlk sürüm hedefi | Durum | Mevcut kimlikler / indirilen aday |
| --- | --- | --- |
| Kafatası | Mevcut | `FMA46565` |
| Mandibula | Mevcut | `FMA52748` |
| Beyin | Mevcut | `FMA50801` |
| Hipokampus, iki taraf | Mevcut | `FMA62493` |
| Servikal omurlar | Mevcut | `FMA9915` |
| Larinks kıkırdakları | Mevcut | `FMA55108` |
| Beyin ventrikülleri ve interventriküler foramen | Mevcut | `FMA78454`, `FMA78469`, `FMA75351`, `FMA78450`, `FMA78449` |
| Omurilik | Kısmi | `FMA7647`; aday: `za-spinal-substructures` |
| Tiroid bezi | Eksik | Bağımsız kayıt bulunamadı; aday: `za-thyroid` |
| Koklea, iki taraf | Eksik | Bağımsız kayıt bulunamadı; aday: `za-cochlea` |

## Toraks

| İlk sürüm hedefi | Durum | Mevcut kimlikler / indirilen aday |
| --- | --- | --- |
| Kalp | Mevcut | `FMA7088` |
| Akciğerler, iki taraf | Mevcut | `FMA7310`, `FMA7309` |
| Trakea | Mevcut | `FMA7394` |
| Diyafram | Mevcut | `FMA13295` |
| Kaburgalar | Mevcut | `FMA7574` |
| Sternum | Mevcut | `FMA7485` |
| Aort | Mevcut | `FMA3734` |
| Özofagus | Mevcut | `FMA7131` |

## Abdomen ve pelvis

| İlk sürüm hedefi | Durum | Mevcut kimlikler / indirilen aday |
| --- | --- | --- |
| Karaciğer | Mevcut | `FMA7197` |
| Mide | Mevcut | `FMA7148` |
| Pankreas | Mevcut | `FMA7198` |
| Dalak | Mevcut | `FMA7196` |
| Böbrekler | Mevcut | `FMA7203` |
| Safra kesesi | Mevcut | `FMA7202` |
| İnce bağırsak | Mevcut | `FMA7200` |
| Kalın bağırsak | Mevcut | `FMA7201` |
| Rektum | Mevcut | `FMA14544` |
| Mesane | Mevcut | `FMA15900` |
| Prostat | Mevcut | `FMA9600` |
| Kalça kemikleri | Mevcut | `FMA16585` |
| Sakrum | Mevcut | `FMA16202` |
| Uterus — ayrı kadın referansı | Eksik | Bağımsız kayıt bulunamadı; aday: `hra-uterus` |
| Sol ovaryum — ayrı kadın referansı | Eksik | Bağımsız kayıt bulunamadı; aday: `hra-left-ovary` |
| Sağ ovaryum — ayrı kadın referansı | Eksik | Bağımsız kayıt bulunamadı |

## Üst ekstremite

| İlk sürüm hedefi | Durum | Mevcut kimlikler / indirilen aday |
| --- | --- | --- |
| Klavikulalar | Mevcut | `FMA13321` |
| Skapulalar | Mevcut | `FMA13394` |
| Humeruslar | Mevcut | `FMA13303` |
| Radiuslar | Mevcut | `FMA23463` |
| Ulnalar | Mevcut | `FMA23466` |
| El bileği kemikleri | Mevcut | `FMA23889` |
| Deltoid kasının mevcut bölümleri | Mevcut | `FMA34676` |
| Biceps brachii uzun başları | Mevcut | `FMA37683` |
| Biceps brachii kısa başları | Mevcut | `FMA37682` |
| Coracobrachialis kasları | Mevcut | `FMA37664` |
| Brakiyal arterler | Mevcut | `FMA22689` |
| Muskülokutan sinirler | Mevcut | `atlas:left-musculocutaneous-nerve`, `atlas:right-musculocutaneous-nerve` |
| Median sinirler | Eksik | Bağımsız kayıt bulunamadı; aday: `za-median` |
| Brakiyal pleksus | Eksik | Bağımsız kayıt bulunamadı; aday: `za-brachial-plexus` |
| Korakoid çıkıntılar | Mevcut — yüzey referans noktası | `atlas:left-coracoid-process`, `atlas:right-coracoid-process`; `surface_anchor`, bağımsız yüzey değil |
| Supraglenoid tüberküller | Mevcut — yüzey referans noktası | `atlas:left-supraglenoid-tubercle`, `atlas:right-supraglenoid-tubercle`; `surface_anchor`, bağımsız yüzey değil |
| Radius tüberoziteleri | Mevcut — yüzey referans noktası | `atlas:left-radial-tuberosity`, `atlas:right-radial-tuberosity`; `surface_anchor`, bağımsız yüzey değil |
| Humerus orta iç tutunma bölgeleri | Doğrulanmamış | `atlas:left-humerus-medial-midshaft`, `atlas:right-humerus-medial-midshaft` |

## Alt ekstremite

| İlk sürüm hedefi | Durum | Mevcut kimlikler / indirilen aday |
| --- | --- | --- |
| Femurlar | Mevcut | `FMA9611` |
| Tibialar | Mevcut | `FMA24476` |
| Fibulalar | Mevcut | `FMA24479` |
| Patellalar | Mevcut | `FMA24485` |
| Gluteus maximus kasları | Mevcut | `FMA22314` |
| Quadriceps femoris mevcut bölümleri | Mevcut | `FMA22429` |
| Femoral arterler | Mevcut | `FMA70248` |
| Ayak bileği kemikleri | Mevcut | `FMA24491` |
| Siyatik sinirler | Eksik | Bağımsız kayıt bulunamadı; aday: `za-sciatic` |
| Medial menisküsler | Eksik | Bağımsız kayıt bulunamadı; aday: `za-medial-menisci` |
| Lateral menisküsler | Eksik | Bağımsız kayıt bulunamadı; aday: `za-lateral-menisci` |
| Ön çapraz bağlar | Eksik | Bağımsız kayıt bulunamadı; aday: `za-acl` |
| Arka çapraz bağlar | Eksik | Bağımsız kayıt bulunamadı; aday: `za-pcl` |

## Hazır sonraki teknik denemeler

“Hazır” kaynak nesne/dosyanın indirildiği ve kimliğinin bulunduğu anlamına gelir; yayıma hazır veya anatomik olarak onaylı anlamına gelmez. Kayıt/atıf, paket teknik kontrolü ve görünür yüzey incelemesi her aktarımda korunmalıdır.

1. **Median sinirler:** `Median nerve.l/.r`, CURVE, her biri 2 spline/20 kontrol noktası. İki musculocutaneous sinirde çalışan eğri aktarımı kullanılabilir; önkol/bilek uyumu ayrıca ölçülmeli.
2. **Diz paketi:** `Medial meniscus.l/.r` (37 polygon/yan), `Lateral meniscus.l/.r` (59), `Anterior cruciate ligament.l/.r` (808), `Posterior cruciate ligament.l/.r` (404). Ayrı yüzeyler indirilen Blender dosyasında var. Femur/tibia/patella ile yeni bölgesel kayıt ve yakın plan kontrol gerekir.
3. **Siyatik sinirler:** `Sciatic nerve.l/.r`, CURVE, her biri 3 spline/20 kontrol noktası. Üst kol dönüşümü alt ekstremiteye doğrulanmadan taşınmaz.
4. **Tiroid:** `Thyroid gland`, 84 vertex/68 polygon yüzey. Bez bağımsız aday olarak var; boyun kaydı ve ayrıntı yeterliliği incelenmeli.
## Kayıtlı landmark temsilleri

`upper-arm-landmarks.json` artık korakoid çıkıntı, supraglenoid tüberkül ve radius tüberozitesinin iki tarafına ait altı referans noktası içeriyor. Katalogdaki `surface_anchor`, bağımsız bir anatomik yüzey yerine kaynak tutunma yüzeyinden hesaplanmış noktayı ifade eder. Noktaların kaynakları sırasıyla `Coracobrachialis muscle.ol/.or`, `Long head of biceps brachii.ol/.or` ve `Biceps brachii muscle.el/.er` yüzeyleridir. Aynı kemik/kas koordinat kaydı uygulanmış; kemik bağlamı ve ölçülmüş artık uzaklıklar manifestte korunmuştur. Anatomik uzman incelemesi bekliyor.

Önceki `.i/.j` iki-vertex işaret adayları ana kaynak olarak reddedildi; sol taraftaki etiket ofset/transformları gerçek tutunma yüzeyleriyle uyuşmadı. Bu adaylar katalogda `rejected_for_anchoring` olarak tarihî kanıt için tutulur ve sonraki aktarım listesinde yer almaz. Gerçek altı anchor bu etiket çizgilerinden türetilmedi.

## Açık kalan belirli boşluklar

- **Omurilik:** `FMA7647` yalnız `FJ1737` merkez kanalına bağlı. Z-Anatomy’nin anterior horn (22 polygon), posterior horn (32), white matter (39) yüzeyleri tam omurilik yerine onaylanmış değil; `Spinal cord.j` yalnız işarettir.
- **Brakiyal pleksus:** 22 geometrili eğri adları kaynakta mevcut; kök/trunk/division/posterior cord örnekleri tamlık kanıtı değil. Aktarımdan önce parça listesi ve birleşimleri incelenmeli.
- **Koklea:** `Cochlea.l/.r` 772 polygon/yan. Yüzey var; upstream iç kulak için ayrıca NC-SA referans/uyarlama bildirimi bulunduğundan nesne kökeni ve kullanım koşulları ayrılmalı. Bu katalog lisans belirsizliğini çözmez.
- **Kadın pelvis:** HRA v1.2 uterus (11 node/10 mesh) ve sol ovaryum (1/1) dosyaları indirili ve hashleri eşleşiyor. Ayrı kadın referansı/koordinat bağlamı gerekir. Sağ ovaryum bu indirilen örneklerde yok; sol modeli aynalamak doğrulanmış sağ organ değildir.
- **Humerus orta iç tutunma alanı:** İki taraf `upper-arm-landmarks.json` dosyasındaki `unresolved` kayıtlarında; özel tutunma yüzeyi veya uygun işaret bulunamadı. Skapuladaki coracobrachialis başlangıç yüzeyi humeral tutunma yerine kullanılmadı. Kayıtlı konum yok; `unanchored_landmark` ve doğrulanmamış durumu korunuyor.

## Veri durumları ve kanıt sınırı

İki musculocutaneous sinir, `upper-arm-nerves.json` extension’ında `ZA-MCN-L/R` olarak mevcut. Eski `knowledge.json` hâlâ `external_candidate` bildirir; katalog geometri varlığı için güncel extension’ı esas alır ve kaynak grafiğini değiştirmez. Benzer şekilde altı landmark için grafikteki eski `landmark_unanchored` yerine güncel landmark extension’ının kayıtlı noktaları esas alınır; humerus hedeflerinin eski bekleyen durumu geçerliliğini korur. Ana atlasın beş beyin parçası için eski `cardiac` değeri dosyada korunur; çalışma zamanı düzeltmesi ayrı uygulanır.

Kaynak envanterindeki MESH taban polygon sayısı, Blender modifier sonrası üçgen sayısı veya anatomik kalite puanı değildir. Koleksiyon üyeliği innervasyon/komşuluk ilişkisi olarak kullanılmadı. Kaynakları indirmiş olmak bölgeler arasında koordinat eşitliği veya bütün lisansların çözülmesi anlamına gelmez.

- [Yerel temel denetim](2026-09-08-audit.md)
- [İndirilmiş kaynak denetimi](2026-09-08-open-assets-review.md) ve [hash/nesne kanıtı](2026-09-08-open-assets-evidence.json)
- [İki sinirin ölçülmüş kayıt raporu](asset-registration-upper-arm-nerves.md)
- [Pilot etiket kapsamı](labels-review.md)

Bu katalog diğer bölgeleri çevrilmiş, etiketlenmiş, geometrisi tamamlanmış veya anatomik olarak kabul edilmiş saymaz. Sonraki ilerleme ölçütü, bu hedeflerde çalışan ve incelenen model davranışıdır.
