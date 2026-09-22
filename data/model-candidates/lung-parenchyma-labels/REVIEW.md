# Akciğer segment parankimi — 17 kavram etiket adayı

22 Eylül 2026. Yalnız `lung-surfaces/lung-parenchyma.json` içindeki **17 segment-parankim kavramı / 18 kaynak yüzeyi** için 17 yeni TR/EN etiketi hazırlandı. Akciğer/lob aggregate kavramlarına yeni etiket eklenmedi. Aktif labels, app veya sources dosyaları değiştirilmedi.

Türkçe görüntü adı “taraf + akciğer + lob + segment parankimi” biçimindedir. Taraf/lob bilgisi resmi 4.3 `part_of` eşlemesine göre aday lob üyeliğinden doğrulandı. `side:null` tutuldu; Türkçe ad zaten tarafı içerdiği için mevcut yardımcı ikinci bir önek eklememelidir. İngilizce alan ve `sourceEnglish` özgün kaynak adını aynen korur; sonradan türetilmiş İngilizce anatomik kimlik oluşturulmaz. Taraf/lob bağlamı `context` alanında ayrıca bulunur.

**FMA27368 apikoposterior segment parankimi iki yüzeydir:** BP43-FJ6595 ve BP43-FJ6597. Tek kavram korunur, iki segment diye bölünmez. Diğer 16 kavram birer yüzeylidir. Yeni segment numarası, eksik yüzey veya medial bazal segment varsayılmadı.

## Kimlik ve kaynak doğrulaması

18 yüzeyin gerçek OBJ başlığındaki File ID, Concept ID ve English name; aday parçalar ve resmi `FMA2Obj.txt` üyelikleriyle karşılaştırıldı. Legacy CSV katalog `fma_id` alanı bu yüzeylerde **FMA14065 ata kimliğini** taşıyor; kanonik yaprak kimliği olarak kullanılmadı. Bu ayrım önceki `source-mapping-review.json` incelemesiyle uyumludur. Her yüzeyin OBJ başlık kanıtı bu teslimin evidence dosyasında tutuldu.

Lob bilgisi kaynak lob `part_of` üyeliğinden gelir. Daha dar parankim aggregate gruplarında önceden kaydedilen üyelik uyuşmazlıkları düzeltilmiş gibi gösterilmedi; aynı kaynak incelemesi korunur. Etiket doğrulaması anatomik eksiksizlik veya mesh doğruluğu onayı değildir. Türkçe karşılıklar editoryaldir, uzman incelemesi bekler.

## Latince sınırı

Pinned TA2.csv içinde 3280–3314 aralığındaki bronkopulmoner segment terimleri incelendi. Bunlar segmentin adıdır; kaynak FMA kimlikleri ise segmentin **parankimini** adlandırır. Tam kapsamı karşılayan Latince terim doğrulanmadığından tüm `la` alanları `null`. “Segmentum …” doğrudan parankim etiketi yerine konmadı; yeni “Parenchyma …” Latince tamlaması üretilmedi. Bu, bütün literatürde terim olmadığı iddiası değildir.

| FMA | Türkçe aday | Kaynak yüzey sayısı |
|---|---|---:|
| FMA27368 | Sol akciğer üst lob — apikoposterior segment parankimi | 2 |
| FMA27394 | Sol akciğer alt lob — posterior bazal segment parankimi | 1 |
| FMA27374 | Sol akciğer üst lob — anterior segment parankimi | 1 |
| FMA27375 | Sol akciğer üst lob — üst lingular segment parankimi | 1 |
| FMA27376 | Sol akciğer üst lob — alt lingular segment parankimi | 1 |
| FMA27386 | Sol akciğer alt lob — superior segment parankimi | 1 |
| FMA27392 | Sol akciğer alt lob — anterior bazal segment parankimi | 1 |
| FMA27390 | Sol akciğer alt lob — lateral bazal segment parankimi | 1 |
| FMA27369 | Sağ akciğer üst lob — apikal segment parankimi | 1 |
| FMA27393 | Sağ akciğer alt lob — posterior bazal segment parankimi | 1 |
| FMA27371 | Sağ akciğer üst lob — posterior segment parankimi | 1 |
| FMA27373 | Sağ akciğer üst lob — anterior segment parankimi | 1 |
| FMA27452 | Sağ akciğer orta lob — lateral segment parankimi | 1 |
| FMA27448 | Sağ akciğer orta lob — medial segment parankimi | 1 |
| FMA27385 | Sağ akciğer alt lob — superior segment parankimi | 1 |
| FMA27391 | Sağ akciğer alt lob — anterior bazal segment parankimi | 1 |
| FMA27389 | Sağ akciğer alt lob — lateral bazal segment parankimi | 1 |

## Teslim ve tekrar üretim

`proposals.json` aktarılabilir etiketleri; `source-evidence.json` kaynak kimlik/ad, lob üyeliği, OBJ başlıkları ve hashleri; `validation.json` kontrol sonuçlarını içerir. `prepare-proposals.py` yalnız bu aday klasörüne yazar. `python3 data/model-candidates/lung-parenchyma-labels/prepare-proposals.py` komutu yeniden üretir; mevcut etiketler sonradan değişirse yeni snapshot oluşacağını dikkate alın.
