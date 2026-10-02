# Önkol, el bileği ve el hedefleri — v1

502 sağ/sol gereksinim aktif iş envanterine alındı:162 kemik/eklem/destek,176 kas/tendon/fasya,140 sinir/damar/lenf,24 kompartıman/geçit.162 D1 ve340 seçilmiş D2 hedefi; eksiksiz müfredat veya tamamlanma paydası değildir. [Makine kaydı](../../data/anatomy/regional-targets-forearm-hand-v1.json) [adayın](../../data/model-candidates/forearm-hand-target-inventory-v1/REVIEW.md) bütün502 kaydını aynen korur.

188 hedefte210 kaynak üyeliği gözlemi vardır:160 ana gövde ve50 bağımsız üst ekstremite referansı.314 hedefte bu sınırlı denetimde pozitif bağ bulunmadı; kaynakta/anatomide yokluk değildir.22 tekil lumbrikal/interosseöz hedefi, birleşik kaynak gruplarına bağlanmaz; yalnız ilgili grup kanıtı taşır. Sekiz kas bütününün kaynak başları bütün kas geometrisi yerine geçmez. Bu envanter yeni geometri/etiket/ilişki veya bölgesel/uzman kabulü eklemez.

Numeric terimler ve özgün satırlar korunur. Asterisk kaynak uzantıları numeric TA2 gibi sunulmaz;2486/4644/4646 şüpheli Latin değerleri kanıt olarak saklanır, aday gösteriminde verilmez. Grup, taraf, digit ve parça kapsamları ayrı kalır. Mevcut ilişki kimlikleri tarihî kanıttır; başka dataset'e yeni ilişki oluşturmaz.

Üretim `python3 scripts/build-forearm-hand-targets.py`; yazmadan `--check`. Üretici aday kimliklerini ve210 gözlemin güncel manifest kavram/parça/metadata eşliğini denetler. Adayın `build.py --check` kontrolü kendi frozen snapshot'ını kullanır; tarihî gözlem yeni aktif kaynak değişiminden bağımsızdır. [Genel envanter](model-inventory.md) tüm1.010 alt/üst/önkol gereksinimini bağsız hedefler dahil208 bekleyen hücreye bağlar. Kaynak seyri/teması, tekil ayrıntı ve uzman kabulü açık kalır. Sıradaki kaynak denetimi tekil intrinsik el kasları ve el bileği destekleridir.
