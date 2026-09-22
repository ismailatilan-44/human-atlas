# Toraks ve abdomen-pelvis — tek adımlı komşu etiketleri

22 Eylül 2026. Bu teslim entegrasyon öncesi adaydır; aktif etiket, grafik, uygulama veya kaynak dosyaları değiştirilmedi. En fazla 40 yeni kavram sınırı içinde **23 yeni TR/EN/LA kayıt** önerildi, **23 kavram gerekçeleriyle bekletildi**. Kapsam atlasın tamamı değildir.

## Denetim yöntemi

Gerçek `app/knowledge.ts` içindeki `relationshipsFor` ve `app/reference-datasets.ts` içindeki `datasetLabel` esbuild ile geçici modüle paketlenip çalıştırıldı. Toraks ve abdomen-pelvis coverage bölgelerindeki **22 erkek sahnesi başlangıç kavramından bir ilişki adımı** ile **46 benzersiz uç** elde edildi. Sağ ve sol ayrı sayıldı. 46 ucun tamamı sentinel kontrolünde TR/LA fallback kullandı. Güncel 155 etiket kaydı, brachial labels ve reference dispatcher çalışma zamanında hesaba katıldı. Ana manifest kavramları ad/geometri çözümlemesinde grafiğin ek varlıklarıyla birleştirildi.

Üç kadın pelvis hedefinin ayrı dataset referansları kaydedildi; uygulamadaki gibi erkek grafiğe taşınmadı. Bu datasetlerde erkek relationshipsFor yürüyüşü yapılmadı. Akciğer lobar bronşları ve ek kalp duvarları için ikinci ilişki adımına geçilmedi. Bu yüzden istenen öncelikler arasında olsalar bile bu doğrudan komşu kümesinde olmayan yapılar listeye alınmadı.

## Kaynak ve anlam sınırları

46 FMA kimliği/adı resmi indirilmiş BodyParts3D IS-A/PART-OF ad tablolarıyla eşleşti. 23 önerinin Latince alanı pinned [TA2.csv](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv) satırından birebir kopyalandı. İngilizce sourceEnglish korunur; upper/superior, lower/inferior, arch/aortic arch gibi açık eşanlam/kelime sırası eşlemeleri evidence içinde kaydedildi. Bu lexical eşleşme bağımsız mesh veya uzman onayı değildir. `ta2TableId` upstream CSV kimliğidir. Yeni FIPAT yayınevi PDF doğrulaması iddia edilmez. Türkçe karşılıklar ve aliaslar editoryaldir.

**Dokuz aday temsil notu gerektirir.** Sağ/sol karaciğer lobu kaynak grupları 17/25 yüzey seçer: damar/safra ağacı ve solda kaudat lob bulunur; bunlar bağımsız tam lob parankim yüzeyi diye sunulmamalıdır. Sağ/sol hemiliver grupları ayrı FMA kimlikleridir ve hepatovenöz V–VIII / II–IV segment yüzeylerini seçer; morfolojik lobla eşitlenmez. Beş akciğer lobu bronş/damar alt yapılarını da toplar. `requiresRepresentationNote` ve `scopeNoteTr` bu dokuz adayda korunmalıdır. Temsil notu desteklenmeden etiket aktarımı tek başına model kapsamını düzeltmez.

Kalbin beş doğrudan komşusuna bu tur yeni etiket önerilmedi. Sol atriyum/ventrikül **boşluğu**, odacığın bütünü değildir. Fibrous skeleton için upstream satır 3974 `Skeleton flbrosum cordis` yazıyor; şüpheli harf sessizce düzeltilmedi veya ürüne önerilmedi. Ayrıca bu FMA seçimi yalnız üç kapakçık/cusp yüzeyi içeriyor. Genel kaynaktaki grup adını çevirmek bu kapsam sorununu gidermez.

| FMA | Kaynak İngilizce | Türkçe aday | Latince aday | Parça | Not gerekli |
|---|---|---|---|---:|---|
| FMA7371 | lower lobe of left lung | Sol akciğer alt lobu | Lobus inferior pulmonis sinistri | 56 | Evet |
| FMA7370 | upper lobe of left lung | Sol akciğer üst lobu | Lobus superior pulmonis sinistri | 68 | Evet |
| FMA7337 | lower lobe of right lung | Sağ akciğer alt lobu | Lobus inferior pulmonis dextri | 69 | Evet |
| FMA7383 | middle lobe of lung | Sağ akciğer orta lobu | Lobus medius pulmonis dextri | 25 | Evet |
| FMA7333 | upper lobe of right lung | Sağ akciğer üst lobu | Lobus superior pulmonis dextri | 62 | Evet |
| FMA7393 | tracheobronchial tree | Trakeobronşiyal ağaç | Arbor tracheobronchialis | 95 | — |
| FMA9576 | thorax | Toraks | Thorax | 537 | — |
| FMA7487 | body of sternum | Sternum gövdesi | Corpus sterni | 1 | — |
| FMA7486 | manubrium | Sternum manubriumu | Manubrium sterni | 1 | — |
| FMA7488 | xiphoid process | Ksifoid çıkıntı | Processus xiphoideus | 1 | — |
| FMA3768 | arch of aorta | Aort kemeri | Arcus aortae | 1 | — |
| FMA3736 | ascending aorta | Çıkan aort | Aorta ascendens | 1 | — |
| FMA3784 | descending aorta | İnen aort | Aorta descendens | 3 | — |
| FMA14772 | hepatic artery proper | Arteria hepatica propria | Arteria hepatica propria | 16 | — |
| FMA15810 | left hemiliver | Karaciğerin sol fonksiyonel bölümü | Pars sinistra hepatis | 3 | Evet |
| FMA13363 | left lobe of liver | Karaciğerin sol lobu | Lobus sinister hepatis | 25 | Evet |
| FMA15809 | right hemiliver | Karaciğerin sağ fonksiyonel bölümü | Pars dextra hepatis | 5 | Evet |
| FMA13362 | right lobe of liver | Karaciğerin sağ lobu | Lobus dexter hepatis | 17 | Evet |
| FMA15414 | right portal vein | Portal venin sağ dalı | Ramus dexter venae portae hepatis | 9 | — |
| FMA7206 | duodenum | Duodenum | Duodenum | 1 | — |
| FMA7208 | ileum | İleum | Ileum | 32 | — |
| FMA7207 | jejunum | Jejunum | Jejunum | 23 | — |
| FMA13478 | vertebral column | Omurga | Columna vertebralis | 48 | — |

## Bekletilenler

| FMA | Kaynak adı | Gerekçe |
|---|---|---|
| FMA9465 | cavity of left atrium | Cavity geometry must not be relabeled as the complete atrium/ventricle. Exact cavity Latin not found in pinned table. |
| FMA9466 | cavity of left ventricle | Cavity geometry must not be relabeled as the complete atrium/ventricle. Exact cavity Latin not found in pinned table. |
| FMA79278 | content of middle mediastinum | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA9496 | fibrous skeleton of heart | Pinned row 3974 has suspect Latin Skeleton flbrosum cordis (letter l instead of i); do not silently publish or correct. Source selection contains only three valve leaflets/cusps, not a verified full fibrous skeleton. |
| FMA7166 | left side of heart | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA68005 | intrapulmonary part of left inferior pulmonary vein | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA67995 | intrapulmonary part of left pulmonary artery | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA68004 | intrapulmonary part of left superior pulmonary vein | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA85056 | left pulmopleural compartment | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA68003 | intrapulmonary part of right inferior pulmonary vein | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA67994 | intrapulmonary part of right pulmonary artery | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA68002 | intrapulmonary part of right superior pulmonary vein | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA45662 | lower respiratory tract | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA24866 | sternal part of chest | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA49894 | systemic arterial tree | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA71132 | gastrointestinal tract | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA68016 | intrahepatic biliary tree | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA63103 | pancreatic duct tree | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA63120 | parenchyma of pancreas | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA14615 | wall of small intestine | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA14619 | wall of large intestine | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA45659 | lower urinary tract | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |
| FMA7160 | genital system | No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ. |

## Dosyalar ve doğrulama

- `ui-neighbor-audit.json`: 22 başlangıç, 46 uç, mevcut dil çıktıları ve erişilen ilişki kimlikleri.
- `proposals.json`: 23 öneri, 23 bekletme; hiçbir eksik kapsam daha geniş organ adıyla doldurulmadı.
- `source-evidence.json`: her uç için BP3D satırı, geometri adları, erişim ilişkisi; öneriler için TA2 satırı; girdi hashleri.
- `validation.json`: kaynak ID/ad, Latince string ve sayı kontrolleri.
- `audit-neighbors.mjs` ve `prepare-proposals.py`: yalnız bu klasöre yazan tekrar üretim araçları.

Çalıştırma sırası: `node data/model-candidates/organ-neighbor-labels/audit-neighbors.mjs`, ardından `python3 data/model-candidates/organ-neighbor-labels/prepare-proposals.py`. Aktif veri değiştikten sonra bu komutlar yeni snapshot üretir; entegrasyon öncesi kanıtlar korunacaksa yeniden çalıştırılmamalıdır.
