# Rotator cuff relationship candidate

The inactive package adds **26 source-supported relations**: eight origins, eight insertions and ten innervation edges. It reuses eight existing bilateral muscle concepts and four existing bone concepts. Eight new side-specific nerve concepts have `geometryPartIds:[]` and `representationStatus:missing_geometry`. No nerve model, landmark coordinate or attachment surface is supplied.

| Muscle | Left concept / part | Right concept / part |
|---|---|---|
| Supraspinatus | FMA32545 / FJ1506M | FMA32544 / FJ1506 |
| Infraspinatus | FMA32548 / FJ1500M | FMA32547 / FJ1500 |
| Teres minor | FMA32554 / FJ1508M | FMA32553 / FJ1508 |
| Subscapularis | FMA13415 / FJ1504M | FMA13414 / FJ1504 |

Scapula targets are FMA13396 left / FMA13395 right; humerus targets are FMA23131 left / FMA23130 right. These are context bones. Every origin/insertion edge retains the named fossa, border region, tubercle or facet under `qualifiers.landmark`. It also has `targetRole:context_bone`, `requiresLandmarkDisplay:true`, and explicit absence of spatial localization. Selecting or framing the bone must not be represented as showing a precise attachment point.

## Display integration requirement

Copy the single short string **`qualifiers.attachmentNoteTr`** into the explorer relation projection and display it alongside each origin/insertion relationship. It contains the Turkish region plus “kesin yüzey işareti yok”. `landmarkTr` is available if the UI needs the region alone; retain `landmark` in the canonical evidence graph. A consumer that drops the qualifier should not activate these bone-target relations. Sinir endpoints have no geometry: the UI should display their names and missing-model state without inventing a camera target or binding them to another nerve.

## Sources and semantic scope

[UAMS upper-limb muscle table](https://medicine.uams.edu/neuroscience/education/medical-school-courses/human-structure-module/anatomy-tables/muscle-tables/muscles-of-the-upper-limb/) and [TTUHSC El Paso shoulder/axilla tables](https://anatomy.ttuhscep.edu/musculoskeletal_system/axilla_tables.html) were checked on 2026-09-22. Evidence locators identify each muscle row and Origin, Insertion or Innervation column; nerve concepts additionally cite the named nerve row's Motor column. The two university tables corroborate the selected facts, but their similar text is not evidence of independent specimen validation. Laterality is instantiated from general anatomy.

Suprascapular nerves supply the two spinatus muscles, axillary nerves supply teres minor, and **upper and lower subscapular nerves are separate endpoints** supplying subscapularis. No root-level, capsule insertion, complete nerve territory or muscle-subregion claim is added. Missing geometry does not invalidate the sourced anatomical nerve identity.

English/Latin labels use pinned Z-Anatomy TA2 rows: muscles 2457–2460, suprascapular nerve 6411, axillary nerve 6440, superior subscapular nerve 6428 and inferior subscapular nerve 6429. Exact CSV line locators and SHA-256 are included. “Upper/lower” university nerve names map to TA2 “superior/inferior”; no unverified FMA nerve IDs are invented. Turkish strings are editorial translations with expert review pending, not claimed to be Turkish TA2 content.

## Files and validation

- `candidate.json`: builder-compatible `entities` and `relations` bundle; currently inactive.
- `entities.json`, `relations.json`, `labels.json`: separate integration payloads.
- `evidence.json`: existing UAMS source plus proposed TTUHSC/terminology records and compact factual scope.
- `mapping.json`: exact canonical mappings and hashes; existing entities are referenced, not replaced.
- `validation.json`: canonical `validateKnowledge` passed on an in-memory merge; all 26 edges match sides, all 16 attachments carry required display regions, all ten innervation subjects have no geometry.
- `build-candidate.py`: reproduces candidate files using pinned local TA2 and canonical identity checks; writes only this directory.

Root may integrate the bundle after preserving its display qualifiers and registering the proposed evidence sources. No shared anatomy, application, coverage, registry or source file was modified. No commit or deployment was performed.

## Entegrasyon kaydı

22 Eylül: Kök görev bu adayın incelenen verilerini etkin etiket/bilgi grafiği/görüntüleme katmanına uyguladı. Bu klasörün aday snapshotı korunur; güncel ürün durumu docs/model/2026-09-20-delivery-plan.md içinde izlenir.
