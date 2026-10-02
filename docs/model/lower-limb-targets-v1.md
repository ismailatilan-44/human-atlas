# Alt ekstremite yapı hedefleri — ilk bireysel liste

Bu sürüm 66 sağ/sol proje hedefini, 33 kesin TA2 teriminden açar. D1 ve seçilmiş D2 için **eksiksiz olmayan başlangıç listesidir**; bütün bölge veya bütün P1 kabulü değildir. Gereken ayrıntı ve taraf, uzman/müfredat incelemesi bekleyen proje gereksinimidir.

48 hedefte mevcut kaynak kavramı veya bağımsız referans nesnesiyle gözlenen parça bağı vardır; 18 hedef henüz bağlanmamıştır. Bu sayılar anatomik kabul veya tamamlanma yüzdesi değildir. Kaynak üyelikleri aynen saklanır. İsim eşleşmesi bağımsız alt geometriyi, doğru konumu veya resmî TA2–FMA eşlemesini kanıtlamaz.

[Makine listesi](../../data/anatomy/regional-targets-lower-limb-v1.json), terim/satır kimliği, taraf, gereken ayrıntı, dataset, kaynak kavramı ve parça bağlarını, ilişkileri ve açık kabul koşullarını taşır. `python3 scripts/build-lower-limb-targets.py` üretir; `--check` dosyaları değiştirmeden güncelliği doğrular. Sabit TA2 kaynağı önceki intake altındaki yerel dosyadır; SHA doğrulanmadan üretim yapılmaz.

| Terim | TA2 | Ayrıntı | Sol / sağ gözlenen bağ sayısı |
| --- | ---: | --- | --- |
| Tibia | 1397 | D1 | 2 / 2 |
| Fibula | 1427 | D1 | 2 / 2 |
| Patella | 1390 | D1 | 2 / 2 |
| Talus | 1448 | D1 | 2 / 2 |
| Calcaneus | 1468 | D1 | 2 / 2 |
| Navicular bone | 1484 | D1 | 1 / 1 |
| Cuboid bone | 1489 | D1 | 1 / 1 |
| Medial cuneiform bone | 1486 | D1 | 1 / 1 |
| Intermediate cuneiform bone | 1487 | D1 | 1 / 1 |
| Lateral cuneiform bone | 1488 | D1 | 1 / 1 |
| Tibialis anterior muscle | 2644 | D1 | 1 / 1 |
| Extensor digitorum longus | 2645 | D1 | 1 / 1 |
| Extensor hallucis longus | 2650 | D1 | 1 / 1 |
| Fibularis longus muscle | 2652 | D1 | 1 / 1 |
| Fibularis brevis muscle | 2653 | D1 | 1 / 1 |
| Tibialis posterior muscle | 2666 | D1 | 1 / 1 |
| Flexor digitorum longus | 2667 | D1 | 1 / 1 |
| Flexor hallucis longus | 2668 | D1 | 1 / 1 |
| Soleus muscle | 2660 | D1 | 1 / 1 |
| Tibial nerve | 6582 | D1 | 1 / 1 |
| Common fibular nerve | 6571 | D1 | 1 / 1 |
| Deep fibular nerve | 6579 | D2 | 0 / 0 |
| Superficial fibular nerve | 6574 | D2 | 0 / 0 |
| Sural nerve | 6586 | D1 | 0 / 0 |
| Medial plantar nerve | 6590 | D2 | 0 / 0 |
| Lateral plantar nerve | 6593 | D2 | 0 / 0 |
| Anterior tibial artery | 4708 | D1 | 1 / 1 |
| Posterior tibial artery | 4721 | D1 | 1 / 1 |
| Fibular artery | 4727 | D1 | 0 / 0 |
| Popliteal artery | 4699 | D1 | 1 / 1 |
| Anterior talofibular ligament | 1919 | D2 | 0 / 0 |
| Posterior talofibular ligament | 1920 | D2 | 0 / 0 |
| Calcaneofibular ligament | 1921 | D2 | 0 / 0 |

Tibia/fibula/patella/talus/calcaneus iki ayrı gövdeye ait temsillerle kayıtlıdır; geometrileri birleştirilmez. Tibial/ortak fibular sinirler ayrı alt ekstremite referansındadır. Yeni referansın ana gövdeye distal kaydı kabul edilmemiştir. Arter kavramlarının birden çok parça içermesi açıkça listelenir; dal kapsamı ayrıca denetlenecek.

Ayak parmak/metatars kemikleri, iç kaslar, gastrocnemius başları, tendon/fasya/retinakulum, tam eklem desteği, ven/lenf, ince sinir dalları ve D3 hedefleri açılmaya devam edecek. Sıfır uzman kabulü vardır; kayıtlar hiçbir kapsam hücresini kapatmaz. Sonraki somut iş: bağlanmamış distal sinir ve ayak bileği bağ hedeflerini kaynak alt nesneleriyle denetlemek.

Doğrulama: 66 benzersiz hedef, 33 kesin TA2 terim/satır çifti, elle seçilmiş mevcut kaynak kavramlarının tam ad karşılıkları ve tüm gözlenen parça bağlarının kendi manifestinde çözülmesi. Bu kontrol geometri/görsel/uzman kabulü değildir.
