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

Publication/live acceptance remains pending at this source commit; final live revision and results will be appended after deployment.

## Açık sınırlar ve sonraki iş

Anatomik uzman kabulü, fiziksel telefon/iOS/Android ve ekran okuyucu kabulü, öğrenme etkisi ve kalan bölgesel kapsam açık. Dar masaüstü tarayıcı görünümü fiziksel mobil cihaz testi değildir. Burs programı, başvuru biçimi/takvimi ve kişisel katkı beyanı verilmedi; başvuru gönderilmedi. Sonraki iş: [insan değerlendirme paketindeki](learning-review-packet.md) sınırlı akışı bir öğrenci ve anatomist ile değerlendirmek.

Ölçüm: başlangıç goal zamanından itibaren duvar süresi kapanışta kaydedilecek; aktif emek ve önceki çalışmaların süresi bilinmiyor. İlk yeniden çalışma nedeni rehber→arama geçişinde gerçek tarayıcıda bulunan kapanış/odak yarışıdır.
