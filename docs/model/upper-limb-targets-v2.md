# Omuz, aksilla ve kol yapı hedefleri — v2

352 mevcut gereksinim korunur; [v1](upper-limb-targets-v1.md) tarihî gözlem olarak değişmez. [Makine kaydı](../../data/anatomy/regional-targets-upper-limb-v2.json), bağımsız üst ekstremite sinir referansından 80 ek ürün bağı taşır: 46 birincil sinir/grup, 24 sinir bağlamı ve 10 kemik bağlamı. 272 hedef kaydı aynıdır; önceki bütün temsiller, kimlikler, terim kanıtları, gereken ilişkiler ve uzman kriterleri korunur.

Hedef düzeyinde geometri gözlemi 132→178; altı tutunma referans noktası ayrı kalır. 166 hedefte pozitif temsil bağı bulunmadı; iki humeral konum çözümsüzdür. Bunlar kaynakta/anatomide yokluk veya tamamlanma sayısı değildir. Sıfır uzman kabulü; bütün bölge hücreleri açık. Yeni gözlemler ana gövde geometrisini değiştirmez.

Sekiz çoğul kas dalı hedefi yalnız aynı kapsamlı kaynak gruplarına bağlanır; tek tek numaralı dallar veya tam kas uçları değildir. Bilateral C5–T1 katkıları ve medial/lateral kordların 14 gereksinimi açık ve değişmeden kalır. Referanstaki 47 nesne bu sınırlı 352 hedefe zorla eşlenmez; başka bölge/kapsam incelemesi gerekir. Mevcut v1 Latin düzeltmeleri ve 18 kesin Latin boşluğu korunur.

[Kaynak eşleme kanıtı](../../data/model-candidates/upper-limb-target-bindings-v2/REVIEW.md) ile [ürün incelemesi](upper-limb-nerve-reference-review.md) farklı kabul aşamalarıdır. Temsil bağı kaynak üyeliği, taraf ve kullanılabilir seçimi gösterir; tam seyir, temas, ağ devamlılığı, D2 ayrıntı veya anatomik uzman kabulü değildir. Ana model ile ayrı referans aynı kaynak koordinatlarında birleşmiş sayılmaz.

Üretim: `python3 scripts/build-upper-limb-reference-targets.py`; yazmadan kontrol: `--check`. Üretici sabitlenmiş aday/v1 kimlik ve hash'lerini, public kavram/parça/etiket üyeliğini ve kayıtlı yerel üretim kabulünün giriş hash'lerini denetler. Canlı yayın ayrı teslim raporunda doğrulanır. [Genel envanter](model-inventory.md) tüm 508 alt/üst gereksinimi, bağsız kayıtlar dahil, bekleyen ayrıntı hücrelerine bağlar.
