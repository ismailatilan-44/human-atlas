# Bölgesel model kapsamı — ilk sürüm hedefleri

22 Eylül 2026. Bu liste ilk sürümde gezinme ve yakın inceleme için seçilmiş somut hedefleri izler. Tıp müfredatı veya bütün insan anatomisi listesi değildir. Bir satır iki tarafı ya da alt yapı grubunu içerebilir; satır sayısı anatomik yapı sayısı değildir.

Makine kaydı: [coverage.json](../../data/anatomy/coverage.json). Mevcut ana atlas, bilgi grafiği, iki sinir extension’ı, altı konum içeren landmark extension’ı ve daha önce indirilmiş kaynak envanteri okundu. Startup.blend, HRA uterus ve sol ovaryum dosyalarının SHA-256 değerleri önceki denetim kaydıyla bu tur yeniden karşılaştırıldı. İlk katalogdan sonra median, diz, siyatik, BodyParts3D tiroid/omurilik ve ayrı HRA kadın pelvis paketleri incelendi; güncel kaynak hash’leri makine kaydında tutulur. Kadın pelvisin public manifesti ve binary/gzip dosyaları ayrı kaynak kaydıdır; erkek atlasa ait geometri sayılmaz.

## Durumların anlamı

- **Mevcut:** Belirtilen dataset veya ayrı referansta adlandırılmış kimlik ve paketlenmiş geometri ya da kayıtlı yüzey referans noktası var. `representation: surface_anchor` olan kayıtlar yalnız noktadır; bağımsız/tam landmark geometrisi veya uzman onayı iddiası yok.
- **Kısmi:** İncelenmiş kanıt, adlandırılan hedefin yalnız bir bölümünün temsil edildiğini gösteriyor.
- **Eksik:** İncelenen atlas/extension içinde bağımsız hedef kaydı bulunamadı. Ad taraması başka yüzeyin içindeki ayrıntının veya olası tüm eş adların yokluğunu kanıtlamaz.
- **Doğrulanmamış:** Semantik hedef veya ilgili kemik yüzeyi var; bağımsız temsil ya da konum henüz doğrulanmadı.

Bütün hedeflerde anatomik uzman incelemesi bekliyor. Geometri varlığından `full` sonucu çıkarılmadı. Toplam 65 hedef satırının 61’i mevcut, 3’ü kısmi, eksik işaretli hedef yok, 1’i doğrulanmamış. Bu toplam üç datasetin hedef satırlarını birleştirir; erkek atlasın geometri sayısı değildir. **Erkek atlas: 57 mevcut, 3 kısmi, eksik işaretli hedef yok, 1 doğrulanmamış; ayrı kadın pelvis: 3 mevcut hedef; ayrı iç kulak: 1 mevcut iki taraflı hedef.** Erkek atlasta mevcut 57 satırın 3’ü toplam altı yüzey referans noktasıdır; yeni bağımsız yüzey geometrisi sayılmaz.

| Bölge | Mevcut | Kısmi | Eksik | Doğrulanmamış |
| --- | ---: | ---: | ---: | ---: |
| Baş ve boyun — 9 erkek + 1 ayrı iç kulak hedefi | 10 | 0 | 0 | 0 |
| Toraks | 8 | 0 | 0 | 0 |
| Abdomen ve pelvis — 13 erkek + 3 ayrı kadın hedefi | 16 | 0 | 0 | 0 |
| Üst ekstremite | 15 | 2 | 0 | 1 |
| Alt ekstremite | 12 | 1 | 0 | 0 |

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
| Omurilik | Mevcut — doku gövdesi | `FMA7647`: FJ1737 merkez kanal + BP43-FJ4426 uzunlamasına sinir dokusu; kök/zar/segment ayrıntısı yok |
| Tiroid bezi | Mevcut | `FMA9603`: BodyParts3D 4.3 sağ/sol lob ve isthmus |
| Koklea, iki taraf — ayrı iç kulak referansı | Mevcut — ayrı dataset | `inner-ear-reference:left-cochlea`, `inner-ear-reference:right-cochlea`; erkek atlasına kayıt yok |

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
| Uterus — ayrı kadın pelvis referansı | Mevcut — ayrı dataset | `female-pelvis`, `hra-female:uterus-female`; 10 primary yüzey, erkek atlasta değil |
| Sol ovaryum — ayrı kadın pelvis referansı | Mevcut — ayrı dataset | `female-pelvis`, `hra-female:ovary-female-left`; resmi sol GLB |
| Sağ ovaryum — ayrı kadın pelvis referansı | Mevcut — ayrı dataset | `female-pelvis`, `hra-female:ovary-female-right`; resmi sağ GLB, bu çalışmada aynalama yok |

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
| Median sinirler | Kısmi — ana gövdeler | `atlas:left-median-nerve`, `atlas:right-median-nerve`; ayrı dallar dahil değil |
| Brakiyal pleksus | Kısmi — kökler hariç | `atlas:left-brachial-plexus`, `atlas:right-brachial-plexus`; her tarafta 3 gövde, 6 bölüm ve arka kordon |
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
| Siyatik sinirler | Kısmi — pelvis/uyluk gövdeleri | `atlas:left-sciatic-nerve`, `atlas:right-sciatic-nerve`; ayrı tibial/fibular devamlar yok |
| Medial menisküsler | Mevcut | Sağ/sol geometri `knee-structures.json` paketinde; uzman incelemesi bekliyor |
| Lateral menisküsler | Mevcut | Sağ/sol geometri `knee-structures.json` paketinde; uzman incelemesi bekliyor |
| Ön çapraz bağlar | Mevcut | Sağ/sol geometri `knee-structures.json` paketinde; uzman incelemesi bekliyor |
| Arka çapraz bağlar | Mevcut | Sağ/sol geometri `knee-structures.json` paketinde; uzman incelemesi bekliyor |

## Aktarım ilerlemesi — 22 Eylül güncellemesi

Median ve diz paketleri sahne kayıt listesine eklendi. Siyatik paketi kayıtlı; ayrı distal devamlar yok. İlk Z-Anatomy tiroid yüzeyi kabul edilmedi; onun yerine BodyParts3D 4.3 iki lob/isthmus paketi kayıtlı. Ayrı HRA kadın pelvis paketi teknik ve yerel görsel kontrolden geçti; bu kayıt yayın durumu veya uzman anatomik kabulü iddiası taşımaz. Aşağıdaki aday notları ilk kaynak incelemesinin teknik girdileridir; güncel ürün durumu yukarıdaki tablolardadır.

## İlk aktarım adaylarının teknik notları

“Hazır” kaynak nesne/dosyanın indirildiği ve kimliğinin bulunduğu anlamına gelir; yayıma hazır veya anatomik olarak onaylı anlamına gelmez. Kayıt/atıf, paket teknik kontrolü ve görünür yüzey incelemesi her aktarımda korunmalıdır.

1. **Median sinirler:** `Median nerve.l/.r`, CURVE, her biri 2 spline/20 kontrol noktası. İki musculocutaneous sinirde çalışan eğri aktarımı kullanılabilir; önkol/bilek uyumu ayrıca ölçülmeli.
2. **Diz paketi:** `Medial meniscus.l/.r` (37 polygon/yan), `Lateral meniscus.l/.r` (59), `Anterior cruciate ligament.l/.r` (808), `Posterior cruciate ligament.l/.r` (404). Ayrı yüzeyler indirilen Blender dosyasında var. Femur/tibia/patella ile yeni bölgesel kayıt ve yakın plan kontrol gerekir.
3. **Siyatik sinirler:** `Sciatic nerve.l/.r`, CURVE, her biri 3 spline/20 kontrol noktası. Üst kol dönüşümü alt ekstremiteye doğrulanmadan taşınmaz.
4. **Tiroid:** `Thyroid gland`, 84 vertex/68 polygon yüzey. Bez bağımsız aday olarak var; boyun kaydı ve ayrıntı yeterliliği incelenmeli.
## Kayıtlı landmark temsilleri

`upper-arm-landmarks.json` artık korakoid çıkıntı, supraglenoid tüberkül ve radius tüberozitesinin iki tarafına ait altı referans noktası içeriyor. Katalogdaki `surface_anchor`, bağımsız bir anatomik yüzey yerine kaynak tutunma yüzeyinden hesaplanmış noktayı ifade eder. Noktaların kaynakları sırasıyla `Coracobrachialis muscle.ol/.or`, `Long head of biceps brachii.ol/.or` ve `Biceps brachii muscle.el/.er` yüzeyleridir. Aynı kemik/kas koordinat kaydı uygulanmış; kemik bağlamı ve ölçülmüş artık uzaklıklar manifestte korunmuştur. Anatomik uzman incelemesi bekliyor.

Önceki `.i/.j` iki-vertex işaret adayları ana kaynak olarak reddedildi; sol taraftaki etiket ofset/transformları gerçek tutunma yüzeyleriyle uyuşmadı. Bu adaylar katalogda `rejected_for_anchoring` olarak tarihî kanıt için tutulur ve sonraki aktarım listesinde yer almaz. Gerçek altı anchor bu etiket çizgilerinden türetilmedi.

## Açık kalan belirli boşluklar

- **Omurilik ayrıntıları:** `FMA7647` artık mevcut merkez kanalına ek olarak BodyParts3D 4.3 `FJ4426` sinir dokusu gövdesini içerir. Tüm kök, zar ve segment ayrıntıları tamamlanmış sayılmaz; ilk Z-Anatomy küçük horn/white-matter yüzeyleri bu kapsamı tamamlamak için onaylanmış değildir.
- **Brakiyal pleksus ayrıntıları:** Kök demetleri kimlik belirsizliği nedeniyle tamamen hariç; 20 eğri/23 kavram kısmi referans olarak kayıtlı. Her tarafta 3 gövde, 6 bölüm ve arka kordon var. Medial/lateral kordonlar ve terminal dallar bu pakette yok. Boyun referanslarında 4,3–4,8 mm, ilk kaburgalarda 8,3–8,4 mm RMS fark bulundu; kaynak uç yakınlığı doğrulanmış anatomik temas/bağlantı değildir.
- **İç kulak ayrıntıları ve kaynak kapsamı:** İki koklea, iki birleşik vestibüler/semisirküler kompleks ve aynı kaynak temporal kemikleri ayrı referansta paketlendi. Koklea satırı iki koklea yüzeyinin varlığını gösterir; membranlar, duyu hücreleri veya Corti organını kapsamaz. Kaynak nesne kökeni arşiv bileşen atfından çıkarımdır: iç kulak NC-SA, temporal kemikler genel BY-SA kapsamını korur. Ticari kullanım veya bağımsız Dundee nesne doğrulaması iddiası yok.
- **Kadın pelvis kapsam sınırı:** Ayrı `female-pelvis` datasetinde uterus, iki bağımsız kaynak ovaryum ve kemik bağlamı mevcut. Uterus v1.2, ovaryumlar ve pelvis v1.3 resmi dijital nesnelerinden 27 yüzey paketlendi. Tam kadın vücudu, tüpler, bağlar, damarlar, mesane veya pelvis tabanı bu seçimle tamamlanmış değildir. Donör ID’si kaynakta verilmediği için tek birey kesinliği iddia edilmez.
- **Humerus orta iç tutunma alanı:** İki taraf `upper-arm-landmarks.json` dosyasındaki `unresolved` kayıtlarında; özel tutunma yüzeyi veya uygun işaret bulunamadı. Skapuladaki coracobrachialis başlangıç yüzeyi humeral tutunma yerine kullanılmadı. Kayıtlı konum yok; `unanchored_landmark` ve doğrulanmamış durumu korunuyor.

## Veri durumları ve kanıt sınırı

Muskülokutan, median ve diz paketleri `extensions/index.json` üzerinden yükleniyor; bilgi grafiği artık kayıtlı paketleri kaynak hash'leriyle birleştiriyor. Altı yüzey referans noktası landmark extension'ından okunuyor; iki humeral hedefin konumu bekliyor. Ana atlasın beş beyin parçası için eski `cardiac` değeri dosyada korunuyor; uygulama yüklemesinde ayrı düzeltme uygulanıyor.

Kaynak envanterindeki MESH taban polygon sayısı, Blender modifier sonrası üçgen sayısı veya anatomik kalite puanı değildir. Koleksiyon üyeliği innervasyon/komşuluk ilişkisi olarak kullanılmadı. Kaynakları indirmiş olmak bölgeler arasında koordinat eşitliği veya bütün lisansların çözülmesi anlamına gelmez.

- [Yerel temel denetim](2026-09-08-audit.md)
- [İndirilmiş kaynak denetimi](2026-09-08-open-assets-review.md) ve [hash/nesne kanıtı](2026-09-08-open-assets-evidence.json)
- [İki sinirin ölçülmüş kayıt raporu](asset-registration-upper-arm-nerves.md)
- [Pilot etiket kapsamı](labels-review.md)

Bu katalog diğer bölgeleri çevrilmiş, etiketlenmiş, geometrisi tamamlanmış veya anatomik olarak kabul edilmiş saymaz. Sonraki ilerleme ölçütü, bu hedeflerde çalışan ve incelenen model davranışıdır.

22 Eylül güncellemesi: Stilize Z-Anatomy tiroidi kabul edilmedi; yerine resmi BP3D 4.3 lob/isthmus yüzeyleri eklendi. Aynı kaynakta FJ4426 omurilik gövdesi bulundu ve mevcut merkezi kanal korunarak FMA7647 genişletildi. Yukarıdaki ilk Z-Anatomy aday değerlendirmeleri tarihî kaynak girdileridir.


## Dataset ayrımı ve kadın referansının kayıt sözleşmesi

Kadın üç hedefin `currentBindings` alanı boş kalır; bu alan yalnız erkek atlas kavram haritasında çözülür. Her hedefte `datasetId: female-pelvis`, `representation: separate_reference_geometry` ve `separateReference: { datasetId, conceptId, nameTr, sourceId, manifest, geometryPartIds }` vardır. Panel bu ayrı referansı açabilir; `hra-female:*` kimlikleri erkek bilgi grafiğine eklenmez. Uterus aggregate 10 primary yüzey içerir; ayrı cervicovaginal junction bağlam yüzeyi bu aggregate dışında kalır.

`summaryByDataset` erkek, kadın pelvis ve iç kulak hedeflerini ayrı sayar. `summaryByRegion` ve `summaryOverall` üç datasetin hedef satırlarıdır; erkek atlas geometri sayısı veya anatomi tamamlanma yüzdesi olarak kullanılamaz. Siyatik kayıtları da canlı `extensions/index.json` ve `sciatic-nerves.json` ile yeniden uzlaştırıldı: iki ana gövde mevcut olduğundan önceki `missing` kaydı `partial` yapıldı; ayrı distal tibial/common-fibular devamlar dahil değil.

Kaynak envanterinde `reference-female-pelvis` public manifest/binary/gzip hashlerini, dört `hra-...` kaydı ise resmi GLB hashleri, DOI, metadata/graph dosyaları ve CC BY 4.0 lisansını taşır. [Kadın pelvis kaynak incelemesi](female-pelvis-source-review.md) ve paket içindeki atıf belgesi sınırlamaları ayrıntılandırır. Yerel görsel kabul veya paket varlığı, yayına alınmış olma ya da anatomik uzman onayıyla eşit tutulmaz.


## Brakiyal pleksus kısmi referansı — kayıt ve etiketler

`brachial-plexus.json` paketi `extensions/index.json` üzerinden yüklenir: 20 kaynak eğri, 23 seçilebilir kavram. Kökler bütünüyle hariç tutulur. Görünür temsil notu yalnız iki aggregate için değil, paketteki bütün 23 kavram için kapsamı ve bölgesel yerleşim farklarını açıklar. Kaynak manifest/binary/üretici değiştirilmedi.

`data/anatomy/brachial-plexus.json` yalnız manifestte doğrulanan parça–yan grup ve yan grup–iki taraflı grup üyeliğini taşıyan 22 `part_of` ilişkisi içerir. Bunlar geometri gruplarıdır; kök düzeyi, innervasyon, sinir iletimi, fiziksel devamlılık veya damar/komşuluk ilişkisi eklenmedi. Anatomik uzman incelemesi bekliyor.

TR/EN/LA etiketleri aynı modülde 23 kimlik için saklanır ve `atlas-metadata.ts` tarafından okunur. İngilizce–Latince çiftleri sabit upstream TA2.csv kaynağının 6395, 6398–6406 ve 6416 kayıtlarıyla doğrulandı (SHA-256 `0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974`). Türkçe karşılıklar editoryal çeviridir. Latince temel terimler aynen saklanır, taraf L/R işaretiyle belirtilir; yeni Latince çekim üretilmez. Bu paket bütün pleksus anatomisinin veya tüm atlas çevirisinin tamamlandığı anlamına gelmez. [Ölçülmüş kaynak/yerleşim raporu](asset-registration-brachial-plexus.md).


## Ayrı iç kulak referansı

`coverage:cochlea` mevcut iki taraflı ayrı referans hedefidir. `currentBindings` boştur; `separateReference.datasetId: inner-ear-reference`, iki `conceptIds` ve `IE-COCHLEA-L/R` part kimlikleri taşır. Manifestte bulunmayan bir bilateral aggregate konsept üretilmedi. Bu referans `extensions/index.json` içine veya erkek bilgi grafiğine eklenmez.

`reference-inner-ear` kaynak kaydı public manifest/binary/gzip ve değişmemiş kaynak adayın hashlerini, tüm altı yüzeye uygulanan `(x,y,z) → (x,z,-y)` katı dönüşümü ve ayrı lisans kapsamlarını saklar. Kaynak göreli konumları korunur; uniform dönüşüm anatomik kayıt değildir. İç kulak için **CC BY-NC-SA 4.0**, temporal kemikler için **CC BY-SA 4.0** atıfları ayrı tutulur; paketin ticari olmayan kullanım sınırı kemikleri yeniden lisanslamaz. Kesin nesne soyu/sertifikası verilmediği için Dundee bağlantısının arşiv bileşen atfından çıkarım olduğu açıkça kaydedilir. Anatomik uzman incelemesi bekler; UI kabulü ve yayın root tarafından ayrı değerlendirilir.

Bu sınırlı 65 hedeflik listede artık “eksik” işaretli satır kalmaması bütün anatominin tamamlandığı anlamına gelmez: üç kısmi hedef, bir konumu doğrulanmamış hedef ve seçilmeyen anatomik yapılar sürmektedir.

## Etiket ve seçim güncellemesi — 22 Eylül

Kafatası hedefi artık `atlas:skull-bones`22 kemiklik seçime bağlı; kaynak `FMA46565`43 parçalık grubu değişmedi. Sayılan65 hedef ve 61/3/0/1 durumları aynı. Doğrudan83bağdaTR/EN etiket boşluğu yok;LA 4 bilinçli boşluk. Alt parça ve bütün atlas kapsamı için bu sonuç genellenmez. Rotator manşete26 kaynak ilişki ve8 geometrisiz sinir kavramı eklendi; bunlar65 hedefe 8 yeni model eklendiği anlamına gelmez.
