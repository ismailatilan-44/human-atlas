# Alt ekstremite yapı hedefleri — v3

Bu sürüm **136 proje hedefi** taşır: [v2'nin](lower-limb-targets-v2.md) 104 hedefi ve değerleri aynen korunur; 32 kaynak kapsamlı ayak hedefi eklenir. Otuz hedef kas nesnesi/başı/grubu, ikisi sesamoid grubudur. Hepsinde gözlenen kaynak bağı vardır; **sıfır anatomik uzman kabulü**. Liste eksiksiz değildir ve hiçbir bölge/kapsam hücresi kapanmaz.

[Makine kaydı](../../data/anatomy/regional-targets-lower-limb-v3.json), [kaynak geometri](../../data/model-candidates/foot-soft-tissue-source-audit-v1/REVIEW.md) ve [etiket/ilişki incelemesi](../../data/model-candidates/foot-soft-tissue-metadata-v1/REVIEW.md) ayrı kimlik, kapsam ve açık koşulları korur. Önceki v1/v2 kayıtları tutulur; güncel envanter sonraki [v4 hedeflerini](lower-limb-targets-v4.md) kullanır; v3'ün 136 kimliği korunur.

Referansta iki taraflı kaynak kasları, ayrı flexor hallucis brevis/adductor hallucis başları ve çoğul interosseöz/lumbrikal gruplar vardır. Grubun birkaç bağlı bileşeni olması numaralı anatomik kimlik kanıtı değildir. Lumbrikal kaynak grubu tek bağlı bileşendir; dört ayrı kas kabul edilmez. Her sesamoid seçimi iki bağlı bileşeni birlikte içerir; medial/lateral kimlik atanmaz. Ana modelin zaten mevcut dört lumbrikal ve üç plantar interosseöz kası her tarafta kendi bireysel kimlikleriyle kalır; iki kaynak eşdeğer geometri değildir. 28 yeni hedefin ana kaynakta da gözlenen bağları vardır; EDB/dorsal interosseöz ana eşlemesi bu sınırlı denetimde çözümlenmemiştir, yokluk iddiası değildir.

İki bütün adlandırılmış kas için 12 referans ve 8 ana model başlangıç/tutunma/innervasyon bağlantısı kaynakla açılır. Bütün kemiğe geçiş tutunma footprint'i değildir; kas başlarına/gruplarına ilişki mirası uygulanmaz. Diğer gerekli kas ilişkileri, eklem destekleri, ince dallar, ayrı numaralı grup/kemik kimlikleri ve uzman incelemesi açıktır.

Üretim: `python3 scripts/build-foot-soft-tissue-targets.py`; yazmadan güncellik kontrolü: `--check`. Kontrol 104 eski hedefin aynen korunmasını, 136 benzersiz kimliği, dataset içindeki exact parça üyeliğini ve yeni aktif etiketlerin dondurulmuş kaynak önerisine eşitliğini kapsar. Anatomik veya bütün bölge kabulü değildir.
