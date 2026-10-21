# Atlas gösterim hazırlığı — 21 Ekim 2026

Bu kayıt güncel teslim durumunu taşır. [2 Ekim ve sonraki tarihî çalışma notları](progress-report-2026-10-02.md) korunur; bu kayıttaki yeni kanıtlar onların yerine geçmiş kabul edilmez.

## Hedef ve başlangıç

Burs başvurusunda gösterilebilecek, kaynak katkıları ve sınırları açık bir ürün: bağlantıdan açılış → arama/seçim → izolasyon/ilişki → geri → referans değiştirme → çalışma → kayıtlı sahneyi yeniden açma. [Sunum ve eksik kanıt planı](scholarship-readiness-2026-10-21.md) tanımlı demo ve sonraki insan değerlendirmelerini taşır.

Başlangıç kaynak SHA `fb39d24f08885e8369d060f1dc5200e57be3cc68`, dal `codex/skull-orientation`; entegrasyon dalı `codex/scholarship-readiness`. Fork `main` başlangıçta `10934178a86b15c58427c7381e4807a87eb38456` ve kaynak tabanının atasıdır. Canlı `release.json` başlangıçta `cf05a4e62a9d9cc9be700df232c88d612b1a1cc6`: yerel kafatası/kamera düzeltmeleri canlıda henüz yoktu. Pages ayarı `gh-pages` köküdür. Tarihî handoff'un 128 satırlık mevcut değişikliği ve izlenmeyen araştırma/ekran/log dosyaları diğer çalışmalar olarak korundu; bu teslimin kaynak commit'ine alınmaz.

Root entegrasyon ve kapanış sahibidir. Kullanıcı isteğiyle üç Astra ajanı belgeler, ziyaretçi rehberi ve yükleme güvenilirliğini bağımsız dosya sahiplikleriyle uyguladı. Yeni geometri, anatomik ilişki, öğrenme puanlama kuralı veya kaynak lisansı değişmedi.

## Uygulanan iyileştirmeler

- README, kapsam sözleşmesi ve anatomi veri rehberi aktif kaynaklarla uzlaştırıldı; tarihî durumlar güncel rehberden ayrıldı. Genel katalog kendi üreticisinden yeniden oluşturulur.
- İsteğe bağlı başlangıç rehberi üç kısa kullanıcı adımını, proje/upstream katkısını ve bileşen kaynaklarını gösterir. Sol kord/akciğer atıfları erişilebilir; genel atıf belgesi mevcut kadın pelvis paketini tarihî tüm-vücut paketinden ayırır.
- Bir model parçası indirilemediğinde kardeş işler ve kuyruk durdurulur. İptal/decode yarışları ve WebGL kaybı geç tamamlanan yüklemeyle hata mesajını silemez. Yeniden deneme seçilen referansı korur.

## Doğrulama ve yayın

macOS, pinned Node 22.23.2: `npm run check:ci` PASS; **33/33 tests**, TypeScript, knowledge/explorer/inventory freshness, atlas/interaction validation, production build, development QA exclusion and transfer budget. [Final log](../../output/playwright/showcase-2026-10-21/check-ci-final.log). JavaScript gzip 398,854 bytes /450,000 budget; bundler large-chunk advisory remains. First full run passed 32 tests; repeated after the study-retry fix and its new regression test changed the implementation.

Real Chrome computer use: initial live uppercase `SİNİR` search; Kalp83 → isolation → Sol atriyum boşluğu1 → Geri restored Kalp83. Local new visitor guide at390×844 and320×568; heading focus/readability and guide→search input focus passed after reproducing/fixing a dialog-close focus race. 320×568 skull22 → Mandibula1 → isolate rendered the selected jaw above its controls. Narrow layouts use a temporary iframe with exact CSS viewport dimensions, not a physical device or touch emulation.

Production build, temporary test-only local HTTP server: one intentional503 on inner-ear gzip → visible error → Yeniden dene → same inner-ear reference loaded six actual surfaces. [Rendered recovery](../../output/playwright/showcase-2026-10-21/retry-inner-ear.png). Temporary QA fixtures are outside the product build.

Production-only local fixture exposed a button invoking the actual `WEBGL_lose_context` extension. Whole-skull Hatırla1/22 → context loss → disabled answer controls + persistent error → Yeniden dene → same1/22 with highlighted ethmoid and active answers, then deliberate Mandibula answer produced correct wrong-answer feedback. [Recovery screenshot](../../output/playwright/showcase-2026-10-21/study-context-recovery.png). This tests recovery from injected context loss, not spontaneous hardware behavior. The added study regression also covers an empty concept map while preserving the stored question.

First integrated source `f3fbc4b4468e69dff795bbe12b7b2e8be4dc000f` was pushed non-force to fork main and integration branch. [Code CI39604006271](https://github.com/ismailatilan-44/human-atlas/actions/runs/39604006271) and [Pages39604100914](https://github.com/ismailatilan-44/human-atlas/actions/runs/39604100914) passed; static revision `f146ba96818f33b661e649c919ffedf2a6549534`. Live release matched source; [HTML/JS/CSS/inner-ear gzip hashes](../../output/playwright/showcase-2026-10-21/live-hashes.json) matched the clean release checkout.

On that live build: guide→search with focused input, uppercase SİNİR, Kalp83→isolation→atrium1→Back83, all four independent references loaded/rendered, skull→study inspection→save/return and own saved skull scene→inner-ear→restore passed. Live320×568 and390×844 mandibula isolation, separation and reassembly rendered correctly. [Guide](../../output/playwright/showcase-2026-10-21/live-guide.png), [320](../../output/playwright/showcase-2026-10-21/live-320-mandible.png), [390](../../output/playwright/showcase-2026-10-21/live-390-mandible.png).

**Reopened landscape criterion:** live844×390 revealed the study launcher obscuring the lower skull and an older CSS rule hiding search/Back. [Failure](../../output/playwright/showcase-2026-10-21/live-landscape.png). Astra corrected only short-landscape inspector CSS: launcher hidden while inspecting, compact navigation in the left header, identity below it. Actual local844×390 now shows the whole skull unobstructed and the search control opens the focused search UI. [Full gate repeated after CSS change](../../output/playwright/showcase-2026-10-21/check-ci-landscape.log):33/33 and all gates PASS, JS budget unchanged. Source `7654d6c7b6bff160d865ffb35399892cdce07a0c` also passed [CI39604754137](https://github.com/ismailatilan-44/human-atlas/actions/runs/39604754137) and [Pages39604875610](https://github.com/ismailatilan-44/human-atlas/actions/runs/39604875610). An additional affected-boundary test568×320 exposed the identity block overlapping the skull and the old340px minimum viewport height. The final tiny-landscape CSS removes that minimum and hides identity only during inspection; closing inspection restores reference selection. [Local568 recovery](../../output/playwright/showcase-2026-10-21/local-568-landscape-fixed.png) was visually inspected and close→selector recovery passed. This final CSS-only boundary adjustment reuses the33-test runtime evidence; publication rebuild and remote CI cover its final source. Final live recheck follows in the closing entry below.

## Açık sınırlar ve sonraki iş

Anatomik uzman kabulü, fiziksel telefon/iOS/Android ve ekran okuyucu kabulü, öğrenme etkisi ve kalan bölgesel kapsam açık. Dar masaüstü tarayıcı görünümü fiziksel mobil cihaz testi değildir. Burs programı, başvuru biçimi/takvimi ve kişisel katkı beyanı verilmedi; başvuru gönderilmedi. Sonraki iş: [insan değerlendirme paketindeki](learning-review-packet.md) sınırlı akışı bir öğrenci ve anatomist ile değerlendirmek.

Ölçüm: goal başlangıcından son canlı kabul/temizlik öncesi ölçüme kadar1465 saniye (24 dakika25 saniye); son doküman commit/push süresi hariç. Aktif emek ve önceki çalışmaların süresi bilinmiyor. Yeniden çalışma: rehber→arama odak yarışı, aktif çalışma retry inceleme bulgusu, iki yatay ekran çakışması ve önbellek/yayın dosyası uyumsuzluğu. Bekleme: Git ağ aktarımı ve Pages dağıtımları. Aynı kontroller yalnız bu kaynak değişimleri nedeniyle tekrarlandı.


## Önbellekte kalan sayfanın yayın güvenilirliği

Son yayın denemesi, Pages HTML yanıtında `Cache-Control: max-age=600` bulunduğunu ve önceki `assets/index-Cx6lOCmP.js` / `assets/index-DQw3vV3e.js` isteklerinin404 döndüğünü kanıtladı. Daha önce açılmış test çerçevesi eski düzeni korudu, yeniden açılışında boş kaldı; doğrudan yeni sayfa güncel bundle ile çiziliyordu. Bu, eski HTML'in silinmiş bundle'a işaret edebilmesiyle tutarlı gerçek dağıtım riskidir.

Astra yayın düzeltmesi son24 saatteki sürümlerin hash'li `assets/` dosyalarını ve pencere başında hâlâ sunulan önceki sürümü Git geçmişinden geri getirir. Her release kendi özgün build dosyalarını listeler; eski taşınmış dosyalar sonsuza dek birikmez. Yeni build aynı yolu kazanır; commit edilmemiş public çıktılar dışarıda kalır; temiz kaynak/revision/non-force kontrolleri korunur. Bağımsız Astra incelemesi blocker bulmadı. Gerçek `file://` Git remote üzerinden iki regresyon testi yeni/güncel/eski sınır sürümlerini, silinmiş bundle kurtarmayı, süresi dolmuş taşınan dosyaları ve exporter dışlamasını doğruladı. Son tamCI ve yayın sonucu kapanışa eklenecek.


## Nihai teslim ve canlı kabul

**Yayındaki kaynak:** `9ccaa60b661f36a95f2cd10355882033eaa8c987`. **Statik dal:** `790dabb9c6d38aab84d7c1141f2fcbda18a77a10`. [Canlı atlas](https://ismailatilan-44.github.io/human-atlas/), [GitHub kodCI39605870022](https://github.com/ismailatilan-44/human-atlas/actions/runs/39605870022) ve [Pages39606073028](https://github.com/ismailatilan-44/human-atlas/actions/runs/39606073028): başarılı. `release.json` kaynak SHA'yı ve bu build'in iki hash'li dosyasını bildirir. [Son HTTP/hash kanıtı](../../output/playwright/showcase-2026-10-21/live-final-hashes.json): HTML/JS/CSS temiz checkout build'iyle aynı; üç eski JavaScript URL'si (önceki uzun süre yayındaki sürüm dahil) artık200 döner.

[Son tam kontrol](../../output/playwright/showcase-2026-10-21/check-ci-publisher.log) Node22.23.2 üzerinde **35/35 test ve tüm check:ci kapıları PASS**. Son iki test yayın önbelleği regresyonudur. Anatomi/model/çalışma semantiği önceki kabulden değişmedi; son dağıtım değişikliği runtime JS/CSS hash'lerini değiştirmedi. Tarihî/yerel/ilk yayın kanıtları yukarıda kendi sürümlerine bağlıdır.

**Son gerçek tarayıcı gözlemi:** normal Pages URL'sini yeniden açan önce boş test çerçevesi atlası yükledi. Masaüstünde kafatası22 çizildi;568×320 ve844×390'da model kontrollerin altında kalmadı, TR/Geri/arama/Rehber erişildi ve arama girişi odaklandı. [Masaüstü](../../output/playwright/showcase-2026-10-21/live-skull-final.png), [568 yatay](../../output/playwright/showcase-2026-10-21/live-568-final.png), [844 yatay](../../output/playwright/showcase-2026-10-21/live-844-final.png). Son [canlı konsol kaydı](../../output/playwright/showcase-2026-10-21/live-console.json): masaüstü ve responsive çerçevede0 hata/0 uyarı. Önceki canlı320/390, tüm referanslar, arama/izolasyon/ilişki/geri, kafatası ayır/yerine döndür, çalışma aç/geri ve sahne referanslar arası/yenileme testleri aynı runtime davranışı için korunur. Masaüstü gerçek sürükleme kafatasının açısını değiştirdi. Kullanıcının eski `Canlı sol talus LA` kaydı korundu; yalnız bu testin oluşturduğu sahne kaydı kaldırıldı.

**Teslim sınırı:** bu sonuç burs için gösterilebilir mevcut prototipin teknik yolculuğudur; bütün anatominin tamamlandığı, fiziksel telefonun veya anatomistin kabul ettiği, öğrenme etkisinin kanıtlandığı anlamına gelmez. [Demo/katkı/sonraki kanıt planı](scholarship-readiness-2026-10-21.md) bu ayrımı korur. Sonraki tek paket: tanımlı demo hedeflerini gerçek öğrenci ve anatomistle [insan değerlendirme paketi](learning-review-packet.md) üzerinden gözlemlemek; başvuruya özel beyan için program ölçütleri ve kişinin doğrulanabilir katkısı gerekir.

Önceden değişmiş2 Ekim handoff'u128 ek satırla aynen ayrı bırakıldı; diğer araştırma/log/ekran dosyaları commit'e alınmadı. Göreve ait yerel sunucular kapatıldı; temiz yayın checkout'u arşivlenir. Bu kapanış yalnız belge ve ekran kanıtıdır; yayındaki ürün revision'ı yukarıdaki SHA'dır.
