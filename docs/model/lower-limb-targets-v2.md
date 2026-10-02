# Alt ekstremite yapı hedefleri — v2

Bu sürüm **104 sağ/sol proje hedefi** taşır: [v1'in](lower-limb-targets-v1.md) 66 hedefi ve kimlikleri aynen korunur; 10 metatars ve 28 falanks için 38 bireysel D1 hedef eklenir. Liste eksiksiz değildir; 104 kaynak bağı, sıfır anatomik uzman kabulü vardır. Hiçbir kapsam hücresi kapanmaz.

[Makine listesi](../../data/anatomy/regional-targets-lower-limb-v2.json), [kaynak audit'i](../../data/model-candidates/foot-bone-targets-v1/REVIEW.md) ve [referans ilişki kanıtı](../../data/model-candidates/foot-reference-relationships-v1/REVIEW.md) kimlik, taraf, parmak, falanks düzeyi, dataset ve açık kabul koşullarını ayrı tutar. Her yeni hedef ana gövdede ve bağımsız referansta birer ayrı parçaya bağlıdır; iki gövde birbirine kayıtlı sayılmaz.

| Yeni hedef | Parmak/metatars | Taraf sayısı | Toplam hedef |
| --- | --- | ---: | ---: |
| Metatars kemiği | I–V | 2 | 10 |
| Proksimal falanks | I–V | 2 | 10 |
| Orta falanks | II–V | 2 | 8 |
| Distal falanks | I–V | 2 | 10 |

Başparmak için orta falanks hedefi açılmaz. Parmak ve taraf özel alanlardır; generic TA2 1496/1510/1511/1512 kimlikleri özel digit kimliği yapılmaz. Birinci/beşinci metatarsın dört taraflı exact Latin adı vardır; diğer 34 bireysel Latin etiket çözümlenmemiştir. Ana modeldeki on kaynak parmak ebeveyni sadece iki/üç falanksı, iki foot-proper ebeveyni sadece beş metatarsı seçer; bütün parmak veya ayak dokusu diye sunulmaz. İki ayak ebeveyni yalnız 26 kemik seçer; bu kapsam ve doğrulanmış Foot/Pes adı ayrı kaydedilir.

Ana gövdenin 38 mevcut PART-OF bağı korunur; yeni ilişki veya kaynak üyeliği eklenmez. Ayrı referansta 48 symmetric/nontransitive eklem ilişkisi ve 12 bağ→kemik bağlantısı vardır. Eklem yüzeyi, kapsül, kıkırdak, doğrulanmış fiziksel temas ve tutunma koordinatı bu bağlantılarla üretilmez. Her target'ın gereken ilişki/kapsam ve görsel incelemesi açık kalır.

Yeni liste `python3 scripts/build-foot-bone-targets.py` ile üretilir; `--check` giriş hash'lerini ve deterministik çıktıyı doğrular. Önce source audit üreticisi kendi güncel girişleriyle üretilebilir. Kontrol 104 benzersiz ID, değişmeyen 66 eski kayıt, 38 yeni hedefin iki dataset içindeki exact tek-parçalı üyeliği ve aktif 52 ana etiketin proposal eşitliğini kapsar; anatomik uzman veya bütün bölge kabulü değildir.

Sonraki açık işler: sesamoidler, ayrı eklem/tutunma bölgeleri, iç ayak kasları, tendon/fasya/retinakulum, tam eklem desteği, damar/lenf ve ince sinir dalları; bütün vücudun diğer bölge hedefleri de açılmaya devam eder. v1 makine/doküman kaydı tarihî ilk kapsam olarak korunur; güncel envanter v2'yi kullanır.
